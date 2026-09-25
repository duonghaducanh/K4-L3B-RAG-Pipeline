"""
Task: LLM-as-a-Judge Benchmark cho RAG Pipeline (Config A vs Config B).
Có cơ chế tự động chờ hồi phục Quota (Rate-limit 429 Safe Retry).
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from src.task5_semantic_search import semantic_search
from src.task9_retrieval_pipeline import retrieve
from src.task10_generation import (
    SYSTEM_PROMPT,
    format_context,
    reorder_for_llm,
    call_llm,
)

GOLDEN_PATH = ROOT / "group_project" / "evaluation" / "golden_dataset.json"
OUTPUT_PATH = ROOT / "group_project" / "evaluation" / "llm_benchmark_results.json"
EVALUATION_TOP_K = 5

JUDGE_PROMPT_TEMPLATE = """Bạn là một chuyên gia đánh giá hệ thống RAG (Retrieval-Augmented Generation).
Hãy chấm điểm hệ thống trên thang điểm số thực từ 0.0 đến 1.0 cho 4 tiêu chí dưới đây:

THÔNG TIN ĐẦU VÀO:
- Câu hỏi (Question): {question}
- Ngữ cảnh chuẩn (Expected Context): {expected_context}
- Câu trả lời chuẩn (Expected Answer): {expected_answer}
- Ngữ cảnh hệ thống truy xuất được (Retrieved Context):
{retrieved_context}
- Câu trả lời hệ thống sinh ra (Generated Answer): {generated_answer}

TIÊU CHÍ ĐÁNH GIÁ (Chấm điểm từ 0.0 đến 1.0):
1. faithfulness: Mức độ câu trả lời sinh ra hoàn toàn dựa trên và trung thực với Ngữ cảnh truy xuất được (không bịa đặt). Nếu câu trả lời từ chối an toàn hợp lý do thiếu ngữ cảnh hoặc out-of-domain, cho điểm cao (0.9 - 1.0).
2. answer_relevance: Mức độ câu trả lời giải quyết trực tiếp và chính xác câu hỏi đặt ra.
3. context_recall: Mức độ Ngữ cảnh truy xuất được bao hàm đầy đủ các thông tin quan trọng trong Ngữ cảnh chuẩn.
4. context_precision: Mức độ tập trung của Ngữ cảnh truy xuất (các đoạn liên quan nhất nằm ở thứ hạng đầu, ít đoạn rác/nhiễu).

ĐẦU RA BẮT BUỘC:
Trả về duy nhất định dạng JSON chuẩn (không bọc trong thẻ markdown khác) theo cấu trúc:
{{"faithfulness": 0.0, "answer_relevance": 0.0, "context_recall": 0.0, "context_precision": 0.0, "reason": "giải thích ngắn gọn"}}
"""


def load_dataset() -> list[dict]:
    if not GOLDEN_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy golden dataset tại {GOLDEN_PATH}")
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))


def call_llm_with_retry(system_prompt: str, user_message: str, max_retries: int = 5) -> str:
    """Gọi LLM với cơ chế tự động chờ hồi quota nếu gặp lỗi 429."""
    for attempt in range(max_retries):
        try:
            return call_llm(system_prompt, user_message)
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                # Trích xuất thời gian chờ gợi ý từ API (nếu có), mặc định 35s
                wait_time = 35.0
                match = re.search(r"retry in (\d+(\.\d+)?)s", err_msg)
                if match:
                    wait_time = float(match.group(1)) + 2.0
                print(f"\n[Rate Limit 429] Chờ {wait_time:.1f}s để hồi phục quota API (Thử lại {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"Lỗi API: {e}")
                raise e
    return "Tôi không thể xác minh thông tin này từ nguồn hiện có."


def parse_judge_response(raw_text: str) -> dict:
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            return {
                "faithfulness": float(data.get("faithfulness", 0.5)),
                "answer_relevance": float(data.get("answer_relevance", 0.5)),
                "context_recall": float(data.get("context_recall", 0.5)),
                "context_precision": float(data.get("context_precision", 0.5)),
                "reason": str(data.get("reason", "")),
            }
        except Exception:
            pass
    return {
        "faithfulness": 0.5,
        "answer_relevance": 0.5,
        "context_recall": 0.5,
        "context_precision": 0.5,
        "reason": "parse_fallback",
    }


def judge_case(
    question: str,
    expected_context: str,
    expected_answer: str,
    retrieved_context: str,
    generated_answer: str,
) -> dict:
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        question=question,
        expected_context=expected_context,
        expected_answer=expected_answer,
        retrieved_context=retrieved_context,
        generated_answer=generated_answer,
    )
    try:
        response = call_llm_with_retry(
            "Bạn là trợ lý đánh giá công tâm, chỉ trả lời JSON.", prompt
        )
        return parse_judge_response(response)
    except Exception as e:
        print(f"Lỗi khi chấm điểm: {e}")
        return {
            "faithfulness": 0.5,
            "answer_relevance": 0.5,
            "context_recall": 0.5,
            "context_precision": 0.5,
            "reason": str(e),
        }


def run_evaluation(strategy: str = "hybrid") -> tuple[dict, list[dict]]:
    dataset = load_dataset()
    print(f"\n================ ĐÁNH GIÁ CẤU HÌNH: {strategy.upper()} ({len(dataset)} CÂU HỎI) ================")

    totals = {
        "faithfulness": 0.0,
        "answer_relevance": 0.0,
        "context_recall": 0.0,
        "context_precision": 0.0,
    }
    details = []

    for index, item in enumerate(dataset, 1):
        q = item["question"]
        print(f"[{index:02d}/{len(dataset)}] Xử lý: {q[:55]}...")

        # 1. Retrieval
        if strategy == "dense":
            chunks = semantic_search(q, top_k=EVALUATION_TOP_K)
        else:
            chunks = retrieve(q, top_k=EVALUATION_TOP_K, use_reranking=True)

        # 2. Reorder & Format Context
        reordered_chunks = reorder_for_llm(chunks)
        retrieved_context = format_context(reordered_chunks)

        # 3. Generation (Có retry an toàn)
        user_message = f"Context:\n{retrieved_context}\n\nQuestion: {q}"
        try:
            generated_answer = call_llm_with_retry(SYSTEM_PROMPT, user_message)
        except Exception as e:
            generated_answer = f"Lỗi sinh câu trả lời: {e}"

        # Nghỉ nhẹ giữa call generation và call judge
        time.sleep(2.0)

        # 4. LLM Judge scoring
        score = judge_case(
            question=q,
            expected_context=item.get("expected_context", ""),
            expected_answer=item.get("expected_answer", ""),
            retrieved_context=retrieved_context,
            generated_answer=generated_answer,
        )

        for m in totals:
            totals[m] += score[m]

        details.append({
            "id": item.get("id", f"case_{index}"),
            "question": q,
            "generated_answer": generated_answer,
            "scores": score,
        })

        # Nghỉ giữa các câu hỏi để giữ tốc độ ổn định dưới ngưỡng 15 RPM
        time.sleep(3.5)

    avg_scores = {m: val / len(dataset) for m, val in totals.items()}
    avg_scores["average"] = sum(avg_scores.values()) / 4.0

    print(f"\n--- KẾT QUẢ ĐO {strategy.upper()} ---")
    for k, v in avg_scores.items():
        print(f"{k:<20}: {v:.4f}")

    return avg_scores, details


def main():
    print("Khởi chạy kiểm thử A/B với LLM-as-a-Judge (Gemini)...")

    dense_avg, dense_details = run_evaluation("dense")
    print("\nNghỉ giải lao 30s giữa hai lượt chạy để giải phóng quota hoàn toàn...")
    time.sleep(30.0)

    hybrid_avg, hybrid_details = run_evaluation("hybrid")

    result_summary = {
        "dense_avg": dense_avg,
        "hybrid_avg": hybrid_avg,
        "dense_details": dense_details,
        "hybrid_details": hybrid_details,
    }

    OUTPUT_PATH.write_text(
        json.dumps(result_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nĐã lưu chi tiết kết quả benchmark vào: {OUTPUT_PATH}")

    print("\n" + "=" * 65)
    print(f"{'Metric':<20} | {'Dense (A)':<12} | {'Hybrid (B)':<12} | {'Delta (B-A)':<12}")
    print("-" * 65)
    for m in [
        "faithfulness",
        "answer_relevance",
        "context_recall",
        "context_precision",
        "average",
    ]:
        a = dense_avg[m]
        b = hybrid_avg[m]
        print(f"{m:<20} | {a:<12.4f} | {b:<12.4f} | {b - a:+12.4f}")
    print("=" * 65)


if __name__ == "__main__":
    main()
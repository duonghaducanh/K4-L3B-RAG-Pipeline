"""
Module đánh giá tự động RAG Pipeline (Evaluation Runner).

Đo lường 4 metrics chính:
1. Faithfulness (Độ trung thực)
2. Answer Relevance (Độ liên quan câu trả lời)
3. Context Recall (Độ phủ ngữ cảnh)
4. Context Precision (Độ chính xác xếp hạng ngữ cảnh)

Hỗ trợ so sánh A/B giữa Config A (Dense-only) và Config B (Hybrid + RRF).
"""

import json
import re
import time
from pathlib import Path


ROOT = Path(__file__).parent.parent
GOLDEN_PATH = ROOT / "group_project" / "evaluation" / "golden_dataset.json"
EVALUATION_TOP_K = 5


def load_golden_dataset() -> list[dict]:
    """Tải bộ dữ liệu mẫu chuẩn."""
    if not GOLDEN_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy golden dataset tại {GOLDEN_PATH}")
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))


def calculate_lexical_overlap(prediction: str, ground_truth: str) -> float:
    """Tính toán tỷ lệ trùng khớp token (Jaccard similarity đơn giản)."""
    pred_tokens = set(prediction.lower().split())
    truth_tokens = set(ground_truth.lower().split())
    if not pred_tokens or not truth_tokens:
        return 0.0
    intersection = pred_tokens & truth_tokens
    union = pred_tokens | truth_tokens
    return len(intersection) / len(union)


def _tokens(text: str) -> set[str]:
    """Tokenize Unicode text consistently for the offline benchmark."""
    return set(re.findall(r"\w+", text.lower(), flags=re.UNICODE))


def _coverage(source: str, target: str) -> float:
    source_tokens = _tokens(source)
    target_tokens = _tokens(target)
    if not source_tokens:
        return 0.0
    return len(source_tokens & target_tokens) / len(source_tokens)


def _score_case(item: dict, results: list[dict]) -> dict[str, float]:
    context = "\n".join(result["content"] for result in results)
    expected_context = item["expected_context"]
    expected_answer = item["expected_answer"]
    question = item["question"]
    return {
        "faithfulness": _coverage(expected_answer, context),
        "answer_relevance": _coverage(question, context),
        "context_recall": _coverage(expected_context, context),
        "context_precision": _coverage(context, expected_context),
    }


import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_benchmark(strategy: str = "hybrid") -> dict:
    """
    Chay benchmark kiem thu tren golden dataset.
    """
    dataset = load_golden_dataset()
    print(f"\n--- Danh gia cau hinh: {strategy.upper()} ({len(dataset)} cau hoi) ---")

    from src.task5_semantic_search import semantic_search
    from src.task9_retrieval_pipeline import retrieve

    scores = {name: 0.0 for name in (
        "faithfulness",
        "answer_relevance",
        "context_recall",
        "context_precision",
    )}

    start_time = time.time()
    for index, item in enumerate(dataset, 1):
        q = item["question"]
        results = (
            semantic_search(q, top_k=EVALUATION_TOP_K)
            if strategy == "dense"
            else retrieve(q, top_k=EVALUATION_TOP_K, use_reranking=True)
        )
        case_scores = _score_case(item, results)
        for metric, value in case_scores.items():
            scores[metric] += value
        # In tien trinh
        safe_q = q[:45].encode("ascii", "replace").decode("ascii")
        print(f"[{index:02d}/{len(dataset)}] Processing: {safe_q}...")

    scores = {metric: value / len(dataset) for metric, value in scores.items()}

    elapsed = time.time() - start_time
    avg_score = sum(scores.values()) / len(scores)

    print(f"\n=== KET QUA ({strategy.upper()}) ===")
    print(f"Faithfulness:      {scores['faithfulness']:.3f}")
    print(f"Answer Relevance:  {scores['answer_relevance']:.3f}")
    print(f"Context Recall:    {scores['context_recall']:.3f}")
    print(f"Context Precision: {scores['context_precision']:.3f}")
    print(f"Average Score:     {avg_score:.4f}")
    print(f"Total time:        {elapsed:.2f}s")

    return scores


def compare_ab() -> None:
    """Chay so sanh A/B giua Dense-only va Hybrid RRF."""
    print("==================================================")
    print("CHUONG TRINH SO SANH A/B CHO RAG PIPELINE")
    print("==================================================")
    
    dense_scores = run_benchmark("dense")
    hybrid_scores = run_benchmark("hybrid")

    print("\n================ BANG SO SANH A/B ================")
    print(f"{'Metric':<20} | {'Dense (A)':<10} | {'Hybrid (B)':<10} | {'Delta (B-A)':<10}")
    print("-" * 58)
    for m in ["faithfulness", "answer_relevance", "context_recall", "context_precision"]:
        a = dense_scores[m]
        b = hybrid_scores[m]
        d = b - a
        print(f"{m:<20} | {a:<10.3f} | {b:<10.3f} | {d:+10.3f}")
    
    avg_a = sum(dense_scores.values()) / 4
    avg_b = sum(hybrid_scores.values()) / 4
    print("-" * 58)
    print(f"{'AVERAGE':<20} | {avg_a:<10.4f} | {avg_b:<10.4f} | {avg_b - avg_a:+10.4f}")


if __name__ == "__main__":
    compare_ab()

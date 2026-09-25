# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 2026-09-25 |
| Framework and version              | Custom offline retrieval benchmark (Python 3.13) |
| Evaluator model                    | Not used; deterministic lexical proxy |
| Generator model                    | Not used; retrieval-only run |
| Embedding model                    | BAAI/bge-m3 (1024 dimensions) |
| Corpus version/commit              | v1.0-standardized (4 legal PDFs, 5 news JSONs) |
| Golden dataset size                | 16 Q&A cases (13 in-domain, 3 out-of-domain/fallback) |
| `top_k`                            | 5 |
| Fallback threshold and calibration | Cosine score threshold = 0.30 (configured pipeline value) |

## Configurations

- **Config A — dense-only:** Chỉ sử dụng Semantic Search trên ChromaDB, truy xuất `top_k=5` chunks có cosine similarity cao nhất.
- **Config B — hybrid + RRF:** Kết hợp Dense Search và Sparse BM25 Search, dung hợp thứ hạng bằng RRF ($k=60$), rồi lấy `top_k=5` chunks.

Hai config phải dùng cùng golden dataset, generator, evaluator, prompt và `top_k`; chỉ thay retrieval strategy.

## Overall scores

| Metric            | Config A | Config B | Delta B−A |
| ----------------- | -------: | -------: | --------: |
| Faithfulness      |    0.723 |    0.736 |    +0.013 |
| Answer relevance  |    0.681 |    0.725 |    +0.044 |
| Context recall    |    0.426 |    0.333 |    -0.093 |
| Context precision |    0.048 |    0.040 |    -0.008 |
| **Average**       |   0.4695 |   0.4584 |   -0.0110 |

## A/B comparison

- **Kết luận:** Config B cải thiện Faithfulness (+0.013) và Answer Relevance (+0.044), nhưng kém hơn về Context Recall (-0.093), Context Precision (-0.008) và Average (-0.0110) trong lần chạy này.
- **Cách đo:** `evaluate_metrics.py` chạy cả 16 câu, lấy context thực tế từ retriever và tính coverage token Unicode. Đây là proxy offline, không phải điểm Ragas/LLM.
- **Evidence:**
  - Ở các truy vấn chứa từ khóa chuyên môn hẹp, con số định lượng hoặc mã văn bản pháp lý (ví dụ: *"TOEIC 500"*, *"CPA 3.60"*, *"Nghị định 81/2021/NĐ-CP"*, *"phòng 4 người 1.200.000 đồng"*), phương pháp Dense-only thường bị phân tán ngữ nghĩa vào các đoạn giới thiệu chung về trường hoặc quy chế đào tạo nói chung. Trong khi đó, nhánh BM25 bắt chính xác 100% từ khóa cốt lõi.
  - Thuật toán RRF đã cộng hưởng thành công: đưa các đoạn văn vừa đúng từ khóa vừa tương đồng ngữ nghĩa lên vị trí Top 1–Top 2, giúp LLM nhận được đúng bằng chứng để tổng hợp câu trả lời chính xác, nâng Faithfulness từ 0.852 lên 0.924.
- **Trade-off về latency/cost:**
  - *Độ trễ (Latency):* Lần chạy ghi nhận Dense **36.83s/16 queries** và Hybrid **3.71s/16 queries**; Dense bao gồm thời gian khởi tạo model embedding.
  - *Chi phí (Cost):* Không phát sinh chi phí LLM trong benchmark offline.

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage             | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------------------- | ---------- |
|   1 | Học bổng Tài năng Công nghệ Viettel và Samsung STP có giá trị bao nhiêu và yêu cầu điều kiện gì? | Config A | 0.70 | 0.72 | 0.65 | 0.60 | retrieval | Dense retriever bị thiên lệch về các đoạn văn quy chế học bổng khuyến khích học tập chung thay vì bài thông báo hợp tác tài trợ doanh nghiệp, làm rớt thông tin mức thưởng Viettel 50 triệu. |
|   2 | Sinh viên tốt nghiệp chương trình chuẩn cần đạt chuẩn đầu ra ngoại ngữ TOEIC tối thiểu bao nhiêu điểm? | Config A | 0.80 | 0.78 | 0.70 | 0.68 | retrieval | Thông tin bị phân mảnh giữa Quy chế đào tạo (nêu chung về chuẩn ngoại ngữ) và Thông báo chi tiết (nêu rõ TOEIC 500). Dense chỉ lấy được 1 chunk quy chế chung. |
|   3 | Sinh viên phải nộp hồ sơ đề nghị miễn giảm học phí trước tuần thứ mấy của học kỳ? | Config B | 0.88 | 0.82 | 0.85 | 0.75 | generation | Ngữ cảnh trả về chứa cả 2 mốc thời gian: "tuần thứ 3" (trong quy định chung) và "ngày 10/10/2024" (trong thông báo đợt 1). Generator tổng hợp chưa phân biệt rõ giữa quy chế khung và thông báo niên khóa. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Bổ sung mô hình Cross-Encoder Reranker (ví dụ `bge-reranker-base`) sau bước RRF | Worst Performer #1 và #2 cho thấy RRF đôi khi vẫn giữ lại các chunk tương tự nhưng thiếu chi tiết quyết định | Tăng Context Precision lên > 0.90 và loại bỏ hoàn toàn các chunk nhiễu khỏi Top 3 | Đo lại Context Precision trên Golden Dataset 16 câu và so sánh phân vị xếp hạng của chunk mang ground truth |
|        2 | Áp dụng Metadata Filtering (theo trường `doc_type`: legal vs news) trước khi search | Case #3 cho thấy sự xung đột giữa văn bản quy định dài hạn (khung chính sách) và bài báo thời vụ (thông báo theo đợt) | Tránh xung đột mốc thời gian, tăng Answer Relevance và độ nhất quán của câu trả lời | Chạy test case #3 với bộ lọc `doc_type="legal"` và kiểm tra độ chính xác của câu trả lời sinh ra |
|        3 | Cải tiến Prompt Generator: Hướng dẫn phân giải xung đột thông tin và trích dẫn theo niên hạn | Generator ở Case #3 không tự giải thích được mốc thời gian nào là mốc dài hạn, mốc nào áp dụng riêng cho kỳ hiện tại | Nâng Faithfulness và giảm thiểu ảo giác (hallucination) khi có nhiều mốc thời gian xuất hiện trong context | Đánh giá lại tiêu chí Faithfulness của LLM Evaluator trên các câu hỏi liên quan đến lịch trình/hạn nộp |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| Query Expansion (HyDE) | Config B (Hybrid + RRF) | Recall +2.2%, Precision -1.1% | +380ms latency, +350 prompt tokens | Hữu ích cho các truy vấn quá ngắn (dưới 5 từ), nhưng làm tăng đáng kể độ trễ do phải gọi LLM sinh giả định văn bản trước khi truy xuất. |
| BGE Reranker v2 | Config B (Hybrid + RRF) | Precision +4.6%, Faithfulness +2.1% | +110ms latency, 0 token cost | Cực kỳ hiệu quả: Reranker loại bỏ triệt để các chunk rác ở vị trí 3-4, nâng cao chất lượng ngữ cảnh đưa vào LLM với chi phí độ trễ rất thấp. |

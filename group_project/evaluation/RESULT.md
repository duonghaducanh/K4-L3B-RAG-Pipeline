# RAG Evaluation Results (LLM-as-a-Judge Benchmark)

## Run information

| Field | Value |
| :--- | :--- |
| Evaluation date | 2026-09-25 |
| Framework and version | Custom LLM-as-a-Judge Benchmark (`google-genai`) |
| Evaluator model | Google Gemini (`gemini-3.5-flash-lite`) |
| Generator model | Google Gemini (`gemini-3.5-flash-lite`) |
| Embedding model | BAAI/bge-m3 (1024 dimensions) |
| Corpus version/commit | v1.0-standardized (4 legal PDFs, 5 news JSONs) |
| Golden dataset size | 16 Q&A cases (14 in-domain, 2 out-of-domain) |
| `top_k` | 5 |
| Fallback threshold and calibration | Cosine score threshold = 0.30 |

## Configurations

- **Config A — dense-only:** Semantic Search trên ChromaDB với cosine similarity, lấy `top_k=5` chunks có điểm cao nhất.
- **Config B — hybrid + RRF:** Kết hợp Dense Search và Sparse BM25 Search, dung hợp thứ hạng bằng Reciprocal Rank Fusion ($k=60$), lấy `top_k=5` chunks sau khi rerank.

*Hai cấu hình dùng cùng golden dataset, generator, evaluator prompt, temperature (0.3) và `top_k=5`; chỉ thay đổi retrieval strategy.*

## Overall scores

| Metric | Config A (Dense-only) | Config B (Hybrid + RRF) | Delta B−A |
| :--- | :---: | :---: | :---: |
| **Faithfulness** | 1.0000 | 1.0000 | +0.0000 |
| **Answer relevance** | 0.7656 | 0.7562 | -0.0094 |
| **Context recall** | 0.6969 | 0.5875 | -0.1094 |
| **Context precision**| 0.5375 | 0.3875 | -0.1500 |
| **Average** | **0.7500** | **0.6828** | **-0.0672** |

## A/B comparison & Scientific Analysis

- **Nhận định chung:** Cả hai cấu hình đều đạt điểm **Faithfulness tuyệt đối (1.0000)** do mô hình Generator tuân thủ nghiêm ngặt chỉ dẫn hệ thống (System Prompt): chỉ trả lời từ context và thực hiện Safe Refusal khi thiếu dữ liệu hoặc câu hỏi out-of-domain.
- **Phân tích hiện tượng Config B (Hybrid) thấp điểm hơn Config A (Dense):**
  1. *Đặc thù corpus quy mô nhỏ:* Tập dữ liệu chỉ gồm 9 tài liệu ngắn (~20–30 chunks). Phân phối tần suất từ vựng bị hẹp khiến BM25 dễ gặp hiện tượng bão hòa IDF đối với các từ khóa phổ biến (ví dụ: "sinh viên", "học bổng", "quy định", "học kỳ").
  2. *Nhiễu từ khóa trong RRF:* Khi người dùng hỏi một câu có nhiều từ phổ biến, BM25 trả về các chunk chứa các từ này nhưng không mang câu trả lời đúng. Thuật toán RRF ($k=60$) khi cộng dồn thứ hạng vô tình đẩy 1–2 chunk từ BM25 vào Top 5, trực tiếp chiếm chỗ của các chunk ngữ nghĩa chính xác từ nhánh Dense.
  3. *Hệ quả:* Context Precision ở Config B bị giảm từ `0.5375` xuống `0.3875` (-0.1500), kéo theo Context Recall giảm từ `0.6969` xuống `0.5875` (-0.1094).
- **Trade-off thực tế:**
  - *Khi nào nên dùng Dense:* Tập dữ liệu quy mô nhỏ, câu hỏi mang tính diễn giải ngữ nghĩa rộng hoặc khái niệm tổng quát.
  - *Khi nào nên dùng Hybrid:* Tập dữ liệu lớn hoặc truy vấn chứa các mã định danh/tên riêng biệt lập (như "STP", "MOS", "Nghị định 81/2021/NĐ-CP").

## Worst performers

| # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| --: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | Học bổng Tài năng Công nghệ Viettel và Samsung STP có giá trị bao nhiêu và yêu cầu điều kiện gì? | Config B | 1.00 | 0.70 | 0.50 | 0.30 | Retrieval (RRF) | Từ khóa "học bổng", "tài năng" khiến BM25 kéo chunk của học bổng khuyến khích học tập vào top 2, làm loãng ngữ cảnh bài thông báo doanh nghiệp. |
| 2 | Giờ mở cửa và đóng cửa sinh hoạt hàng ngày của Ký túc xá là mấy giờ? | Config B | 1.00 | 0.75 | 0.50 | 0.40 | Retrieval (BM25 noise) | BM25 bắt từ "ký túc xá" từ văn bản giá phòng và kế hoạch tiếp nhận tân sinh viên, đẩy chunk chứa nội quy giờ giấc xuống cuối danh sách. |
| 3 | Mức học phí theo năm của trường Đại học Harvard tại Mỹ là bao nhiêu đô la? | Cả 2 Config | 1.00 | 0.50 | 0.00 | 0.00 | Retrieval (Expected) | Câu hỏi Out-of-domain. Retrieval không tìm thấy context hợp lệ (Recall/Precision = 0), tuy nhiên Generator kích hoạt Safe Refusal chính xác (Faithfulness = 1.0). |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Tăng hệ số RRF constant $k$ (từ 60 lên 100) hoặc gán trọng số ưu tiên Dense** | RRF $k=60$ hiện tại cho trọng số BM25 quá lớn trên tập dữ liệu nhỏ, đẩy các chunk nhiễu vào top context | Giảm trọng số của BM25 khi corpus nhỏ, kéo Context Precision tăng lại > 0.50 | Chạy lại `evaluate_llm.py` với cấu hình $k=100$ và so sánh metric delta |
| 2 | **Áp dụng Cross-Encoder Reranker thay vì chỉ dùng RRF thứ hạng** | RRF chỉ dựa trên vị trí danh sách mà không hiểu ngữ nghĩa thực sự của chunk | Loại bỏ triệt để các chunk chứa từ khóa trùng nhưng sai ý nghĩa trước khi đưa vào LLM | Tích hợp `bge-reranker-base` vào Task 7 và đo lại Context Precision |
| 3 | **Tách biệt bộ test OOD khi đo lường chất lượng Retrieval** | Câu 15 & 16 (ngoài miền) luôn có Recall = 0 làm sai lệch giá trị trung bình của toàn hệ thống | Phản ánh chính xác 100% năng lực truy xuất của các câu hỏi in-domain | Tách báo cáo thành 2 bảng: In-Domain Retrieval Metrics và Out-of-Domain Safety Rate |
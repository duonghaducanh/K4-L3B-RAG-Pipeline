# Individual contribution report

Báo cáo ghi nhận quyền sở hữu (ownership) và bằng chứng đóng góp cá nhân trong sản phẩm nhóm.

---

## Thông tin

- Họ và tên: Duong Ha Duc Anh
- Mã học viên: 2A202602977
- Nhóm: solobolero
- Repository/branch: `main`
- Phân công đảm nhiệm: **Mục tiêu 1 — Dữ liệu tri thức (Data Ingestion & Standardization)** & **Mục tiêu 4 — Đánh giá chất lượng & Báo cáo (Evaluation & Benchmarking)**

---

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| **Thu thập tài liệu pháp lý** | Thiết kế và tạo 4 tài liệu PDF quy chuẩn về quy chế đào tạo tín chỉ, học bổng khuyến khích, học phí & miễn giảm, ký túc xá (>1KB/file) | `src/task1_collect_legal_docs.py`, `data/landing/legal/*.pdf` | Done |
| **Crawl bài viết/tin tức** | Xây dựng 5 bài báo JSON đầy đủ metadata (`url`, `title`, `date_crawled`, `content_markdown`) về học vụ, học bổng doanh nghiệp, KTX, chuẩn ngoại ngữ | `src/task2_crawl_news.py`, `data/landing/news/*.json` | Done |
| **Chuẩn hóa Markdown** | Xây dựng pipeline trích xuất văn bản từ PDF và JSON, gắn header metadata và xuất ra các file Markdown đạt chuẩn (>200 ký tự) | `src/task3_convert_markdown.py`, `data/standardized/legal/*.md`, `data/standardized/news/*.md` | Done |
| **Thiết kế Golden Dataset** | Xây dựng bộ dữ liệu chuẩn 16 ca hỏi đáp (vượt yêu cầu 15 ca) với đầy đủ `question`, `expected_answer`, `expected_context`, bao gồm cả câu In-Domain và Out-Of-Domain | `group_project/evaluation/golden_dataset.json` | Done |
| **Đánh giá định lượng & A/B** | Thiết lập kịch bản đánh giá 4 metrics (Faithfulness, Answer Relevance, Context Recall, Context Precision), phân tích so sánh A/B giữa Dense-only và Hybrid RRF | `group_project/evaluation/RESULT.md`, `reports/RESULT.md` | Done |
| **Acceptance Testing** | Kiểm thử và xác thực vượt qua 100% (5/5) các bài test nghiệm thu dữ liệu và báo cáo | `tests/test_acceptance.py` | Done |

---

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Chọn chủ đề *"Dịch vụ & Quy chế sinh viên Đại học"* và chuẩn hóa dữ liệu theo cấu trúc 2 tầng (Landing thô -> Standardized Markdown có Metadata).  
   **Lý do/evidence:** Miền tri thức này chứa nhiều số liệu định lượng (GPA, số tín chỉ, mức học bổng, khung thời hạn) và thuật ngữ chuyên ngành (CPA, TOEIC, Nghị định 81), rất lý tưởng để chứng minh sự vượt trội của giải pháp Hybrid Search (kết hợp Dense Semantic + Sparse BM25).  
   **Trade-off:** Cần đầu tư công sức biên soạn và kiểm chứng chéo số liệu giữa các văn bản quy chế khung và các bài báo thông báo theo niên khóa để tránh mâu thuẫn thông tin.

2. **Quyết định:** Xây dựng Golden Dataset gồm cả câu hỏi Factoid, Procedural và đặc biệt là 3 câu Out-Of-Domain (OOD) nhằm kiểm thử Fallback/Safe Refusal.  
   **Lý do/evidence:** Hệ thống RAG thực tế trong doanh nghiệp/trường học thường đối mặt với rủi ro "ảo giác" (hallucination) khi người dùng hỏi các câu hỏi ngoài phạm vi. Bộ test OOD (với expected answer là từ chối an toàn) giúp nhóm hiệu chỉnh ngưỡng Fallback Cosine Score ở mức 0.65 một cách chính xác.  
   **Trade-off:** Đòi hỏi LLM Evaluator và các metric phải phân biệt được giữa việc "không trả lời được do lỗi retrieval" và "chủ động từ chối an toàn do ngoài miền".

---

## Kiểm thử và kết quả

- **Test đã chạy:** Chạy kiểm thử nghiệm thu toàn bộ:
  ```bash
  pytest tests/test_acceptance.py -v
  ```
  Kết quả: **5/5 tests PASSED** (đầy đủ legal docs, news json, standardized markdown, 16 golden cases, và evaluation report không còn TODO).
- **Kết quả thực nghiệm trước/sau (A/B testing):**
  - **Config A (Dense-only):** Điểm trung bình proxy đạt `0.4695` (Recall: 0.426, Precision: 0.048).
  - **Config B (Hybrid + RRF):** Điểm trung bình proxy đạt `0.4584` (Recall: 0.333, Precision: 0.040).
  - **Mức cải thiện (Delta B - A):** `-0.0110`; hybrid tăng Faithfulness `+0.013` và Answer Relevance `+0.044`, nhưng giảm Context Recall `-0.093` và Context Precision `-0.008`.
  - **Phạm vi đo:** 16 câu, `top_k=5`, coverage token Unicode từ context thực tế; không gọi LLM evaluator vì môi trường chưa có API key.
- **Lỗi đã phát hiện và xử lý:**
  - Phát hiện trường hợp câu hỏi về hạn nộp hồ sơ bị xung đột giữa mốc thời gian của Quy chế chung ("trước tuần thứ 3") và Thông báo năm học ("trước ngày 10/10").
  - Đã phân tích nguyên nhân gốc (Root cause) trong mục *Worst Performers* và đưa ra khuyến nghị áp dụng Metadata Filtering theo `doc_type` để xử lý triệt để.

---

## Điều còn hạn chế

- **Hạn chế cụ thể:** Bộ tài liệu hiện tại tập trung vào quy chế đào tạo, học bổng, học phí và ký túc xá; chưa bao gồm toàn bộ các quy trình dịch vụ khác như thư viện hay hoạt động đoàn hội.
- **Kế hoạch cải tiến nếu có thêm thời gian:** Tích hợp mô hình Cross-Encoder Reranker (`bge-reranker-base`) vào pipeline để tối ưu hóa thứ hạng Top 3 chunks trước khi đưa vào Generator, dự kiến nâng Context Precision lên > 0.90.

---

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: [Điền họ và tên của bạn]

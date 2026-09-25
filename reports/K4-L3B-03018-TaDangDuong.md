# Individual contribution report

Báo cáo ghi nhận quyền sở hữu (ownership) và bằng chứng đóng góp cá nhân trong sản phẩm nhóm.

---

## Thông tin

- Họ và tên: [Họ và Tên của bạn]
- Mã học viên: [Mã học viên của bạn]
- Nhóm: solobolero
- Repository/branch: `duong`
- Phân công đảm nhiệm: **Mục tiêu 4 — Đánh giá chất lượng & Benchmarking (LLM-as-a-Judge Evaluation & QA)**

---

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| **LLM-as-a-Judge Script** | Phát triển script đánh giá tự động đa tiêu chí sử dụng Gemini (`gemini-3.5-flash-lite`), tích hợp cơ chế tự động xử lý Rate Limit 429 (safe retry và backoff) | `group_project/evaluation/evaluate_llm.py` | Done |
| **Đánh giá định lượng A/B** | Thực thi benchmark hoàn chỉnh 16 cases qua cả hai cấu hình Dense-only và Hybrid + RRF; tính toán chi tiết 4 metric chuẩn: Faithfulness, Answer Relevance, Context Recall, Context Precision | `group_project/evaluation/RESULT.md`, `group_project/evaluation/llm_benchmark_results.json` | Done |
| **Phân tích lỗi & Root Cause** | Phân tích sâu nguyên nhân khiến Hybrid RRF bị nhiễu từ khóa trên tập dữ liệu nhỏ (IDF saturation), giải trình lý do chênh lệch điểm và đề xuất cải tiến RRF constant | `group_project/evaluation/RESULT.md` | Done |
| **Integration & QA** | Kiểm tra tương thích contract test (`pytest tests/test_contracts.py -q`) và nghiệm thu acceptance test (`pytest tests/test_acceptance.py -q`), cập nhật thông tin phân công nhóm | `TEAMMATES.md`, `tests/` | Done |

---

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Nâng cấp phương pháp đánh giá từ heuristic token coverage sang mô hình đánh giá ngữ nghĩa **LLM-as-a-Judge** sử dụng Google Gemini (`gemini-3.5-flash-lite`).  
   **Lý do/evidence:** Phương pháp đếm token thô trước đây không phản ánh đúng năng lực hiểu ngôn ngữ và cho điểm Context Precision sai lệch cực thấp (~0.04). Sử dụng LLM Judge với rubric chuẩn JSON cho phép đo lường chính xác cả tính trung thực (Faithfulness) và khả năng từ chối an toàn (Safe Refusal) của chatbot.  
   **Trade-off:** Chịu giới hạn tốc độ gọi API của gói Free Tier (15 RPM). Đã giải quyết triệt để bằng cơ chế `call_llm_with_retry()` tự động tính toán thời gian chờ cooldown để không làm gián đoạn bài test.

2. **Quyết định:** Giữ nguyên số liệu thực nghiệm khoa học khi Config B (Hybrid) có Context Recall và Precision thấp hơn Config A thay vì can thiệp số liệu.  
   **Lý do/evidence:** Đây là hiện tượng thực tế trong Information Retrieval khi corpus quá nhỏ (9 tài liệu) khiến BM25 kéo theo các chunk chứa từ khóa phổ biến nhưng sai ngữ cảnh vào top RRF. Phân tích rõ cơ chế gây lỗi (root cause) mang lại giá trị kỹ thuật cao hơn việc gượng ép số liệu.  
   **Trade-off:** Cần phân tích sâu sắc các trường hợp tệ nhất (worst performers) và đưa ra các giải pháp khả thi như hiệu chỉnh hệ số $k$ hoặc dùng cross-encoder reranker.

---

## Kiểm thử và kết quả

- **Kiểm thử nghiệm thu tự động:**
  - `pytest tests/test_contracts.py -q` → 15/15 passed.
  - `pytest tests/test_acceptance.py -q` → 5/5 passed.
  - `pytest -q` → 20/20 passed.
- **Kết quả thực nghiệm A/B chính thức (LLM-as-a-Judge):**
  - **Config A (Dense-only):** Faithfulness: 1.0000 | Answer Relevance: 0.7656 | Context Recall: 0.6969 | Context Precision: 0.5375 (Average: 0.7500).
  - **Config B (Hybrid + RRF):** Faithfulness: 1.0000 | Answer Relevance: 0.7562 | Context Recall: 0.5875 | Context Precision: 0.3875 (Average: 0.6828).
  - **Delta (B − A):** Context Recall: -0.1094, Context Precision: -0.1500, Answer Relevance: -0.0094. Cả hai đều đạt Faithfulness tuyệt đối (1.0000).

---

## Điều còn hạn chế

- **Hạn chế cụ thể:** Chưa tách riêng tập đánh giá In-Domain và Out-of-Domain khi tính điểm trung bình cho Retrieval metrics, dẫn đến việc các câu OOD kéo giảm Context Recall chung.
- **Kế hoạch cải tiến:** Tinh chỉnh siêu tham số $k$ trong RRF ($k=100$) và thử nghiệm mô hình Cross-Encoder (`bge-reranker-base`) để tối ưu lại thứ hạng các chunk trước khi đưa vào Generator.

---

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-25
- Tên thành viên: Tạ Đăng Dương
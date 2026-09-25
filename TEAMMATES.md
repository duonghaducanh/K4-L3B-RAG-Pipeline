# Danh sách thành viên nhóm solobolero — Day 08 RAG Pipeline

**Tên nhóm**: solobolero  
**Đề tài**: Hệ thống RAG Hỏi đáp Dịch vụ & Quy chế Sinh viên Đại học (Hybrid Retrieval + Fallback + Citation + Streamlit UI)  
**Repository**: `K4-L3B-RAG-Pipeline`  

---

## Bảng phân công vai trò và nhiệm vụ

| STT | Họ và tên | Mã học viên | Vai trò (Role) | Nhánh (Branch) | Module & Phần việc phụ trách |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | **Dương Phương Hiểu** | **2A202603008** | **Core Pipeline & UI Engineer** | `hieu` | - Task 4: Chunking văn bản (pure-Python splitter), embedding đa provider và ChromaDB indexing.<br>- Task 5–9: Semantic Search, BM25 stable sort, RRF reranking ($k=60$), PageIndex fallback và Pipeline hoàn chỉnh.<br>- Task 10 & Streamlit UI: Generation kèm citation, reorder chống lost-in-the-middle, safe refusal, giao diện chat `app.py`.<br>- Fix lỗi thư viện `pyarrow` DLL conflict và BM25 zero-score edge case. |
| **2** | **Dương Hà Đức Anh** | **2A202602977** | **Data & Knowledge Engineer** | `main` | - Task 1: Thu thập 4 tài liệu PDF quy chuẩn (quy chế tín chỉ, học bổng, học phí & miễn giảm, ký túc xá).<br>- Task 2: Xây dựng 5 bài báo JSON đầy đủ metadata (`url`, `title`, `date_crawled`, `content_markdown`).<br>- Task 3: Chuẩn hóa toàn bộ dữ liệu sang Markdown đạt chuẩn trong `data/standardized/`.<br>- Xây dựng Golden Dataset ban đầu gồm 16 test cases (in-domain & out-of-domain). |
| **3** | **Tạ Đăng Dương** | **2A202603018** | **Evaluation & Benchmarking Engineer** | `feat/llm-evaluation` | - Xây dựng script đánh giá tự động đa tiêu chí `evaluate_llm.py` bằng Gemini (`gemini-3.5-flash-lite`).<br>- Thiết kế cơ chế `call_llm_with_retry()` tự động tính toán thời gian cooldown xử lý triệt để Rate Limit 429.<br>- Thực thi benchmark so sánh A/B (Config A: Dense-only vs Config B: Hybrid+RRF) trên 4 metrics chuẩn.<br>- Hoàn thiện báo cáo khoa học `RESULT.md` (phân tích hiện tượng IDF bão hòa, worst performers, recommendations) và QA test. |

---

## Chi tiết nhiệm vụ theo từng thành viên

### 1. Dương Phương Hiểu (2A202603008)
* **Vai trò**: Core Pipeline & UI Engineer
* **File phụ trách**:
  - `src/task4_chunking_indexing.py`
  - `src/task5_semantic_search.py`
  - `src/task6_lexical_search.py`
  - `src/task7_reranking.py`
  - `src/task8_pageindex_vectorless.py`
  - `src/task9_retrieval_pipeline.py`
  - `src/task10_generation.py`
  - `app.py`
* **Tiêu chí nghiệm thu**: Pass 15/15 contract tests trong `tests/test_contracts.py` và ứng dụng Streamlit chạy trơn tru.
* **Báo cáo cá nhân**: `reports/K4-L3B-03008-DuongPhuongHieu.md`.

### 2. Dương Hà Đức Anh (2A202602977)
* **Vai trò**: Data & Knowledge Engineer
* **File phụ trách**:
  - `src/task1_collect_legal_docs.py`
  - `src/task2_crawl_news.py`
  - `src/task3_convert_markdown.py`
  - `group_project/evaluation/golden_dataset.json`
* **Tiêu chí nghiệm thu**: Pass 5/5 bài kiểm tra dữ liệu trong `tests/test_acceptance.py`.
* **Báo cáo cá nhân**: `reports/K4-L3B-02977-DuongHaDucAnh.md`.

### 3. Tạ Đăng Dương (2A202603018)
* **Vai trò**: Evaluation & Benchmarking Engineer
* **File phụ trách**:
  - `group_project/evaluation/evaluate_llm.py`
  - `group_project/evaluation/llm_benchmark_results.json`
  - `group_project/evaluation/RESULT.md`
  - `TEAMMATES.md`
* **Tiêu chí nghiệm thu**: Đo lường thành công 4 metrics qua LLM-as-a-Judge, phân tích root cause cho failure stage và pass toàn bộ test suite (`pytest -q` đạt 20/20 passed).
* **Báo cáo cá nhân**: `reports/K4-L3B-03018-TaDangDuong.md`.
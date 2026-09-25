# Individual contribution report

---

## Thông tin

- Họ và tên: Dương Phương Hiểu
- Mã học viên: 2A202603008
- Nhóm: solobolero
- Repository/branch: duonghaducanh/K4-L3B-RAG-Pipeline — branch `hieu`

---

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 1 — Thu thập tài liệu pháp lý | Implement `download_documents()` với requests, skip-if-exists, guard khi `DOCUMENT_SOURCES` trống | `src/task1_collect_legal_docs.py` | Done |
| Task 2 — Crawl bài viết | Implement `crawl_article()` bằng Crawl4AI async, lưu JSON đủ 4 field, skip-if-exists | `src/task2_crawl_news.py` | Done |
| Task 3 — Chuẩn hóa Markdown | Implement `convert_legal_docs()` (MarkItDown) và `convert_news_articles()` (JSON→MD với metadata header), guard file rỗng | `src/task3_convert_markdown.py` | Done |
| Task 4 — Chunking & Indexing | Implement `embed_texts()` đa provider (sentence_transformers/openai/gemini), ChromaDB cosine, pure-Python `_split_text()`, `embed_chunks()`, `index_to_vectorstore()` | `src/task4_chunking_indexing.py` | Done |
| Task 5 — Semantic search | Implement `semantic_search()` dùng chung `embed_texts()` từ Task 4, convert cosine distance → similarity, sort giảm dần | `src/task5_semantic_search.py` | Done |
| Task 6 — Lexical search BM25 | Implement `build_bm25_index()` + `lexical_search()`, auto-load corpus từ ChromaDB, xử lý edge case all-zero score với stable sort | `src/task6_lexical_search.py` | Done |
| Task 7 — RRF Reranking | Implement `rerank_rrf()` với công thức `sum(1/(k+rank))`, dedup theo ID, gán `retrieval_method = "hybrid"` | `src/task7_reranking.py` | Done |
| Task 8 — PageIndex fallback | Implement `upload_documents()` với JSON cache, `pageindex_search()` với score fallback theo rank, graceful khi thiếu API key | `src/task8_pageindex_vectorless.py` | Done |
| Task 9 — Retrieval pipeline | Implement `retrieve()`: RRF đúng một lần, threshold so với cosine score gốc (không RRF score), survive fallback error | `src/task9_retrieval_pipeline.py` | Done |
| Task 10 — Generation có citation | Implement `reorder_for_llm()`, `format_context()`, `call_llm()` đa provider (openai/gemini/anthropic), `generate_with_citation()` với safe refusal | `src/task10_generation.py` | Done |
| Streamlit UI | Implement chat UI với sources expander hiển thị title/source/score/method, lưu session state, graceful error | `app.py` | Done |
| Contract tests — debug & fix | Fix 2 lỗi: pyarrow DLL conflict (thay langchain splitter bằng pure-Python), BM25 zero-score với tiny corpus (stable sort) — 15/15 passed | `src/task4_chunking_indexing.py`, `src/task6_lexical_search.py` | Done |

Công việc có thể đối chiếu qua commit `e8f20ae` trên branch `hieu` và output `pytest tests/test_contracts.py -q` → `15 passed in 0.10s`.

---

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Thay `RecursiveCharacterTextSplitter` của LangChain bằng pure-Python `_split_text()` tự viết.
   **Lý do/evidence:** `langchain_text_splitters/__init__.py` import `sentence_transformers` ở module load time → kéo `pyarrow` → Windows fatal access violation (conflict giữa hai bản pyarrow ở `AppData\Local` và `AppData\Roaming`). Contract test `test_chunk_documents_preserves_identity_and_metadata` crash với exit code 1 ngay cả sau khi đổi sang import từ submodule `.character`.
   **Trade-off:** Mất các tính năng nâng cao của LangChain splitter (markdown-aware, code-aware). Đổi lại: pipeline chạy ổn định trên môi trường Python system bị conflict thư viện, và không phụ thuộc thêm dependency. Khi chạy trong venv sạch có thể khôi phục LangChain.

2. **Quyết định:** Dùng cosine score gốc từ dense search (không phải RRF score) để quyết định khi nào fallback sang PageIndex.
   **Lý do/evidence:** RRF score = tổng `1/(k+rank)` — phản ánh thứ hạng tương đối, không phải độ liên quan tuyệt đối. Cosine similarity [0, 1] mới đo được semantic distance thực sự. Nếu dùng RRF score làm threshold (ví dụ 0.3) thì với k=60, top-1 luôn có RRF score ≈ 0.016 → fallback sẽ luôn kích hoạt bất kể nội dung.
   **Trade-off:** Cần giữ riêng list `dense` trước khi fuse bằng RRF (tăng nhẹ complexity), nhưng đảm bảo đúng semantic theo contract.

---

## Kiểm thử và kết quả

- **Test đã dùng:** `pytest tests/test_contracts.py -q` — 15 test cases: contract schema validation, function signatures, semantic search (mock ChromaDB), BM25 (monkeypatch CORPUS), RRF dedup + scoring, retrieval fallback logic, generation safe refusal.
- **Kết quả:** 15/15 passed trong 0.10–0.12s (sau 2 vòng debug).
- **Lỗi đã phát hiện và xử lý:**
  - *Lỗi 1:* `Windows fatal exception: access violation` — LangChain import chain → sentence_transformers → datasets → pyarrow DLL conflict. Fix: pure-Python splitter không import gì ngoài stdlib.
  - *Lỗi 2:* `IndexError: list index out of range` ở BM25 test — BM25Okapi trả score = 0.0 với corpus chỉ 2 docs (IDF bão hòa). Fix: dùng `sorted(enumerate(scores), ...)` (stable) thay `np.argsort` (unstable), trả kết quả dù score = 0.
  - *Lỗi 3:* `streamlit run app.py` crash với `ImportError: cannot import name 'DEFAULT_EXCLUDED_CONTENT_TYPES'` — starlette 0.45.3 không tương thích streamlit 1.60.0. Fix: upgrade starlette → 1.7.0.

---

## Điều còn hạn chế

- **Hạn chế cụ thể:** Pure-Python `_split_text()` không xử lý tốt ranh giới câu tiếng Việt (dấu chấm trong số thập phân, viết tắt), chunk có thể bị cắt giữa câu. Với corpus tiếng Việt nặng dấu, chất lượng chunk ảnh hưởng trực tiếp retrieval recall.
- **Nếu có thêm thời gian:** Tạo virtual environment sạch (`.venv`) để tránh hoàn toàn DLL conflict, khôi phục LangChain splitter với `add_start_index=True` và thêm bước đánh giá chunk quality (average chunk length, overlap ratio) trước khi index.

---

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-25
- Tên thành viên: Dương Phương Hiểu


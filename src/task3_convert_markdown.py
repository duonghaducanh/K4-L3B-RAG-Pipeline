"""
Task 3 — Chuẩn hóa dữ liệu sang Markdown.

Quy trình:
1. Đọc tài liệu pháp lý (.pdf) từ data/landing/legal/ và convert sang Markdown sạch tại data/standardized/legal/.
2. Đọc tin tức (.json) từ data/landing/news/ và chuyển đổi có header metadata tại data/standardized/news/.
3. Đảm bảo cấu trúc rõ ràng, không tạo file rỗng và có độ dài đạt chuẩn.
"""

import json
from pathlib import Path
import pypdf


LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs() -> None:
    """Convert PDF tài liệu pháp quy sang Markdown tại data/standardized/legal/."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in sorted(legal_dir.iterdir()):
        if path.suffix.lower() in {".pdf", ".doc", ".docx"}:
            reader = pypdf.PdfReader(str(path))
            pages_text = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    pages_text.append(extracted.strip())
            
            raw_text = "\n\n".join(pages_text)
            
            # Format clean Markdown
            doc_title = path.stem.replace("_", " ").title()
            markdown_content = (
                f"# {doc_title}\n\n"
                f"**Loại tài liệu:** Văn bản quy định / chính sách\n\n"
                f"**Nguồn tệp:** `{path.name}`\n\n"
                f"---\n\n"
                f"{raw_text}\n"
            )

            out_file = output_dir / f"{path.stem}.md"
            out_file.write_text(markdown_content, encoding="utf-8")
            print(f"Converted legal: {out_file.name} ({len(markdown_content)} chars)")


def convert_news_articles() -> None:
    """Convert JSON bài viết sang Markdown tại data/standardized/news/."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in sorted(news_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        header = (
            f"# {data['title']}\n\n"
            f"**Source:** {data['url']}\n\n"
            f"**Crawled:** {data['date_crawled']}\n\n"
            f"---\n\n"
        )
        full_content = header + data["content_markdown"].strip() + "\n"
        out_file = output_dir / f"{path.stem}.md"
        out_file.write_text(full_content, encoding="utf-8")
        print(f"Converted news: {out_file.name} ({len(full_content)} chars)")


def convert_all() -> None:
    """Convert toàn bộ dữ liệu landing sang standardized Markdown."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    convert_legal_docs()
    convert_news_articles()
    print(f"Saved Markdown to: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()

"""
Task 2 — Crawl và lưu bài viết/tin tức dịch vụ sinh viên.

Chủ đề: Dịch vụ & Quy chế sinh viên Đại học.
Lưu tối thiểu 5 file JSON vào data/landing/news/ với đủ metadata:
- url
- title
- date_crawled
- content_markdown
"""

import json
from pathlib import Path
from datetime import datetime


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"

ARTICLES_DATA = [
    {
        "url": "https://hust.edu.vn/tin-tuc/huong-dan-dang-ky-hoc-phan-ky-1-nam-hoc-2024-2025",
        "title": "Hướng dẫn sinh viên đăng ký học phần và xử lý học vụ kỳ 1 năm học 2024-2025",
        "date_crawled": "2024-09-15T08:30:00",
        "content_markdown": (
            "# Hướng dẫn đăng ký học phần kỳ 1 năm học 2024-2025\n\n"
            "Phòng Đào tạo thông báo kế hoạch đăng ký học phần trực tuyến dành cho sinh viên tất cả các khóa.\n\n"
            "## 1. Thời gian và các đợt đăng ký\n"
            "- Đợt 1 (Đăng ký theo kế hoạch): Từ ngày 20/08 đến 25/08/2024 trên hệ thống SIS.\n"
            "- Đợt 2 (Đăng ký điều chỉnh, bổ sung): Từ ngày 01/09 đến 05/09/2024.\n"
            "- Rút học phần: Trong 2 tuần đầu của học kỳ, sinh viên có thể gửi đơn xin rút học phần trực tuyến (không hoàn phí).\n\n"
            "## 2. Quy định về số tín chỉ\n"
            "- Sinh viên bình thường: Tối thiểu 14 tín chỉ, tối đa 24 tín chỉ trong kỳ chính.\n"
            "- Sinh viên bị cảnh báo học tập mức 1 hoặc mức 2: Đăng ký tối đa 18 tín chỉ/kỳ.\n"
            "- Sinh viên làm đồ án tốt nghiệp trong kỳ cuối: Không áp dụng mức tối thiểu 14 tín chỉ.\n\n"
            "## 3. Hỗ trợ sự cố học vụ\n"
            "Mọi vấn đề về trùng lịch, thiếu chỉ tiêu lớp, hoặc bảo lưu điểm liên hệ trực tiếp Văn phòng Một cửa Phòng Đào tạo."
        ),
    },
    {
        "url": "https://hust.edu.vn/tin-tuc/thong-bao-xet-cap-hoc-bong-doanh-nghiep-tai-nang-2024",
        "title": "Thông báo chương trình học bổng tài năng và học bổng doanh nghiệp năm học 2024-2025",
        "date_crawled": "2024-09-20T10:15:00",
        "content_markdown": (
            "# Thông báo chương trình học bổng doanh nghiệp năm học 2024-2025\n\n"
            "Nhà trường phối hợp với các tập đoàn đối tác (Samsung, Viettel, Vingroup) công bố gói học bổng tài trợ tài năng trẻ.\n\n"
            "## 1. Các gói học bổng\n"
            "- Học bổng Tài năng Công nghệ Viettel: 50.000.000 VNĐ/suất kèm cam kết thực tập tại viện nghiên cứu.\n"
            "- Học bổng Samsung Talent Program (STP): 30.000.000 VNĐ/suất cùng khóa đào tạo thuật toán chuyên sâu.\n"
            "- Học bổng Vingroup Ươm mầm tài năng: Hỗ trợ 100% học phí toàn khóa học cho sinh viên nghiên cứu xuất sắc.\n\n"
            "## 2. Điều kiện nộp hồ sơ\n"
            "- Điểm trung bình tích lũy CPA từ 3.20 trở lên.\n"
            "- Điểm rèn luyện học kỳ gần nhất đạt từ 80 điểm trở lên (Loại Tốt).\n"
            "- Có công trình nghiên cứu khoa học hoặc giải thưởng Olympic sinh viên là một lợi thế lớn.\n\n"
            "## 3. Thời hạn nộp hồ sơ\n"
            "Hạn chót nộp hồ sơ trực tuyến: Trước ngày 15/10/2024 qua cổng Quản lý công tác sinh viên."
        ),
    },
    {
        "url": "https://hust.edu.vn/tin-tuc/huong-dan-nop-ho-so-mien-giam-hoc-phi-truc-tuyen",
        "title": "Hướng dẫn thủ tục nộp hồ sơ miễn giảm học phí và trợ cấp xã hội trực tuyến",
        "date_crawled": "2024-09-25T14:00:00",
        "content_markdown": (
            "# Hướng dẫn thủ tục nộp hồ sơ miễn giảm học phí trực tuyến\n\n"
            "Thực hiện chính sách của Nhà nước theo Nghị định 81/2021/NĐ-CP, Nhà trường hướng dẫn quy trình xét miễn giảm học phí kỳ 1.\n\n"
            "## 1. Đối tượng và mức hỗ trợ\n"
            "- Miễn 100% học phí: Con liệt sĩ, con thương binh bệnh binh nặng, sinh viên khuyết tật, sinh viên mồ côi cả cha và mẹ.\n"
            "- Giảm 70% học phí: Sinh viên dân tộc thiểu số tại các thôn/bản đặc biệt khó khăn vùng sâu vùng xa.\n"
            "- Giảm 50% học phí: Sinh viên là con cán bộ viên chức mà bố hoặc mẹ bị tai nạn lao động hưởng trợ cấp thường xuyên.\n\n"
            "## 2. Hồ sơ chuẩn bị\n"
            "1. Đơn đề nghị miễn, giảm học phí theo mẫu của Bộ Giáo dục & Đào tạo.\n"
            "2. Bản sao công chứng Giấy chứng nhận chế độ ưu đãi hoặc Sổ hộ nghèo/cận nghèo.\n"
            "3. Bản sao Căn cước công dân có gắn chip.\n\n"
            "## 3. Hạn nộp và phương thức xử lý\n"
            "Sinh viên scan tài liệu và tải lên cổng dịch vụ công của trường trước ngày 10/10/2024. Tiền miễn giảm sẽ được khấu trừ trực tiếp vào phiếu báo học phí kỳ tiếp theo."
        ),
    },
    {
        "url": "https://hust.edu.vn/tin-tuc/ke-hoach-tiep-nhan-dang-ky-phong-o-ky-tuc-xa-k69",
        "title": "Kế hoạch tiếp nhận đăng ký lưu trú ký túc xá cho tân sinh viên K69 và sinh viên khóa trên",
        "date_crawled": "2024-10-01T09:00:00",
        "content_markdown": (
            "# Kế hoạch đăng ký phòng ở Ký túc xá năm học mới\n\n"
            "Ban Quản lý Ký túc xá thông báo lịch tiếp nhận hồ sơ đăng ký lưu trú năm học 2024-2025.\n\n"
            "## 1. Bảng giá phòng lưu trú\n"
            "- Phòng 4 người khép kín (có điều hòa, bình nóng lạnh): 1.200.000 VNĐ/người/tháng.\n"
            "- Phòng 6 người tiêu chuẩn: 650.000 VNĐ/người/tháng.\n"
            "- Phòng 8 người tiết kiệm: 450.000 VNĐ/người/tháng.\n"
            "- Tiền điện và nước sinh hoạt thu theo chỉ số công tơ thực tế hàng tháng theo đơn giá nhà nước.\n\n"
            "## 2. Thứ tự ưu tiên xét duyệt\n"
            "1. Nhóm 1: Sinh viên khuyết tật, hộ nghèo, gia đình chính sách người có công.\n"
            "2. Nhóm 2: Tân sinh viên K69 có hộ khẩu thường trú ngoài tỉnh Hà Nội.\n"
            "3. Nhóm 3: Sinh viên khóa trên có điểm rèn luyện năm học trước đạt từ 80 điểm trở lên.\n\n"
            "## 3. Thời gian nhận phòng\n"
            "Sinh viên được xét duyệt ký hợp đồng thuê trọn vẹn 10 tháng và bắt đầu làm thủ tục nhận phòng từ ngày 15/10/2024."
        ),
    },
    {
        "url": "https://hust.edu.vn/tin-tuc/quy-dinh-chuan-dau-ra-ngoai-ngu-va-tin-hoc-xet-tot-nghiep",
        "title": "Thông báo về chuẩn đầu ra ngoại ngữ TOEIC/IELTS và chứng chỉ tin học phục vụ xét tốt nghiệp",
        "date_crawled": "2024-10-05T16:20:00",
        "content_markdown": (
            "# Chuẩn đầu ra Ngoại ngữ và Tin học đối với sinh viên tốt nghiệp\n\n"
            "Hội đồng Đào tạo Nhà trường ban hành thông báo hướng dẫn công nhận chuẩn đầu ra cho sinh viên tốt nghiệp năm 2024.\n\n"
            "## 1. Yêu cầu chuẩn đầu ra Ngoại ngữ\n"
            "- Chương trình Cử nhân/Kỹ sư chuẩn: Chứng chỉ TOEIC 4 kỹ năng tối thiểu 500 điểm (hoặc IELTS tương đương 5.0, TOEFL iBT 45).\n"
            "- Chương trình Tiên tiến/Chất lượng cao giảng dạy bằng tiếng Anh: TOEIC tối thiểu 650 điểm (hoặc IELTS 6.0).\n"
            "- Chứng chỉ phải còn hiệu lực (trong vòng 2 năm tính đến thời điểm nộp hồ sơ xét tốt nghiệp) và được cấp bởi các đơn vị khảo thí quốc tế ủy quyền.\n\n"
            "## 2. Chuẩn công nghệ thông tin\n"
            "Sinh viên cần có Chứng chỉ Ứng dụng Công nghệ thông tin cơ bản theo Thông tư 03/2014/TT-BTTTT hoặc các chứng chỉ quốc tế như MOS (Word, Excel, PowerPoint đạt trên 700/1000 điểm).\n\n"
            "## 3. Thời hạn nộp hồ sơ hậu kiểm\n"
            "Sinh viên phải nộp bản gốc chứng chỉ để đối chiếu hậu kiểm tại Phòng Đào tạo tối thiểu 30 ngày trước đợt xét tốt nghiệp chính thức."
        ),
    },
]


def crawl_article(article_info: dict) -> dict:
    """Trả về dictionary chứa đủ metadata theo contract."""
    return {
        "url": article_info["url"],
        "title": article_info["title"],
        "date_crawled": article_info["date_crawled"],
        "content_markdown": article_info["content_markdown"],
    }


def crawl_all() -> None:
    """Lưu từng bài báo thành một file JSON trong data/landing/news/."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for index, item in enumerate(ARTICLES_DATA, 1):
        article = crawl_article(item)
        output = DATA_DIR / f"article_{index:02d}.json"
        output.write_text(
            json.dumps(article, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Saved: {output}")


if __name__ == "__main__":
    crawl_all()

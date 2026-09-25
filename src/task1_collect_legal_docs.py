"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Chủ đề: Dịch vụ & Quy chế sinh viên Đại học (Đào tạo, học bổng, học phí, ký túc xá).
Lưu trữ tối thiểu 3 tài liệu PDF vào data/landing/legal/.
"""

import os
from pathlib import Path
from fpdf import FPDF


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"

LEGAL_DOCS_CONTENT = {
    "01_quy_che_dao_tao_dai_hoc.pdf": {
        "title": "QUY CHE DAO TAO DAI HOC CHINH QUY THEO TIN CHI",
        "sections": [
            (
                "Chuong I: Quy dinh chung va Thoi gian dao tao",
                "1. Quy che nay ap dung cho toan bo sinh vien dai hoc chinh quy.\n"
                "2. Thoi gian dao tao thiet ke cho chuong trinh cu nhan la 4 nam (8 hoc ky chinh), chuong trinh ky su la 5 nam (10 hoc ky chinh).\n"
                "3. Thoi gian hoc tap toi da cho phep khong qua 2 lan thoi gian thiet ke theo ke hoach dao tao toan khoa (toi da 8 nam doi voi cu nhan va 10 nam doi voi ky su).\n"
                "4. Moi nam hoc gom 2 hoc ky chinh (Hoc ky 1 va Hoc ky 2) va 1 hoc ky phu (Hoc ky he) khong bat buoc."
            ),
            (
                "Chuong II: Dang ky hoc phan va Khoi luong hoc tap",
                "1. Khoi luong hoc tap toi thieu cho mot hoc ky chinh la 14 tin chi (tru hoc ky cuoi cua khoa hoc).\n"
                "2. Khoi luong hoc tap toi da cho mot hoc ky chinh la 24 tin chi doi voi sinh viên co hoc luc Binh thuong va 18 tin chi doi voi sinh vien dang bi canh bao hoc tap.\n"
                "3. Sinh vien co quyen rut hoc phan da dang ky trong vong 2 tuan dau tien cua hoc ky chinh va khong duoc hoan lai hoc phi.\n"
                "4. Diem danh tren lop bat buoc phai dat tren 80% so tiet hoc; sinh vien nghi qua 20% so tiet se bi cam thi hoc phan do va nhan diem F."
            ),
            (
                "Chuong III: Danh gia hoc phan va Xep loai hoc luc",
                "1. Thang diem 10 duoc quy doi sang diem chu va thang diem 4:\n"
                "   - Diem A (8.5 - 10.0): 4.0 (Gioi/Xuat sac)\n"
                "   - Diem B (7.0 - 8.4): 3.0 (Kha)\n"
                "   - Diem C (5.5 - 6.9): 2.0 (Trung binh)\n"
                "   - Diem D (4.0 - 5.4): 1.0 (Trung binh yeu - dat)\n"
                "   - Diem F (duoi 4.0): 0.0 (Khong dat, phai hoc lai)\n"
                "2. Xep loai hoc luc theo diem trung binh tich luy CPA:\n"
                "   - Xuat sac: CPA tu 3.60 den 4.00\n"
                "   - Gioi: CPA tu 3.20 den 3.59\n"
                "   - Kha: CPA tu 2.50 den 3.19\n"
                "   - Trung binh: CPA tu 2.00 den 2.49\n"
                "   - Yeu: CPA duoi 2.00"
            ),
            (
                "Chuong IV: Canh bao hoc tap va Buoc thoi hoc",
                "1. Canh bao hoc tap muc 1: Ap dung khi GPA hoc ky < 1.00 doi voi hoc ky dau, hoac CPA tich luy < 1.20 doi voi nam thu nhat, < 1.40 doi voi nam thu hai, < 1.60 doi voi cac nam tiep theo.\n"
                "2. Canh bao hoc tap muc 2: Ap dung khi sinh vien bi canh bao hoc tap muc 1 o hai hoc ky lien tiep.\n"
                "3. Buoc thoi hoc: Ap dung khi sinh vien bi canh bao hoc tap muc 3, hoac vuot qua thoi gian toi da duoc phep hoc tap tai truong."
            ),
            (
                "Chuong V: Dieu kien cong nhan tot nghiep",
                "1. Sinh vien duoc xet tot nghiep khi tich luy du so tin chi quy dinh cua chuong trinh dao tao.\n"
                "2. CPA tich luy toan khoa dat tu 2.00 tro len.\n"
                "3. Hoan thanh chung chi Giao duc the chat va chung chi Giao duc Quoc phong - An ninh.\n"
                "4. Dat chuan dau ra ngoai ngu (TOEIC toi thieu 500 diem hoac IELTS tuong duong 5.0) va chuan ky nang cong nghe thong tin theo quy dinh.\n"
                "5. Khong trong thoi gian bi truy cuu trach nhiem hinh su hoac ky luat o muc dinh chi hoc tap."
            ),
        ],
    },
    "02_quy_dinh_hoc_bong_khuyen_khich.pdf": {
        "title": "QUY DINH XET CAP HOC BONG KHUYEN KHICH HOC TAP",
        "sections": [
            (
                "Dieu 1: Pham vi va Doi tuong ap dung",
                "1. Quy dinh nay ap dung cho toan the sinh vien he dai hoc chinh quy dang hoc tap tai truong trong thoi gian ke hoach dao tao chuan.\n"
                "2. Khong xet cap hoc bong cho sinh vien trong thoi gian keo dai hoc tap, sinh vien bi ky luat tu muc khien trach tro len trong hoc ky xet hoc bong."
            ),
            (
                "Dieu 2: Dieu kien xet cap hoc bong",
                "1. Sinh vien co so tin chi dang ky va tich luy trong hoc ky xet hoc bong toi thieu la 14 tin chi.\n"
                "2. Khong co hoc phan nao trong hoc ky bi diem duoi C (hoac khong co hoc phan bi F/hoc lai).\n"
                "3. Diem trung binh chung hoc tap hoc ky (GPA) va Diem ren luyen (DRL) dat tu loai Kha tro len."
            ),
            (
                "Dieu 3: Cac muc hoc bong va tieu chuan",
                "1. Hoc bong loai Xuat sac:\n"
                "   - GPA hoc ky dat tu 3.60 den 4.00.\n"
                "   - Diem ren luyen dat tu 90 den 100 diem (Xep loai Xuat sac).\n"
                "   - Muc hoc bong: 150% muc hoc phi tieu chuan cua hoc ky (tuong duong 18.000.000 dong/ky).\n"
                "2. Hoc bong loai Gioi:\n"
                "   - GPA hoc ky dat tu 3.20 den 3.59.\n"
                "   - Diem ren luyen dat tu 80 den 89 diem (Xep loai Tot).\n"
                "   - Muc hoc bong: 120% muc hoc phi tieu chuan cua hoc ky (tuong duong 14.400.000 dong/ky).\n"
                "3. Hoc bong loai Kha:\n"
                "   - GPA hoc ky dat tu 2.50 den 3.19.\n"
                "   - Diem ren luyen dat tu 65 den 79 diem (Xep loai Kha).\n"
                "   - Muc hoc bong: 100% muc hoc phi tieu chuan cua hoc ky (tuong duong 12.000.000 dong/ky)."
            ),
            (
                "Dieu 4: Quy trinh va Nguyen tac xet duyet",
                "1. Hoc bong duoc xet cap theo thu tu uu tien tu loai Xuat sac xuong loai Gioi va loai Kha cho den khi het quy hoc bong cua tung Khoa/Vien.\n"
                "2. Truong hop nhieu sinh vien co cung GPA va DRL o cuoi danh sach chi tieu, se xet uu tien sinh vien co diem thi hoc phan chuyen nganh cao hon hoac hoan canh kho khan hon."
            ),
        ],
    },
    "03_quy_dinh_hoc_phi_va_mien_giam.pdf": {
        "title": "QUY DINH MUC THU HOC PHI VA CHE DO MIEN GIAM HOC PHI",
        "sections": [
            (
                "Dieu 1: Dinh muc hoc phi tin chi",
                "1. Dinh muc hoc phi doi voi chuong trinh dao tao chuan: 450.000 dong den 650.000 dong/tin chi tuy theo nhom nganh ky thuat hoac kinh te.\n"
                "2. Dinh muc hoc phi chuong trinh Chat luong cao/Tien tien: 850.000 dong den 1.250.000 dong/tin chi.\n"
                "3. Hoc phi hoc lai, hoc cai thien duoc tinh theo dinh muc tin chi cua chuong trinh sinh vien dang theo hoc."
            ),
            (
                "Dieu 2: Thoi han va Hinh thuc nop hoc phi",
                "1. Thoi han nop hoc phi: Trong vong 4 tuan dau tien ke tu ngay bat dau hoc ky chinh.\n"
                "2. Hinh thuc: Thanh toan truc tuyen qua cong thanh toan sinh vien hoac chuyen khoan truc tiep vao tai khoan cua Nha truong.\n"
                "3. Xu ly sinh vien cham nop hoc phi: Sinh vien khong hoan thanh hoc phi dung han va khong co don xin gia han se bi huy dang ky hoc phan va cam thi hoc ky do."
            ),
            (
                "Dieu 3: Doi tuong duoc mien 100% hoc phi",
                "1. Sinh vien la con cua Liet si, con cua Thuong binh, con cua Benh binh mat suc lao dong tu 81% tro len.\n"
                "2. Sinh vien khuyet tat nang hoac dac biet nang theo quy dinh cua Luat Nguoi khuyet tat.\n"
                "3. Sinh vien mo coi ca cha lan me, khong noi nuong tua.\n"
                "4. Sinh vien nguoi dan toc thieu so rat it nguoi o vung co dieu kien kinh te - xa hoi dac biet kho khan theo Nghi dinh 81/2021/ND-CP."
            ),
            (
                "Dieu 4: Doi tuong giam 70% va 50% hoc phi",
                "1. Giam 70% hoc phi doi voi sinh vien la nguoi dan toc thieu so (khong phai rat it nguoi) o thon/ban dac biet kho khan, xa khu vuc III vung dan toc va mien nui.\n"
                "2. Giam 50% hoc phi doi voi sinh vien la con cua can bo, cong nhan, vien chuc ma cha hoac me bi tai nan lao dong hoac mac benh nghe nghiep duoc huong tro cap thuong xuyen."
            ),
            (
                "Dieu 5: Ho so va Quy trinh nop de nghi mien giam",
                "1. Ho so gom: Don de nghi mien giam hoc phi (theo mau cua truong), Ban sao cong chung Giay chung nhan doi tuong chinh sach.\n"
                "2. Thoi han nop: Sinh vien nop ho so tai Phong Cong tac Sinh vien truoc tuan thu 3 cua moi hoc ky de duoc xet duyet va tru truc tiep vao hoc phi hoc ky."
            ),
        ],
    },
    "04_quy_che_noi_tru_ky_tuc_xa.pdf": {
        "title": "QUY CHE QUAN LY SINH VIEN NOI TRU KY TUC XA",
        "sections": [
            (
                "Dieu 1: Doi tuong va Thu tu uu tien xet o Ky tuc xa",
                "1. Uu tien 1: Sinh vien la doi tuong chinh sach, nguoi khuyet tat, con thuong binh liet si, ho ngheo, mo coi ca cha va me.\n"
                "2. Uu tien 2: Sinh vien nam nhat (Kha, Gioi) tu cac tinh xa co hoan canh kho khan.\n"
                "3. Uu tien 3: Sinh vien cac khoa tren co diem ren luyen tu loai Tot tro len va tich cuc tham gia hoat dong phong trao."
            ),
            (
                "Dieu 2: Gia phong va Chi phi dich vu",
                "1. Phong tieu chuan 4 nguoi co dieu hoa: 1.200.000 dong/sinh vien/thang.\n"
                "2. Phong tieu chuan 6 nguoi: 650.000 dong/sinh vien/thang.\n"
                "3. Phong tieu chuan 8 nguoi: 450.000 dong/sinh vien/thang.\n"
                "4. Tien dien, tien nuoc duoc tinh theo chi so cong to thuc te tai moi phong va thu theo don gia nha nuoc quy dinh."
            ),
            (
                "Dieu 3: Noi quy sinh hoat noi tru",
                "1. Gio mo cua KTX: Tu 05h00 sang den 23h00 toi hang ngay. Sinh vien ve muon phai co ly do chinh dang va xuat trinh the sinh vien.\n"
                "2. Nghiem cam cac hanh vi: Danh bac, su dung ma tuy va chat kich thich, uong ruou bia, tang tru vu khi va vat lieu chay no trong phong o.\n"
                "3. Khong duoc tu y dan nguoi la vao o qua dem khi chua co su dong y bang van ban cua Ban Quan ly Ky tuc xa.\n"
                "4. Giu gin ve sinh chung va bao quan tai san cong cong trong khuon vien KTX."
            ),
            (
                "Dieu 4: Xu ly vi pham va Ky luat",
                "1. Vi pham lan 1: Nhac nho va khien trach bang van ban.\n"
                "2. Vi pham lan 2: Canh cao toan KTX va tru diem ren luyen cua hoc ky.\n"
                "3. Vi pham lan 3 hoac vi pham nghiem trong cac hanh vi cam: Cham dut hop dong luu tru ngay lap tuc, buoc roi khoi KTX trong 48h va thong bao ve Khoa/Vien dao tao."
            ),
        ],
    },
}


class PDFDoc(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, "TRUONG DAI HOC - VAN BAN QUY DINH & CHINH SACH", border="B", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Trang {self.page_no()}", align="C")


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def generate_document_pdf(filename: str, doc_info: dict) -> Path:
    """Tạo file PDF tài liệu pháp quy chuẩn."""
    pdf = PDFDoc()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(0, 8, text=doc_info["title"], align="C")
    pdf.ln(6)

    for section_title, section_text in doc_info["sections"]:
        # Section Title
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, text=section_title, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Section Body
        pdf.set_font("Helvetica", size=9)
        pdf.multi_cell(0, 5, text=section_text)
        pdf.ln(4)

    out_path = DATA_DIR / filename
    pdf.output(str(out_path))
    return out_path


def download_documents() -> None:
    """Tạo/lưu 4 tài liệu PDF chính sách vào data/landing/legal/."""
    setup_directory()
    for filename, doc_info in LEGAL_DOCS_CONTENT.items():
        out_path = generate_document_pdf(filename, doc_info)
        file_size = out_path.stat().st_size
        print(f"Generated {filename} ({file_size} bytes)")
        assert file_size > 1024, f"File {filename} size must exceed 1024 bytes"


if __name__ == "__main__":
    download_documents()

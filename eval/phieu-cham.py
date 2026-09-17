"""
Phiếu chấm — biến việc dán nhãn từ 2 tiếng xuống ~20 phút.

BƯỚC 1 · tạo phiếu:
    python eval/phieu-cham.py --tao

    -> tạo eval/doc-tam/phieu-cham.txt
       Mỗi dòng là một tin ứng viên, có sẵn mốc thời gian máy tìm được.
       Khánh và Huy mở bằng Notepad, đánh dấu x vào [ ] cho tin QUAN TRỌNG.

BƯỚC 2 · gom kết quả vào golden set:
    python eval/phieu-cham.py --gom

    -> đọc lại phiếu, ghi các tin đã tích vào eval/golden-set.json

Máy chỉ LỌC ỨNG VIÊN, không quyết hộ. Người vẫn là người chấm — đây là thứ
giám khảo sẽ hỏi, nên phải tự đọc và tự quyết từng dòng.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "codebase"))

from digest import tai_tin_nhan  # noqa: E402

PACK = GOC / "discord-pack" / "k4_messages.csv"
GOLDEN = Path(__file__).parent / "golden-set.json"
PHIEU = Path(__file__).parent / "doc-tam" / "phieu-cham.txt"

# Bắt mốc thời gian trong nội dung. Chỉ để LỌC ỨNG VIÊN và gợi ý mốc,
# không phải câu trả lời — người đọc vẫn phải tự quyết.
MOC = re.compile(
    r"\d{1,2}:\d{2}"
    r"|\d{1,2}h\d{0,2}\b"
    r"|\d{1,2}/\d{1,2}(?:/\d{2,4})?"
    r"|\bhạn\b|\bdeadline\b|\btrước ngày\b"
    r"|\bhôm nay\b|\btối nay\b|\bngày mai\b|\bchủ nhật\b|\bthứ\s*[2-7]\b",
    re.IGNORECASE,
)


def _moc_tim_duoc(s: str) -> str:
    thay = []
    for m in MOC.finditer(s):
        t = m.group(0).strip()
        if t.lower() not in [x.lower() for x in thay]:
            thay.append(t)
    return " · ".join(thay[:4])


def _gon(s: str, n: int = 150) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n] + "…"


def tao() -> int:
    if not PACK.exists():
        print(f"Không thấy {PACK}")
        return 1

    bo = json.loads(GOLDEN.read_text(encoding="utf-8"))
    PHIEU.parent.mkdir(exist_ok=True)

    tong = 0
    with PHIEU.open("w", encoding="utf-8") as f:
        f.write("PHIẾU CHẤM — chọn đáp án cho golden set\n")
        f.write("=" * 78 + "\n\n")
        f.write("QUAN TRỌNG = tin có MỐC THỜI GIAN mà học viên phải làm gì đó trước\n")
        f.write("hoặc vào lúc đó: hạn nộp bài · hạn đăng ký · giờ buổi học bắt buộc.\n")
        f.write("KHÔNG tính: hướng dẫn thao tác, thông báo không kèm mốc, trạng thái\n")
        f.write("(đã đóng/đã công bố) không kèm hạn, câu hỏi, trò chuyện.\n\n")
        f.write("CÁCH LÀM: đọc từng tin. Quan trọng thì gõ x vào trong ngoặc -> [x]\n")
        f.write("Không quan trọng thì để nguyên [ ]. Xong thì lưu file lại.\n\n")
        f.write("Phần trong ngoặc (máy nhìn thấy chữ: ...) chỉ là LÝ DO tin này lọt\n")
        f.write("vào danh sách. Máy chỉ nhìn thấy chữ trông giống thời gian, nó KHÔNG\n")
        f.write("biết tin có quan trọng hay không.\n")
        f.write("Ví dụ tin 'BẮT ĐẦU TỪ HÔM NAY NÈ' có chữ 'hôm nay' nên lọt vào đây,\n")
        f.write("nhưng không cho biết hạn gì, không ai phải làm gì -> ĐỪNG tích.\n\n")
        f.write("NẾU GẶP TIN ĐỔI LỊCH (vd 'Workshop dời từ 20:00 sang 21:00'):\n")
        f.write("  tích tin MỚI, ĐỪNG tích tin cũ. Chỉ vậy thôi.\n\n")

        for lat in bo["ngay"]:
            # Lát cửa sổ 3 ngày (ngay=None) không cần chấm tay: đáp án của nó
            # là hợp nhất ba lát ngày, chấm lại là chấm trùng.
            if lat.get("ngay") is None:
                continue
            tin, _ = tai_tin_nhan(PACK, guild=lat["guild"], ngay=lat["ngay"])
            ung_vien = [t for t in tin if MOC.search(t.noi_dung)]
            tong += len(ung_vien)

            f.write("\n" + "=" * 78 + "\n")
            f.write(f"### {lat['guild']} · {lat['ngay']} "
                    f"· {len(ung_vien)} ứng viên / {len(tin)} tin "
                    f"· người chấm: {lat['nguoi_dan_nhan']}\n")
            f.write("=" * 78 + "\n\n")

            for t in ung_vien:
                f.write(f"[ ] {t.id}  {t.gio}   "
                        f"(máy nhìn thấy chữ: {_moc_tim_duoc(t.noi_dung) or 'không rõ'})\n")
                f.write(f"    {_gon(t.noi_dung)}\n\n")

    print(f"\nĐã tạo phiếu: {PHIEU}")
    print(f"  {tong} tin cần chấm trên {len(bo['ngay'])} ngày")
    print(f"  Chia theo người: mở file ra là thấy từng mục ### có tên\n")
    print("Mở bằng Notepad, đánh dấu x vào [ ], lưu lại, rồi chạy:")
    print("  python eval/phieu-cham.py --gom\n")
    return 0


def gom() -> int:
    if not PHIEU.exists():
        print("Chưa có phiếu. Chạy: python eval/phieu-cham.py --tao")
        return 1

    bo = json.loads(GOLDEN.read_text(encoding="utf-8"))
    theo_lat: dict[tuple[str, str], list[dict]] = {}
    lat_hien_tai = None
    dang_xet = None

    for dong in PHIEU.read_text(encoding="utf-8").splitlines():
        d = dong.strip()

        m = re.match(r"### (\S+) · (\d{4}-\d{2}-\d{2})", d)
        if m:
            lat_hien_tai = (m.group(1), m.group(2))
            theo_lat.setdefault(lat_hien_tai, [])
            continue

        m = re.match(r"\[([ xX])\]\s+(M\d+)", d)
        if m:
            dang_xet = None
            if m.group(1).lower() == "x" and lat_hien_tai:
                dang_xet = {"msg_ref": m.group(2), "loai": "DEADLINE", "vi_sao": ""}
                theo_lat[lat_hien_tai].append(dang_xet)
            continue

        if dang_xet is not None and d.lower().startswith("thay:"):
            cu = d[5:].strip()
            if cu:
                dang_xet["thay_the_cho"] = cu
            dang_xet = None

    tong = 0
    cua_so = [l for l in bo["ngay"] if l.get("ngay") is None]
    for lat in bo["ngay"]:
        if lat.get("ngay") is None:
            continue                      # gộp ở dưới, không chấm tay
        khoa = (lat["guild"], lat["ngay"])
        lat["muc_quan_trong"] = theo_lat.get(khoa, [])
        tong += len(lat["muc_quan_trong"])
        print(f"   {lat['guild']} {lat['ngay']}: {len(lat['muc_quan_trong'])} mục vàng")

    # Lát cửa sổ 3 ngày: đáp án = hợp nhất các lát ngày của cùng server, để
    # không phải dán nhãn hai lần cho cùng một tin.
    for lat in cua_so:
        gop, da_co = [], set()
        for ngay_lat in bo["ngay"]:
            if ngay_lat.get("ngay") is None or ngay_lat["guild"] != lat["guild"]:
                continue
            for m in ngay_lat["muc_quan_trong"]:
                if m["msg_ref"] not in da_co:
                    da_co.add(m["msg_ref"])
                    gop.append(m)
        lat["muc_quan_trong"] = gop
        print(f"   {lat['guild']} cửa sổ 3 ngày: {len(gop)} mục vàng (hợp nhất)")

    GOLDEN.write_text(json.dumps(bo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nĐã ghi {tong} mục vàng vào {GOLDEN.name}")

    if tong == 0:
        print("\nChưa tích dòng nào. Mở phiếu ra đánh dấu x vào [ ] đã.")
        return 1

    print("\nChạy tiếp để ra số đo cho CP3:")
    print("  python eval/eval.py\n")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Phiếu chấm golden set")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--tao", action="store_true", help="tạo phiếu để chấm")
    g.add_argument("--gom", action="store_true", help="gom kết quả vào golden-set.json")
    a = ap.parse_args()
    raise SystemExit(tao() if a.tao else gom())

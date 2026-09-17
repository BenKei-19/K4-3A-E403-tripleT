"""
Chạy Trợ Lý Kute trên một ngày tin nhắn và in kết quả ra terminal.

    python codebase/run.py
    python codebase/run.py --file <đường dẫn tới file ngày khác>

Đây là bản chạy chắc chắn nhất — dùng để quay video CP3 nếu bot Discord
chưa kịp. Có gọi AI thật, đủ điều kiện "≥1 lời gọi AI chạy thật".
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

# Console Windows mặc định là cp1252 -> in tiếng Việt là UnicodeEncodeError.
# Hai dòng này phải nằm trước mọi lệnh print.
if sys.platform == "win32":
    os.system("")                                          # bật màu ANSI
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))

from digest import ChuaCoKey, digest, tai_tin_nhan, ten_provider  # noqa: E402

GOC = Path(__file__).resolve().parent.parent
PACK = GOC / "discord-pack" / "k4_messages.csv"
MOCK = GOC / "data" / "messages-mock.json"

# Lát cắt mặc định: MỘT SERVER, MỘT NGÀY, GỘP MỌI KÊNH.
# Không lọc kênh vì học viên quan tâm "hôm nay có gì", không quan tâm tin nằm
# ở kênh nào — mà thông báo trong pack lại rải đều 12 kênh.
# K4-L3-4 · 13/09: 129 tin người, ~5k token. Cỡ vừa đẹp để quay video.
LAT_MAC_DINH = dict(guild="K4-L3-4", channel=None, ngay="2026-09-13")

XANH = "\033[96m"
VANG = "\033[93m"
XAM = "\033[90m"
DAM = "\033[1m"
HET = "\033[0m"


def main() -> int:
    parser = argparse.ArgumentParser(description="Trợ Lý Kute — bản tin trong ngày")
    parser.add_argument("--file", default=None, help="file dữ liệu (mặc định: discord-pack)")
    parser.add_argument("--guild", default=LAT_MAC_DINH["guild"])
    parser.add_argument("--channel", default=LAT_MAC_DINH["channel"])
    parser.add_argument("--ngay", default=LAT_MAC_DINH["ngay"])
    parser.add_argument("--mock", action="store_true", help="chạy trên data mock tự sinh")
    args = parser.parse_args()

    if args.mock:
        tin, ngay = tai_tin_nhan(MOCK)
        nguon = "mock tự sinh"
    else:
        duong_dan = Path(args.file) if args.file else PACK
        if not duong_dan.exists():
            print(f"{VANG}Không thấy {duong_dan}{HET}")
            print(f"{XAM}Chạy thử trên mock: python codebase/run.py --mock{HET}\n")
            return 1
        tin, ngay = tai_tin_nhan(duong_dan, guild=args.guild, channel=args.channel, ngay=args.ngay)
        nguon = args.guild + (f" · {args.channel}" if args.channel else " · mọi kênh")

    if not tin:
        print(f"{VANG}Lát cắt này không có tin nào. Thử --ngay / --channel khác.{HET}\n")
        return 1

    print(f"\n{XAM}Đọc {len(tin)} tin nhắn · {nguon} · ngày {ngay}{HET}")
    print(f"{XAM}Đang hỏi {ten_provider()}...{HET}", flush=True)

    bat_dau = time.time()
    try:
        kq = digest(tin, ngay)
    except ChuaCoKey as e:
        print(f"\n{VANG}{e}{HET}\n")
        return 1
    giay = time.time() - bat_dau

    print(f"\n{DAM}Hôm nay bạn cần lưu ý {len(kq.muc)} việc{HET}\n")

    for i, m in enumerate(kq.muc, 1):
        mau = VANG if m.loai == "DEADLINE" else XANH
        canh_bao = f"  {VANG}[cần xác nhận]{HET}" if m.do_chac < 0.7 else ""
        print(f"  {mau}{i}. {m.tom_tat}{HET}{canh_bao}")
        if m.han_chot:
            print(f"     {DAM}Hạn: {m.han_chot}{HET}")
        if m.thay_the_cho:
            print(f"     {XAM}(đính chính cho tin {m.thay_the_cho}){HET}")
        if m.tin_goc:
            print(f"     {XAM}tin gốc [{m.message_id}] {m.tin_goc.gio} · {m.tin_goc.nguoi}{HET}")
        print()

    print(f"{XAM}{'-' * 58}{HET}")
    print(f"{XAM}Đã đọc {kq.tong_tin_doc} tin · bỏ qua {kq.so_tin_bo_qua} tin trò chuyện"
          f" · {giay:.1f}s{HET}")

    if kq.bi_loai_vi_id_khong_co_that:
        print(f"{VANG}Guardrail đã chặn {len(kq.bi_loai_vi_id_khong_co_that)} mục "
              f"có id không tồn tại: {kq.bi_loai_vi_id_khong_co_that}{HET}")
    if kq.bi_loai_vi_da_bi_dinh_chinh:
        print(f"{XAM}Bỏ {len(kq.bi_loai_vi_da_bi_dinh_chinh)} tin đã bị đính chính: "
              f"{kq.bi_loai_vi_da_bi_dinh_chinh}{HET}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

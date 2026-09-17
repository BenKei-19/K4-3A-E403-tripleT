"""
Đo Trợ Lý Kute trên golden set — ra con số cho CP3.

    python eval/eval.py

In ra ba con số: bỏ sót, nhiễu, link sai.
Người phụ trách: Nguyễn Thị Minh Khánh
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Console Windows mặc định là cp1252 -> in tiếng Việt là UnicodeEncodeError.
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "codebase"))

from digest import digest, tai_tin_nhan  # noqa: E402

GOLDEN = Path(__file__).parent / "golden-set.json"


def main() -> int:
    bo = json.loads(GOLDEN.read_text(encoding="utf-8"))
    ngay_list = bo["ngay"]

    tong_vang = tong_bat_dung = tong_nhieu = tong_link_sai = 0
    dong_bang = []

    chua_dan_nhan = [f"{l['guild']} {l['ngay']} ({l.get('nguoi_dan_nhan','?')})"
                     for l in ngay_list if not l["muc_quan_trong"]]
    ngay_list = [l for l in ngay_list if l["muc_quan_trong"]]

    if chua_dan_nhan:
        print("\n!! BỎ QUA các lát CHƯA DÁN NHÃN (không có đáp án thì không chấm được):")
        for t in chua_dan_nhan:
            print(f"     {t}")
        print("   Dán nhãn xong rồi chạy lại, con số sẽ dày hơn.\n")

    if not ngay_list:
        print("Chưa lát nào có đáp án. Chạy: python eval/phieu-cham.py --tao")
        return 1

    for muc_ngay in ngay_list:
        duong_dan = muc_ngay.get("file", "discord-pack/k4_messages.csv")
        if not Path(duong_dan).is_absolute():
            duong_dan = GOC / duong_dan

        tin, ngay = tai_tin_nhan(
            duong_dan,
            guild=muc_ngay.get("guild"),
            channel=muc_ngay.get("channel"),
            ngay=muc_ngay.get("ngay"),
        )
        # ngay=None nghĩa là lát CỬA SỔ 3 NGÀY, không phải thiếu dữ liệu
        nhan = (f"{muc_ngay.get('ngay') or 'cửa sổ 3 ngày'} "
                f"{muc_ngay.get('channel', '')}").strip()
        id_co_that = {t.id for t in tin}

        vang = {m["msg_ref"] for m in muc_ngay["muc_quan_trong"]}
        # Nhãn cửa sổ phải TRÙNG với nhãn chay-test.py dùng, nếu không prompt
        # khác một chữ là mất cache và tốn thêm một lượt API cho cùng một lát.
        kq = digest(tin, muc_ngay.get("ngay") or "3 ngày gần nhất")
        tra_ve = [m.message_id for m in kq.muc]

        bat_dung = vang & set(tra_ve)
        bo_sot = vang - set(tra_ve)
        nhieu = set(tra_ve) - vang
        link_sai = [i for i in tra_ve if i not in id_co_that]

        tong_vang += len(vang)
        tong_bat_dung += len(bat_dung)
        tong_nhieu += len(nhieu)
        tong_link_sai += len(link_sai)

        dong_bang.append((nhan, len(vang), len(bat_dung), len(bo_sot), len(nhieu)))

        print(f"\n── {nhan} ──────────────────────────────")
        print(f"   vàng {len(vang)} · bắt đúng {len(bat_dung)} · bỏ sót {len(bo_sot)} · nhiễu {len(nhieu)}")
        if bo_sot:
            print(f"   BỎ SÓT: {sorted(bo_sot)}")
        if nhieu:
            print(f"   NHIỄU:  {sorted(nhieu)}")

    print("\n" + "=" * 52)
    print("  Lát cắt               vàng  đúng  sót  nhiễu")
    print("  " + "-" * 46)
    for ngay, v, d, s, n in dong_bang:
        print(f"  {str(ngay)[:20]:<20}  {v:>4}  {d:>4}  {s:>3}  {n:>5}")
    print("  " + "-" * 46)
    print(f"  {'TỔNG':<20}  {tong_vang:>4}  {tong_bat_dung:>4}"
          f"  {tong_vang - tong_bat_dung:>3}  {tong_nhieu:>5}")
    print("=" * 52)

    print(f"\nCÂU SỐ ĐO CHO CP3 — chép nguyên vào form:\n")
    print(f"  Chạy trên {len(ngay_list)} ngày dữ liệu. {tong_vang} mục quan trọng đã dán")
    print(f"  nhãn tay: bot bắt đúng {tong_bat_dung}, bỏ sót {tong_vang - tong_bat_dung}.")
    print(f"  Trong {tong_bat_dung + tong_nhieu} mục bot trả về có {tong_nhieu} mục không đáng đưa vào.")
    if tong_link_sai:
        print(f"  {tong_link_sai} link trỏ tới tin không tồn tại.")
    else:
        print(f"  Mọi link đều trỏ đúng tin có thật (guardrail chặn được hết).")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

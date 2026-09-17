"""
Chạy bộ test case CP3 và in bảng kết quả.

    python eval/chay-test.py

Mỗi lát dữ liệu chỉ gọi AI MỘT lần rồi dùng lại cho mọi test case trên lát đó,
nên cả bộ chỉ tốn vài lời gọi.

Kết quả ghi ra eval/ket-qua-luot-1.md — giữ nguyên để đối chiếu khi chạy lại,
đúng yêu cầu của BTC ("giữ nguyên kết quả lượt đầu").
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "codebase"))

from digest import digest, tai_tin_nhan  # noqa: E402

PACK = GOC / "discord-pack" / "k4_messages.csv"
BO = Path(__file__).parent / "test-cases.json"
RA = Path(__file__).parent / "ket-qua-luot-1.md"

# Mốc thời gian trong tóm tắt — dùng cho điều kiện "moi_muc_co_moc"
MOC = re.compile(r"\d{1,2}:\d{2}|\d{1,2}h\d{0,2}\b|\d{1,2}/\d{1,2}"
                 r"|hôm nay|tối nay|ngày mai|sáng mai", re.IGNORECASE)


def chay_mot_lat(guild: str, ngay: str):
    tin, _ = tai_tin_nhan(PACK, guild=guild, ngay=ngay)
    kq = digest(tin, ngay)
    return kq, {t.id for t in tin}, len(tin)


def kiem(dk: dict, kq, id_dau_vao: set[str]) -> tuple[bool, str]:
    ra = [m.message_id for m in kq.muc]
    kieu = dk["kieu"]

    if kieu == "phai_co":
        ok = dk["msg"] in ra
        return ok, "có trong bản tin" if ok else f"KHÔNG có {dk['msg']} trong bản tin"

    if kieu == "phai_vang":
        ok = dk["msg"] not in ra
        return ok, "không bị đưa vào" if ok else f"{dk['msg']} BỊ đưa vào bản tin"

    if kieu == "id_co_that":
        bia = [i for i in ra if i not in id_dau_vao]
        bia += kq.bi_loai_vi_id_khong_co_that
        return (not bia), "mọi mã tin đều có thật" if not bia else f"BỊA mã: {bia}"

    if kieu == "nhieu_nhat_mot_trong":
        co = [i for i in dk["msg"] if i in ra]
        ok = len(co) <= 1
        return ok, f"chỉ nêu {co or 'không nêu cái nào'}" if ok else f"nêu CẢ HAI: {co}"

    if kieu == "khong_trung_msg":
        ok = len(ra) == len(set(ra))
        trung = [i for i in set(ra) if ra.count(i) > 1]
        return ok, "không mục nào lặp" if ok else f"mục lặp: {trung}"

    if kieu == "toi_da":
        ok = len(kq.muc) <= dk["so"]
        return ok, f"{len(kq.muc)} mục (tối đa {dk['so']})"

    if kieu == "moi_muc_co_moc":
        thieu = [m.message_id for m in kq.muc
                 if not (m.han_chot.strip() or MOC.search(m.tom_tat))]
        return (not thieu), "mục nào cũng có mốc" if not thieu else f"thiếu mốc: {thieu}"

    return False, f"chưa hỗ trợ kiểu '{kieu}'"


def main() -> int:
    if not PACK.exists():
        print(f"Không thấy {PACK}")
        return 1

    bo = json.loads(BO.read_text(encoding="utf-8"))
    tcs = bo["test_case"]

    lat_can = {(t["dau_vao"]["guild"], t["dau_vao"]["ngay"]) for t in tcs}
    print(f"\nChạy {len(tcs)} test case trên {len(lat_can)} lát dữ liệu")
    print(f"({len(lat_can)} lời gọi AI, dùng lại cho mọi test case cùng lát)\n")

    cache = {}
    for g, n in sorted(lat_can):
        print(f"  đang chạy {g} · {n} ...", flush=True)
        cache[(g, n)] = chay_mot_lat(g, n)

    ket = []
    for t in tcs:
        k = (t["dau_vao"]["guild"], t["dau_vao"]["ngay"])
        kq, ids, so_tin = cache[k]
        ok, ly_do = kiem(t["dieu_kien_dat"], kq, ids)
        ket.append((t, ok, ly_do, so_tin))

    dat = sum(1 for _, ok, _, _ in ket if ok)
    tong = len(ket)

    print("\n" + "=" * 76)
    print(f"  {'Mã':<6}{'Loại':<30}{'Kết quả':<10}Ghi chú")
    print("  " + "-" * 72)
    for t, ok, ly_do, _ in ket:
        print(f"  {t['ma']:<6}{t['loai'][:28]:<30}{'ĐẠT' if ok else 'KHÔNG ĐẠT':<10}{ly_do[:34]}")
    print("  " + "-" * 72)
    print(f"  Đã chạy {tong} test case · ĐẠT {dat} · KHÔNG ĐẠT {tong - dat}"
          f" · tỉ lệ {dat * 100 // tong}%")
    print("=" * 76)

    with RA.open("w", encoding="utf-8") as f:
        f.write("# Kết quả lượt đo đầu — CP3\n\n")
        f.write("Giữ nguyên để đối chiếu khi chạy lại. Không sửa file này.\n\n")
        f.write(f"**Đã chạy {tong} test case · ĐẠT {dat} · KHÔNG ĐẠT {tong - dat} "
                f"· tỉ lệ đạt lượt đầu {dat * 100 // tong}%**\n\n")
        f.write(f"Định nghĩa \"quan trọng\": {bo['_dinh_nghia_quan_trong']}\n\n")
        f.write(f"Phần còn là mock: {bo['_phan_con_la_mock']}\n\n")
        f.write("| Mã | Loại | Đầu vào | Hành vi mong đợi | Kết quả | Ghi chú |\n")
        f.write("|---|---|---|---|---|---|\n")
        for t, ok, ly_do, so_tin in ket:
            dv = f"{t['dau_vao']['guild']} · {t['dau_vao']['ngay']} ({so_tin} tin)"
            f.write(f"| {t['ma']} | {t['loai']} | {dv} | {t['hanh_vi_mong_doi']} "
                    f"| {'ĐẠT' if ok else '**KHÔNG ĐẠT**'} | {ly_do} |\n")

    print(f"\nĐã ghi bảng kết quả: {RA}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

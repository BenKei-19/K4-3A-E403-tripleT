"""
Đổ tin nhắn một ngày từ discord-pack vào kênh test qua webhook.

    python codebase/do-tin-vao-kenh.py                      # thử trước, không đăng
    python codebase/do-tin-vao-kenh.py --that               # đăng thật
    python codebase/do-tin-vao-kenh.py --that --so-tin 40   # chỉ đăng 40 tin

Cần DISCORD_WEBHOOK_URL trong .env.

Dùng để dựng lại một ngày trong kênh lớp vào SERVER TEST CỦA NHÓM, rồi bot đọc
lịch sử kênh đó. Data đã được BTC ẩn danh sẵn; server test phải để riêng tư,
chỉ thành viên nhóm.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "codebase"))

from digest import tai_tin_nhan  # noqa: E402  (đã load .env sẵn)

PACK = GOC / "discord-pack" / "k4_messages.csv"

# Webhook cho đăng tối đa 5 tin mỗi 2 giây. Chờ 0.5s cho chắc.
NGHI = 0.5


def dang(url: str, ten: str, noi_dung: str) -> tuple[bool, str]:
    """Đăng một tin qua webhook. Trả về (thành công, ghi chú)."""
    import json

    du_lieu = json.dumps({
        "username": ten,
        "content": noi_dung[:1900] or "(tin rỗng)",
        # Chặn bot ping @everyone thật khi nội dung có chữ đó
        "allowed_mentions": {"parse": []},
    }).encode("utf-8")

    yeu_cau = urllib.request.Request(
        url, data=du_lieu,
        headers={"Content-Type": "application/json", "User-Agent": "tripleT-seeder/1.0"},
    )
    try:
        with urllib.request.urlopen(yeu_cau, timeout=20) as ph:
            return ph.status < 300, str(ph.status)
    except urllib.error.HTTPError as e:
        than = e.read().decode("utf-8", "replace")[:160]
        if e.code == 429:                       # bị giới hạn tốc độ, chờ rồi thử lại
            time.sleep(3)
            try:
                with urllib.request.urlopen(yeu_cau, timeout=20) as ph:
                    return ph.status < 300, f"{ph.status} (sau khi chờ)"
            except Exception as e2:
                return False, f"429 rồi lỗi tiếp: {e2}"
        return False, f"HTTP {e.code}: {than}"
    except Exception as e:
        return False, str(e)[:160]


def main() -> int:
    ap = argparse.ArgumentParser(description="Đổ tin nhắn vào kênh test qua webhook")
    ap.add_argument("--guild", default="K4-L3-4")
    ap.add_argument("--ngay", default="2026-09-13",
                    help="một ngày 'YYYY-MM-DD', hoặc 'tat-ca' để đổ cả cửa sổ 3 ngày")
    ap.add_argument("--so-tin", type=int, default=0, help="giới hạn số tin, 0 = tất cả")
    ap.add_argument("--that", action="store_true", help="đăng thật (mặc định chỉ thử)")
    a = ap.parse_args()

    url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not url.startswith("https://discord.com/api/webhooks/"):
        print("Chưa có DISCORD_WEBHOOK_URL hợp lệ trong .env")
        return 1
    if not PACK.exists():
        print(f"Không thấy {PACK}")
        return 1

    # 'tat-ca' = đổ cả cửa sổ 3 ngày, để demo được đúng phạm vi thật của bot
    ngay_loc = None if a.ngay.lower() in ("tat-ca", "all", "") else a.ngay
    tin, _ = tai_tin_nhan(PACK, guild=a.guild, ngay=ngay_loc)
    tin.sort(key=lambda t: (t.ngay, t.gio))      # đăng theo đúng thứ tự thời gian
    if a.so_tin:
        tin = tin[: a.so_tin]

    print(f"\n{a.guild} · ngày {ngay_loc or 'cả 3 ngày'} · {len(tin)} tin sẽ được đăng")
    print(f"Ước tính {len(tin) * NGHI / 60:.1f} phút\n")

    if not a.that:
        print("CHẾ ĐỘ THỬ — chưa đăng gì. Xem 5 tin đầu:\n")
        for t in tin[:5]:
            print(f"  {t.ngay} {t.gio} · {t.nguoi}: {' '.join(t.noi_dung.split())[:80]}")
        print(f"\nĐăng thật:  python codebase/do-tin-vao-kenh.py --that\n")
        return 0

    ok = loi = 0
    for i, t in enumerate(tin, 1):
        # Đặt tên hiển thị kèm NGÀY + GIỜ gốc, để kênh test giống kênh thật.
        # Phải có ngày: cửa sổ của bot là 3 ngày, mà tin đăng lại đều mang dấu
        # thời gian của hôm nay -> thiếu ngày là bot mất khả năng phân biệt.
        nhan = f"{t.nguoi} · {t.ngay} {t.gio}" if t.ngay else f"{t.nguoi} · {t.gio}"
        thanh_cong, ghi_chu = dang(url, nhan[:80], t.noi_dung)
        if thanh_cong:
            ok += 1
        else:
            loi += 1
            print(f"  lỗi ở tin {t.id}: {ghi_chu}")
        if i % 20 == 0 or i == len(tin):
            print(f"  ...{i}/{len(tin)}", flush=True)
        time.sleep(NGHI)

    print(f"\nXong: {ok} tin đã đăng, {loi} lỗi.")
    print("Mở kênh test xem lại, rồi chạy bot:  python codebase/bot.py\n")
    return 0 if loi == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

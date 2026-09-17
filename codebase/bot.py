"""
Cửa Discord của Trợ Lý Kute.

Bot nghe mention trong kênh -> gọi digest() -> trả embed.

    pip install -r requirements.txt
    # .env: DISCORD_BOT_TOKEN=...  và  ANTHROPIC_API_KEY=...
    python codebase/bot.py

Chuẩn bị trước khi chạy:
  1. Developer Portal -> New Application -> Bot -> bật MESSAGE CONTENT INTENT
  2. OAuth2 URL Generator: scope "bot", quyền Read Messages + Send Messages
     + Read Message History -> mời vào SERVER TEST CỦA NHÓM
  3. Dán tin nhắn một ngày từ discord-pack vào một kênh trong server test đó

Bot chỉ là lớp vỏ mỏng — mọi logic nằm trong digest.py, đừng viết lại ở đây.
Người phụ trách: Nguyễn Quang Huy
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Console Windows mac dinh cp1252 -> print tieng Viet la crash.
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import discord
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

from digest import TinNhan, digest  # noqa: E402

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

XANH_LA = 0x4FA88A
CAM = 0xE0924E

intents = discord.Intents.default()
intents.message_content = True          # bắt buộc, phải bật cả ở Developer Portal
client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f"Trợ Lý Kute đã online: {client.user}")


@client.event
async def on_message(tin_nhan: discord.Message):
    # CHAN DOAN — in ra moi tin bot nhan duoc, de biet ket noi co thong khong
    print(f"[nhan] {tin_nhan.author} | bot={tin_nhan.author.bot} | "
          f"noi_dung={tin_nhan.content[:60]!r} | "
          f"mentions={[str(u) for u in tin_nhan.mentions]}", flush=True)

    if tin_nhan.author.bot:
        print("       -> bo qua: tin cua bot", flush=True)
        return
    # Discord tao san mot ROLE trung ten bot khi moi bot vao server, nen nguoi
    # dung rat hay tag nham role (<@&id>) thay vi tai khoan bot (<@id>).
    # Chap nhan ca hai cho chac.
    vai_cua_bot = tin_nhan.guild.self_role if tin_nhan.guild else None
    duoc_goi = (client.user in tin_nhan.mentions) or (
        vai_cua_bot is not None and vai_cua_bot in tin_nhan.role_mentions
    )
    if not duoc_goi:
        print("       -> bo qua: khong tag bot", flush=True)
        return
    print("       -> DANG XU LY", flush=True)

    async with tin_nhan.channel.typing():
        # Đọc tin nhắn trong kênh này
        tin: list[TinNhan] = []
        async for m in tin_nhan.channel.history(limit=300, oldest_first=True):
            # CHỈ bỏ qua tin của chính bot. KHÔNG dùng m.author.bot vì tin đổ vào
            # kênh test qua webhook cũng bị Discord đánh dấu là bot -> bỏ hết thì
            # bot không còn gì để đọc.
            if m.author.id == client.user.id or m.id == tin_nhan.id:
                continue

            # Script đổ tin đặt tên hiển thị dạng "D3115 · 00:08" để giữ giờ gốc,
            # vì tin đăng lại mang dấu thời gian của hôm nay.
            ten, gio = m.author.display_name, m.created_at.strftime("%H:%M")
            if " · " in ten:
                ten, _, gio_goc = ten.rpartition(" · ")
                if re.fullmatch(r"\d{1,2}:\d{2}", gio_goc.strip()):
                    gio = gio_goc.strip()

            tin.append(
                TinNhan(
                    id=str(m.id),
                    gio=gio,
                    nguoi=ten,
                    vai="hv",
                    noi_dung=m.content,
                )
            )

        if not tin:
            await tin_nhan.reply("Kênh này chưa có tin nào để mình đọc.")
            return

        ngay = tin_nhan.created_at.strftime("%d/%m/%Y")
        kq = digest(tin, ngay)

    if not kq.muc:
        await tin_nhan.reply(
            embed=discord.Embed(
                title="Hôm nay chưa có gì cần lưu ý",
                description=(
                    f"Mình đã đọc {kq.tong_tin_doc} tin trong kênh, không có thông báo "
                    "hay deadline nào. Mình chỉ trả lời từ tin có thật — không có thì nói không có."
                ),
                colour=XANH_LA,
            )
        )
        return

    embed = discord.Embed(
        title=f"Hôm nay bạn cần lưu ý {len(kq.muc)} việc",
        colour=CAM if any(m.loai == "DEADLINE" for m in kq.muc) else XANH_LA,
    )

    for m in kq.muc:
        ten = m.tom_tat
        if m.do_chac < 0.7:
            ten += "  ·  cần xác nhận"

        chi_tiet = []
        if m.han_chot:
            chi_tiet.append(f"**Hạn: {m.han_chot}**")
        if m.thay_the_cho:
            chi_tiet.append("_đã được đính chính lại trong ngày_")
        if m.tin_goc:
            link = f"https://discord.com/channels/{tin_nhan.guild.id}/{tin_nhan.channel.id}/{m.message_id}"
            chi_tiet.append(f"[Xem tin gốc →]({link}) · {m.tin_goc.gio} · {m.tin_goc.nguoi}")

        embed.add_field(name=ten, value="\n".join(chi_tiet) or "​", inline=False)

    embed.set_footer(
        text=f"Đã đọc {kq.tong_tin_doc} tin · bỏ qua {kq.so_tin_bo_qua} tin trò chuyện"
    )
    await tin_nhan.reply(embed=embed)


if __name__ == "__main__":
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit("Chưa có DISCORD_BOT_TOKEN — tạo file .env từ .env.example")
    client.run(token)

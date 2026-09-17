"""
Cửa Discord của Trợ Lý Kute.

Học viên tag bot -> bot quét MỌI KÊNH người đó có quyền đọc, trong 3 NGÀY gần
nhất -> NHẮN RIÊNG cho người đó toàn bộ mốc thời gian tìm được.

    pip install -r requirements.txt
    # .env: DISCORD_BOT_TOKEN=...  và  GEMINI_API_KEY=...
    python codebase/bot.py

Chuẩn bị trước khi chạy:
  1. Developer Portal -> New Application -> Bot -> bật MESSAGE CONTENT INTENT
  2. OAuth2 URL Generator: scope "bot", quyền Read Messages + Send Messages
     + Read Message History -> mời vào SERVER TEST CỦA NHÓM
  3. Đổ tin từ discord-pack vào kênh test: python codebase/do-tin-vao-kenh.py --that

Bot chỉ là lớp vỏ mỏng — mọi logic phân loại nằm trong digest.py.
Người phụ trách: Nguyễn Quang Huy
"""

from __future__ import annotations

import os
import re
import sys
from datetime import timedelta
from pathlib import Path

# Console Windows mac dinh cp1252 -> print tieng Viet la crash.
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

from digest import NGUONG_CAN_XAC_NHAN, TinNhan, digest  # noqa: E402

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

XANH_LA = 0x4FA88A
CAM = 0xE0924E

SO_NGAY = int(os.environ.get("SO_NGAY_QUET", "3"))   # phạm vi: 3 ngày gần nhất
TOI_DA_KENH = 25                                     # chặn quét lan man
TOI_DA_TIN_MOI_KENH = 300
MUC_MOI_TIN = 10                                     # Discord cho tối đa 25 field/embed

intents = discord.Intents.default()
intents.message_content = True          # bắt buộc, phải bật cả ở Developer Portal
client = commands.Bot(command_prefix="!khong-dung", intents=intents)


@client.event
async def on_ready():
    print(f"Trợ Lý Kute đã online: {client.user}", flush=True)
    print(f"Phạm vi quét: {SO_NGAY} ngày gần nhất, mọi kênh người hỏi đọc được", flush=True)
    # Đăng ký lệnh gạch chéo theo từng server -> có hiệu lực ngay, không phải
    # chờ Discord phát tán toàn cục (mất tới 1 tiếng).
    for g in client.guilds:
        try:
            client.tree.copy_global_to(guild=g)
            await client.tree.sync(guild=g)
            print(f"      da dang ky /luuy trong server {g.name}", flush=True)
        except Exception as e:
            print(f"      khong dang ky duoc /luuy: {e}", flush=True)


def _ten_ngay_gio(m: discord.Message) -> tuple[str, str, str]:
    """Trả về (tên, ngày 'YYYY-MM-DD', giờ 'HH:MM').

    Cửa sổ là 3 NGÀY nên phải giữ được ngày gốc, không chỉ giờ: thiếu ngày thì
    model không biết "hôm nay / sáng mai" trong tin là ngày nào.

    Script đổ tin đặt tên hiển thị dạng 'D3115 · 2026-09-13 00:08' để giữ dấu
    thời gian gốc, vì tin đăng lại mang thời gian của hôm nay. Bản cũ chỉ có
    giờ ('D3115 · 00:08') nên vẫn đọc được, khi đó lấy ngày của tin đăng lại.
    """
    ten = m.author.display_name
    ngay, gio = m.created_at.strftime("%Y-%m-%d"), m.created_at.strftime("%H:%M")
    if " · " in ten:
        ten_cat, _, dau = ten.rpartition(" · ")
        dau = dau.strip()
        khop = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})", dau)
        if khop:
            return ten_cat, khop.group(1), khop.group(2)
        if re.fullmatch(r"\d{1,2}:\d{2}", dau):
            return ten_cat, ngay, dau
    return ten, ngay, gio


async def _quet_kenh_cua_nguoi(nguoi: discord.Member, bo_qua_id: int):
    """Đọc mọi kênh NGƯỜI ĐÓ có quyền xem, trong SO_NGAY ngày gần nhất.

    Đây là phần cá nhân hoá: hai người ở hai đội khác nhau sẽ quét ra hai tập
    kênh khác nhau, nên nhận hai câu trả lời khác nhau.
    """
    tu_luc = discord.utils.utcnow() - timedelta(days=SO_NGAY)
    tin: list[TinNhan] = []
    nguon: dict[str, discord.TextChannel] = {}
    da_quet: list[str] = []

    for kenh in nguoi.guild.text_channels[:TOI_DA_KENH]:
        quyen_nguoi = kenh.permissions_for(nguoi)
        quyen_bot = kenh.permissions_for(nguoi.guild.me)
        # Không đọc kênh mà NGƯỜI HỎI không được xem — tránh rò rỉ giữa các đội
        if not (quyen_nguoi.read_messages and quyen_nguoi.read_message_history):
            continue
        if not (quyen_bot.read_messages and quyen_bot.read_message_history):
            continue

        dem = 0
        try:
            async for m in kenh.history(limit=TOI_DA_TIN_MOI_KENH, after=tu_luc,
                                        oldest_first=True):
                if m.author.id == client.user.id or m.id == bo_qua_id:
                    continue
                ten, ngay, gio = _ten_ngay_gio(m)
                tin.append(TinNhan(id=str(m.id), gio=gio, nguoi=ten,
                                   vai="hv", noi_dung=m.content, ngay=ngay))
                nguon[str(m.id)] = kenh
                dem += 1
        except discord.Forbidden:
            continue

        if dem:
            da_quet.append(f"#{kenh.name} ({dem})")

    return tin, nguon, da_quet


def _dung_embed(kq, nguon, da_quet, guild) -> list[discord.Embed]:
    """Chia thành nhiều embed vì Discord chỉ cho 25 field mỗi embed,
    mà thiết kế của nhóm là KHÔNG giới hạn số mục."""
    khoi = [kq.muc[i:i + MUC_MOI_TIN] for i in range(0, len(kq.muc), MUC_MOI_TIN)]
    ra = []
    for i, phan in enumerate(khoi):
        e = discord.Embed(
            title=(f"Bạn cần lưu ý {len(kq.muc)} việc trong {SO_NGAY} ngày qua"
                   if i == 0 else f"(tiếp) {i * MUC_MOI_TIN + 1}–{i * MUC_MOI_TIN + len(phan)}"),
            colour=CAM if any(m.loai == "DEADLINE" for m in kq.muc) else XANH_LA,
        )
        for m in phan:
            ten = m.tom_tat
            if m.do_chac <= NGUONG_CAN_XAC_NHAN:
                ten += "  ·  cần xác nhận"

            chi_tiet = []
            if m.han_chot:
                chi_tiet.append(f"**Hạn: {m.han_chot}**")
            if m.thay_the_cho:
                chi_tiet.append("_đã được đính chính lại_")
            kenh = nguon.get(m.message_id)
            if kenh is not None:
                link = f"https://discord.com/channels/{guild.id}/{kenh.id}/{m.message_id}"
                # Cửa sổ 3 ngày nên phải ghi cả ngày, không chỉ giờ: người đọc
                # cần biết tin này của hôm nào mới tự kiểm chứng được.
                khi = ""
                if m.tin_goc:
                    nn = m.tin_goc.ngay
                    khi = f"{nn[8:10]}/{nn[5:7]} {m.tin_goc.gio}" if len(nn) == 10 else m.tin_goc.gio
                chi_tiet.append(f"[Xem tin gốc →]({link}) · #{kenh.name} · {khi}")

            e.add_field(name=ten[:250], value="\n".join(chi_tiet) or "​", inline=False)

        if i == len(khoi) - 1:
            e.set_footer(text=f"Đã đọc {kq.tong_tin_doc} tin · "
                              f"{len(da_quet)} kênh: {', '.join(da_quet)[:180]}")
        ra.append(e)
    return ra


# ------------------------------------------- đường ③: câu hỏi ngoài phạm vi

# Bot này CHỈ làm một việc: liệt kê mốc thời gian trong cửa sổ của người hỏi.
# Tag bot kèm câu hỏi khác (hỏi quy định, hỏi kỹ thuật, nhờ giải bài) mà vẫn đổ
# ra danh sách mốc là trả lời lạc đề — §6 đường ③. Cổng lọc này là CODE, không
# phải AI: rẻ, đoán trước được, và không tốn thêm một lời gọi.
Y_DINH = re.compile(
    r"lưu ý|cần nắm|cần biết|quan trọng|bỏ lỡ|bỏ sót|bỏ qua|trôi"
    r"|deadline|hạn|dealine|mốc|lịch|sắp tới|hôm nay|mấy ngày|vắng"
    r"|thông báo|nhắc|gì mới|update|tổng hợp|catch ?up",
    re.IGNORECASE)


def _hoi_dung_viec(noi_dung: str) -> bool:
    """Tag trống (chỉ mention) = hỏi đúng việc. Có chữ thì phải khớp ý định."""
    con_lai = re.sub(r"<@[!&]?\d+>", " ", noi_dung).strip()
    return (not con_lai) or bool(Y_DINH.search(con_lai))


def _embed_ngoai_pham_vi() -> discord.Embed:
    e = discord.Embed(
        title="Mình chưa chắc bạn đang hỏi gì",
        description=(
            "Mình chỉ làm được đúng một việc: liệt kê **những mốc thời gian bạn cần "
            f"lưu ý trong {SO_NGAY} ngày gần nhất**, trong các kênh bạn đọc được.\n\n"
            "Nếu bạn muốn xem danh sách đó, gõ `/luuy` hoặc tag mình kèm câu "
            "*\"những thông tin quan trọng tôi cần nắm là gì\"*.\n\n"
            "Còn câu hỏi về quy định, điểm, hay lỗi kỹ thuật thì mình chưa trả lời "
            "được — cái đó bạn hỏi TA/Coach sẽ chắc hơn, mình không đoán bừa."),
        colour=CAM)
    return e


# ------------------------------------------- đường correction: người dùng sửa

NHAT_KY_PHAN_HOI = Path(__file__).resolve().parent.parent / "eval" / "phan-hoi.log"


class NutBaoSai(discord.ui.View):
    """Nút 'Có mục sai' dưới câu trả lời — §6 đường correction.

    Không tự sửa được câu trả lời, nhưng ghi lại để nhóm chấm lại và để có
    đường đi cho người dùng thay vì phải im lặng chịu.
    """

    def __init__(self, ma_tin: list[str]):
        super().__init__(timeout=900)
        self.ma_tin = ma_tin

    @discord.ui.button(label="Có mục sai", style=discord.ButtonStyle.secondary, emoji="🚩")
    async def bao_sai(self, tuong_tac: discord.Interaction, nut: discord.ui.Button):
        nut.disabled = True
        dong = (f"{discord.utils.utcnow():%Y-%m-%d %H:%M}\t{tuong_tac.user}\t"
                f"{','.join(self.ma_tin)}\n")
        try:
            NHAT_KY_PHAN_HOI.parent.mkdir(parents=True, exist_ok=True)
            with NHAT_KY_PHAN_HOI.open("a", encoding="utf-8") as f:
                f.write(dong)
        except OSError as e:
            print(f"      khong ghi duoc phan hoi: {e}", flush=True)
        await tuong_tac.response.send_message(
            "Cảm ơn bạn. Mình đã ghi lại để nhóm chấm lại mục này.\n"
            "Trong lúc chờ, bạn bấm \"Xem tin gốc →\" để đọc thẳng tin gốc nhé — "
            "tin gốc luôn đúng hơn phần tóm tắt của mình.",
            ephemeral=True)
        print(f"      [phan hoi] {tuong_tac.user} bao sai: {self.ma_tin}", flush=True)


@client.event
async def on_message(tin_nhan: discord.Message):
    if tin_nhan.author.bot or tin_nhan.guild is None:
        return

    # Discord tạo sẵn một ROLE trùng tên bot khi mời bot vào server, nên người
    # dùng rất hay tag nhầm role (<@&id>) thay vì tài khoản bot (<@id>).
    vai_cua_bot = tin_nhan.guild.self_role
    duoc_goi = (client.user in tin_nhan.mentions) or (
        vai_cua_bot is not None and vai_cua_bot in tin_nhan.role_mentions
    )
    if not duoc_goi:
        return

    nguoi = tin_nhan.author
    print(f"[hoi] {nguoi} trong #{tin_nhan.channel}", flush=True)

    # Đường ③: tag bot nhưng hỏi chuyện khác -> nói thẳng phạm vi, KHÔNG đổ
    # danh sách mốc ra cho có. Trả lời sai việc còn tệ hơn không trả lời.
    if not _hoi_dung_viec(tin_nhan.content):
        print("      -> ngoai pham vi, khong tra danh sach", flush=True)
        await _gui_rieng(tin_nhan, nguoi, [_embed_ngoai_pham_vi()])
        return

    async with tin_nhan.channel.typing():
        tin, nguon, da_quet = await _quet_kenh_cua_nguoi(nguoi, tin_nhan.id)
        print(f"      quet {len(da_quet)} kenh, {len(tin)} tin", flush=True)

        if not tin:
            await _gui_rieng(tin_nhan, nguoi, [discord.Embed(
                title=f"Không có gì trong {SO_NGAY} ngày qua",
                description=("Mình không thấy tin nào trong các kênh bạn đọc được "
                             f"ở {SO_NGAY} ngày gần nhất."),
                colour=XANH_LA)])
            return

        kq = digest(tin, f"{SO_NGAY} ngày gần nhất")

    if not kq.muc:
        e = discord.Embed(
            title=f"Không có mốc nào trong {SO_NGAY} ngày qua",
            description=(f"Mình đã đọc {kq.tong_tin_doc} tin trong {len(da_quet)} kênh "
                         "bạn có quyền xem, không có hạn nộp hay lịch nào.\n"
                         "Mình chỉ trả lời từ tin có thật — không có thì nói không có."),
            colour=XANH_LA)
        e.set_footer(text=", ".join(da_quet)[:180])
        await _gui_rieng(tin_nhan, nguoi, [e])
        return

    await _gui_rieng(tin_nhan, nguoi,
                     _dung_embed(kq, nguon, da_quet, tin_nhan.guild),
                     view=NutBaoSai([m.message_id for m in kq.muc]))


async def _gui_rieng(tin_nhan: discord.Message, nguoi, embeds: list[discord.Embed],
                     view: discord.ui.View | None = None):
    """Nhắn riêng cho người hỏi. Bị chặn tin nhắn riêng thì nói thẳng trong kênh
    thay vì im lặng để người dùng tưởng bot hỏng."""
    try:
        for i, e in enumerate(embeds):
            cuoi = i == len(embeds) - 1
            if cuoi and view is not None:
                await nguoi.send(embed=e, view=view)
            else:
                await nguoi.send(embed=e)
        await tin_nhan.reply("Mình đã nhắn riêng cho bạn rồi nhé.",
                             mention_author=False, delete_after=30)
        print("      -> da nhan rieng", flush=True)
    except discord.Forbidden:
        await tin_nhan.reply(
            f"{nguoi.mention} mình không nhắn riêng cho bạn được — bạn đang chặn "
            "tin nhắn từ thành viên server. Bật lại trong Cài đặt quyền riêng tư "
            "của server rồi tag mình lần nữa nhé.",
            mention_author=False)
        print("      -> BI CHAN DM", flush=True)


# ------------------------------------------------------------------ lệnh /luuy

@client.tree.command(name="luuy",
                     description="Xem mọi mốc thời gian trong các kênh của bạn, 3 ngày gần nhất")
async def luuy(tuong_tac: discord.Interaction):
    """Trả lời ephemeral: hiện ngay trong kênh nhưng CHỈ người gõ lệnh thấy được."""
    if tuong_tac.guild is None:
        await tuong_tac.response.send_message("Lệnh này chỉ dùng trong server.", ephemeral=True)
        return

    # Phải báo Discord biết là đang xử lý, nếu không lệnh sẽ hết hạn sau 3 giây
    await tuong_tac.response.defer(ephemeral=True, thinking=True)
    nguoi = tuong_tac.user
    print(f"[/luuy] {nguoi} trong #{tuong_tac.channel}", flush=True)

    tin, nguon, da_quet = await _quet_kenh_cua_nguoi(nguoi, 0)
    print(f"        quet {len(da_quet)} kenh, {len(tin)} tin", flush=True)

    if not tin:
        await tuong_tac.followup.send(
            f"Mình không thấy tin nào trong các kênh bạn đọc được ở {SO_NGAY} ngày qua.",
            ephemeral=True)
        return

    kq = digest(tin, f"{SO_NGAY} ngày gần nhất")

    if not kq.muc:
        e = discord.Embed(
            title=f"Không có mốc nào trong {SO_NGAY} ngày qua",
            description=(f"Mình đã đọc {kq.tong_tin_doc} tin trong {len(da_quet)} kênh "
                         "bạn có quyền xem, không có hạn nộp hay lịch nào.\n"
                         "Mình chỉ trả lời từ tin có thật — không có thì nói không có."),
            colour=XANH_LA)
        await tuong_tac.followup.send(embed=e, ephemeral=True)
        return

    embeds = _dung_embed(kq, nguon, da_quet, tuong_tac.guild)
    for i, e in enumerate(embeds):
        if i == len(embeds) - 1:      # nút báo sai gắn ở tin cuối — §6 correction
            await tuong_tac.followup.send(
                embed=e, ephemeral=True,
                view=NutBaoSai([m.message_id for m in kq.muc]))
        else:
            await tuong_tac.followup.send(embed=e, ephemeral=True)
    print("        -> da tra ephemeral", flush=True)


if __name__ == "__main__":
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit("Chưa có DISCORD_BOT_TOKEN — tạo file .env từ .env.example")
    client.run(token)

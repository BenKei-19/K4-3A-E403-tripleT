# Trợ Lý Kute — hướng dẫn cho cả nhóm

Một file duy nhất: dự án là gì · cài thế nào · chạy thế nào · bị hỏi thì trả lời sao.

| Cần gì | Nhảy tới |
|---|---|
| **Mới nhận bàn giao — đọc cái này trước** | [Phần 0](#phần-0--bàn-giao) |
| Hiểu dự án làm gì | [Phần 1](#phần-1--dự-án-này-là-gì) |
| Cài máy từ đầu | [Phần 2](#phần-2--cài-đặt-từ-máy-trắng) |
| Chạy thử ngay | [Phần 3](#phần-3--cách-chạy) |
| Dựng Discord để chạy thật | [Phần 4](#phần-4--dựng-discord-để-chạy-thật) |
| File nào làm gì | [Phần 5](#phần-5--file-nào-làm-gì) |
| Sửa cái gì thì sửa ở đâu | [Phần 6](#phần-6--muốn-sửa-thì-sửa-ở-đâu) |
| Chạy bị lỗi | [Phần 7](#phần-7--lỗi-hay-gặp) |
| Chuẩn bị thuyết trình | [Phần 8](#phần-8--thuyết-trình-ai-nói-gì) |
| Bị giám khảo hỏi | [Phần 9](#phần-9--câu-hỏi-có-thể-bị-hỏi) |

---

# Phần 0 · Bàn giao

*Cập nhật sáng 18/09. Làm xong việc nào thì xoá dòng đó khỏi bảng.*

**Mốc giờ hôm nay 18/09:** nộp CP5 trước **13:00** · thuyết trình **17:30**

## Đã xong

- Code chạy thật: bot Discord (`codebase/bot.py`) + phần đọc và lọc tin (`codebase/digest.py`)
- `spec.md` đủ 9 phần, số liệu đều đếm từ tin nhắn thật
- Đo 2 lần. Lần 2 đúng **20/20** câu thử — có 2 câu đã sửa đề chấm, giữ đề cũ thì là 18/20
- Slide 6 trang: `demo-slides.pdf`
- Đã bỏ lệnh `/luuy`. Giờ chỉ có **một cách dùng là tag bot**
- Repo đã push, file bí mật và dữ liệu thật đều đã bị chặn không lên GitHub được

## Còn phải làm — theo thứ tự

| # | Việc | Hạn | Mất bao lâu | Xem ở đâu |
|---|---|---|---|---|
| 1 | **Quay video demo dự phòng** | **13:00** | 20 phút | `design/kich-ban-video-cp5.md` |
| 2 | **Cho 5 bạn ngoài nhóm dùng thử** — trong đó 2 bạn đã khai từ CP1 | **13:00** | 1 tiếng | `validation/` |
| 3 | **Mỗi người tự viết reflection** của mình | **13:00** | 15 phút/người | `reflection/` |
| 4 | Bấm 5 câu thử tay (TC15–18, TC25), điền vào bảng cuối | trước 17:30 | 15 phút | `eval/ket-qua-luot-2.md` |
| 5 | Điền 2 mã học viên willing user, chỗ `[CẦN NHÓM ĐIỀN 2 MÃ HỌC VIÊN]` | trước 17:30 | 1 phút | `spec.md` |

**Việc 2 đáng 8 điểm** — không làm thì tối đa chỉ được 92.

⚠️ **Làm xong việc 2 thì sửa 2 chỗ** đang ghi "chưa cho 5 bạn dùng thử":
- Slide 6: sửa `design/demo-slides.html` rồi xuất lại PDF (lệnh xuất ghi ở đầu file đó)
- [Phần 8](#phần-8--thuyết-trình-ai-nói-gì) của file này

**Thứ tự nên làm:** đổ dữ liệu vào kênh test trước vì nó chạy mất 5 phút → trong lúc chờ
thì viết reflection → quay video → gọi người tới thử → cuối cùng bấm 5 câu thử.

## Những thứ không có trên GitHub — phải xin trong nhóm

| Thứ | Để làm gì | Đặt ở đâu |
|---|---|---|
| File `k4_messages.csv` | Dữ liệu tin nhắn thật để chạy | `discord-pack/k4_messages.csv` |
| Khoá AI (dạng `AIzaSy...`) | Để bot hỏi được AI | file `.env`, dòng `GEMINI_API_KEY=` |
| Mã bot Discord | Để bật được bot | file `.env`, dòng `DISCORD_BOT_TOKEN=` |
| Link webhook kênh test | Để đổ dữ liệu vào kênh | file `.env`, dòng `DISCORD_WEBHOOK_URL=` |
| Quyền vào server test của nhóm | Để demo | xin người giữ server |
| Thư mục `eval/dem-api/` | Chạy không tốn lượt hỏi AI (không bắt buộc) | chép nguyên thư mục vào `eval/` |

> **Không có khoá AI thì không chạy được gì cả**, kể cả `run.py`. Khoá của ai cũng được,
> tự lấy miễn phí ở [2.3](#23--lấy-khoá-ai).
>
> Muốn chạy **không tốn lượt hỏi AI** thì xin chép thêm thư mục `eval/dem-api/` từ máy
> người trong nhóm — trong đó là kết quả đã nhớ sẵn. Có thư mục này + khoá Gemini của mình
> thì chạy bao nhiêu lần cũng không mất lượt. Thư mục này **không có trên GitHub** vì bên
> trong có tóm tắt tin nhắn thật.

---

# Phần 1 · Dự án này là gì

## Nói một câu

> **Bọn em sửa lại con bot Trợ Lý mà lớp đang dùng. Trước đây hỏi nó thì nó trả lời
> giữa kênh, ai cũng thấy, và chỉ đọc tin trong ngày. Giờ hỏi nó thì nó nhắn riêng cho
> mình bạn, đọc 3 ngày gần đây, và chỉ đọc những kênh mà chính bạn vào được.**

Nhớ ba chữ: **nhắn riêng · 3 ngày · kênh của bạn**.

## Dùng nó thế nào

Chỉ có **một cách**: tag bot ngay trong kênh lớp.

```
Bạn:          @Trợ Lý Kute có gì quan trọng em cần biết không
Trợ Lý Kute:  Mình đã nhắn riêng cho bạn rồi nhé.        (dòng này tự xoá sau 30 giây)
```

Nội dung đi vào **tin nhắn riêng**:

```
Bạn cần lưu ý 8 việc trong 3 ngày qua

  Hạn đăng ký đề tài — 23:59 ngày 20/09
  Xem tin gốc → · #thong-bao · 13/09 21:49

  Hạn đăng ký team QA video — hết ngày 16/9
  Xem tin gốc → · #hoi-dap · 14/09 14:48
  ...

Đã đọc 515 tin · 3 kênh: #thong-bao (4), #hoi-dap (170), #chung (341)
[🚩 Có mục sai]
```

## Ba điều nhóm chọn, mỗi điều có một con số đứng sau

| Chọn gì | Vì sao |
|---|---|
| **Nhắn riêng**, không nói giữa kênh nữa | Bot đang chiếm gần nửa số tin và **88% số chữ** của kênh đông nhất. Chính nó làm kênh ngập. |
| **Mỗi người một câu trả lời khác nhau** | **85%** các bạn chỉ vào đúng 1 kênh, mà việc thì nằm rải ở 5 kênh. Bot chỉ đọc kênh chính bạn vào được — Discord tự chặn, không phải dặn AI. |
| **Đọc 3 ngày**, nhắc lại cũng không sao | **40%** việc còn hạn lại báo từ hôm trước. Bot không nhớ hôm qua bạn xem gì; việc cũ còn hạn thì hôm nay vẫn nhắc. |

## Bot **không** làm mấy việc này

1. Không trả lời giữa kênh cho cả lớp cùng thấy
2. Không tự đăng bản tin hằng ngày — ai hỏi mới trả lời
3. Không đọc kênh mà bạn không vào được
4. Không trả lời câu hỏi về quy định — chỗ đó nhóm không có nguồn để dẫn
5. Không đọc chữ trong ảnh chụp màn hình

## Con số phải thuộc

| Số | Nghĩa |
|---|---|
| **85%** | các bạn chỉ vào đúng 1 kênh (171/201 người) |
| **88%** | chữ trong kênh đông nhất là do bot nói ra |
| **40%** | việc còn hạn lại báo từ hôm trước (2 trong 5) |
| **515 tin → 8 việc** | trong 8 giây |
| **0** | số lần bot dẫn tới một tin không có thật |

## Đã thử bao nhiêu, đúng bao nhiêu

| Lần đo | Lúc đó bot thế nào | Câu thử | Đúng |
|---|---|---|---|
| 1 · 17/09 | đọc 1 ngày · trả lời giữa kênh | 14 | 12 — 85% |
| 2 · 18/09 | đọc 3 ngày · nhắn riêng · theo kênh của bạn | 20 | **20 — 100%** |

**Nói cho sòng phẳng:** 2 trong 20 câu thử là nhóm **sửa lại đề bài chấm**, vì đề cũ chấm
sai chứ bot không sai. Giữ đề cũ thì là **18/20 = 90%**. Nhóm ghi cả hai số.
Còn **5 câu thử phải bấm tay** chưa bấm.

Nhóm cũng tự đọc tay rồi ghi ra đáp án: bot tìm đúng **12/12**, **sót 0**, **thừa 1**.

---

# Phần 2 · Cài đặt từ máy trắng

Khoảng **20 phút**. Mỗi bước có dòng **"✅ Đúng khi"** — chưa thấy thì đừng đi tiếp.

## 2.1 · Cần có sẵn

| Cần gì | Lấy ở đâu |
|---|---|
| **Python 3.10 trở lên** | python.org — lúc cài **nhớ tích "Add Python to PATH"** |
| **Git** | git-scm.com |
| **Tài khoản Discord** | discord.com |
| **Khoá AI của Google (miễn phí)** | aistudio.google.com/apikey |
| **File dữ liệu** | `k4_messages.csv` — **xin trong nhóm**, không có trên GitHub |

> **Mấy chữ tiếng Anh bạn sẽ gặp ở dưới** — không dịch được vì đó là chữ in sẵn trên màn hình,
> phải tìm đúng chữ đó mà bấm:
>
> | Chữ trên màn hình | Nghĩa là gì |
> |---|---|
> | **Add Python to PATH** | ô tích lúc cài Python, để máy biết chỗ tìm Python. Quên tích là gõ lệnh không chạy |
> | **Token** | mã bí mật của con bot, như mật khẩu. Ai có mã này là điều khiển được bot |
> | **Intents** | mấy công tắc cho phép bot được đọc gì. Phải bật cái cho đọc nội dung tin nhắn |
> | **Scopes** | bot được làm những việc gì trong server |
> | **Webhook** | một đường dẫn đặc biệt. Có nó thì chương trình đăng tin vào kênh được mà không cần tài khoản |

```bash
python --version
```

✅ **Đúng khi:** in ra `Python 3.10.x` trở lên.
❌ Báo "không tìm thấy lệnh" → cài lại Python, nhớ tích "Add Python to PATH".

## 2.2 · Tải dự án và cài thư viện

```bash
git clone https://github.com/BenKei-19/K4-3A-E403-tripleT
cd K4-3A-E403-tripleT
pip install -r requirements.txt
```

✅ **Đúng khi:** dòng cuối hiện `Successfully installed ...`
❌ `pip` không chạy → thử `python -m pip install -r requirements.txt`

## 2.3 · Lấy khoá AI

1. Vào **aistudio.google.com/apikey**, đăng nhập Google
2. **Create API key** → **Create API key in new project** → bấm copy
3. Khoá có dạng `AIzaSy...`

> Miễn phí nhưng chỉ **20 lượt hỏi mỗi ngày**. Yên tâm là dự án có nhớ sẵn kết quả cũ:
> hỏi lại đúng thứ đã hỏi rồi thì nó lấy trong máy ra, không tốn lượt nào.

## 2.4 · Đặt file dữ liệu đúng chỗ

File `k4_messages.csv` **cố tình không có trên GitHub** — đó là tin nhắn thật của các bạn
khoá 4, quy định của khoá cấm đưa lên nơi công khai.

```
K4-3A-E403-tripleT/
└── discord-pack/
    └── k4_messages.csv      ← để đúng đây
```

✅ **Đúng khi:** gõ `dir discord-pack` (Windows) hoặc `ls discord-pack` (Mac) thấy file csv.

> Thư mục này đã bị chặn sẵn, lỡ tay `git add` cũng không đẩy lên GitHub được.

## 2.5 · Tạo file `.env`

```bash
# Windows PowerShell
Copy-Item .env.example .env
# Mac / Linux
cp .env.example .env
```

Mở `.env` bằng Notepad, dán khoá vào:

```
GEMINI_API_KEY=AIzaSy...dán khoá của bạn vào đây
```

⚠️ **File `.env` không bao giờ được đẩy lên GitHub.** Trong đó có khoá AI và mã bot.

---

# Phần 3 · Cách chạy

## 3.1 · Chạy thử, chưa cần Discord — làm cái này trước

```bash
python codebase/run.py
```

✅ **Đúng khi:**

```
Đọc 515 tin nhắn · K4-L3-4 · mọi kênh · 3 ngày gần nhất
Đang hỏi Gemini · gemini-2.5-flash...
    (dùng lại kết quả đã lưu, không tốn lượt API)

Bạn cần lưu ý 8 việc

  1. Khung giờ daily standup để được cộng XP: 0h-10h sáng
     Hạn: 10:00 ngày 14/09
     tin gốc [M78917] 2026-09-14 15:46 · D9617
  ...
```

**Tới đây là phần lõi đã chạy.** Mấy phần sau chỉ là gắn nó vào Discord.

Đọc một ngày thay vì 3 ngày:

```bash
python codebase/run.py --ngay 2026-09-13
```

## 3.2 · Đo — khi cần số liệu

```bash
python eval/chay-test.py --luot 3    # chạy 25 câu thử, ghi ra file kết quả
python eval/eval.py                  # đếm bot sót bao nhiêu, thừa bao nhiêu
```

> Đổi số sau `--luot` mỗi lần chạy để không đè kết quả cũ. Lượt 1 bị khoá, gõ `--luot 1`
> nó sẽ từ chối.
>
> ⚠️ Chạy đo tốn khoảng **6 lượt hỏi AI**, mà mỗi ngày chỉ có 20 lượt miễn phí.
> **Đừng chạy sát giờ demo.**

## 3.3 · Chạy bot thật

Cần dựng Discord trước — xem [Phần 4](#phần-4--dựng-discord-để-chạy-thật).

```bash
python codebase/bot.py
```

✅ **Đúng khi:**

```
Trợ Lý Kute đã online: Tro Ly Kute Test#1234
Bot sẽ đọc: 3 ngày gần nhất, mọi kênh người hỏi vào được
Cách dùng: tag bot trong kênh, bot sẽ nhắn riêng cho người hỏi
```

**Để cửa sổ này chạy.** Tắt nó là bot tắt theo.

---

# Phần 4 · Dựng Discord để chạy thật

Khoảng **20 phút**, làm một lần.

## 4.1 · Tạo con bot

1. Vào **discord.com/developers/applications** → **New Application** → đặt tên → **Create**
2. Menu trái chọn **Bot** → **Reset Token** → **Yes, do it!** → **Copy**
3. Dán ngay vào `.env`, dòng `DISCORD_BOT_TOKEN=`

> Mã này **chỉ hiện một lần**. Lỡ đóng cửa sổ thì Reset Token lấy mã mới.
> Ai có mã này là điều khiển được bot — đừng gửi cho ai.

## 4.2 · Bật quyền đọc tin nhắn — ⚠️ hay quên nhất

Vẫn ở trang **Bot**, kéo xuống **Privileged Gateway Intents**:

- Bật **MESSAGE CONTENT INTENT** → gạt sang xanh → **Save Changes**

❌ **Quên bước này thì bot online nhưng tag nó không thèm trả lời.** Lỗi 90% người mới gặp.

## 4.3 · Mời bot vào server

1. Menu trái chọn **OAuth2** → **URL Generator**
2. Ô **SCOPES**: tích `bot`
3. Ô **BOT PERMISSIONS**: tích **View Channels**, **Send Messages**, **Read Message History**
4. Copy link dài ở **GENERATED URL** → dán vào trình duyệt → chọn server → **Authorize**

## 4.4 · Tạo server test

Cột trái Discord bấm **+** → **Create My Own** → **For me and my friends** → đặt tên.

> Phải là server **riêng của nhóm**. Tuyệt đối không đổ dữ liệu vào server thật của lớp.

Tạo 3 kênh thường: `chung`, `thong-bao`, `hoi-dap`

Rồi tạo **2 kênh đội có khoá** — chỗ để thử phần "mỗi người một câu trả lời khác nhau":

1. Bấm **+** → tên `doi-1` → **bật ổ khoá "Private Channel"** → Next → chọn người được vào → Create
2. Làm tương tự với `doi-2`

> ⚠️ **Bot cũng phải được vào các kênh khoá này** thì mới đọc được.
> Vào từng kênh → Edit Channel → Permissions → thêm con bot vào.

## 4.5 · Lấy webhook để đổ dữ liệu

1. Chuột phải kênh `chung` → **Edit Channel** → **Integrations** → **Webhooks**
2. **New Webhook** → **Copy Webhook URL** → dán vào `.env`, dòng `DISCORD_WEBHOOK_URL=`

File `.env` lúc này có đủ 3 dòng:

```
GEMINI_API_KEY=AIzaSy...
DISCORD_BOT_TOKEN=MTU1...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

## 4.6 · Đổ dữ liệu vào kênh test

Xem thử trước, chưa đăng gì:

```bash
python codebase/do-tin-vao-kenh.py --guild K4-L3-4 --ngay tat-ca
```

Thấy đúng thì đăng thật:

```bash
python codebase/do-tin-vao-kenh.py --guild K4-L3-4 --ngay tat-ca --that
```

⏳ **Chờ 4–5 phút** — 515 tin, mỗi tin cách nhau nửa giây cho Discord khỏi chặn.

✅ **Đúng khi:** hiện `Xong: 515 tin đã đăng, 0 lỗi.` và trong Discord thấy tên người
hiện dạng `D3115 · 2026-09-13 00:08`.

> Cái đuôi ngày giờ trong tên là **cố ý**. Tin đăng lại mang giờ của hôm nay, nên phải
> nhét ngày gốc vào tên thì bot mới biết tin nào của ngày nào.

## 4.7 · Thử bot

Bật bot (`python codebase/bot.py`), rồi trong Discord gõ:

```
@Tro Ly Kute Test có gì quan trọng em cần biết không
```

✅ **Đúng khi:** bot **nhắn riêng** cho bạn danh sách, còn trong kênh chỉ còn một dòng
*"Mình đã nhắn riêng cho bạn rồi nhé"* và dòng đó **tự xoá sau 30 giây**.

Thử thêm câu này cho vui:

```
@Tro Ly Kute Test cho mình hỏi cách cài docker với
```

✅ Bot nói thẳng là nó không làm được việc đó, **không đổ danh sách ra**.

## 4.8 · Thử phần "mỗi người một câu trả lời khác nhau"

Đây là phần ăn điểm nhất lúc demo.

1. Rủ một bạn vào server, **chỉ cho bạn ấy vào `doi-2`**, còn bạn ở `doi-1`
2. Đăng vài tin có hạn vào mỗi kênh đội, ví dụ:
   - `doi-1`: *"Nhóm mình họp 20:00 tối mai nhé"*
   - `doi-2`: *"Hạn nộp phần thiết kế là 23:59 ngày mai"*
3. Hai người cùng tag bot

✅ **Đúng khi:** hai người ra hai danh sách khác nhau, và dòng cuối mỗi câu trả lời liệt kê
**tập kênh khác nhau**.

---

# Phần 5 · File nào làm gì

```
codebase/
  digest.py            ← phần lõi: đọc tin, hỏi AI, lọc kết quả. Sửa gì cũng chủ yếu ở đây
  bot.py               ← nối với Discord: nghe tag, quét kênh, nhắn riêng
  run.py               ← chạy trên dòng lệnh, không cần Discord. Thử nhanh
  do-tin-vao-kenh.py   ← đổ dữ liệu vào kênh test

eval/
  chay-test.py         ← chạy 25 câu thử, ra bảng kết quả
  eval.py              ← đếm bot sót / thừa bao nhiêu
  test-cases.json      ← 25 câu thử
  golden-set.json      ← đáp án nhóm tự đọc tay rồi ghi ra
  ket-qua-luot-1.md    ← kết quả lần đo đầu (đã khoá, không sửa)
  ket-qua-luot-2.md    ← kết quả lần đo hai

validation/            ← đồ nghề cho người ngoài nhóm dùng thử
reflection/            ← mỗi người một file tự viết
design/                ← canvas, file gốc của slide, hướng dẫn quay video

spec.md                ← tài liệu chính, giải thích mọi quyết định
huong-dan.md           ← file này
demo-slides.pdf        ← slide 6 trang
```

## Bot chạy theo thứ tự nào

```
bạn tag bot
    ↓
Hỏi chuyện khác? → nói luôn là không làm được, dừng          ← máy
    ↓
Lấy tin 3 ngày gần đây, ở các kênh bạn vào được              ← máy
    ↓
Đọc một lượt, chỉ ra chỗ nào có hạn                          ← AI
    ↓
Kiểm lại: tin này có thật không? Không có thì bỏ             ← máy
    ↓
Tin cũ đã bị đổi hạn → bỏ tin cũ                             ← máy
    ↓
Hai chỗ nói cùng một việc → chỉ giữ một                      ← máy
    ↓
Sắp thứ tự: việc có hạn lên trước, tin mới lên trước         ← máy
    ↓
Nhắn riêng cho bạn + nút "Có mục sai"
```

**AI chỉ đọc. Còn lại máy làm theo luật nhóm viết.** Chia ra như vậy để lúc sai thì biết
là **AI đọc sai** hay **luật nhóm viết sai**.

---

# Phần 6 · Muốn sửa thì sửa ở đâu

| Muốn đổi gì | Sửa chỗ nào |
|---|---|
| Đọc 5 ngày thay vì 3 ngày | `.env`, thêm `SO_NGAY_QUET=5` |
| Bot trả lời chậm quá | `.env`, thêm `DIGEST_EFFORT=low` |
| Bắt hỏi AI lại từ đầu, không lấy kết quả cũ trong máy | `.env`, thêm `DIGEST_CACHE=0` |
| Đổi mức "cần kiểm lại" | `codebase/digest.py`, dòng `NGUONG_CAN_XAC_NHAN` |
| Đổi cách bot hiểu "việc quan trọng" | `codebase/digest.py`, phần `SYSTEM` — ⚠️ **sửa thì phải sửa cả `eval/golden-set.json`**, không thì số đo sai mà không ai biết |
| Thêm từ khoá để bot nhận ra câu hỏi đúng việc | `codebase/bot.py`, dòng `Y_DINH` |
| Đổi số việc mỗi tin nhắn | `codebase/bot.py`, dòng `MUC_MOI_TIN` |

---

# Phần 7 · Lỗi hay gặp

| Thấy gì | Vì sao | Sửa thế nào |
|---|---|---|
| Bot online nhưng **tag không trả lời** | Chưa bật MESSAGE CONTENT INTENT | Developer Portal → Bot → bật **MESSAGE CONTENT INTENT** → Save → chạy lại bot |
| `Chưa có DISCORD_BOT_TOKEN` | Chưa có file `.env`, hoặc lỡ đặt tên `.env.txt` | Kiểm tên file đúng là `.env`, không đuôi |
| `Không thấy .../discord-pack/k4_messages.csv` | File dữ liệu đặt sai chỗ | Xem lại [2.4](#24--đặt-file-dữ-liệu-đúng-chỗ) |
| Máy báo `Hết lượt gọi Gemini free tier` | Hỏi AI quá 20 lần trong ngày | Chờ hôm sau, hoặc mở `.env` đổi `GEMINI_MODEL=gemini-2.0-flash` (model khác có lượt riêng) |
| Bot bảo **"không nhắn riêng cho bạn được"** | Người hỏi đang chặn tin nhắn riêng | Chuột phải server → **Privacy Settings** → bật **Direct Messages** |
| Bot trả lời **"không thấy tin nào"** | Tin đổ vào từ hơn 3 ngày trước nên ngoài tầm đọc | Đổ lại dữ liệu ([4.6](#46--đổ-dữ-liệu-vào-kênh-test)) |
| Bot **không đọc kênh đội** | Bot chưa được thêm vào kênh khoá | Edit Channel → Permissions → thêm bot |
| Tiếng Việt hiện thành **ô vuông** trong PowerShell | Font cửa sổ dòng lệnh | Không ảnh hưởng kết quả, bỏ qua |
| `pip` không tìm thấy | Python chưa vào PATH | Dùng `python -m pip install ...` |

---

# Phần 8 · Thuyết trình: ai nói gì

Slide là `demo-slides.pdf`, 6 trang. Tổng khoảng **6 phút**.

Giám khảo có thể hỏi **bất kỳ ai** về phần có tên người đó. Không giải thích được thì
phần đó 0 điểm. **Mỗi người chỉ nói phần mình làm, đừng nói hộ nhau.**

| Người | Slide | Khoảng | Nói gì |
|---|---|---|---|
| **Hiếu** | 1 + 2 | 1' 45 | Nhóm làm gì · vì sao làm · mấy con số |
| **Huy** | 3 + 4 | 2' 30 | Ba điều nhóm chọn · bấm demo |
| **Khánh** | 5 | 1' | Thử bao nhiêu lần, đúng bao nhiêu |
| **Hải** | 6 | 45" | Cái chưa xong |

## Lúc demo bấm đúng 4 cái

1. Trong kênh lớp gõ `@Trợ Lý Kute có gì quan trọng em cần biết không`
2. Chỉ vào kênh: **chỉ còn một dòng**, rồi mở tin nhắn riêng ra
3. Bấm một **"Xem tin gốc →"** → Discord nhảy đúng tin đó
4. Đổi tài khoản thứ hai, tag lại → danh sách khác

## Chuẩn bị trước, đừng làm tại chỗ

```bash
python codebase/do-tin-vao-kenh.py --guild K4-L3-4 --ngay tat-ca --that   # làm sớm, 4-5 phút
python codebase/bot.py                                                    # để chạy
python codebase/run.py                                                    # kiểm cho chắc
```

**Lệnh thứ 3 quan trọng.** Phải thấy dòng `(dùng lại kết quả đã lưu, không tốn lượt API)` —
nghĩa là kết quả nằm sẵn trong máy, lúc demo **không cần mạng**.

Thêm: phóng to chữ Discord (`Ctrl` `+` hai lần) · tắt thông báo · đăng nhập sẵn 2 tài khoản.

## Nếu hỏng

| Hỏng gì | Làm gì |
|---|---|
| **Mạng chết** | Chiếu video dự phòng đã nộp ở CP5. Không bị trừ điểm. |
| **Bot không trả lời** | Đừng sửa giữa chừng. Gõ `python codebase/run.py` — chạy chắc chắn vì lấy từ bộ nhớ trong máy. Nói thẳng: *"đây là bản chạy trên terminal của cùng một phần lõi"*. |
| **Bot chậm** | Cứ nói tiếp phần bảng bên phải slide 4, đừng đứng im nhìn màn hình. |
| **Máy chiếu hỏng** | Đọc theo `demo-slides.pdf`, ai cũng có sẵn một bản trong máy. |

**Đừng bao giờ sửa code khi đang đứng trên bục.**

---

# Phần 9 · Câu hỏi có thể bị hỏi

### "Phần nào là AI, phần nào các em tự viết?"

> "AI làm đúng một việc: đọc một lượt rồi chỉ ra chỗ nào có hạn. Còn kiểm tin có thật không,
> bỏ tin cũ đã đổi hạn, bỏ chỗ nói trùng, sắp thứ tự — đều là luật bọn em viết bằng code,
> không dùng AI. Chia ra để lúc sai thì biết sai ở đâu."

### "Làm sao chắc bot không bịa?"

> "Bọn em bắt nó chép lại đúng mã tin có trong danh sách đưa vào. Xong code kiểm lại từng mã.
> Mã nào không có thật thì vứt dòng đó, người dùng không bao giờ thấy. Qua hai lần đo,
> số lần nó dẫn tới tin không có thật là **0**."

### "Sao lại 3 ngày, không phải 7 ngày hay 1 ngày?"

> "Vì bọn em đếm được: tính tới hết ngày 14 có 5 việc còn hạn, thì 2 việc trong đó báo từ
> hôm trước. Chỉ đọc 1 ngày là sót 40%. Còn 7 ngày thì bọn em **chưa đo**, nên chưa dám nói.
> 3 ngày là con số bọn em có số liệu để đứng sau."

### "Người khác hỏi cùng lúc thì sao?"

> "Mỗi người nhận một câu trả lời khác nhau, vì bot chỉ đọc kênh người đó vào được.
> Hai bạn ở hai đội khác nhau sẽ ra hai danh sách khác nhau. Em demo được luôn ạ."

### "Bot trả lời sai thì sao?"

> "Có nút 'Có mục sai' ngay dưới câu trả lời. Bấm vào thì bọn em ghi lại để chấm lại.
> Nhưng em nói thật là nó mới chỉ ghi lại thôi, chưa hỏi sai ở dòng nào và chưa tự sửa được."

### "Cái này khác gì bản tin cuối ngày mà bot đang làm?"

> "Khác hẳn ạ. Bản tin cuối ngày là bot tự đăng cho cả lớp cùng đọc, ai cũng nhận như nhau.
> Cái của bọn em là bạn hỏi thì mới trả lời, trả lời riêng, và nội dung theo đúng kênh của bạn.
> Bọn em còn cố ý **không làm** bản tin tự đăng — vì bot đã làm rồi, làm lại là trùng."

### "Sao lại nhắc lại việc hôm qua đã báo? Không phiền à?"

> "Bọn em chọn thế có chủ ý. Bot không nhớ hôm qua bạn xem gì. Đọc lại một dòng mất 2 giây,
> còn quên một hạn nộp thì mất điểm bài. Hai cái lệch nhau xa quá nên bọn em chọn thà thừa.
> Mà chính chương trình cũng đăng lại thông báo sau 2 ngày, nên bot phải chịu được chuyện đó."

### "Người dùng chặn tin nhắn riêng thì sao?"

> "Thì bot trả lời ngay trong kênh, nói rõ là không nhắn riêng được và chỉ cách bật lại.
> Em nhận đây là điểm yếu: bọn em đã bỏ lệnh gạch chéo để chỉ còn một cách dùng duy nhất,
> nên trường hợp này chưa có đường lui. Bọn em có ghi trong spec."

### ⚠️ Câu khó nhất: "Các em sửa đề bài chấm rồi mới được 100%, thế có gian không?"

**Khánh trả lời:**

> "Dạ em nói rõ ạ. Có một tin dài 741 chữ, dòng cuối cùng ghi 'Hạn: hết ngày 16/9'.
> Lúc ngồi đọc để ghi đáp án, bạn em chỉ đọc phần đầu nên ghi là 'tin này không có hạn'. Bot đưa nó vào
> và bị chấm là sai. Nhưng đọc kỹ thì **bot đúng, đề bài của bọn em sai**.
>
> Bọn em sửa đề bài, nhưng **không xoá kết quả cũ** — file kết quả lần đo đầu bọn em khoá lại,
> code còn từ chối ghi đè lên nó. Và bọn em ghi cả hai số trong spec: theo đề mới là 100%,
> theo đề cũ là 90%."

### Nếu bị hỏi số mà không nhớ

> "Cái đó em ghi trong spec ạ, em không nhớ chính xác nên không dám nói bừa."

Nói vậy tốt hơn đoán sai.

---

# Ba điều đừng làm

1. **Đừng đẩy file `.env` lên GitHub.** Trong đó có khoá AI và mã bot. File này đã bị chặn
   sẵn, đừng tự gỡ chặn.
2. **Đừng đổ dữ liệu vào server thật của lớp.** Chỉ đổ vào server test riêng của nhóm.
3. **Đừng chép file `k4_messages.csv` ra ngoài.** Đó là tin nhắn thật của các bạn cùng khoá.
   Cần dẫn ví dụ thì ghi mã tin dạng `M09449`, đừng chép nguyên câu.

---

*Muốn hiểu sâu vì sao dự án làm như vậy — mọi con số, mọi quyết định, cả những hướng đã bỏ —
đọc `spec.md`.*

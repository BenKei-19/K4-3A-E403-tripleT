# codebase — Trợ Lý Kute

Học viên hỏi bot *"những thông tin quan trọng tôi cần nắm là gì?"* → bot quét
**mọi kênh người đó có quyền đọc** (kể cả kênh đội/nhóm) trong **3 ngày gần
nhất**, rồi **trả lời riêng — chỉ người hỏi thấy** — danh sách mốc thời gian
kèm link về tin gốc.

Đây là **tối ưu một lượt tương tác đã có** của bot Trợ Lý trong server lớp,
không phải bot mới và không phải bảng tin. Chi tiết thiết kế: `../spec.md`.

Hai cửa vào, cả hai đều riêng tư:

| Cách hỏi | Bot trả ở đâu |
|---|---|
| `/luuy` | **ephemeral** — hiện ngay trong kênh nhưng chỉ người gõ thấy |
| Tag bot | **nhắn riêng (DM)**; trong kênh chỉ còn 1 dòng báo, tự xoá sau 30 giây |

## Phần nào chạy thật, phần nào mock

| Thành phần | Trạng thái | Ghi chú |
|---|---|---|
| `digest.py` — phân loại tin bằng AI | **Chạy thật** | Một lời gọi cho cả cửa sổ; tự chọn Gemini hay Claude theo key có trong `.env` |
| `digest.py` — guardrail, chống trùng theo mốc, xếp hạng | **Chạy thật** | Code thuần, không dùng AI |
| `run.py` — chạy trên terminal | **Chạy thật** | Đọc pack hoặc file JSON, gọi AI, in kết quả |
| `bot.py` — quét theo quyền kênh của người hỏi, cửa sổ 3 ngày | **Chạy thật** | Chỉ đọc kênh mà **cả người hỏi lẫn bot** có quyền đọc |
| `bot.py` — trả lời riêng (`/luuy` ephemeral + DM) | **Chạy thật** | Bị chặn DM thì nói thẳng lý do, không im lặng |
| `bot.py` — cổng lọc câu hỏi ngoài phạm vi, nút "Có mục sai" | **Chạy thật** | Phản hồi ghi vào `../eval/phan-hoi.log` |
| `../mock/tro-ly-demo-mock.html` | **Mock** | Giao diện mô phỏng, câu trả lời viết cứng. Dùng ở CP2 để trình bày luồng, **không gọi AI** |
| Dữ liệu | **Mock / data BTC** | `data/messages-mock.json` là dữ liệu giả tự sinh. Data thật lấy từ `discord-pack` của BTC, để ngoài repo |

## Cài đặt

```bash
pip install -r ../requirements.txt
cp ../.env.example ../.env     # rồi điền GEMINI_API_KEY hoặc ANTHROPIC_API_KEY
```

Biến trong `.env` đáng biết: `SO_NGAY_QUET` (mặc định 3) · `DIGEST_EFFORT`
(low/medium/high) · `DIGEST_CACHE=0` để ép gọi API mới.

## Chạy

```bash
# Bản terminal — nhanh nhất, dùng để quay video nếu bot chưa kịp
python codebase/run.py

# Đổ cả cửa sổ 3 ngày vào kênh test (giữ ngày + giờ gốc)
python codebase/do-tin-vao-kenh.py --ngay tat-ca --that

# Trên một ngày khác (file discord-pack để ngoài repo)
python codebase/run.py --file "C:/duong/dan/ngoai/repo/ngay-04.json"

# Bot Discord trong server test của nhóm
python codebase/bot.py

# Đo trên golden set — ra số cho CP3
python eval/eval.py

# Chạy bộ 25 test case (lượt 1 đã khoá, không ghi đè được)
python eval/chay-test.py --luot 2
```

## Luồng xử lý

```
học viên hỏi (/luuy hoặc tag bot)
      ↓
  CỔNG LỌC Ý ĐỊNH                         ← bot.py, code thuần
  hỏi chuyện khác → nói rõ phạm vi, dừng
      ↓
  QUÉT THEO QUYỀN KÊNH CỦA NGƯỜI HỎI      ← bot.py
  chỉ kênh cả người hỏi lẫn bot đọc được,
  3 ngày gần nhất, giữ NGÀY + GIỜ gốc
      ↓
  MỘT lời gọi AI cho cả cửa sổ            ← digest.py, gọi AI thật
  trả JSON: message_id, loại, tóm tắt,
            hạn chót, độ chắc, thay_thế_cho
      ↓
  GUARDRAIL: message_id có thật không?    ← code, không dùng AI
  không có trong input → vứt mục đó
      ↓
  Tin bị đính chính → bỏ bản cũ           ← so bằng NGÀY ĐĂNG, phủ cả cửa sổ
      ↓
  Bỏ mục TRÙNG MỐC                        ← trùng theo (hạn + tóm tắt),
      ↓                                      KHÔNG theo mã tin: một tin có
  Xếp hạng bằng code                         thể chứa hai mốc khác nhau
      ↓                                    ← DEADLINE trước ANNOUNCE,
  TRẢ RIÊNG cho người hỏi                    tin mới trước tin cũ (tính cả ngày)
  + nút "Có mục sai"
```

**AI phân loại, code quyết định.** Model chỉ nói "tin này là loại gì"; việc
chọn mục nào vào bản tin và xếp theo thứ tự nào là code làm. Như vậy khi kết
quả sai thì biết sai ở tầng nào.

## Ba chỗ chống bịa

1. **Model phải chép lại `message_id` có trong danh sách.** Code kiểm tra lại
   từng id; id không tồn tại thì mục đó bị vứt, không hiển thị cho người dùng.
2. **Mỗi mục đều dẫn link về tin gốc**, người đọc tự kiểm chứng được trong một cú bấm.
3. **Không tìm thấy thì nói không tìm thấy**, không đoán bừa.

## Đổi sang dữ liệu `discord-pack`

Sửa đúng một hàm: `_chuan_hoa()` trong `digest.py` — ánh xạ tên trường của pack
sang `TinNhan(id, gio, nguoi, vai, noi_dung)`. Phần còn lại giữ nguyên.

File pack phải để **ngoài repo** (`.gitignore` đã chặn sẵn) — quy định bảo mật
điều 3 cấm commit data pack vào repo nộp bài vì repo này công khai.

## Chi phí và tốc độ

Một lời gọi cho cả ngày (~40 tin) thay vì gọi từng tin. Rẻ hơn, nhanh hơn, và
model nhìn được ngữ cảnh cả ngày nên biết tin nào đính chính tin nào.

Video 30 giây mà gọi API lâu quá thì đặt `DIGEST_EFFORT=low` trong `.env` —
phân loại không phải việc cần suy nghĩ sâu.

Cache theo prompt: cùng một cửa sổ hỏi lại thì đọc từ `../eval/dem-api/`,
không tốn lượt API. **Sửa prompt là mất cache** — mọi kết quả cũ phải chạy lại.

Lưu ý về cache và cá nhân hoá: hai người ở hai tập kênh khác nhau sẽ tạo ra hai
prompt khác nhau, nên cache **không** làm họ nhận chung một câu trả lời. Đó là
chủ ý — xem `../spec.md` §4, phần "Cá nhân hoá được xác định thế nào".

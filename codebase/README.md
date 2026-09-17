# codebase — Trợ Lý Kute

Bot Discord trả lời câu hỏi *"hôm nay tôi cần lưu ý gì?"* bằng cách đọc tin nhắn
trong ngày của kênh lớp và chỉ ra những thông báo, deadline cần biết — kèm link
về tin gốc.

## Phần nào chạy thật, phần nào mock

| Thành phần | Trạng thái | Ghi chú |
|---|---|---|
| `digest.py` — phân loại tin bằng AI | **Chạy thật** | Gọi Claude API thật, một lời gọi cho cả ngày |
| `digest.py` — guardrail, xếp hạng | **Chạy thật** | Code thuần, không dùng AI |
| `run.py` — chạy trên terminal | **Chạy thật** | Đọc file JSON, gọi AI, in kết quả |
| `bot.py` — bot Discord | **Chạy thật** | Đọc lịch sử kênh thật trong server test của nhóm |
| `../mock/tro-ly-demo-mock.html` | **Mock** | Giao diện mô phỏng, câu trả lời viết cứng. Dùng ở CP2 để trình bày luồng, **không gọi AI** |
| Dữ liệu | **Mock / data BTC** | `data/messages-mock.json` là dữ liệu giả tự sinh. Data thật lấy từ `discord-pack` của BTC, để ngoài repo |

## Cài đặt

```bash
pip install -r ../requirements.txt
cp ../.env.example ../.env     # rồi điền ANTHROPIC_API_KEY
```

## Chạy

```bash
# Bản terminal — nhanh nhất, dùng để quay video nếu bot chưa kịp
python codebase/run.py

# Trên một ngày khác (file discord-pack để ngoài repo)
python codebase/run.py --file "C:/duong/dan/ngoai/repo/ngay-04.json"

# Bot Discord trong server test của nhóm
python codebase/bot.py

# Đo trên golden set — ra số cho CP3
python eval/eval.py
```

## Luồng xử lý

```
tin nhắn một ngày
      ↓
  MỘT lời gọi Claude cho cả ngày          ← digest.py, gọi AI thật
  trả JSON: message_id, loại, tóm tắt,
            hạn chót, độ chắc, thay_thế_cho
      ↓
  GUARDRAIL: message_id có thật không?    ← code, không dùng AI
  không có trong input → vứt mục đó
      ↓
  Tin bị đính chính → bỏ bản cũ
      ↓
  Xếp hạng bằng code                      ← DEADLINE trước ANNOUNCE,
      ↓                                      TA/Coach trước học viên,
  bản tin trả về học viên                    mới trước cũ
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

Bước tiếp theo nếu có thời gian: phân loại **một lần mỗi ngày rồi cache lại**,
ai hỏi cũng trả cùng một bản. Vừa rẻ vừa đảm bảo hai người hỏi không nhận hai
câu trả lời khác nhau.

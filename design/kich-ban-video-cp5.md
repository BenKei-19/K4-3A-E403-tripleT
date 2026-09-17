# Kịch bản quay video demo dự phòng — CP5

**Video này để buổi pitch không chết vì mạng.** Nếu hôm pitch mạng hỏng, BTC chiếu
video này và **không trừ điểm**. Nên nó phải quay đúng phần định demo trên sân khấu,
không phải quay cho có.

> Khác với video CP3: CP3 chứng minh sản phẩm chạy, quay thô cũng được.
> **CP5 là bản sao lưu của màn demo** — cái gì định bấm trên sân khấu thì quay đúng cái đó.

**Độ dài nhắm tới: 90–120 giây.** Một lượt, không dựng.

---

## Chuẩn bị (làm trước khi bấm quay)

| # | Việc | Lệnh / thao tác |
|---|---|---|
| 1 | Đổ dữ liệu 3 ngày vào kênh test, giữ ngày giờ gốc | `python codebase/do-tin-vao-kenh.py --guild K4-L3-4 --ngay tat-ca --that` |
| 2 | Bật bot, chờ dòng `da dang ky /luuy` | `python codebase/bot.py` |
| 3 | **Kiểm tra cache đã ấm** — chạy thử một lần, phải thấy dòng `(dùng lại kết quả đã lưu, không tốn lượt API)` | `python codebase/run.py` |
| 4 | Đăng nhập **2 tài khoản Discord** ở 2 kênh đội khác nhau (cảnh 3 cần) | |
| 5 | Phóng to chữ Discord: Ctrl `+` hai lần. Chữ nhỏ trên máy chiếu là không ai đọc được | |
| 6 | Tắt thông báo, tắt Slack/Zalo, đóng tab thừa | |

> **Cache là thứ giữ cho video không chết.** Bước 3 bắt buộc: nếu nó gọi API thật thì
> lúc quay có thể dính giới hạn tốc độ và treo giữa chừng. Thấy dòng "dùng lại kết quả
> đã lưu" nghĩa là an toàn.

---

## Bốn cảnh

### Cảnh 1 · Nỗi đau — 15 giây

**Quay:** cuộn kênh `#chung` của server test từ dưới lên, cuộn nhanh và dài.

**Nói:**
> "Đây là 3 ngày tin nhắn của một lớp. 515 tin. Trong đó chỉ có 6 tin là mốc thời gian
> thật sự phải làm gì đó. Học viên vắng hai hôm, mở lên là phải cuộn thế này."

**Lưu ý:** cuộn đủ lâu để người xem thấy *mệt*. Đây là chỗ bán bài toán.

---

### Cảnh 2 · Hỏi và nhận riêng — 35 giây

**Quay:** gõ `/luuy` trong kênh lớp → chờ → embed hiện ra.

**Phải thấy rõ trong khung hình:**
- Nhãn **"Only you can see this"** của Discord → bằng chứng trả lời riêng
- Tiêu đề **"Bạn cần lưu ý 8 việc trong 3 ngày qua"**
- Ít nhất 2 mục có **Hạn:** và dòng **"Xem tin gốc → · #kênh · ngày giờ"**
- Chân embed: **"Đã đọc 515 tin · 3 kênh: …"**

**Nói:**
> "Hỏi một câu. Bot đọc mọi kênh mình có quyền xem trong 3 ngày, trả lời riêng — chỉ mình
> thấy. Kênh lớp không thêm một chữ nào. Mỗi mốc kèm link về tin gốc để tự kiểm."

**Rồi bấm vào một link "Xem tin gốc →"** — Discord nhảy đúng tin đó. Cảnh này quan trọng:
nó chứng minh không bịa nguồn.

---

### Cảnh 3 · Cá nhân hoá — 25 giây

**Quay:** chuyển sang tài khoản thứ hai (ở kênh đội khác), gõ `/luuy`.

**Phải thấy:** danh sách **khác** danh sách của tài khoản 1, và chân embed liệt kê
**tập kênh khác**.

**Nói:**
> "Người ở đội khác hỏi cùng lúc thì nhận câu trả lời khác — vì bot chỉ đọc kênh mà
> chính người hỏi có quyền đọc. Không phải nhờ dặn dò trong prompt, mà nhờ quyền của Discord."

**Đây là cảnh ăn điểm nhất.** Không có nó thì "cá nhân hoá" chỉ là lời nói.

---

### Cảnh 4 · Khi bot không biết — 20 giây

**Quay hai thứ, nhanh:**

1. Tag bot kèm câu lệch chủ đề: `@Trợ Lý Kute cho mình hỏi cách cài docker với`
   → bot trả lời nói rõ phạm vi, **không đổ ra danh sách mốc**.
2. Chỉ vào nút **"🚩 Có mục sai"** dưới câu trả lời (bấm luôn cũng được).

**Nói:**
> "Hỏi chuyện khác thì nó nói thẳng là không làm được, không đoán bừa. Và nếu nó sai,
> người dùng có nút báo lại."

---

## Checklist trước khi nộp video

- [ ] Có nhãn **"Only you can see this"** hiện rõ ít nhất một lần
- [ ] Có **bấm vào link tin gốc** và Discord nhảy đúng tin
- [ ] Có **hai tài khoản** ra hai kết quả khác nhau
- [ ] Có cảnh bot **từ chối** câu ngoài phạm vi
- [ ] Không lộ token, không lộ `.env`, không lộ tên thật của ai trong data pack
- [ ] Không quay nhầm cửa sổ có nội dung pack dán nguyên văn ra ngoài server test
- [ ] Nghe lại tiếng: không có tiếng thông báo, không có tiếng ồn nền

---

## Nếu bot hỏng lúc quay

Đừng sửa giữa chừng cho kịp. **Quay bản terminal** — chắc chắn chạy, và vẫn là AI chạy thật:

```bash
python codebase/run.py
```

Nó in đúng 8 mục đó kèm mã tin, giờ, và số tin đã đọc. Kém ấn tượng hơn bot Discord,
nhưng còn hơn video treo giữa chừng. Nói thẳng trong lúc pitch là "bản terminal của cùng
một hàm lõi" — giám khảo chấm chuỗi quyết định, không chấm độ hoành tráng.

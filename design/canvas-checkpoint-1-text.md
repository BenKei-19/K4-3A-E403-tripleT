# CANVAS CHECKPOINT 1 — nội dung 4 ô

[Tên nhóm] · [Tên sản phẩm] — nâng cấp bot Trợ Lý sẵn có: hỏi một câu, biết hôm nay cần lưu ý gì

---

## 01 · NGƯỜI DÙNG & NỖI ĐAU

**Thông báo quan trọng trôi mất giữa dòng tin nhắn**

Job: Học viên mở Discord sau vài giờ vắng mặt (đi học, đi làm, ngủ) và cần biết ngay
hôm nay có thông báo gì, deadline nào mới, mình phải làm gì — mà không phải cuộn ngược
lại cả ngày tin nhắn.

Pain: Tin quan trọng của TA nằm lẫn giữa hàng trăm tin chat. Học viên hoặc mất thời gian
cuộn lại thủ công, hoặc bỏ qua và chấp nhận rủi ro biết muộn một deadline. Hệ quả là phải
đi hỏi lại bot, nhắn bạn bè hoặc tag TA để xác nhận những thông tin vốn đã được thông báo
trong kênh.

---

## 02 · BẰNG CHỨNG BAN ĐẦU

**Khảo sát 12 học viên trong lớp**

Nguồn: Google Form nội bộ của nhóm, 12 phản hồi, ngày 16/09/2026.

- Thứ học viên tag bot hỏi nhiều nhất đều là thông tin đã từng được thông báo trong kênh:
  deadline (4 lượt), điểm danh/XP/quy định (4 lượt), cách dùng Discord (3 lượt).
- 11/12 phải tự đi tìm lại thông tin khi không có câu trả lời chắc chắn: nhắn bạn bè (6),
  tag tay TA/Coach (5), tự cuộn lại thông báo gốc để đọc lại (4).
- 6/12 từng nhận thông tin sai hoặc không chắc chắn từ bot Trợ Lý hiện tại.
- Trong 7 người đã từng hỏi bot về quy định/deadline, 6 người thất bại ở lần gần nhất:
  3 dài dòng lạc trọng tâm · 2 sai hoặc mâu thuẫn · 1 không biết nhưng vẫn cố đoán.
  Chỉ 1 người được trả lời đúng.

Khoảng trống đã biết: form chưa hỏi trực tiếp "bạn đã từng biết muộn một thông báo/deadline
vì nó trôi trong kênh chưa" — nhóm bổ sung 2 câu này trước CP2.

---

## 03 · LÁT CẮT & AUTOMATION

**Một câu hỏi cho bot, một danh sách cần lưu ý**

Nhãn quyết định: DIGEST · CLARIFY · NONE

Lát cắt: học viên tag bot ngay trong kênh — "@Trợ Lý hôm nay tôi cần lưu ý gì?" — bot quét
tin nhắn trong ngày và trả về những mục quan trọng, mỗi mục 1 dòng kèm link tới tin gốc để
học viên tự kiểm chứng. Đây là nâng cấp trên chính con bot lớp đang dùng, không phải bot mới.

Conditional:
- DIGEST — trả danh sách khi có thông báo hoặc deadline từ TA–Coach.
- CLARIFY — hỏi lại một câu khi chưa rõ mốc thời gian (hôm nay, hay từ lần cuối bạn đọc).
- NONE — nói thẳng "hôm nay không có gì mới" khi không tìm thấy; không bịa mục không có
  trong kênh.

---

## 04 · NGƯỜI THỬ & PHÂN CÔNG

**Có người thử, có người chịu trách nhiệm**

Willing users: 7/12 người khảo sát đồng ý thử tính năng mới của bot trước giờ demo; 6 người
đã để lại tên + mã học viên (danh sách giữ trong nhóm, không đưa lên slide).

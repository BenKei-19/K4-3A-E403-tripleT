# R6 — Cho người ngoài nhóm dùng thử

Buổi này để biết **giải pháp có ăn thua không**, không phải để lấy lời khen.
Người thử chê cũng tính đủ điểm — miễn là bằng chứng thật.

Cần đủ bốn thứ, thiếu một thứ là mất điểm khối này:

| | |
|---|---|
| **5 người ngoài nhóm** dùng thử | trong đó **2 người đã khai từ CP1** |
| **Quote nguyên văn** | chép đúng lời họ nói, **kể cả viết sai chính tả** |
| **Bảng nhật ký** | ai thử · giao task gì · kẹt ở đâu · quote · quyết định → `nhat-ky.md` |
| **Ít nhất 1 thay đổi** | ghi vào **§9 Changelog** của `spec.md`. Giữ nguyên thì phải nói rõ vì sao |

---

## Chuẩn bị trước (10 phút, làm một lần)

1. Đổ dữ liệu 3 ngày vào server test, giữ nguyên ngày giờ gốc:
   ```bash
   python codebase/do-tin-vao-kenh.py --guild K4-L3-4 --ngay tat-ca --that
   ```
2. Bật bot: `python codebase/bot.py` — chờ dòng `da dang ky /luuy trong server ...`
3. **Tạo ít nhất 2 kênh đội** với quyền khác nhau, mỗi người thử chỉ vào được một
   kênh đội. Đây là chỗ chứng minh cá nhân hoá — hai người phải nhận hai câu trả lời khác nhau.
4. Mở sẵn `nhat-ky.md` để gõ trực tiếp trong lúc quan sát.

## Cách chạy một lượt (8–10 phút mỗi người)

1. Đưa họ **`phieu-task.md`**, đọc to task một lần, rồi **ngồi im**.
2. **Không hướng dẫn, không gợi ý, không chữa.** Họ loay hoay chỗ nào thì đó chính
   là dữ liệu. Chỉ mở miệng khi họ kẹt quá 60 giây và hỏi thẳng.
3. **Bấm giờ** từ lúc họ bắt đầu tới lúc họ nói "xong".
4. Gõ lại **nguyên văn** mọi câu họ nói ra miệng. Đừng sửa câu cho gọn,
   đừng bỏ từ đệm. Sai chính tả thì cứ để nguyên.
5. Hết lượt mới được hỏi thêm — và chỉ hỏi về **chuyện đã xảy ra**:
   - "Lúc nãy bạn dừng lại ở chỗ này, bạn đang nghĩ gì?"
   - "Cái nào trong danh sách này bạn thấy không liên quan tới mình?"
   - **Không hỏi** "bạn thấy sản phẩm thế nào", "có hay không", "có dùng không".

## Chia nhóm để có cái đối chiếu

| Ai | Cách làm | Để đo |
|---|---|---|
| 3 người | Dùng bot (`/luuy` hoặc tag bot) | Thời gian tìm · số mốc tìm ra |
| 2 người | **Cuộn tay**, không được dùng bot | Cùng task, để biết bot có nhanh hơn thật không |

Người cuộn tay là đối chứng. Không có họ thì con số "nhanh hơn" chỉ là cảm giác.

## Quote thế nào mới ăn điểm

| Chưa đạt | Đạt |
|---|---|
| *"Demo này ok rồi đấy"* | *"ủa cái này là của đội em hả, sao em không thấy trong kênh"* |

Bên trái là lời khen xã giao — bỏ. Bên phải là lời nói **lúc đang cố làm việc**,
nhìn vào biết ngay họ vướng ở đâu.

## Ba thứ nhóm đang muốn biết nhất

Ghi riêng nếu thấy, vì đây là ba chỗ thiết kế còn cãi nhau được:

1. **Cá nhân hoá có bị hiểu nhầm không** — người thử có nhận ra câu trả lời của mình
   khác của bạn bên cạnh không, và họ thấy thế là đúng hay thấy là thiếu?
2. **Cho phép lặp có phiền không** — hỏi lần hai thì mốc cũ hiện lại. Họ thấy yên tâm
   hay thấy thừa? (spec §4 non-goal 3 — nếu họ thấy phiền thì thiết kế này phải cãi lại được)
3. **Nhãn "cần xác nhận"** có làm họ đi kiểm tin gốc không, hay bị lướt qua?

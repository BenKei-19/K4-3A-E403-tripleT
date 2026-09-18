# Reflection — Nguyễn Quang Huy

**Mã học viên:** `2A202602421` · **Phần việc:** Bot Discord · quét theo quyền kênh · trả lời riêng · server test


## 1 · Phần mình làm

Mô tả bằng lời của mình — file nào, hàm nào, quyết định gì là của mình.

> Mình chịu trách nhiệm chính về toàn bộ **Ứng dụng Bot Discord & Hạ tầng thử nghiệm thực tế** trong file `codebase/bot.py` và script nạp dữ liệu `codebase/do-tin-vao-kenh.py`:
> - **Xử lý sự kiện tin nhắn (`on_message`):** Lắng nghe tin nhắn trên server lớp, bắt đúng cả 2 trường hợp người dùng tag user bot (`<@id>`) hoặc tag role bot (`<@&id>`) do Discord tự động tạo ra.
> - **Thuật toán quét tin theo quyền cá nhân (`_quet_kenh_cua_nguoi()`):** Quét qua tối đa 25 kênh văn bản, kiểm tra chéo đồng thời hai quyền `permissions_for(người hỏi)` và `permissions_for(bot)` (`read_messages` và `read_message_history`) trong phạm vi `SO_NGAY` ngày gần nhất. Tuyệt đối không đọc kênh mà người hỏi không có quyền xem.
> - **Thiết kế giao diện tin nhắn riêng & Embed (`_dung_embed()`):** Xây dựng format danh sách mốc thời gian, tự động chia nhỏ thành các khối 10 mục/embed để không vượt ngưỡng trần 25 field của Discord. Đổi màu viền cam khi có DEADLINE, xanh lá khi chỉ có ANNOUNCE. Gắn hyperlink trỏ thẳng về tin nhắn gốc kèm tên kênh và ngày giờ đăng.
> - **Cổng lọc ý định bằng code thuần (`_hoi_dung_viec()`, `_embed_ngoai_pham_vi()`):** Dùng regex bắt các từ khóa nghiệp vụ. Nếu học viên tag bot hỏi chuyện ngoài phạm vi (nhờ code hộ, hỏi quy định chung), bot từ chối lịch sự và hướng dẫn hỏi TA chứ không đổ danh sách mốc ra bừa bãi.
> - **Cơ chế phản hồi của người dùng (`NutBaoSai`):** Tạo nút bấm "🚩 Có mục sai" dưới embed, ghi nhận log người bấm và mã tin vào file `eval/phan-hoi.log`.
> - **Hạ tầng Server Test & Webhook (`do-tin-vao-kenh.py`):** Giả lập đổ 515 tin nhắn từ CSV vào server Discord test của nhóm, bảo toàn mốc ngày và giờ gốc trong nickname hiển thị (`D#### · YYYY-MM-DD HH:MM`) để phục vụ demo trực tiếp.

## 2 · Một chỗ mình làm sai rồi sửa

Không phải "em học được nhiều". Một lỗi cụ thể: lúc đó nghĩ gì, sai thế nào,
biết là sai nhờ đâu, sửa ra sao.

> **Lỗi chỉ kiểm tra `client.user in tin_nhan.mentions` khiến bot "câm nín" khi người dùng tag:**
> - **Lúc đó nghĩ gì:** Khi viết code ban đầu cho sự kiện `on_message`, mình viết điều kiện nhận diện đơn giản là: `if client.user in tin_nhan.mentions:`. Mình nghĩ rằng khi người dùng gõ `@Trợ Lý Kute` trong kênh chat thì Discord sẽ luôn chuyển thành một mention trỏ đến đối tượng bot.
> - **Sai thế nào:** Khi tích hợp bot vào server Discord test của nhóm, Discord tự động sinh ra một Managed Role có cùng tên với bot là `"Trợ Lý Kute"`. Khi người dùng gõ `@Trợ Lý` và bấm Enter hoặc Tab theo gợi ý tự động của Discord, Discord lại chèn thẻ Role Mention (`<@&role_id>`) thay vì User Mention (`<@user_id>`). Vì chuỗi là role mention nên thuộc tính `tin_nhan.mentions` hoàn toàn trống rỗng (`client.user in tin_nhan.mentions` trả về `False`). Hậu quả là bot hoàn toàn không có bất kỳ phản hồi nào, trông như bot bị crash hoặc ngắt kết nối!
> - **Biết là sai nhờ đâu:** Chiều 17/09 (~14:30), khi mình và Hiếu bắt đầu kịch bản thử nghiệm trên server test, gõ tag bot liên tục 5 lần giữa kênh mà bot vẫn trơ ra dù terminal báo bot online bình thường. Mình in đối tượng `tin_nhan` ra console mới phát hiện `role_mentions` có dữ liệu còn `mentions` thì rỗng.
> - **Sửa ra sao:** Mình sửa ngay điều kiện nhận diện ở dòng 241–245 của `codebase/bot.py`:
>   ```python
>   vai_cua_bot = tin_nhan.guild.self_role
>   duoc_goi = (client.user in tin_nhan.mentions) or (
>       vai_cua_bot is not None and vai_cua_bot in tin_nhan.role_mentions
>   )
>   ```
>   Sau khi sửa, dù người dùng bấm gợi ý của Discord theo thẻ role hay thẻ user cá nhân, bot đều nhận diện chuẩn xác 100% và phản hồi ngay lập tức.

## 3 · Ba câu giám khảo nhiều khả năng hỏi mình

**a. "Cá nhân hoá của các bạn chặn rò rỉ bằng cách nào?"**
*(`permissions_for(người hỏi)` VÀ `permissions_for(bot)` — vì sao dựa vào quyền Discord
chứ không dựa vào prompt, và điều đó khác nhau chỗ nào về mức độ tin được)*

> - **Cơ chế chặn rò rỉ (Chặn ngay từ tầng lấy dữ liệu của Discord API):**
>   Trong hàm `_quet_kenh_cua_nguoi()`, bot duyệt qua từng kênh và kiểm tra song song 2 lớp quyền hạn:
>   ```python
>   quyen_nguoi = kenh.permissions_for(nguoi)
>   quyen_bot = kenh.permissions_for(nguoi.guild.me)
>   if not (quyen_nguoi.read_messages and quyen_nguoi.read_message_history):
>       continue
>   if not (quyen_bot.read_messages and quyen_bot.read_message_history):
>       continue
>   ```
>   Nếu người hỏi không có quyền xem kênh đó (ví dụ kênh kín của ban tổ chức hoặc kênh riêng của một nhóm khác), bot bỏ qua kênh đó ngay từ đầu, không đọc một tin nhắn nào.
> - **Vì sao dựa vào quyền Discord chứ không dựa vào prompt:**
>   - *Dựa vào prompt:* Gom toàn bộ tin nhắn cả server rồi dặn model *"hãy lọc ra tin mà bạn A được xem"*. Cách này cực kỳ nguy hiểm vì model có thể bị hallucinate hoặc bị prompt injection lừa để lộ tin nhắn bí mật của kênh khác. Mức độ tin cậy mang tính xác suất, không thể chấp nhận được trong bảo mật.
>   - *Dựa vào quyền Discord:* Bảng phân quyền (ACL) của Discord được thực thi ở tầng socket máy chủ Discord bằng mã hoá. Dữ liệu nạp vào AI chỉ là những tin mà chính người hỏi đã có quyền nhìn thấy trên màn hình Discord của họ. Mức độ tin cậy là tuyệt đối (100%), hoàn toàn loại bỏ nguy cơ rò rỉ chéo giữa các đội thi.

**b. "Vì sao trả lời bằng tin nhắn riêng, mà không hiện luôn tại chỗ?"**
*(tin nhắn riêng giữ lại đọc sau được, hợp với thói quen tag bot sẵn có · đổi lại
phải xử lý khi người dùng chặn tin nhắn riêng · và vì sao nhóm bỏ hẳn lệnh gạch chéo
ngày 18/09 thay vì giữ cả hai)*

> - **Vì sao trả lời bằng tin nhắn riêng (DM):**
>   1. *Cứu kênh lớp khỏi ngập lụt:* Số liệu khai thác trên server K4-L3-4 cho thấy bot đang chiếm 48% số tin và **88% tổng số chữ** của kênh đông nhất. Mỗi câu trả lời bot xả ra kênh chung dài trung bình 486 ký tự, đẩy trôi mất 6 tin nhắn thảo luận của học viên. Trả lời qua DM giữ cho kênh lớp luôn sạch sẽ.
>   2. *Tạo to-do list cá nhân tiện lợi:* Tin nhắn DM không bị trôi theo dòng chat của lớp, học viên có thể ghim lại hoặc mở ra tra cứu bất kỳ lúc nào trên điện thoại.
>   3. Trong kênh lớp, bot chỉ gửi một dòng: *"Mình đã nhắn riêng cho bạn rồi nhé."* và dùng `delete_after=30` để dòng này tự động biến mất sau 30 giây.
> - **Xử lý khi người dùng chặn DM:** Nếu người dùng tắt tính năng nhận DM từ server, hàm `_gui_rieng()` sẽ bắt ngoại lệ `discord.Forbidden` và gửi thông báo trực tiếp trong kênh: hướng dẫn người dùng chuột phải vào tên Server -> Privacy Settings -> bật Direct Messages.
> - **Vì sao bỏ hẳn lệnh gạch chéo (`/luuy`) sáng 18/09:** Thống kê pack thật cho thấy 307/779 tin (39%) của học viên là thói quen tag bot trực tiếp. Nếu duy trì cả lệnh `/luuy` lẫn tag bot, người dùng sẽ bị phân vân không biết dùng cái nào, và nhóm phải duy trì gấp đôi số test case. Nhóm quyết định tinh gọn thành một cách dùng duy nhất là tag bot để mang lại trải nghiệm trực quan và nhất quán nhất.

**c. "Vì sao phải `defer` trước khi gọi AI?"**
*(Discord huỷ lượt tương tác sau 3 giây — kể lại lúc gặp lỗi này thì mới thuyết phục)*

> - **Quy luật 3 giây của Discord API:** Trong cơ chế Interaction (hoặc Slash Command) của Discord, một khi người dùng kích hoạt lệnh, con bot bắt buộc phải gửi phản hồi xác nhận (Acknowledge) về Discord Gateway trong vòng **tối đa 3 giây**. Nếu sau 3 giây bot vẫn im lặng, Discord sẽ lập tức đóng phiên tương tác và in ra dòng chữ đỏ lỗi: *"The interaction failed"* (Tương tác thất bại).
> - **Lúc gặp lỗi này trong thực tế:** Ở giai đoạn đầu khi thử nghiệm gọi API trực tiếp với Gemini, việc quét qua 515 tin nhắn của 3 ngày và chờ mô hình suy luận thường mất từ **4 đến 8 giây**. Lúc bấm lệnh trên Discord, bot cứ chạy được 3 giây là Discord báo lỗi đỏ `interaction failed`, trong khi ở terminal vài giây sau AI mới trả về kết quả!
> - **Khắc phục:** Khi chuyển sang luồng `on_message` tag bot, mình sử dụng context manager `async with tin_nhan.channel.typing():` trước khi thực hiện hàm `_quet_kenh_cua_nguoi()` và `digest()`. Lệnh này vừa liên tục gửi tín hiệu "bot đang gõ..." để giữ kết nối với Discord gateway không bị timeout, vừa tạo cảm giác chân thực cho người dùng rằng Trợ Lý đang đọc và xử lý tin nhắn.

---

## 4 · Một chỗ mình còn chưa chắc

Thứ mình làm mà nếu giám khảo hỏi sâu thì mình sẽ lúng túng. Viết ra đây để
trước buổi pitch còn kịp đọc lại.

> **Khả năng chịu tải và giới hạn Rate Limit của Discord API khi nhiều người hỏi cùng lúc:**
> - Hiện tại trong hàm `_quet_kenh_cua_nguoi()`, bot duyệt lịch sử bằng vòng lặp `async for m in kenh.history(limit=300, after=tu_luc)`.
> - Nếu vào giờ cao điểm trước giờ nộp bài có khoảng 10 đến 15 bạn học viên cùng tag bot trong vòng 1 phút, việc bot liên tục gửi hàng chục request `channel.history` qua HTTP API tới Discord có thể kích hoạt cơ chế Rate Limit toàn cục (HTTP 429) của Discord, khiến bot bị đình chỉ tạm thời từ vài giây đến vài phút.
> - Hiện tại nhóm chưa dựng hàng đợi Message Queue (như Celery hay Redis) hay cơ chế pooling/cache lịch sử kênh giữa các học viên có cùng quyền đọc kênh. Nếu giám khảo hỏi: *"Nếu mở cho toàn trường 1.000 sinh viên dùng thì bot xử lý bottleneck này thế nào?"*, mình sẽ phải thẳng thắn thừa nhận đây là giới hạn kiến trúc của phiên bản MVP hiện tại.

## 5 · Nếu làm lại từ đầu

Một quyết định mình sẽ làm khác, và vì sao.

> **Mình sẽ xây dựng một bộ nhớ đệm tin nhắn cục bộ (Local SQLite Message Cache) theo thời gian thực thay vì quét ngược lịch sử qua Discord API mỗi lần được hỏi:**
> - Hiện tại mỗi lần học viên tag bot, bot lại phải gọi `kenh.history()` để kéo hàng trăm tin nhắn qua internet về máy, vừa tốn băng thông, vừa chậm mất 3-4 giây, lại tiềm ẩn nguy cơ chạm trần rate limit của Discord.
> - Nếu làm lại từ đầu, mình sẽ tận dụng sự kiện `on_message` để bot tự động lưu mọi tin nhắn mới phát sinh trong server vào một database SQLite local. Khi học viên hỏi, bot chỉ cần chạy một câu lệnh SQL query theo quyền kênh và mốc thời gian mất chưa tới 5 mili-giây. Điều này sẽ giúp thời gian phản hồi của bot giảm từ 8 giây xuống chỉ còn 2-3 giây, nâng tầm trải nghiệm mượt mà hơn rất nhiều.

---

*Luật vibe-coding của khoá: dùng AI để build thoải mái, nhưng **không giải thích được
phần có tên mình thì phần đó 0 điểm** — giám khảo hỏi bất kỳ thành viên nào khi thuyết
trình. File này là chỗ chuẩn bị cho đúng câu hỏi đó.*

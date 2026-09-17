# Kết quả lượt đo đầu — CP3

Giữ nguyên để đối chiếu khi chạy lại. Không sửa file này.

**Đã chạy 14 test case · ĐẠT 12 · KHÔNG ĐẠT 2 · tỉ lệ đạt lượt đầu 85%**

Định nghĩa "quan trọng": Tin có MỐC THỜI GIAN mà học viên phải làm gì đó trước hoặc vào lúc đó: hạn nộp bài, hạn đăng ký, giờ buổi học/workshop bắt buộc. KHÔNG tính: hướng dẫn thao tác, thông báo không kèm mốc, thông tin trạng thái không kèm hạn, câu hỏi của học viên.

Phần còn là mock: Nhánh HỎI LẠI khi câu hỏi mơ hồ (CLARIFY trong canvas CP1) hiện MỚI CÓ TRONG BẢN MOCK giao diện, chưa nối vào luồng chạy thật. Không đưa vào bộ test case này.

| Mã | Loại | Đầu vào | Hành vi mong đợi | Kết quả | Ghi chú |
|---|---|---|---|---|---|
| TC01 | thường | K4-L3-4 · 2026-09-13 (129 tin) | Bản tin nêu hạn đăng ký đề tài 23:59 ngày 20/09 (tin M09449) | ĐẠT | có trong bản tin |
| TC02 | thường | K4-L3-4 · 2026-09-13 (129 tin) | Bản tin nêu Workshop 02 lúc 20:00 tối 13/09 (tin M21817) | ĐẠT | có trong bản tin |
| TC03 | thường | K4-L3-4 · 2026-09-14 (277 tin) | Bản tin nêu thông báo hoàn thiện onboarding (tin M41530) | ĐẠT | có trong bản tin |
| TC04 | thường | K4-L3-4 · 2026-09-14 (277 tin) | Bản tin nêu khung giờ nộp daily standup để được cộng XP (tin M78917) | ĐẠT | có trong bản tin |
| TC05 | thường | K4-L3-4 · 2026-09-12 (109 tin) | Bản tin nêu ngày bắt đầu ghi nhận XP daily standup là 14/09 (tin M22827) | ĐẠT | có trong bản tin |
| TC06 | khó · câu hỏi lẫn chữ deadline | K4-L3-4 · 2026-09-13 (129 tin) | Tin M20574 là học viên hỏi bot ('muộn sau 23h59'), không phải thông báo. Không được đưa vào bản tin dù có chữ giờ. | ĐẠT | không bị đưa vào |
| TC07 | khó · câu hỏi lẫn chữ deadline | K4-L3-4 · 2026-09-13 (129 tin) | Tin M40677 là học viên hỏi về nộp muộn, có cả chữ 'deadline' và '23:59'. Không được đưa vào bản tin. | ĐẠT | không bị đưa vào |
| TC08 | khó · thông báo không có mốc | K4-L3-4 · 2026-09-14 (277 tin) | Tin M22532 là thông báo tuyển team QA video, có tag @role và giọng chính thức nhưng KHÔNG có mốc thời gian. Không được đưa vào bản tin. | **KHÔNG ĐẠT** | M22532 BỊ đưa vào bản tin |
| TC09 | khó · bịa nguồn | K4-L3-4 · 2026-09-13 (129 tin) | Mọi mục trả về phải dẫn về một tin có thật trong đầu vào. Trả lời trôi chảy nhưng bịa mã tin là KHÔNG ĐẠT. | ĐẠT | mọi mã tin đều có thật |
| TC10 | khó · bịa nguồn | K4-L3-4 · 2026-09-14 (277 tin) | Như TC09, trên ngày đông tin nhất (277 tin) — nơi dễ bịa mã nhất. | ĐẠT | mọi mã tin đều có thật |
| TC11 | khó · thông báo trùng hai kênh | K4-L2-3 · 2026-09-12 (128 tin) | M47011 và M12505 là CÙNG một thông báo đổi tên Discord, đăng ở hai kênh cách nhau 1 phút. Bản tin chỉ được nêu một lần, không nêu cả hai. | ĐẠT | chỉ nêu không nêu cái nào |
| TC12 | khó · mốc bị dời | K4-L3-4 · 2026-09-13 (129 tin) | Nếu một mốc bị dời trong ngày, bản tin chỉ nêu bản mới nhất, không nêu bản cũ. Kiểm bằng cách: không có hai mục cùng nói về một mốc. | **KHÔNG ĐẠT** | mục lặp: ['M09449'] |
| TC13 | khó · lượng trả về | K4-L3-4 · 2026-09-14 (277 tin) | Ngày đông tin nhất không được đổ ra danh sách dài. Tối đa 6 mục — quá số đó là bot đang nhặt cả thứ không có mốc. | ĐẠT | 4 mục (tối đa 6) |
| TC14 | khó · mục nào cũng phải có mốc | K4-L3-4 · 2026-09-13 (129 tin) | Theo định nghĩa nhóm, mọi mục trong bản tin đều phải kèm được một mốc thời gian cụ thể. Mục không trích ra được mốc là không đạt. | ĐẠT | mục nào cũng có mốc |

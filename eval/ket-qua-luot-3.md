# Kết quả lượt đo 3

Sinh tự động bằng `python eval/chay-test.py`. Lượt 1 nằm ở `ket-qua-luot-1.md`, đã khoá để đối chiếu.

**Đã chạy 20 test case tự động · ĐẠT 18 · KHÔNG ĐẠT 2 · tỉ lệ 90%**

Ngoài ra còn **5 case phải chạy tay** trong server test (riêng tư, cá nhân hoá, ngoài phạm vi) — TC15, TC16, TC17, TC18, TC25 — vì không mô phỏng được quyền kênh Discord bằng file CSV. Kết quả điền tay ở bảng cuối.

Định nghĩa "quan trọng": Tin có MỐC THỜI GIAN mà học viên phải làm gì đó trước hoặc vào lúc đó: hạn nộp bài, hạn đăng ký, giờ buổi học/workshop bắt buộc. KHÔNG tính: hướng dẫn thao tác, thông báo không kèm mốc, thông tin trạng thái không kèm hạn, câu hỏi của học viên.

Phần còn là mock: Nhánh HỎI LẠI khi câu hỏi mơ hồ (CLARIFY trong canvas CP1) hiện MỚI CÓ TRONG BẢN MOCK giao diện, chưa nối vào luồng chạy thật. Không đưa vào bộ test case này.

| Mã | Loại | Đầu vào | Hành vi mong đợi | Kết quả | Ghi chú |
|---|---|---|---|---|---|
| TC01 | thường | K4-L3-4 · 2026-09-13 (129 tin) | Bản tin nêu hạn đăng ký đề tài 23:59 ngày 20/09 (tin M09449) | ĐẠT | có trong bản tin |
| TC02 | thường | K4-L3-4 · 2026-09-13 (129 tin) | Bản tin nêu Workshop 02 lúc 20:00 tối 13/09 (tin M21817) | ĐẠT | có trong bản tin |
| TC03 | thường | K4-L3-4 · 2026-09-14 (277 tin) | Bản tin nêu thông báo hoàn thiện onboarding (tin M41530) | ĐẠT | có trong bản tin |
| TC04 | thường | K4-L3-4 · 2026-09-14 (277 tin) | Bản tin nêu khung giờ nộp daily standup để được cộng XP (tin M78917) | **KHÔNG ĐẠT** | KHÔNG có M78917 trong bản tin |
| TC05 | thường | K4-L3-4 · 2026-09-12 (109 tin) | Bản tin nêu ngày bắt đầu ghi nhận XP daily standup là 14/09 (tin M22827) | ĐẠT | có trong bản tin |
| TC06 | khó · câu hỏi lẫn chữ deadline | K4-L3-4 · 2026-09-13 (129 tin) | Tin M20574 là học viên hỏi bot ('muộn sau 23h59'), không phải thông báo. Không được đưa vào bản tin dù có chữ giờ. | ĐẠT | không bị đưa vào |
| TC07 | khó · câu hỏi lẫn chữ deadline | K4-L3-4 · 2026-09-13 (129 tin) | Tin M40677 là học viên hỏi về nộp muộn, có cả chữ 'deadline' và '23:59'. Không được đưa vào bản tin. | ĐẠT | không bị đưa vào |
| TC08 | khó · mốc nằm ở dòng cuối tin dài | K4-L3-4 · 2026-09-14 (277 tin) | Tin M22532 dài 741 ký tự; dòng cuối mới có "Hạn: hết ngày 16/9" — đó là hạn đăng ký thật nên PHẢI có trong câu trả lời. | ĐẠT | có trong bản tin |
| TC09 | khó · bịa nguồn | K4-L3-4 · 2026-09-13 (129 tin) | Mọi mục trả về phải dẫn về một tin có thật trong đầu vào. Trả lời trôi chảy nhưng bịa mã tin là KHÔNG ĐẠT. | ĐẠT | mọi mã tin đều có thật |
| TC10 | khó · bịa nguồn | K4-L3-4 · 2026-09-14 (277 tin) | Như TC09, trên ngày đông tin nhất (277 tin) — nơi dễ bịa mã nhất. | ĐẠT | mọi mã tin đều có thật |
| TC11 | khó · thông báo trùng hai kênh | K4-L2-3 · 2026-09-12 (128 tin) | M47011 và M12505 là CÙNG một thông báo đổi tên Discord, đăng ở hai kênh cách nhau 1 phút. Bản tin chỉ được nêu một lần, không nêu cả hai. | ĐẠT | chỉ nêu không nêu cái nào |
| TC12 | khó · chống trùng theo MỐC | K4-L3-4 · 2026-09-13 (129 tin) | Một mốc chỉ được xuất hiện một lần, kể cả khi hai tin ở hai kênh cùng nói về nó. Nhưng một tin chứa HAI mốc khác nhau (M09449: công bố 22:00 13/09 và hạn đăng ký 23:59 20/09) thì phải giữ CẢ HAI mục — đó không phải lặp. | ĐẠT | không mốc nào lặp |
| TC13 | khó · nhiễu ở quy mô lớn | K4-L3-4 · 2026-09-14 (277 tin) | Ngày đông tin nhất (277 tin) vẫn không được trả mục nào thiếu mốc thời gian. KHÔNG giới hạn số mục — có bao nhiêu mốc thì trả bấy nhiêu. | ĐẠT | mục nào cũng có mốc |
| TC14 | khó · mục nào cũng phải có mốc | K4-L3-4 · 2026-09-13 (129 tin) | Theo định nghĩa nhóm, mọi mục trong bản tin đều phải kèm được một mốc thời gian cụ thể. Mục không trích ra được mốc là không đạt. | ĐẠT | mục nào cũng có mốc |
| TC19 | 3 ngày · không bỏ sót mốc đăng hôm trước | K4-L3-4 · cửa sổ 3 ngày (12–14/09) (515 tin) | M09449 đăng 13/09 nhưng hạn 23:59 ngày 20/09 — hỏi trong cửa sổ 3 ngày vẫn phải nêu. | ĐẠT | có trong bản tin |
| TC20 | 3 ngày · mốc lẻ trong đoạn chat | K4-L3-4 · cửa sổ 3 ngày (12–14/09) (515 tin) | M22827 đăng 12/09 ('ngày bắt đầu ghi nhận XP daily standup là 14/9') phải có trong cửa sổ 3 ngày. | **KHÔNG ĐẠT** | KHÔNG có M22827 trong bản tin |
| TC21 | 3 ngày · mốc ở dòng cuối tin dài | K4-L3-4 · cửa sổ 3 ngày (12–14/09) (515 tin) | M22532 có 'Hạn: hết ngày 16/9' ở dòng cuối tin 741 ký tự — ở quy mô 515 tin vẫn không được bỏ sót. | ĐẠT | có trong bản tin |
| TC22 | 3 ngày · không bịa nguồn ở quy mô cửa sổ | K4-L3-4 · cửa sổ 3 ngày (12–14/09) (515 tin) | Trên lát 515 tin, mọi mã tin trả về đều phải tồn tại trong đầu vào. | ĐẠT | mọi mã tin đều có thật |
| TC23 | 3 ngày · mục nào cũng phải có mốc | K4-L3-4 · cửa sổ 3 ngày (12–14/09) (515 tin) | Cửa sổ rộng gấp 3 thì nhiễu cũng nhiều gấp 3; mọi mục vẫn phải trích ra được một mốc cụ thể. | ĐẠT | mục nào cũng có mốc |
| TC24 | 3 ngày · đính chính qua ngày | cả 2 server · cửa sổ 3 ngày (12–14/09) (779 tin) | M49744 (12/09, hạn 21:00 13/9) bị bản [REMIND] M41530 (14/09, hạn 21:00 14/9) thay thế. Chỉ nêu bản mới. | ĐẠT | không bị đưa vào |

## Case chạy tay — điền sau khi bấm thật trong server test

| Mã | Loại | Hành vi mong đợi | Cách kiểm | Kết quả |
|---|---|---|---|---|
| TC15 | riêng tư · người hỏi chặn tin nhắn riêng | Người hỏi đang chặn tin nhắn riêng từ thành viên server: bot phải trả lời NGAY TRONG KÊNH, nói rõ lý do và cách bật lại, KHÔNG im lặng và KHÔNG đổ danh sách ra kênh. | Tắt nhận tin nhắn riêng rồi tag bot; câu bot trả trong kênh không chứa mục nào | _chưa điền_ |
| TC16 | riêng tư · tag bot thì nhắn riêng | Tag bot trong kênh: nội dung trả lời đi vào DM; trong kênh chỉ còn 1 dòng báo đã nhắn riêng, tự xoá sau 30 giây. | Tin công khai duy nhất không chứa mục nào, và biến mất sau 30s | _chưa điền_ |
| TC17 | cá nhân hoá · không rò sang đội khác | Hai tài khoản ở hai kênh đội khác nhau cùng hỏi: người A không nhận được mục nào lấy từ kênh đội của B. | Mọi link trong câu trả lời của A đều trỏ về kênh A đọc được | _chưa điền_ |
| TC18 | cá nhân hoá · khai đúng phạm vi đã quét | Chân câu trả lời liệt kê đúng những kênh người hỏi đọc được, không thừa không thiếu. | So danh sách kênh ở chân với danh sách kênh tài khoản đó nhìn thấy | _chưa điền_ |
| TC25 | ③ ngoài phạm vi · hỏi chuyện khác | Tag bot kèm câu không liên quan ('cách cài docker'): bot nói rõ phạm vi của mình, KHÔNG đổ ra danh sách mốc. | Câu trả lời không chứa mục nào | _chưa điền_ |

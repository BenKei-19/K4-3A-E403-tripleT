# Reflection — Nguyễn Thị Minh Khánh

**Mã học viên:** `2A202602546` · **Phần việc:** Evidence · golden set · bộ test case · đo và phân tích lỗi

## 1 · Phần mình làm

Mô tả bằng lời của mình — file nào, hàm nào, quyết định gì là của mình.

> Mình chịu trách nhiệm chính về phần **Evidence và Đánh giá (Evaluation)** của dự án:
> - **Viết script đo lường:** File `eval/eval.py` (hàm `main()`), trực tiếp tính toán 4 chỉ số cốt lõi: số mốc vàng, bắt đúng, bỏ sót, nhiễu và link sai (`tong_link_sai`).
> - **Xây dựng bộ test case và golden set:** Quản lý file `eval/golden-set.json` và bộ 25 test case trong `eval/test-cases.json` (20 case chạy tự động qua `eval/chay-test.py`, 5 case chạy thực nghiệm bằng tay).
> - **Dán nhãn dữ liệu:** Cùng Huy dùng script `eval/phieu-cham.py` để dán nhãn thủ công trên dữ liệu thật `k4_messages.csv`. Mình trực tiếp dán 3 lát ngày của server `K4-L3-4` (ngày 12, 13, 14/09) với 515 tin nhắn, và dán chéo kiểm tra 1 lát của Huy (`K4-L2-3`).
> - **Quyết định đo đạc then chốt:** Đề xuất bổ sung lát cắt **"cửa sổ 3 ngày"** (515 tin, tổng hợp đáp án 3 ngày) vào `golden-set.json` để đo đúng phạm vi hoạt động thực tế của sản phẩm thay vì chỉ đo từng ngày riêng lẻ.

## 2 · Một chỗ mình làm sai rồi sửa

Không phải "em học được nhiều". Một lỗi cụ thể: lúc đó nghĩ gì, sai thế nào,
biết là sai nhờ đâu, sửa ra sao.

> **Lỗi viết điều kiện chống trùng lặp trong test case TC12:**
> - **Lúc đó nghĩ gì:** Khi viết điều kiện cho TC12 trong `eval/test-cases.json`, mình nghĩ đơn giản rằng "trong một câu trả lời, mỗi tin nhắn gốc chỉ được trích xuất tối đa một lần", nên mình code điều kiện bắt lỗi trùng lặp là kiểm tra danh sách `message_id` không được có phần tử trùng (`len(tra_ve) == len(set(tra_ve))`).
> - **Sai thế nào:** Ở lượt đo 1, bot trả về 2 mục đều trỏ về tin `M09449`, làm TC12 bị đánh rớt (ghi **KHÔNG ĐẠT**). Khi mở tin `M09449` ra đọc kỹ cùng Hải và Hiếu, mình mới nhận ra tin này thực chất chứa **hai sự kiện với hai mốc thời gian hoàn toàn khác nhau**: công bố ngân hàng đề tài (22:00 ngày 13/09) và hạn chót đăng ký đề tài (23:59 ngày 20/09). Bot tách thành 2 mục là hoàn toàn đúng và hữu ích cho học viên, còn điều kiện test của mình đã sai khi đồng nhất "trùng tin" với "trùng mốc".
> - **Sửa ra sao:** Mình sửa lại định nghĩa kiểm tra của TC12: **chống trùng theo mốc thời gian, không chống trùng theo mã tin gốc**. Một tin có thể sinh ra 2 mục nếu chứa 2 mốc độc lập. Nhóm giữ nguyên kết quả trượt của lượt 1 trong `ket-qua-luot-1.md` để trung thực, và áp dụng điều kiện sửa này từ lượt 2.

## 3 · Ba câu giám khảo nhiều khả năng hỏi mình

**a. "Golden set dán nhãn thế nào, ai dán, và chỗ nào hai người dán lệch nhau?"**

> - **Quy trình dán nhãn:** Để không bị ngợp trước 779 tin nhắn thật, nhóm dùng script `eval/phieu-cham.py --tao` để tự động lọc sơ bộ các tin ứng viên (tin có `@everyone`, `@here`, `@role` hoặc chứa regex mốc giờ/ngày). Sau đó mình và Huy mở file `phieu-cham.txt` đọc từng tin và đánh dấu `[x]` bằng tay: mình dán 3 lát của `K4-L3-4`, Huy dán 2 lát của `K4-L2-3`. Mỗi người dán thêm 1 lát chéo của người kia để đối chiếu.
> - **Chỗ hai người dán lệch nhau:** Ở tin `M47011` và `M12505` (thông báo nhắc đổi tên Discord hiển thị đúng cú pháp). Huy đánh dấu là QUAN TRỌNG vì thấy có tag `@everyone` và mang giọng điệu chính thức của ban tổ chức. Mình thì đánh dấu BỎ QUA vì bám sát định nghĩa: tin này chỉ hướng dẫn thao tác, không hề có mốc hạn chót (deadline) hay thời gian bắt buộc nào. Sau khi họp nhóm, nhóm thống nhất giữ nguyên lập luận của mình: không có mốc thời gian hành động thì dứt khoát không đưa vào bản tin, tránh làm loãng thông tin của học viên.

**b. "M22532 — kể lại chuyện nhãn vàng sai."**
*(tin dài 741 ký tự, hạn nằm ở dòng cuối, người dán chỉ đọc phần đầu. Bot đúng, nhãn sai.
Nhóm xử lý thế nào để không bị coi là sửa điểm cho đẹp?)*

> - **Sự cố nhãn vàng:** Tin `M22532` là bài đăng tuyển thành viên team QA video bài giảng, dài tới 741 ký tự. Khi dán nhãn thủ công cho TC08, mình đọc lướt 2/3 tin thấy toàn mô tả quyền lợi và công việc nên kết luận là "thông báo không có hạn" và gán nhãn mong đợi là *không được đưa vào*. Đến khi chạy lượt 1, bot lại đưa `M22532` vào bản tin, khiến TC08 bị tính là **KHÔNG ĐẠT**.
> - **Phát hiện bot đúng:** Khi mở lại tin gốc để mổ xẻ lỗi, mình ngỡ ngàng khi thấy ở dòng cuối cùng của tin có dòng: *"⏰ Hạn: hết ngày 16/9. Số lượng có hạn, bạn nào quan tâm điền sớm nhé!"*. Hóa ra bot đã đọc trọn vẹn đến ký tự cuối cùng và trích xuất đúng hạn đăng ký, trong khi chính người dán nhãn (là mình) đã mắc lỗi đọc sót vì tin quá dài.
> - **Cách xử lý minh bạch:** Để không mang tiếng "thấy bot sai thì sửa đề cho đẹp điểm":
>   1. Nhóm **khóa chặt file `eval/ket-qua-luot-1.md`**, giữ nguyên kết quả lượt đầu là 12/14 ĐẠT (85%), trong đó TC08 vẫn ghi nhận là KHÔNG ĐẠT.
>   2. Bổ sung ghi chú minh bạch `_sua_ngay_17_09` ngay trong `golden-set.json` và `test-cases.json` để giải trình rõ lý do.
>   3. Khi báo cáo kết quả lượt 2 (20/20 đạt), nhóm chủ động công khai cả 2 cách tính: nếu tính theo nhãn ban đầu thì lượt 2 là 18/20 (90%), còn tính theo nhãn đã đính chính thì là 20/20 (100%).

**c. "Mục nhiễu duy nhất của lượt 2 là gì, và nó dẫn tới sửa gì?"**
*(M01842, hạn tương đối có điều kiện, `do_chac` đúng 0.7 nên lọt qua luật `< 0.7`
→ đổi ngưỡng thành `<= 0.7`)*

> - **Mục nhiễu ở lượt 2:** Khi chạy `eval/eval.py` trên lát ngày 14/09 ở lượt 2, hệ thống phát hiện 1 mục nhiễu duy nhất là tin `M01842`: *"các bạn sẽ feedback trong 24 tiếng sau khi nhận video nhé"*.
> - **Nguyên nhân lọt lưới:** Đây là một mốc **tương đối và có điều kiện** (chỉ dành cho ai đã vào team QA, và thời điểm phụ thuộc vào lúc nhận video). Model Gemini đã đánh giá độ chắc chắn `do_chac` của tin này là **đúng 0.7**. Tuy nhiên, điều kiện trong code `digest.py` lúc đó lại là `if do_chac < 0.7: [cần xác nhận]`. Do `0.7 < 0.7` ra `False`, mục này đã lọt qua mà không bị gắn cờ cảnh báo, hiển thị như thể một deadline tuyệt đối.
> - **Cách khắc phục:** Mình đã phản ánh lại cho Hải để sửa biến `NGUONG_CAN_XAC_NHAN = 0.7` và đổi điều kiện so sánh thành `<= NGUONG_CAN_XAC_NHAN` (nhỏ hơn hoặc bằng 0.7). Nhờ đó, tin `M01842` không bị giấu đi hay loại bỏ, mà được hiển thị kèm nhãn `[cần xác nhận]` màu vàng để người dùng cảnh giác và bấm vào link tin gốc kiểm tra lại.

---

## 4 · Một chỗ mình còn chưa chắc

Thứ mình làm mà nếu giám khảo hỏi sâu thì mình sẽ lúng túng. Viết ra đây để
trước buổi pitch còn kịp đọc lại.

> **Độ bao phủ của golden set đối với các kênh ẩn và ngữ cảnh ngoài server lớp:**
> - Golden set hiện tại của nhóm được xây dựng tập trung trên dữ liệu thật của 2 server lớp (`K4-L3-4` và `K4-L2-3`). Dữ liệu này chủ yếu là tin nhắn tiếng Việt có văn phong chuẩn mực từ giảng viên và mentor.
> - Nếu giám khảo hỏi: *"Nếu học viên chat bằng tiếng Anh lóng, viết tắt không dấu, gửi deadline bằng ảnh chụp màn hình, hoặc các kênh dự án riêng có quy ước viết tắt đặc thù thì bộ test hiện tại đo được bao nhiêu %?"*, mình sẽ phải thừa nhận là bộ 25 test case hiện tại chưa bao phủ được trường hợp OCR hình ảnh hay ngôn ngữ pha trộn phức tạp.
> - Ngoài ra, 5 test case về bảo mật phân quyền (TC15–TC18, TC25) hiện vẫn phải bấm tay trực tiếp trên Discord chứ chưa được mock tự động hóa hoàn toàn trong CI/CD, nên tính ổn định khi mở rộng quy mô (scale) cần được kiểm chứng thêm.

## 5 · Nếu làm lại từ đầu

Một quyết định mình sẽ làm khác, và vì sao.

> **Mình sẽ thiết lập bộ tiêu chuẩn dán nhãn (Annotation Guidelines) có ví dụ đối chiếu và quy trình kiểm tra chéo (Double-blind annotation) ngay từ ngày đầu tiên:**
> - Lúc đầu nhóm dán nhãn theo cảm nhận cá nhân và định nghĩa bằng lời, dẫn đến việc mình đọc lướt bỏ sót dòng cuối ở tin `M22532` và Huy hiểu nhầm tin đổi tên Discord thành tin quan trọng.
> - Nếu làm lại, mình sẽ viết rõ checklist: *"bắt buộc đọc từ chữ đầu đến chữ cuối", "chỉ tính tin có mốc thời gian hành động"*, và cho hai người cùng dán nhãn độc lập 100% dữ liệu rồi tính độ tương đồng (Inter-annotator agreement - Cohen's Kappa). Những tin hai người chấm lệch nhau sẽ được đem ra biểu quyết trước khi chạy bất kỳ lượt đo nào. Điều này sẽ tiết kiệm cho nhóm nửa ngày rà soát và tránh hoàn toàn việc phải giải trình về sự cố sửa nhãn vàng sau lượt 1.

---

*Luật vibe-coding của khoá: dùng AI để build thoải mái, nhưng **không giải thích được
phần có tên mình thì phần đó 0 điểm** — giám khảo hỏi bất kỳ thành viên nào khi thuyết
trình. File này là chỗ chuẩn bị cho đúng câu hỏi đó.*

# Reflection — Phạm Minh Hiếu

**Mã học viên:** `2A202602919` · **Phần việc:** Đội trưởng · spec · chốt định nghĩa và quality bar · nộp mốc

## 1 · Phần mình làm

Mô tả bằng lời của mình — file nào, hàm nào, quyết định gì là của mình.

> Mình là Đội trưởng của nhóm tripleT, chịu trách nhiệm chính về định hướng sản phẩm, tài liệu kỹ thuật và điều phối chung:
> - **Chủ trì và trực tiếp viết toàn bộ `spec.md`:** Xây dựng đầy đủ từ §1 đến §9. Trực tiếp tổng hợp bằng chứng từ khảo sát người dùng Chuẩn A (n=12) và dữ liệu data mining Chuẩn B (1.092 tin của BTC).
> - **Quản trị Repo & Hướng dẫn (`README.md`, `huong-dan.md`):** Khởi tạo repo GitHub, thiết lập cấu trúc thư mục, quản lý checklist tiến độ bàn giao và kịch bản thuyết trình phân vai cho cả 4 thành viên.
> - **Các quyết định sản phẩm mang tính bước ngoặt:**
>   1. *Không làm bot mới, không làm bảng tin:* Chỉ tối ưu đúng 1 lượt tương tác có sẵn (học viên hỏi mốc quan trọng) để không làm xáo trộn thói quen của người dùng (39% tin của học viên là tag bot).
>   2. *Mở rộng cửa sổ từ 1 ngày lên 3 ngày:* Phát hiện 40% mốc còn hiệu lực được thông báo từ hôm trước.
>   3. *Chuyển từ trả lời công khai sang trả lời riêng (DM):* Dựa trên số liệu chứng minh bot đang chiếm 88% số chữ ở kênh đông nhất và làm loãng server nghiêm trọng.
>   4. *Thiết lập Quality Bar 3 vế:* Đặt ra lằn ranh đỏ về kỹ thuật và chất lượng cho toàn bộ dự án.

## 2 · Một chỗ mình làm sai rồi sửa

Không phải "em học được nhiều". Một lỗi cụ thể: lúc đó nghĩ gì, sai thế nào,
biết là sai nhờ đâu, sửa ra sao.

> **Lỗi áp đặt giới hạn cứng "Tối đa 6 mục" trong spec và prompt:**
> - **Lúc đó nghĩ gì:** Khi viết bản spec ban đầu ở CP2 và đầu CP3, mình rất sợ học viên bị "ngợp" thông tin khi đọc một bản tin quá dài, đồng thời sợ tin nhắn vượt quá giới hạn hiển thị của Discord. Vì vậy, mình tự ý đưa vào spec quy định: *"chỉ trả về tối đa 6 mục quan trọng nhất"* và yêu cầu Hải cấu hình prompt giới hạn cứng con số 6.
> - **Sai thế nào:** Đến chiều 17/09 (~15:30), khi kiểm tra thực tế dữ liệu 3 ngày của server `K4-L3-4` (515 tin nhắn), nhóm phát hiện có tới 8 mốc hạn nộp và sự kiện thật sự cần làm. Khi bot bị ép trần 6 mục, nó buộc phải tự ý cắt bỏ ngẫu nhiên 2 mốc hợp lệ. Mình bàng hoàng nhận ra: **Giới hạn số mục chính là một dạng cố tình tạo ra lỗi bỏ sót (false negative)**. Học viên tin tưởng hỏi bot để không bị sót deadline, mà bot lại giấu đi 2 deadline vì trần số lượng, có thể khiến học viên bị trượt môn hoặc mất điểm!
> - **Biết là sai nhờ đâu:** Khánh chạy bộ test case TC13 trên lát 3 ngày và báo lại rằng bot đã bỏ sót mốc đăng ký team QA và mốc XP standup chỉ vì chạm trần 6 mục.
> - **Sửa ra sao:** Mình lập tức họp nhóm lúc 15:30 ngày 17/09 để bỏ hoàn toàn quy tắc "tối đa 6 mục" trong spec (§9) và prompt. Thay vào đó, mình chỉ đạo Huy sửa `bot.py` để chia nhỏ câu trả lời thành nhiều Discord Embed (mỗi embed 10 mục) gửi riêng cho người dùng. Nguyên tắc mới là: **có bao nhiêu mốc thật thì trả về bấy nhiêu, không bao giờ tự ý cắt xén của người dùng**.

## 3 · Ba câu giám khảo nhiều khả năng hỏi mình

**a. "Định nghĩa QUAN TRỌNG của nhóm là gì, và vì sao siết lại còn mỗi mốc thời gian?"**
*(gợi ý bám vào: 17/09 ~13:00 trong §9 — cả nhóm cùng chấm 6 mục bot trả ra, 6 mục → 3 mục)*

> - **Định nghĩa chốt:** QUAN TRỌNG = Tin có **mốc thời gian** mà học viên phải làm gì đó trước hoặc vào lúc đó. Cụ thể chỉ gồm 3 loại: *Hạn nộp bài · Hạn đăng ký · Giờ diễn ra buổi học/workshop bắt buộc*. Mọi thông báo không kèm mốc thời gian hành động đều bị loại bỏ.
> - **Vì sao siết lại (bước ngoặt 13:00 ngày 17/09):**
>   - Ban đầu nhóm định nghĩa rộng hơn: gom cả hướng dẫn kỹ thuật (cách gõ lệnh, đổi tên Discord) và thông báo trạng thái (BTC đã mở cổng, danh sách đã duyệt).
>   - Lúc 13:00 ngày 17/09, khi chạy thử bản đầu tiên, bot trả ra 6 mục. Cả nhóm ngồi lại đọc từng mục và tranh luận nảy lửa: 3 mục là hướng dẫn đổi tên và nhắc nộp codelab. Mình đặt câu hỏi cho cả nhóm: *"Nếu học viên mở Discord lúc 23h đêm sau một ngày đi làm kiệt sức, điều gì nếu họ không biết thì sáng mai họ sẽ bị phạt hoặc trượt môn?"* Câu trả lời duy nhất là DEADLINE. Những tin hướng dẫn thao tác tuy hữu ích nhưng không mang tính sống còn khẩn cấp; đưa vào chỉ làm loãng danh sách và che khuất deadline.
>   - Cả nhóm đồng thuận gọt từ 6 mục xuống đúng 3 mục. Từ thời điểm đó, "không có mốc thời gian thì không trả về" trở thành kỷ luật sắt của dự án.

**b. "Quality bar chốt lúc nào, và vì sao hai vế sau lại là tuyệt đối?"**
*(≥80%, VÀ 0 mã tin bịa, VÀ 0 mục ngoài kênh người hỏi — vì sao hai lỗi đó không đổi
được bằng độ chính xác?)*

> - **Thời điểm chốt:** Chiều 17/09/2026, trước khi chạy bất kỳ lượt đo chính thức nào, và giữ nguyên không thay đổi sau đó.
> - **Nội dung Quality Bar:** `Đạt khi ≥ 80% số case trong golden set qua, VÀ không có bất kỳ mục nào dẫn về message_id không tồn tại, VÀ không có bất kỳ mục nào lấy từ kênh người hỏi không có quyền đọc.`
> - **Vì sao 2 vế sau là tuyệt đối (Zero-tolerance):**
>   - Tỉ lệ ≥80% trích xuất là ngưỡng có thể dung thứ trong xử lý ngôn ngữ tự nhiên vì tin chat thực tế rất đa dạng văn phong.
>   - Nhưng **mã tin bịa (hallucination / link chết)** là đòn chí mạng vào lòng tin: học viên bấm vào link thấy 404 hoặc nhảy sang một tin nhắn nhảm nhí, họ sẽ lập tức xóa bỏ niềm tin vào trợ lý ảo và quay về làm phiền TA.
>   - Còn **đưa nhầm mục ngoài kênh người hỏi đọc được (rò rỉ dữ liệu / permission leak)** là vi phạm đạo đức và quy tắc bảo mật nghiêm trọng: nếu học viên đội A nhìn thấy đề tài mật, hạn nội bộ hay trao đổi riêng của đội B, tính công bằng của cuộc thi sẽ sụp đổ.
>   - Hai lỗi này phá hủy hoàn toàn giá trị sản phẩm, nên dù model có đạt độ chính xác 99% mà dính 1 lỗi này thì toàn bộ hệ thống vẫn bị đánh RỚT ngay lập tức.

**c. "Lượt 2 đạt 100%, nhưng nhóm có sửa điều kiện chấm. Giải thích đi."**
*(TC08 và TC12 — vì sao đó là nhãn sai chứ không phải bot sai, và vì sao nhóm vẫn ghi
cả con số 18/20 theo điều kiện cũ)*

> - **Bản chất của việc sửa điều kiện chấm ở TC08 và TC12:**
>   - *Ở TC08:* Nhãn vàng ban đầu đánh dấu tin `M22532` là "không có mốc nên không được lấy". Nhưng khi rà soát lại, dòng cuối cùng của tin dài 741 ký tự này ghi rõ: *"⏰ Hạn: hết ngày 16/9"*. Người dán nhãn (Khánh) đọc lướt nên sót, còn bot đọc trọn vẹn và trích xuất đúng hạn đăng ký. Do đó, **bot đúng, nhãn vàng của con người sai**.
>   - *Ở TC12:* Điều kiện ban đầu cấm trùng lặp theo `message_id`. Tuy nhiên, tin `M09449` chứa hai sự kiện hoàn toàn độc lập (công bố đề tài 22:00 13/09 và hạn đăng ký 23:59 20/09). Việc bot tách thành 2 mục là chuẩn xác về nghiệp vụ. Điều kiện test ban đầu đã sai lầm khi đồng nhất "trùng tin" với "trùng mốc".
> - **Vì sao nhóm vẫn ghi nhận con số 18/20:**
>   - Để đảm bảo tính liêm chính học thuật tuyệt đối, nhóm **khóa cứng file `eval/ket-qua-luot-1.md`** và code `chay-test.py` chặn luôn việc ghi đè lên lượt 1. Con số của lượt 1 vĩnh viễn là **85%**.
>   - Khi báo cáo lượt 2, nhóm công khai cả 2 lăng kính: nếu tính theo bộ tiêu chí đã sửa chữa thì đạt **20/20 (100%)**, nhưng nếu chấm theo bộ tiêu chí cũ chưa sửa thì đạt **18/20 (90%)**. Nhóm không bao giờ giấu giếm hay làm đẹp số liệu trước ban giám khảo.

---

## 4 · Một chỗ mình còn chưa chắc

Thứ mình làm mà nếu giám khảo hỏi sâu thì mình sẽ lúng túng. Viết ra đây để
trước buổi pitch còn kịp đọc lại.

> **Đánh đổi khi bỏ hẳn Slash Command (`/luuy`) để chỉ giữ 1 cách dùng duy nhất:**
> - Sáng 18/09, mình quyết định bỏ hoàn toàn lệnh gạch chéo `/luuy` để người dùng chỉ có một hành vi duy nhất là tag `@Trợ Lý Kute`. Về mặt trải nghiệm, điều này giúp loại bỏ sự phân vân của học viên.
> - Tuy nhiên, nhược điểm chí mạng là: Nếu học viên **chặn tin nhắn riêng (DM)** từ thành viên server, bot không thể gửi DM được. Nếu còn Slash Command, bot có thể dùng cờ `ephemeral` (chỉ người gõ thấy ngay trong kênh) làm phương án dự phòng hoàn hảo. Khi bỏ Slash Command, bot buộc phải tag học viên trên kênh chung để nhắc bật lại DM chứ không thể hiển thị kết quả riêng tư được nữa.
> - Nếu giám khảo hỏi: *"Tại sao không giữ Slash Command làm fallback khi DM bị chặn?"*, mình sẽ phải thừa nhận đây là sự đánh đổi có phần vội vã để kịp tiến độ CP5, và là điểm yếu trải nghiệm mà nhóm cần khắc phục sau hackathon.

## 5 · Nếu làm lại từ đầu

Một quyết định mình sẽ làm khác, và vì sao.

> **Mình sẽ cho nhóm chạy script phân tích dữ liệu phân phối (Data Distribution Mining) ngay từ 2 giờ đầu tiên của cuộc thi thay vì ngồi họp chay thảo luận ý tưởng:**
> - Ở giai đoạn đầu, nhóm mình mất gần nửa ngày để tranh luận về các tính năng hào nhoáng như bot tự động tổng hợp tin mỗi sáng, hệ thống bảng tin tin tức, hay phân loại tin theo tag TA.
> - Mãi đến khi mình viết script quét file `k4_messages.csv` và bóc tách được các con số biết nói: **85% học viên chỉ ở đúng 1 kênh, 88% số chữ kênh chung do bot xả ra làm ngập kênh, và 40% mốc còn hạn được đăng từ hôm trước**, nhóm mới vỡ lẽ ra bài toán thực sự cần giải.
> - Nếu làm lại từ đầu, việc đầu tiên mình làm khi nhận đề là phân tích định lượng data pack ngay lập tức. Những con số thực tế sẽ định hình kiến trúc sản phẩm chuẩn xác hơn bất kỳ cuộc họp giả định nào, giúp nhóm tiết kiệm ít nhất 10 tiếng đồng hồ quý giá.

---

*Luật vibe-coding của khoá: dùng AI để build thoải mái, nhưng **không giải thích được
phần có tên mình thì phần đó 0 điểm** — giám khảo hỏi bất kỳ thành viên nào khi thuyết
trình. File này là chỗ chuẩn bị cho đúng câu hỏi đó.*

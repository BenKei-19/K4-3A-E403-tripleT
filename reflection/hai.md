# Reflection — Nguyễn Việt Hoàng Hải

**Mã học viên:** `2A202602967` · **Phần việc:** Hàm lõi digest.py · prompt · guardrail · chống trùng · xếp hạng


## 1 · Phần mình làm

Mô tả bằng lời của mình — file nào, hàm nào, quyết định gì là của mình.

> Mình chịu trách nhiệm chính về toàn bộ khối **Xử lý cốt lõi (Core Processing) & Trích xuất AI** trong file `codebase/digest.py` và runner `codebase/run.py`:
> - **Hàm điều phối trung tâm `digest()`:** Thiết kế luồng xử lý 4 chặng: (1) Gói toàn bộ tin trong cửa sổ vào một lời gọi AI duy nhất; (2) Tầng Guardrail code thuần kiểm tra tính có thật của `message_id`; (3) Loại bỏ các tin đã bị đính chính qua `thay_the_cho`; (4) Khử trùng lặp theo mốc thời gian và xếp hạng ưu tiên hoàn toàn bằng code.
> - **Thiết kế Prompt & Cấu trúc Schema (`SYSTEM`, `SCHEMA`, `_dung_prompt()`):** Định nghĩa chặt chẽ nguyên tắc chỉ trích xuất mốc hành động (deadline, lịch học), yêu cầu model đọc tới ký tự cuối cùng của tin dài, quy đổi các từ tương đối ("hôm nay", "sáng mai") thành ngày tuyệt đối dựa trên ngày đăng của tin, và cho phép 1 tin trả về nhiều mốc độc lập.
> - **Tích hợp Model & Caching (`goi_ai()`, `_goi_gemini()`, `_goi_claude()`):** Hỗ trợ linh hoạt cả 2 provider Gemini và Claude. Đặc biệt xây dựng cơ chế đệm kết quả vào `eval/dem-api/` băm theo SHA256 để không cạn quota 20 lượt/ngày của Gemini Free Tier trong suốt quá trình demo và test.
> - **Thuật toán Xếp hạng & Khử trùng (`_moc_tin()`, `_gon()`):** Xếp hạng ưu tiên DEADLINE trước ANNOUNCE, tin mới trước tin cũ tính theo mốc phút tuyệt đối từ năm 2000. Lọc trùng mốc dựa trên cặp khóa chuẩn hóa `(han_chot, tom_tat)`.
> - **Quyết định kiến trúc then chốt:** Triệt để tuân thủ nguyên lý **"AI phân loại, code quyết định"**. Model chỉ trích xuất dữ liệu thô, toàn bộ việc giữ, bỏ, xếp thứ tự và kiểm tra an toàn do code Python đảm nhiệm để đảm bảo tính tất định (deterministic).

## 2 · Một chỗ mình làm sai rồi sửa

Không phải "em học được nhiều". Một lỗi cụ thể: lúc đó nghĩ gì, sai thế nào,
biết là sai nhờ đâu, sửa ra sao.

> **Lỗi bỏ sót trường `ngay` trong `TinNhan` khi mở rộng cửa sổ từ 1 ngày lên 3 ngày:**
> - **Lúc đó nghĩ gì:** Ở giai đoạn đầu khi chỉ đo trên lát cắt 1 ngày, `TinNhan` chỉ cần trường `gio` dạng `"HH:MM"` là đủ để sắp xếp. Khi nhóm quyết định mở rộng phạm vi lên 3 ngày vào chiều 17/09, mình ban đầu chỉ gom thêm tin từ CSV vào mảng mà không nghĩ đến việc định dạng thời gian đã bị thiếu chiều kích ngày tháng.
> - **Sai thế nào:** Trong prompt gửi cho Gemini, mỗi dòng tin chỉ hiện `[id] 21:49 · author: nội dung`. Vì không có ngày đăng, khi gặp tin đăng từ ngày 12/09 có chữ "tối nay", model nhầm tưởng là tối ngày 14/09. Nghiêm trọng hơn, hàm sắp xếp lúc đó dùng `_phut(t.gio)` để so sánh số phút trong ngày: một tin đăng lúc 23:50 của ngày 12/09 có phút là 1430, lớn hơn tin đăng lúc 08:00 sáng ngày 14/09 (phút là 480). Hậu quả là tin cũ từ 2 ngày trước lại bị đẩy lên đầu bản tin, đè bẹp tin mới!
> - **Biết là sai nhờ đâu:** Chiều muộn 17/09 (~17:30), khi in thử prompt và kiểm tra thứ tự sắp xếp của lát 3 ngày cùng Hiếu, mình thấy các tin ngày 12 và ngày 14 nhảy lộn xộn, không theo thứ tự thời gian thực tế.
> - **Sửa ra sao:** Mình thêm ngay trường `ngay: str = ""` vào dataclass `TinNhan`. Trong `_tu_csv()` bóc tách thêm `created_at_vn[:10]`. Cập nhật `_dung_prompt()` để in rõ ngày trên từng dòng tin. Đồng thời viết lại hàm `_moc_tin()` quy đổi toàn bộ ngày + giờ ra số phút tuyệt đối tính từ mốc 2000-01-01 để code sort chính xác 100% dòng thời gian trải dài nhiều ngày.

## 3 · Ba câu giám khảo nhiều khả năng hỏi mình

**a. "Guardrail của các bạn chặn được cái gì, và chặn ở tầng nào?"**
*(mã tin không có thật → vứt mục; tin bị đính chính → bỏ bản cũ; trùng mốc → bỏ.
Vì sao để code làm chứ không dặn model?)*

> - **Các tầng chặn của Guardrail (100% ở tầng Code Python):**
>   1. *Chặn mã tin bịa:* Tạo từ điển `tra_cuu = {t.id: t for t in tin}` từ đầu vào. Bất kỳ mục nào AI trả về có `message_id` không tồn tại trong từ điển sẽ bị vứt ngay lập tức vào danh sách `bi_loai_vi_id_khong_co_that`. Kết quả: 0 link bịa qua 2 lượt đo.
>   2. *Chặn tin cũ đã bị đính chính:* Duyệt qua các mục có `thay_the_cho`, lập danh sách `bi_thay_the`, sau đó loại bỏ toàn bộ bản ghi cũ có `message_id` nằm trong danh sách này, chỉ giữ lại bản mới nhất.
>   3. *Chặn trùng lặp mốc:* Dùng hash set lưu khóa `(_gon(m.han_chot), _gon(m.tom_tat))`. Nếu mốc đã xuất hiện ở kênh khác hoặc tin khác thì bỏ qua.
> - **Vì sao để code làm chứ không dặn model:**
>   - Prompting chỉ mang tính xác suất (probabilistic). Dù có dặn dò kỹ đến đâu ("không được bịa", "không được lặp"), mô hình vẫn có thể hallucinate khi context dài hàng trăm tin nhắn.
>   - Code Python là tất định (deterministic). Khi có lỗi xảy ra, việc tách biệt ranh giới giúp nhóm định vị ngay: nếu mã tin sai là do model bịa (đã bị guardrail tóm), còn nếu mất tin là do logic lọc của code. Nhờ đó hệ thống đạt độ tin cậy tuyệt đối về mặt kỹ thuật.

**b. "Vì sao một tin được trả về hai mục?"**
*(M09449 chứa hai mốc khác nhau — và vì sao chống trùng phải theo mốc chứ không theo
`msg_id`)*

> - **Trường hợp điển hình `M09449`:** Tin nhắn này chứa 2 sự kiện với thời gian và tính chất tách biệt: (1) Công bố ngân hàng đề tài lúc 22:00 ngày 13/09 (ANNOUNCE), và (2) Hạn chót đăng ký đề tài lúc 23:59 ngày 20/09 (DEADLINE).
> - **Vì sao phải tách 2 mục:** Đối với học viên, đây là 2 đầu việc khác nhau cần lưu vào lịch. Nếu ép mỗi tin chỉ sinh ra 1 mục, hệ thống sẽ buộc phải vứt bỏ 1 trong 2 mốc quan trọng, gây ra lỗi sót thông tin nghiêm trọng.
> - **Chống trùng theo mốc, không theo `msg_id`:** Ở lượt đo 1, test case TC12 bắt lỗi trùng bằng cách đếm xem có `message_id` nào lặp lại không, dẫn đến việc đánh rớt trường hợp đúng đắn của `M09449`. Trong thực tế, tình trạng lặp thông tin trên Discord là do cùng một deadline được nhắc lại ở 2 kênh khác nhau (khác `msg_id` nhưng cùng nội dung). Do đó, thuật toán chống trùng đúng đắn phải gom cụm theo nội dung mốc `(han_chot, tom_tat)`, đồng thời cho phép một tin gốc chứa nhiều mốc được phân tách thành nhiều mục độc lập.

**c. "Cửa sổ 3 ngày mà prompt chỉ có `HH:MM` thì hỏng ở đâu?"**
*(trường `ngay` trong `TinNhan`, `_moc_tin()` khi xếp hạng — mô tả được lỗi TRƯỚC khi
sửa thì mới ăn điểm)*

> - **Lỗi trong prompt trước khi sửa:** Ban đầu mỗi dòng tin đưa vào prompt chỉ có dạng `[M09449] 21:49 · D3115: ...`. Khi mở cửa sổ ra 3 ngày (từ 12 đến 14/09), model hoàn toàn mù về ngày tháng. Khi đọc một tin ngày 12/09 bảo "hạn nộp bài là 23:59 tối nay", model Gemini lấy ngày hiện tại (14/09) gán vào, biến thành "23:59 ngày 14/09". Mốc thời gian bị trễ đi 2 ngày so với thực tế, cực kỳ nguy hiểm.
> - **Lỗi trong hàm xếp hạng trước khi sửa:** Code cũ dùng hàm `_phut(gio)` chỉ tính phút trong ngày (`h * 60 + p`). Ví dụ: Tin `M22827` đăng lúc 08:28 ngày 14/09 có số phút là 508. Tin `M09449` đăng lúc 21:49 ngày 13/09 có số phút là 1309. Khi sắp xếp giảm dần theo độ mới, tin cũ ngày 13/09 (1309 phút) lại được ưu tiên xếp trên tin mới sáng ngày 14/09 (508 phút).
> - **Khắc phục:** Đưa `ngay` vào `TinNhan`, hiển thị rõ `YYYY-MM-DD` trên từng dòng prompt để model hiểu đúng ngữ cảnh thời gian, và viết hàm `_moc_tin()` nhân hệ số ngày để so sánh chính xác mốc thời gian qua nhiều ngày.

---

## 4 · Một chỗ mình còn chưa chắc

Thứ mình làm mà nếu giám khảo hỏi sâu thì mình sẽ lúng túng. Viết ra đây để
trước buổi pitch còn kịp đọc lại.

> **Hiện tượng model bị "trôi" sinh ra 24 mục `SKIP` khi cửa sổ phình to (779 tin):**
> - Ở lượt 2 trên lát tổng hợp 779 tin, model Gemini trả về thêm 24 mục có nhãn `SKIP` chứa toàn tin nhắn trò chuyện thông thường, dù trong prompt mình đã ghi rất gắt: *"Không có mốc thời gian thì KHÔNG trả về. Đây là quy tắc cứng"*.
> - Tầng code của mình đã lọc sạch bằng lệnh `if m.get("loai") == "SKIP": continue` nên người dùng không thấy rác, nhưng việc model sinh thêm 24 mục làm tốn đáng kể token đầu ra và làm tăng độ trễ phản hồi.
> - Nếu giám khảo hỏi: *"Tại sao không bỏ chữ SKIP ra khỏi JSON SCHEMA để ép model tuyệt đối không sinh ra mục SKIP?"*, mình sẽ phải giải thích thành thật: Việc bỏ `SKIP` khỏi schema là thay đổi lớn về hành vi của LLM (nếu không có đường thoát `SKIP`, model có thể bị dồn ép và gán bừa tin chat thành `ANNOUNCE`). Lúc phát hiện ra thì đã đêm muộn 17/09, quota API cạn kiệt không thể chạy lại bộ 25 test case để thẩm định rủi ro, nên mình quyết định chọn giải pháp an toàn là giữ nguyên schema và dùng code Python chặn lại.

## 5 · Nếu làm lại từ đầu

Một quyết định mình sẽ làm khác, và vì sao.

> **Mình sẽ thiết kế kiến trúc Pipeline dạng hướng đối tượng rõ ràng (Extract -> Validate -> Deduplicate -> Rank) kèm kiểm thử đơn vị độc lập ngay từ giờ đầu tiên:**
> - Ban đầu mình viết `digest.py` theo lối script kịch bản nhanh cho lát cắt 1 ngày, gom nhiều bước xử lý vào chung một hàm lớn. Đến chiều tối 17/09, khi spec thay đổi từ 1 ngày sang 3 ngày và đổi quy tắc chống trùng, mình phải vừa sửa prompt, vừa sửa cấu trúc dữ liệu `TinNhan`, vừa viết lại hàm sort ngay trong cùng một file dưới áp lực thời gian.
> - Nếu làm lại từ đầu, mình sẽ tách riêng tầng Adapter nạp dữ liệu, tầng Prompt Engine, và tầng Rule Engine thành các module độc lập. Khi đó việc mở rộng thêm chiều kích ngày hay thay đổi luật nghiệp vụ chỉ cần thay thế một hàm filter mà không có nguy cơ làm ảnh hưởng chéo tới các phần khác.

---

*Luật vibe-coding của khoá: dùng AI để build thoải mái, nhưng **không giải thích được
phần có tên mình thì phần đó 0 điểm** — giám khảo hỏi bất kỳ thành viên nào khi thuyết
trình. File này là chỗ chuẩn bị cho đúng câu hỏi đó.*

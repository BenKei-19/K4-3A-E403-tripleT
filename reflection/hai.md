# Reflection — Nguyễn Việt Hoàng Hải

**Mã học viên:** `2A202602967` · **Phần việc:** Hàm lõi digest.py · prompt · guardrail · chống trùng · xếp hạng

> Tự viết, không nhờ ai viết hộ. Ngắn cũng được, nhưng phải là chuyện thật.

## 1 · Phần mình làm

Mô tả bằng lời của mình — file nào, hàm nào, quyết định gì là của mình.

> …

## 2 · Một chỗ mình làm sai rồi sửa

Không phải "em học được nhiều". Một lỗi cụ thể: lúc đó nghĩ gì, sai thế nào,
biết là sai nhờ đâu, sửa ra sao.

> …

## 3 · Ba câu giám khảo nhiều khả năng hỏi mình

**a. "Guardrail của các bạn chặn được cái gì, và chặn ở tầng nào?"**
*(mã tin không có thật → vứt mục; tin bị đính chính → bỏ bản cũ; trùng mốc → bỏ.
Vì sao để code làm chứ không dặn model?)*

> …

**b. "Vì sao một tin được trả về hai mục?"**
*(M09449 chứa hai mốc khác nhau — và vì sao chống trùng phải theo mốc chứ không theo
`msg_id`)*

> …

**c. "Cửa sổ 3 ngày mà prompt chỉ có `HH:MM` thì hỏng ở đâu?"**
*(trường `ngay` trong `TinNhan`, `_moc_tin()` khi xếp hạng — mô tả được lỗi TRƯỚC khi
sửa thì mới ăn điểm)*

> …

---

## 4 · Một chỗ mình còn chưa chắc

Thứ mình làm mà nếu giám khảo hỏi sâu thì mình sẽ lúng túng. Viết ra đây để
trước buổi pitch còn kịp đọc lại.

> …

## 5 · Nếu làm lại từ đầu

Một quyết định mình sẽ làm khác, và vì sao.

> …

---

*Luật vibe-coding của khoá: dùng AI để build thoải mái, nhưng **không giải thích được
phần có tên mình thì phần đó 0 điểm** — giám khảo hỏi bất kỳ thành viên nào khi thuyết
trình. File này là chỗ chuẩn bị cho đúng câu hỏi đó.*

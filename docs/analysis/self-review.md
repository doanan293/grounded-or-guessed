# Tự phản biện bản thảo (Phase 4, Task 6)

Bản thảo (báo cáo tiếng Việt và bài báo tiếng Anh) được đọc như một người phản biện hoài nghi theo năm chiều của
`research-paper-writing/references/paper-review.md`. Mỗi câu hỏi đi kèm câu trả lời và chỗ đã sửa. 16 phát hiện của lượt
phản biện đối kháng được liệt kê ở cuối cùng trạng thái.

## 1. Đóng góp

- **Có mới không, hay chỉ là chạy lại?** Mới ở ba điểm: phân rã Shapley tách phần đoán/phần bằng chứng (chưa ai đo cho
  SemLoc), bộ dòng lỗi chuẩn sửa bằng thực thi, và một phương pháp đối chứng một prompt chưa có trong bài gốc. Tái hiện
  là điều kiện cần, không phải đóng góp chính.
- **"Phần lớn top-1 là đoán" có phải hiển nhiên do thiết kế?** Đúng là do thiết kế (+1,2 > điểm phổ tối đa), nên bài viết
  nói thẳng "theo cấu tạo" và báo thêm giá trị biên (bỏ điểm thưởng thì Acc@1 giảm bao nhiêu) thay vì chỉ Shapley.

## 2. Độ rõ ràng

- Thuật ngữ thống nhất: "SemFault-250 đã sửa" / "SemFault-250-repaired", "phương pháp đối chứng", "quy trình nhiều bước",
  "bộ phán định"; bảng thuật ngữ đã cập nhật.
- Mỗi chương mở đầu bằng câu nêu thông điệp; các định nghĩa (Acc@k, hạng trung bình, mẫu số cố định, nhãn
  semantic/coverage_revealed/not_executed) đặt trước lần dùng đầu tiên.

## 3. Sức mạnh thực nghiệm

- Ba lần lặp, bootstrap cụm theo khuôn mẫu, McNemar, Wilcoxon; mọi Δ có khoảng tin cậy.
- **Điểm yếu còn lại:** một mô hình chính; 31 lỗi thật của một dự án (CI chứa 0); so sánh nhiều mô hình chỉ trên 44 chương
  trình dev, chưa có CI. Đã ghi rõ ở phần giới hạn và mối đe dọa.

## 4. Độ đầy đủ của đánh giá

- Kết quả báo trên cả dòng lỗi chuẩn gốc (toàn bộ và tập con được chạy tới) lẫn bản đã sửa, nên người đọc thấy kết luận
  phụ thuộc nhãn thế nào.
- **Chưa có:** thí nghiệm loại bỏ chú thích độ phủ khỏi prompt LLM + độ phủ (khoảng 600 lượt gọi). Hiện kết luận được
  diễn đạt là "bằng chứng thực thi" (kiểm thử thất bại + độ phủ), không quy riêng cho độ phủ.

## 5. Tính hợp lý của thiết kế phương pháp

- Bộ phán định sửa tối thiểu chấp nhận bản sửa bù trừ; dòng trống đã bị loại, phần còn lại được nêu là nhiễu.
- CovGate với λ chọn trên dev thực chất là bộ phá hòa Ochiai; bài viết gọi đúng tên và không trình bày như phương pháp mới
  mạnh.
- Prompt đối chứng viết trước khi xem tập test và không tinh chỉnh.

## Danh sách 16 phát hiện và trạng thái

| # | Mức | Phát hiện | Trạng thái |
|---|---|---|---|
| 1 | Nghiêm trọng | Khẳng định chính phụ thuộc dòng lỗi chuẩn | Đã sửa: giới hạn phạm vi "lỗi được chạy tới", báo cả nhãn gốc (Δ nhỏ hơn, SemLoc hơn ở Acc@5) |
| 2 | Nghiêm trọng | Phương pháp đối chứng gộp nhiều khác biệt | Đã sửa cách diễn đạt; thí nghiệm loại bỏ chờ quyết định |
| 3 | Lớn | "Đoán" là do cấu tạo | Đã sửa: nói rõ, báo giá trị biên |
| 4 | Lớn | Tên "verified" quá mạnh, thiếu chi tiết bộ phán định | Đã sửa: đổi tên "đã sửa/repaired", thêm chi tiết |
| 5 | Lớn | CovGate thực chất là bộ phá hòa | Đã sửa |
| 6 | Lớn | Giải thích bước CF | Đã sửa |
| 7 | Lớn | Cách diễn đạt về DD | Đã sửa |
| 8 | Lớn | Tập con 44 chương trình | Đã sửa: nêu n và cảnh báo |
| 9 | Lớn | Thiếu giới hạn phạm vi | Đã sửa (tóm tắt, mở đầu, kết luận, slide) |
| 10 | Lớn | "Tái hiện" thực chất là tính lại từ nhật ký | Đã sửa + chạy lại Claude trên dev |
| 11 | Lớn | Thiếu định nghĩa | Đã sửa |
| 12 | Nhỏ | Nhiều phép so sánh / gộp | Đã nêu |
| 13 | Nhỏ | Diễn đạt không dấu | Đã sửa |
| 14 | Nhỏ | Vị trí bảng/hình, độ dễ đọc | Đã sửa |
| 15 | Nhỏ | Bảng kiểm 6 hay 7 mục | Đã thống nhất 7 mục |
| 16 | Nhỏ | Thuật ngữ tiếng Việt | Đã sửa |

## Phase 5 (09/11): tự phản biện sau khi đổi câu chuyện

1. **Đóng góp.** Đóng góp chính chuyển từ "một cải tiến" (CovGate) sang "hiểu biết có bằng chứng": hạng 1 là dòng đoán,
   nhãn lệch gần một nửa, prompt đơn giản có kiểm thử thất bại thắng, và các cách phức tạp hơn không thêm gì kèm cơ chế.
   Rủi ro: giám khảo hỏi "cái mới là gì" — trả lời bằng ablation (tách kiểm thử thất bại và độ phủ), bộ nhãn rà soát, và
   cơ chế bản sửa "lách" kiểm thử, ba thứ chưa có trong tài liệu về SemLoc.
2. **Độ rõ.** Câu chuyện mở đầu từ thực tế (chạy kiểm thử, đưa lỗi cho LLM), có tài liệu chống lưng
   (`docs/literature/practice-evidence.md`); kinh nghiệm riêng không dùng làm bằng chứng.
3. **Sức mạnh thực nghiệm.** Ba bộ nhãn song song; kết luận chính giữ trên cả ba. Yếu: đề xuất rồi kiểm chứng và biểu
   quyết chỉ trên dev; lỗi thật 31 lỗi, CI chứa 0; một mô hình chính.
4. **Độ đầy đủ.** Đã có ablation độ phủ, phân tích tĩnh có mức ngẫu nhiên. Chưa có: thí nghiệm giấu tên kiểm thử, định vị
   cấp dự án — ghi là hướng phát triển.
5. **Tính hợp lý của thiết kế.** Bộ nhãn rà soát có nguy cơ vòng tròn và người duyệt xem gợi ý (đồng ý 111/111) — nêu thẳng
   trong phần phương pháp và các mối đe dọa; kết quả chính dùng bộ gốc và bộ đã sửa. Quy tắc chọn tham số của đề xuất rồi
   kiểm chứng được cố định trong mã trước khi chạy và không dùng bộ đã sửa.

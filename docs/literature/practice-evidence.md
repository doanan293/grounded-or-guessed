# Bằng chứng tài liệu cho phần động lực và thảo luận (Phase 5)

Mục đích: mỗi câu về "thực tế phát triển phần mềm" trong bài phải có tài liệu chống lưng; kinh nghiệm của nhóm
(và của công ty chủ dự án) chỉ là động lực, không phải bằng chứng. Khóa BibTeX trong `docs/report/references.bib`.
Đã kiểm tra tồn tại và metadata (tác giả, năm, nơi đăng, DOI) qua tìm kiếm ngày 09/11/2026.

| Câu định viết trong bài | Tài liệu | Ghi chú — viết đúng mức |
|---|---|---|
| Lập trình viên dùng trợ lý AI rộng rãi trong công việc hằng ngày | `stackoverflow2025` (84% đang hoặc định dùng AI; 46% không tin độ chính xác), `jetbrains2025` (85% dùng AI thường xuyên; 24.534 người, 194 nước) | Hai khảo sát lớn của ngành, không phải bài báo bình duyệt. Chỉ nói về *dùng AI nói chung*, không riêng gỡ lỗi |
| Gỡ lỗi là một trong các việc lập trình viên đem hỏi ChatGPT | `xiao2024devgpt` (DevGPT: hội thoại thật giữa lập trình viên và ChatGPT, lấy từ GitHub và Hacker News; nhiều bài MSR 2024 phân loại nhiệm vụ) | Không trích tỉ lệ cụ thể (chưa xác minh được con số trong bài gốc); viết "là một trong các nhóm việc thường gặp" |
| Đưa thông tin lỗi (error log / kiểm thử thất bại) cho LLM làm định vị lỗi chính xác hơn hẳn | `wu2023llmfl` (ChatGPT trên Defects4J: thêm error log nâng Top-1 và độ ổn định; tốt ở mức hàm, giảm mạnh ở mức lớp) | Ủng hộ trực tiếp kết quả ablation của nhóm; cũng ủng hộ giới hạn "một hàm mỗi lần" |
| Định vị lỗi bằng LLM chỉ cần một kiểm thử thất bại | `kang2024autofl` (AutoFL, FSE 2024) | Đã có trong bib; AutoFL dùng thêm lệnh duyệt mã — không phải một prompt duy nhất |
| Cách làm đơn giản có thể thắng hệ thống phức tạp | `xia2024agentless` (Agentless: hai bước định vị → sửa, không agent, rẻ hơn mà tốt nhất trong các phương pháp mã nguồn mở trên SWE-bench Lite) | Bối cảnh sửa lỗi cấp kho mã, khác bài toán định vị cấp dòng; dùng như tiền lệ "simple beats complex". Agentless cũng phát hiện vấn đề nhãn/đề bài trong SWE-bench Lite |
| Bản sửa làm kiểm thử đạt chưa chắc đúng ("plausible" ≠ đúng) | `qi2015kali` (ISSTA 2015: phần lớn bản vá của GenProg/RSRepair/AE không đúng; nhiều bản chỉ xóa chức năng), `smith2015cure` (FSE 2015: sửa tự động "quá khớp" bộ kiểm thử; 956 lỗi) | Giải thích cơ chế: đề xuất rồi kiểm chứng thất bại, CF của SemLoc vô dụng, bộ kiểm chứng nhãn nhận nhầm |
| Nhãn sai có trong cả các benchmark nổi tiếng và làm thay đổi kết luận | `northcutt2021labels` (NeurIPS 2021: trung bình ~3,3% nhãn sai ở tập test của 10 bộ dữ liệu phổ biến; ~6% ở ImageNet validation; nhãn sai có thể đảo thứ hạng mô hình) | So sánh: SemFault-250 có tỉ lệ cao hơn nhiều; nêu đúng là hai lĩnh vực khác nhau |
| Kỹ thuật định vị lỗi tự động thường được đánh giá theo giả định không khớp cách lập trình viên làm | `parnin2011` (ISSTA 2011, hai nghiên cứu người dùng, 34 lập trình viên; giải ISSTA Impact Paper 2021) | Ủng hộ việc đặt bài toán theo quy trình thực tế |
| Người làm nghề có kỳ vọng cụ thể với công cụ định vị lỗi | `kochhar2016` (ISSTA 2016, khảo sát 386 người làm nghề ở hơn 30 nước) | Không trích ngưỡng "top-5" (chưa xác minh); chỉ nói khảo sát tồn tại và đối chiếu với nghiên cứu |
| Kiểm thử viết trước mô tả ý định của mã | `beck2003tdd` (sách gốc về TDD) | Dùng cho câu động lực về TDD |

## Những gì KHÔNG có tài liệu và không được viết như sự thật

- Tỉ lệ lập trình viên "dán kiểm thử thất bại vào LLM" — không tìm được khảo sát đo đúng việc này. Viết: "trợ lý AI được dùng
  rộng rãi [stackoverflow2025, jetbrains2025], gỡ lỗi là một trong các việc thường được hỏi [xiao2024devgpt], và thông tin lỗi
  giúp LLM định vị tốt hơn [wu2023llmfl]".
- Kinh nghiệm của công ty chủ dự án: không nêu tên, không dùng làm bằng chứng.

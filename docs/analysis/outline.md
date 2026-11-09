# Dàn ý báo cáo và bài báo — bản Phase 5 (chờ chủ dự án duyệt)

Thay dàn ý Phase 4 (đã duyệt 09/11). Giữ khung của thầy (`HuongDanTieuLuan 2026.pdf`, §I, §III.1, §III.2), giữ
công tắc phiên bản: **[1]** có từ `lan1`, **[2]** từ `lan2`, **[F]** chỉ bản `full`. Mọi con số là macro
(`numbers-vi.tex` / `numbers.tex`); bảng từ `docs/report/generated/`.

## Câu chuyện (một đoạn)

Trong thực tế, lập trình viên viết kiểm thử (nhất là khi làm TDD); khi chạy kiểm thử thấy fail — trên máy cá nhân
(pytest, pre-commit, IDE) hay trên CI — họ đưa kết quả đó cho LLM để tìm chỗ sai. SemLoc đề xuất một quy trình nhiều bước phức tạp hơn nhiều và tuyên bố nó "neo lập luận của LLM
vào thực thi". Bài này kiểm tra lời tuyên bố đó: (i) dòng hạng 1 của SemLoc luôn là dòng LLM tự đoán, do một điểm
thưởng không được mô tả; (ii) gần một nửa nhãn của SemFault-250 không trỏ đúng dòng lỗi, và nhãn sai vô tình có lợi
cho SemLoc; (iii) một prompt duy nhất có kiểm thử thất bại — đúng cách lập trình viên vẫn làm — chính xác hơn và rẻ
hơn khoảng sáu lần; (iv) mọi thứ phức tạp hơn mà nhóm thử (độ phủ từng dòng, gắn thêm vào SemLoc, kiểm chứng bằng bản
sửa, biểu quyết) và công cụ phân tích tĩnh (ruff, pyrefly) đều không thêm được gì, kèm giải thích cơ chế.

**Thông điệp một câu:** *Quy trình phức tạp của SemLoc thực chất dựa vào phỏng đoán của LLM và được đánh giá trên bộ
nhãn lệch gần một nửa; đưa kiểm thử thất bại cho LLM — cách lập trình viên vẫn làm — chính xác hơn và rẻ hơn khoảng
sáu lần, và các thành phần phức tạp hơn không thêm được gì.*

## Ba câu hỏi nghiên cứu (đổi so với Phase 4)

- **RQ1 — Tái hiện và kiểm tra cách đánh giá:** kết quả SemLoc có tái hiện được không; điểm thưởng ẩn, bước vá thử
  (CF), cách chấm, và **chất lượng nhãn** (bộ gốc → đã sửa → đã rà soát) ảnh hưởng thế nào.
- **RQ2 — LLM thật sự cần gì?** So SemLoc với một prompt có kiểm thử thất bại; ablation tách độ phủ khỏi kiểm thử
  thất bại; các cách bổ sung (CovGate, đề xuất rồi kiểm chứng, biểu quyết); phân tích tĩnh (ruff, pyrefly); chi phí.
- **RQ3 — Độ bền:** lỗi thật (BugsInPy, 31 lỗi), mã đổi tên định danh, nhiều họ mô hình; kết luận có giữ trên cả ba
  bộ nhãn không.

## Ba bộ nhãn (trình bày song song ở mọi bảng chính)

| Bộ nhãn | Ai quyết định | Vai trò |
|---|---|---|
| Gốc (tác giả) | Tác giả SemLoc | So với bài gốc |
| **Đã sửa** | Chỉ kiểm thử (bộ kiểm chứng sửa tối thiểu) | **Kết quả chính** — không có ý kiến LLM |
| Đã rà soát | Fable rà trước 250 nhãn → 6 thành viên duyệt 111 nhãn (có xem gợi ý; đồng ý cả 111) → trưởng nhóm sửa 5 ca có bằng chứng chạy kiểm thử | Góc nhìn độ nhạy; nêu nguy cơ vòng tròn |

---

## A. Báo cáo đầy đủ (tiếng Việt)

**Tiền nội dung [1]:** bìa (tên mới: "TÁI HIỆN VÀ ĐÁNH GIÁ VIỆC ĐỊNH VỊ LỖI NGỮ NGHĨA BẰNG MÔ HÌNH NGÔN NGỮ LỚN"),
cam kết (thêm: dùng LLM rà nhãn, thành viên duyệt nhãn), mục lục, danh sách bảng/hình, thuật ngữ (thêm: TDD, CI (chỉ nhắc như một nơi chạy kiểm thử),
phân tích tĩnh/động, bản sửa "lách" kiểm thử, đề xuất rồi kiểm chứng, biểu quyết, bộ nhãn đã rà soát).

### Chương 1. Mở đầu [1]
- 1.1 Đặt vấn đề **từ thực tế**: TDD → chạy kiểm thử thấy fail (máy cá nhân hoặc CI) → tìm dòng lỗi; ruff/pyrefly không bắt lỗi logic; lập trình viên
  đưa kiểm thử thất bại cho LLM. Nghiên cứu đề xuất quy trình phức tạp hơn (SemLoc) — có cần không?
- 1.2 Câu hỏi "grounded hay guessed?" và 3 RQ.
- 1.3 Đóng góp (mỗi cái một câu có số): C1 hạng 1 là dòng đoán; C2 nhãn lệch gần một nửa → hai bộ nhãn mới; C3 một
  prompt có kiểm thử thất bại thắng SemLoc, rẻ hơn ~6 lần; C4 các thành phần phức tạp hơn không thêm gì (ablation độ
  phủ, CovGate, kiểm chứng bằng bản sửa, biểu quyết, phân tích tĩnh) + cơ chế; C5 bảng kiểm 7 mục + gói tái hiện.
- 1.4 Cấu trúc báo cáo.

### Chương 2. Tổng quan tài liệu và từ khóa [1] — nội dung 1
- Giữ 2.1–2.4. Thêm vào 2.3: nhãn sai trong benchmark (Northcutt và cộng sự 2021); bản sửa "plausible" vượt kiểm thử
  yếu trong sửa lỗi tự động (Qi và cộng sự 2015, Kali); phân tích tĩnh và lỗi logic.

### Chương 3. Cơ sở lý thuyết [1]
- Giữ 3.1–3.4. Thêm 3.5: phân tích tĩnh (lint, kiểm tra kiểu) và phân tích động (kiểm thử, độ phủ) — mỗi loại thấy được
  gì; vì sao lỗi ngữ nghĩa cần thông tin thực thi.

### Chương 4. Phương pháp và thiết kế thực nghiệm [1] — nội dung 2
- 4.1 Ba RQ và giả thuyết (mới).
- 4.2 Dữ liệu: SemFault-250 (dev/test), **ba bộ nhãn** (bảng trên; quy trình rà soát mô tả đúng sự thật), BugsInPy,
  biến thể đổi tên.
- 4.3 Phương pháp so sánh: SBFL; ruff/pyrefly; LLM hỏi thẳng; SemLoc; **LLM + kiểm thử thất bại** (giải pháp chính);
  LLM + kiểm thử thất bại + độ phủ (ablation); CovGate; đề xuất rồi kiểm chứng (thiết kế, tham số, quy tắc chọn trên dev);
  biểu quyết.
- 4.4 Kiểm tra cách đánh giá (audit). 4.5 Phân rã Shapley. 4.6 Mô hình, lặp 3 lần, thống kê, chi phí.

### Chương 5. Kết quả thực nghiệm [1]
- 5.1 RQ1: tái hiện 13/13; điểm thưởng ẩn; CF; cách chấm; **chất lượng nhãn** (phân loại nhãn lệch; nhãn sai có lợi cho
  SemLoc so với LLM hỏi thẳng).
- 5.2 RQ2: bảng chính (ba bộ nhãn); ablation độ phủ; **ruff/pyrefly (một đoạn + bảng nhỏ, kèm mức trúng ngẫu nhiên)**;
  CovGate; đề xuất rồi kiểm chứng + biểu quyết (trên dev, kết quả âm tính, tỉ lệ sửa được ở dòng đúng / dòng sai);
  chi phí + hình Pareto; phân rã Shapley.
- 5.3 RQ3: BugsInPy (thêm LLM + kiểm thử thất bại), đổi tên, họ mô hình.
- 5.4 Tóm tắt trả lời 3 RQ.

### Chương 6. Phân tích thất bại và thảo luận [2] — nội dung 3
- 6.1–6.3 giữ (phân nhóm, mơ hồ dòng kề cạnh, năm mẫu nguyên nhân).
- 6.4 **Vì sao kiểm thử không làm trọng tài tốt**: bản sửa "lách" kiểm thử yếu — cùng một cơ chế giải thích CF vô dụng,
  bộ kiểm chứng nhận nhầm 8 ca, và đề xuất rồi kiểm chứng không cải thiện.
- 6.5 **Bộ dữ liệu bão hòa khi nhãn đúng**; vì sao (hàm ngắn, lỗi một token, tên kiểm thử mô tả ý định) → cần lỗi thật.
- 6.6 Hàm ý cho thực tế: AI agent sửa lỗi (trên máy cá nhân hay trong CI) — bản sửa làm kiểm thử đạt chưa chắc sửa đúng chỗ.

### Chương 7. Đóng góp, triết lý khoa học và các mối đe dọa [2] — nội dung 3
- 7.1 Đóng góp C1–C5 (khẳng định, bằng chứng, điều kiện bác bỏ, giới hạn).
- 7.2 Triết lý: kiểm thử là trọng tài *khi kiểm thử đủ chặt*; cái đơn giản phải là mốc so sánh bắt buộc; kết quả âm tính
  cũng được báo cáo.
- 7.3 Mối đe dọa: vòng tròn của bộ nhãn rà soát; người duyệt xem gợi ý LLM; tên kiểm thử "nói hộ" lỗi; một hàm mỗi lần
  (lỗi thật được cho sẵn hàm đích); 31 lỗi một dự án; một mô hình chính; đề xuất rồi kiểm chứng chỉ đánh giá trên dev.

### Chương 8. Kết luận và hướng phát triển [1]
- 8.1 Kết luận theo thông điệp một câu. 8.2 Hướng phát triển: định vị cấp dự án (thu hẹp từ dự án xuống hàm); ablation
  giấu tên kiểm thử; kiểm thử chặt hơn để kiểm chứng có ý nghĩa; benchmark lỗi thật nhiều dự án.

### Phụ lục [F]
- A. Tái hiện (4 mức, Docker). B. Bảng đầy đủ (theo từng bộ nhãn, họ mô hình, lưới tham số đề xuất rồi kiểm chứng).
- C. Các prompt (LLM + kiểm thử thất bại, bản có độ phủ, prompt viết bản sửa). D. Quy trình rà soát nhãn (mẫu tệp duyệt).

---

## B. Bài báo tiếng Anh (arXiv, IEEEtran)

Tên: *Grounded or Guessed: A Reproducibility Study of LLM-Based Semantic Fault Localization*.

1. **Abstract:** thực tế (kiểm thử fail, chạy cục bộ hay trên CI → LLM) → SemLoc tuyên bố → 4 kết quả có số → hàm ý (mốc đơn giản bắt buộc).
2. **Introduction:** động lực từ TDD và việc chạy kiểm thử hằng ngày (cục bộ hoặc CI); câu hỏi; phát hiện; đóng góp C1–C5; artifact.
3. **Related Work:** SBFL; LLM-based FL; benchmark label errors; plausible patches / test overfitting; static analysis.
4. **Background:** SBFL, SemLoc (hình), lỗi ngữ nghĩa, Acc@k.
5. **Approach:** audit; ba bộ nhãn; phân rã; LLM + failing tests và ablation; CovGate; propose-and-verify; vote; static tools.
6. **Evaluation:** setup; RQ1; RQ2 (bảng chính ba bộ nhãn, ablation, static, negative results); RQ3; failure analysis.
7. **Discussion:** why tests make poor arbiters; benchmark saturation; implications for repair agents (local or CI).
8. **Threats**; 9. **Conclusion**; **Data Availability**.

Bảng/hình: Fig. 1 SemLoc + điểm kiểm tra; Table I audit; **Table II kết quả chính (ba bộ nhãn)**; Table III ablation +
các cách bổ sung (độ phủ, CovGate, kiểm chứng, biểu quyết, ruff, pyrefly); Fig. 2 Pareto; Table IV RQ3; Table V nhãn lệch.

## C. Slide
- Lần 1 / lần 2 / bảo vệ: thay trang "cải tiến" bằng "LLM thật sự cần gì?" (bảng ablation + các cách bổ sung), thêm trang
  "nhãn lệch gần một nửa", trang mở đầu từ TDD và việc chạy kiểm thử; giữ số trang tương đương.

## D. Điểm cần chủ dự án quyết
1. Duyệt câu chuyện và thông điệp một câu ở trên.
2. Giữ CovGate trong bài như **một trong các cách bổ sung** (không còn là "cải tiến chính") — đề xuất: giữ.
3. Kinh nghiệm dùng cách đơn giản ở công ty chủ dự án: chỉ dùng làm động lực ở phần mở đầu (không nêu tên công ty,
   không dùng làm bằng chứng) — đề xuất: viết chung "trong thực tế phát triển phần mềm".

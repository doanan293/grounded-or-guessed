# Dàn ý báo cáo và bài báo (Phase 4, Task 2) — chờ chủ dự án duyệt

Khung theo hướng dẫn của thầy (`HuongDanTieuLuan 2026.pdf`):
- **Báo cáo đầy đủ** (§III.1): bìa, cam kết, mục lục, danh sách bảng/hình/viết tắt, nội dung chính, phụ lục, tài liệu tham khảo. Thuật ngữ nước ngoài Việt hóa; chỉ giữ tiếng Anh khi không có từ tương ứng, kèm bảng thuật ngữ ở danh mục viết tắt.
- **Báo cáo tóm tắt = bài báo** (§III.2): Giới thiệu → Tổng quan và định hướng giải pháp → Cơ sở lý thuyết → Giải pháp đề xuất → Cài đặt, thực nghiệm, đánh giá → Kết luận.
- 4 nội dung chấm điểm (§I): (1) tài liệu và từ khóa, (2) ≥3 RQ và thực nghiệm, (3) đóng góp khoa học và triết lý, (4) bài báo đủ chuẩn arXiv.

Ký hiệu phiên bản: **[1]** có từ bản `lan1`, **[2]** từ `lan2`, **[F]** chỉ bản `full`. Nguồn số liệu: macro trong `numbers-vi.tex` / `numbers.tex`; bảng: `docs/report/generated/*.tex`.

---

## A. Báo cáo đầy đủ (tiếng Việt), ~45–55 trang nội dung

**Tiền nội dung [1]:** bìa (ĐHBK Hà Nội, IT5440, học kỳ 20261, đề tài 02-KH, nhóm M9, 7 tên + MSHV theo thứ tự đã chốt, GVHD), cam kết trung thực (ghi rõ phần dùng từ SemLoc và việc dùng công cụ AI), mục lục, danh sách bảng, danh sách hình, danh mục viết tắt và thuật ngữ (SBFL, LLM, RQ, CF, GT, Acc@k…).

### Chương 1. Mở đầu [1] (~4 trang)
- 1.1 Đặt vấn đề: định vị lỗi; lỗi ngữ nghĩa làm SBFL mất tín hiệu; LLM hiểu ý đồ nhưng khó kiểm chứng; SemLoc tuyên bố "neo lập luận vào thực thi".
- 1.2 Câu hỏi "grounded hay guessed?" và 3 câu hỏi nghiên cứu (RQ1 tái hiện + kiểm tra cách đánh giá; RQ2 cải tiến và đối chứng; RQ3 độ bền).
- 1.3 Đóng góp chính (tóm tắt C1–C7 của `contributions.md`, mỗi đóng góp một câu có số) — [1] ghi C1–C4 và C6 dưới dạng kết quả; [2] thêm C5, C7 và phần triết lý.
- 1.4 Cấu trúc báo cáo.

### Chương 2. Tổng quan tài liệu và từ khóa [1] — *nội dung 1* (~8 trang)
- 2.1 Phương pháp tìm và chọn tài liệu: từ khóa (bảng song ngữ `docs/literature/keywords.md`), nguồn, tiêu chí; 3 bài thầy giao + 23 tài liệu.
- 2.2 Ba bài báo được giao: 2.2.1 SemLoc, 2.2.2 EffiHolmes, 2.2.3 Crash report + LLM — mỗi bài: vấn đề, phương pháp, đánh giá, điểm mạnh/yếu (nguồn: `docs/literature/notes-*.md`).
- 2.3 Các hướng nghiên cứu liên quan: 2.3.1 SBFL kinh điển, 2.3.2 định vị lỗi bằng LLM (AutoFL, AgentFL, FlexFL…), 2.3.3 benchmark và tính hợp lệ của benchmark, 2.3.4 nhiễm dữ liệu / ghi nhớ của LLM.
- 2.4 Bảng so sánh và khoảng trống nghiên cứu (bảng so sánh của slide lần 1, mở rộng); học được gì và áp dụng ra sao.

### Chương 3. Cơ sở lý thuyết [1] (~6 trang)
- 3.1 Định vị lỗi dựa trên phổ: ma trận độ phủ, công thức Ochiai, Tarantula, DStar (có đánh số phương trình); chỉ số Acc@k, hạng, cách xử lý hòa điểm.
- 3.2 Lỗi ngữ nghĩa: định nghĩa khách quan bằng độ phủ (semantic / coverage-revealed / not-executed).
- 3.3 SemLoc: ràng buộc do LLM suy ra, chèn mã kiểm tra, phổ vi phạm, kiểm chứng phản thực tế (counterfactual); hình pipeline (ghi nguồn SemLoc).
- 3.4 Công cụ thống kê: McNemar, Wilcoxon và hệ số tương quan hạng hai chuỗi, bootstrap theo cụm, giá trị Shapley.

### Chương 4. Phương pháp và thiết kế thực nghiệm [1] — *nội dung 2* (~8 trang)
- 4.1 Ba câu hỏi nghiên cứu và giả thuyết.
- 4.2 Dữ liệu: SemFault-250 (chia dev 50 / test 200, cụm template), SemFault-250-verified (oracle sửa tối thiểu, trạng thái, loại vị trí ở dòng trống), BugsInPy (31 lỗi youtube-dl, chọn hàm đích), biến thể đổi tên.
- 4.3 Phương pháp so sánh: SBFL, LLM hỏi thẳng, SemLoc, **CovGate** (4 thành phần, chọn tham số trên dev), **LLM + độ phủ** (prompt một lượt).
- 4.4 Kiểm tra cách đánh giá của SemLoc (audit): cách chấm của tác giả và cách chấm công bằng.
- 4.5 Phân rã "grounded vs guessed" (trò chơi Shapley hai người chơi).
- 4.6 Mô hình, mức suy luận, hạ tầng (proxy, cache, `run_health`), lặp 3 lần, chi phí.

### Chương 5. Kết quả thực nghiệm [1] (~10 trang)
- 5.1 RQ1 — Tái hiện và kiểm tra cách đánh giá: bảng `rq1_audit`, thưởng ẩn +1,2, CF không đổi thứ hạng, DD/SBFL dưới hai cách chấm, lỗi của artifact; ảnh hưởng của ground truth (gốc → đã sửa).
- 5.2 RQ2 — Cải tiến và đối chứng: bảng `rq2_ours` (Δ + CI), `rq2_by_label`, ablation CovGate, phân rã Shapley (`rq_decomposition_*`), chi phí + hình Pareto.
- 5.3 RQ3 — Độ bền: 5.3.1 lỗi thật BugsInPy (`rq3_bugsinpy`), 5.3.2 đổi tên (`rq3_renamed`), 5.3.3 họ mô hình (`rq3_families`).
- 5.4 Tóm tắt trả lời 3 RQ (bảng một dòng mỗi RQ).

### Chương 6. Phân tích thất bại và thảo luận [2] — *nội dung 3* (~6 trang)
- 6.1 Phân nhóm tự động 179 chương trình (`failure_signals`).
- 6.2 Mơ hồ dòng kề cạnh: phân bố độ lệch, quan hệ đầu khối–thân khối, Acc@1 chặt / chấp nhận (`failure_tolerance`).
- 6.3 Năm mẫu nguyên nhân (P1–P5) với ví dụ mã ngắn.
- 6.4 Thảo luận: "guessed" đọc thế nào cho đúng; khi nào bằng chứng thực thi có ích.

### Chương 7. Đóng góp, triết lý khoa học và các mối đe dọa [2] — *nội dung 3* (~5 trang)
- 7.1 Đóng góp C1–C7 (khẳng định, bằng chứng, điều kiện bác bỏ, giới hạn).
- 7.2 Triết lý khoa học (6 nguyên tắc).
- 7.3 Các mối đe dọa đến tính hợp lệ (nội tại, ngoại tại, cấu trúc, kết luận).

### Chương 8. Kết luận và hướng phát triển [1] (~2 trang)
- 8.1 Kết luận (bản [1]: trả lời 3 RQ; bản [2]/[F]: thêm đóng góp).
- 8.2 Hướng phát triển: oracle nhiều vị trí và chống sửa bù trừ, thêm lỗi thật nhiều dự án, chuẩn đánh giá cho định vị lỗi bằng LLM.

### Phụ lục [F]
- A. Hướng dẫn tái hiện (4 mức, `REPRODUCE.md`), Docker, link GitHub.
- B. Bảng đầy đủ: kết quả theo ground truth gốc, theo từng họ mô hình, checklist đánh giá.
- C. Prompt baseline LLM + độ phủ và mẫu prompt đã dùng.

**Tài liệu tham khảo [1]:** IEEE theo mẫu của thầy, chỉ những tài liệu được trích dẫn.

---

## B. Bài báo tiếng Anh (arXiv, IEEEtran hai cột), ~10–12 trang + tài liệu

Tiêu đề: *Grounded or Guessed: A Reproducibility Study of LLM-Based Semantic Fault Localization*. Tác giả: 7 tên, HUST. Bản `lan2` có dòng "Draft".

1. **Abstract** (~200 từ): bối cảnh → câu hỏi → phương pháp (audit, SemFault-250-verified, phân rã, baseline) → 4 kết quả có số → hàm ý.
2. **Introduction**: lỗi ngữ nghĩa và lời hứa "grounding"; câu hỏi; tóm tắt phát hiện; danh sách đóng góp đánh số (mỗi cái có số); link artifact.
3. **Related Work and Research Direction**: SBFL; LLM-based FL; benchmark validity & reproducibility; memorization. Đoạn cuối: khoảng trống → hướng của bài.
4. **Background**: SBFL và Ochiai; SemLoc pipeline (hình); định nghĩa lỗi ngữ nghĩa; Acc@k và hòa điểm.
5. **Approach** (giải pháp đề xuất): A. evaluation audit; B. SemFault-250-verified (oracle, giới hạn); C. grounded-vs-guessed decomposition; D. CovGate; E. LLM + coverage baseline.
6. **Evaluation** (cài đặt, thực nghiệm, đánh giá): setup (models, repeats, stats); RQ1; RQ2 (bảng chính, Pareto); RQ3 (BugsInPy, renamed, families); failure analysis (ambiguity + patterns).
7. **Threats to Validity**.
8. **Conclusion and Future Work**; **Data Availability** (GitHub, Docker, offline replay).

Hình/bảng dự kiến: Fig. 1 pipeline SemLoc + điểm can thiệp của nhóm; Table I audit; Table II RQ2; Fig. 2 Pareto; Table III decomposition; Table IV RQ3 (gộp BugsInPy + renamed); Table V failure categories / tolerance.

---

## C. Slide (Task 7)
- **Lần 1** (dựng lại bộ hiện tại, 20 trang): số liệu ground truth mới, bìa có tên nhóm.
- **Lần 2** (~22 trang): tóm tắt lần 1 (4 trang) + phân tích thất bại (mơ hồ dòng kề cạnh, 5 mẫu), đóng góp, triết lý khoa học, Threats, bản nháp bài báo, kế hoạch nộp.
- **Bảo vệ** (~25 trang, ≤20 phút): toàn bộ câu chuyện theo cấu trúc bài báo.

## D. Điểm cần chủ dự án quyết
1. Tên giảng viên hướng dẫn và mã lớp trên bìa.
2. Hướng dẫn ghi "tiêu đề mục có kích thước **24**, chữ hoa in đậm" — có vẻ là lỗi đánh máy (chương chỉ 16). Đề xuất dùng **14 chữ hoa đậm** (như khung hiện tại).
3. Báo cáo đầy đủ viết tiếng Việt, bài báo tiếng Anh (hướng dẫn cho phép cả hai) — giữ như spec.

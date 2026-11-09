# Specs tổng quan — Tiểu luận 2KH: Grounded or Guessed (định vị lỗi ngữ nghĩa dựa trên SemLoc)

- Môn: IT5440 – Nguyên lý và kỹ thuật phân tích chương trình, kỳ 2026.1, ĐH Bách khoa Hà Nội
- Đề tài: **2KH** — Chương 10 "Phát hiện lỗi và định vị lỗi", hướng nghiên cứu khoa học
- Ngày viết: 08/11/2026 · cập nhật 08/11/2026 (sau mốc 1: proxy, model, mức suy luận, audit SemLoc, CovGate, lộ trình) · cập nhật 09/11/2026 (Phase 2–3 xong; bỏ DOI; viết trọn bài trước rồi cắt 2 nhánh báo cáo tiến độ) · cập nhật 09/11/2026 tối (Phase 5: ablation độ phủ, SemFault-250 đã rà soát, phương pháp "đề xuất rồi kiểm chứng", đổi tên bài)
- Người thực hiện: chủ dự án (học viên) + Claude, làm trọn từ đầu đến cuối. Các thành viên khác trong nhóm 7 người không nhận phần việc nào (đã chốt 08/11), trừ việc duyệt nhãn ở Phase 5: 6 thành viên (trừ nhóm trưởng) duyệt 111 nhãn dòng lỗi.
- Nhóm **M9**, thứ tự tác giả trên bìa, bài báo, slide (chủ dự án chốt 09/11): Doãn Văn An – 20252778M (nhóm trưởng), Tạ Công Nam – 20252640M, Nguyễn Hoàng Hải – 20252583M, Đỗ Xuân Tráng – 20252774M, Hoàng Trung Kiên – 20251333M, Mai Văn Tùng – 20252788M, Nguyễn Đức Tùng – 20252772M.
- Tài liệu gốc của thầy: `docs/requirement/HuongDanTieuLuan 2026.pdf`; 3 bài báo: `docs/requirement/dt2-chap10/` (cũng có trong `Detai2.Chapter10/`)

---

## 1. Mục đích và lý do

Thầy chấm tiểu luận hướng KH theo 4 nội dung: (1) nghiên cứu tài liệu, xác định từ khóa, tìm thêm tài liệu; (2) xây dựng ít nhất 3 câu hỏi nghiên cứu (RQ) và thử nghiệm bằng công cụ; (3) xây dựng đóng góp khoa học và làm rõ triết lý khoa học; (4) một bài báo đủ để đăng arXiv. **Mục tiêu là điểm A**: "bài báo hoàn thành, đủ điều kiện để công bố/nộp vào arXiv hoặc một hội nghị/tạp chí phù hợp". Slide của thầy yêu cầu nêu bật "cách cải tiến đã thực hiện, các thực nghiệm chứng minh các cải tiến", nên đề tài phải có **một cải tiến đo được** so với một phương pháp gốc.

Phương pháp gốc được chọn là **SemLoc** (arXiv 2603.29109, UC Riverside + Cisco Research), một trong 3 bài thầy giao. SemLoc định vị **lỗi ngữ nghĩa** — lỗi mà test pass và test fail chạy qua cùng các dòng code, khiến định vị lỗi dựa trên độ phủ (SBFL) thất bại. SemLoc nhờ LLM sinh ràng buộc ngữ nghĩa dạng có cấu trúc (cbfl-ir), cài chúng vào chương trình, chạy test để lấy **phổ vi phạm ràng buộc** (ma trận ràng buộc × test), chấm điểm Ochiai trên phổ đó, rồi dùng **kiểm chứng phản thực tế** (LLM vá thử dòng nghi ngờ, chạy lại test) để lọc nhiễu. Kết quả bài báo: Acc@1 42.8%, Acc@3 68% trên SemFault-250, so với SBFL-Ochiai 6.4% / 13.2%.

**Phát hiện quan trọng (08/11):** tác giả đã công bố đầy đủ mã nguồn, benchmark và kết quả tại https://github.com/jerry729/SemLoc (Apache-2.0, cập nhật 28/10/2026):
- `src/` — toàn bộ pipeline + baseline (SBFL, delta debugging, LLM hỏi thẳng `llm_direct_fl.py`, chạy BugsInPy `bip_runner.py`)
- `benchmark/` — SemFault-250: 250 chương trình Python, 250 bộ pytest, `ground_truth.json` (file, hàm, dòng lỗi)
- `results/RQ1/` — 13 cấu hình đã chạy sẵn (SemLoc Claude/Gemini × T=0/0.3/0.8, SBFL Ochiai/Tarantula, DD, các ablation), mỗi cấu hình có `constraints/`, `violations/`, `scores/`, `results/`
- `results/RQ3/bugsInPy_results/` — 465 file JSON; bài báo nói SemLoc chỉ chạy trọn được 68/463 lỗi BugsInPy
- `scripts/reproduce_rq{1,2,3}.sh`, lệnh `semloc report` in lại bảng mà không cần API

Vì vậy đề tài **không tự cài lại SemLoc**, mà dùng mã gốc để (a) tái hiện, (b) xây cải tiến trên đó, (c) đánh giá độ bền ở những chỗ bài gốc còn yếu.

**Triết lý khoa học** (dùng cho nội dung 3): *"LLM đưa ra giả thuyết, bằng chứng thực thi mới là người phán xử."* Không kết luận nào của LLM được tin nếu chưa được kiểm chứng bằng việc chạy chương trình. Kèm theo đó là tinh thần **khoa học tái hiện được**: kiểm tra lại kết quả đã công bố bằng mô hình khác, dữ liệu khác, và công bố đầy đủ dữ liệu của chính mình.

## 2. Câu hỏi nghiên cứu

- **RQ1 — Tái hiện và kiểm tra cách đánh giá.** Kết quả của SemLoc có tái hiện được khi (a) tính lại từ log đã công bố và (b) chạy lại bằng mô hình hiện có của nhóm (Gemini qua proxy) không? Khoảng chênh so với bài báo là bao nhiêu, và do đâu? (c) Kết quả còn đứng được không khi chấm công bằng và khi bỏ các chi tiết cài đặt không được mô tả trong bài (mục 3.6)?
- **RQ2 — Cải tiến.** Cải tiến của nhóm (mục 4) có tốt hơn SemLoc gốc về độ chính xác (Acc@k) **và** về chi phí (số lượt gọi LLM, token, thời gian) không? Mỗi thành phần của cải tiến đóng góp bao nhiêu (ablation)?
- **RQ3 — Độ bền.** Kết quả của SemLoc và của cải tiến có giữ được khi (a) chuyển sang **lỗi thật** (BugsInPy), (b) chuyển sang **code LLM khó đã thấy** (SemFault-250 bị đổi tên định danh/làm nhiễu bề mặt), và (c) đổi **họ mô hình** (Gemini ↔ Claude ↔ GPT, bản mạnh ↔ bản nhẹ) không?

Thêm một câu hỏi phụ dùng để phân loại, không tính là RQ: lỗi nào là "lỗi ngữ nghĩa" theo định nghĩa khách quan ở mục 3.3.

## 3. Thiết kế thực nghiệm

### 3.1 Benchmark

| Nguồn | Vai trò | Ghi chú |
|---|---|---|
| **SemFault-250** (của SemLoc) | Benchmark chính cho RQ1, RQ2 | Chia **dev / test** cố định (50 / 200, chia ngẫu nhiên có seed, phân tầng theo nhãn ngữ nghĩa ở mục 3.3 — benchmark không kèm nhãn miền ứng dụng theo từng chương trình) — cải tiến chỉ được thiết kế và chỉnh tham số trên dev, kết quả báo cáo trên test. |
| **SemFault-250 đổi tên** | RQ3(b) | Biến đổi giữ nguyên ngữ nghĩa: đổi tên hàm/biến/hằng sang tên vô nghĩa, xóa docstring/comment, có thể đảo thứ tự hàm phụ. Phải giữ nguyên số dòng hoặc ánh xạ lại dòng lỗi; phải kiểm tra test vẫn cho đúng kết quả pass/fail như bản gốc. |
| **BugsInPy — tập con** | RQ3(a) | Dùng hạ tầng `bip_runner.py` của SemLoc; ưu tiên 68 lỗi họ đã chạy trọn. **Log RQ3 đã công bố không dùng lại được để chấm CovGate** (382/450 file chỉ chứa lỗi; 68 file còn lại chỉ có tóm tắt, không có constraints/violations, không có dữ liệu độ phủ) → bắt buộc dựng lại môi trường. Ngưỡng: **≥20 lỗi chạy trọn** cả SBFL, SemLoc và CovGate. **Trạng thái 08/11:** 31 lỗi youtube-dl dựng được (môi trường riêng theo requirements, test fail ở commit lỗi và pass ở commit sửa, đo được độ phủ) → ngưỡng **tạm đạt**, chờ SemLoc/CovGate chạy trọn; cả 31 lỗi cùng một project (nêu trong Threats). 35 lỗi của 6 project khác hỏng ở khâu môi trường. Chi tiết `docs/literature/bugsinpy-setup.md`. |
| **SemFault-250 đã sửa** (SemFault-250-repaired, nhóm tạo) | RQ1, RQ2 (độ bền theo ground truth) | Ground truth được **kiểm chứng bằng thực thi**: một dòng là dòng lỗi nếu vá đúng một dòng ở đó (thay thế, hoặc chèn với lỗi thiếu mã) làm **mọi test pass**. LLM chỉ đề xuất bản vá cho các dòng ứng viên (±4 dòng quanh ground truth gốc, trong hàm đích); test phán xử. Mỗi chương trình có nhãn `confirmed` / `corrected` / `unverifiable`. Mọi bảng chính báo cáo thêm trên ground truth đã kiểm chứng. Phát hành kèm bài. |
| **SemFault-250 đã rà soát** (nhóm tạo, Phase 5) | RQ1–RQ3, bộ nhãn thứ ba | LLM (Fable, mức high) rà trước cả 250 nhãn; 6 thành viên duyệt 111 nhãn bị dời hoặc bị LLM nghi sai (người duyệt có xem gợi ý của LLM; đồng ý với gợi ý ở cả 111 ca); trưởng nhóm sửa 5 ca dựa trên kết quả chạy test. Cho phép nhãn hai dòng (lỗi trải hai dòng). `data/semfault_reviewed_gt.json`, `scripts/build_reviewed_gt.py`. Có nguy cơ vòng tròn (nhãn do LLM đề xuất, chấm phương pháp dùng LLM) nên là **góc nhìn độ nhạy**, kết quả chính vẫn báo trên bộ gốc và bộ đã sửa. |
| QuixBugs (Python) | Tùy chọn | Chỉ thêm nếu còn thời gian; không bắt buộc. |

### 3.2 Phương pháp được so sánh

1. SBFL-Ochiai, SBFL-DStar (Tarantula có sẵn trong log thì báo cáo luôn)
2. LLM hỏi thẳng (`llm_direct_fl.py` — tương ứng SemLoc† trong bài)
2b. **LLM + bằng chứng độ phủ** (baseline mạnh mà đơn giản, nhóm thêm): một prompt gồm hàm có đánh số dòng, test fail kèm thông báo lỗi, và số test fail/pass chạy qua từng dòng; LLM trả về 5 dòng nghi ngờ nhất. Trả lời câu hỏi "pipeline nhiều bước của SemLoc có cần không?"
2c. **LLM + test fail** (ablation của 2b, Phase 5): cùng prompt nhưng bỏ chú thích độ phủ từng dòng. Kết quả: độ phủ không giúp (Acc@3 +2,1 [−0,2; +4,9], Acc@1 −5,4 [−9,4; −2,1]); thông tin test fail mới là tín hiệu chính (+27,2 Acc@3 so với LLM hỏi thẳng).
3. SemLoc gốc (có / không kiểm chứng phản thực tế)
4. **Cải tiến của nhóm** (mục 4), cùng các biến thể ablation
5. **Đề xuất rồi kiểm chứng** (PAV, Phase 5, mục 4b)

### 3.3 Định nghĩa "lỗi ngữ nghĩa" (khách quan, tự động)

Một lỗi được gắn nhãn **ngữ nghĩa** (`semantic`) nếu dòng lỗi thật được **cả test fail lẫn ít nhất một test pass** chạy qua (tính bằng coverage.py theo từng test); **lộ ra qua độ phủ** (`coverage_revealed`) nếu test fail chạy qua mà không test pass nào chạy qua; và **không được thực thi** (`not_executed`) nếu không test fail nào chạy qua dòng lỗi thật — trên SemFault-250 nhãn này gồm 65 chương trình, 56 trong đó có ground truth trỏ vào dòng trống (xem `docs/literature/benchmark-notes.md`). Kết quả báo cáo cả tập đầy đủ và tập 185 chương trình có dòng lỗi thực thi được. Mọi kết quả Acc@k được báo cáo cả tổng và tách theo hai nhãn này. Đây cũng chính là điều kiện mà SemLoc nói SBFL thất bại, nên tiêu chí khớp với bài gốc mà không phụ thuộc người gán nhãn.

### 3.4 Chỉ số

- **Độ chính xác:** Acc@1, Acc@3, Acc@5 (cấp dòng, khớp `ground_truth.json`), thứ hạng trung vị, %Susp (tỉ lệ dòng bị đánh dấu nghi ngờ). Báo cáo **hai cách chấm song song**: (i) **cách của tác giả** (mã `print_results.py`: hòa điểm theo thứ tự dòng, DD tính mọi dòng trúng là hạng 1, bỏ chương trình chạy lỗi khỏi mẫu số) để so sánh được với bài; (ii) **cách công bằng** (hòa điểm = hạng trung bình, mẫu số cố định — chương trình không chạy được tính là trượt). Mỗi cách báo cáo trên tập đầy đủ và tập 185 chương trình có dòng lỗi thực thi được.
- **Chi phí:** số lượt gọi LLM, token vào/ra, thời gian chạy cho mỗi chương trình; vẽ **biểu đồ chi phí – độ chính xác** (Pareto) cho mọi phương pháp và model.
- **Độ ổn định:** độ lệch Acc@k giữa các lần chạy lặp.

### 3.5 Thống kê

- Mỗi cấu hình có LLM chạy lặp **ít nhất 3 lần** (mục tiêu 5 nếu quota cho phép); báo cáo trung bình ± độ lệch chuẩn.
- So sánh cặp phương pháp trên cùng tập lỗi bằng **McNemar** (đúng/sai ở Top-k) hoặc **Wilcoxon** (thứ hạng), kèm p-value và effect size.
- Không khẳng định "tốt hơn" nếu không có ý nghĩa thống kê; khi đó ghi đúng là "tương đương" hoặc "không đủ bằng chứng".

### 3.6 Kiểm tra cách đánh giá của SemLoc (audit, thuộc RQ1)

Phát hiện khi đọc mã và log công bố (08/11), mỗi điểm được kiểm chứng bằng số liệu trong repo:
1. **Kiểm chứng phản thực tế (CF) không đổi Acc@k trong mã công bố**: Acc@k lấy từ `scores/ranked_lines`; CF chỉ ảnh hưởng %Susp và thống kê RQ2. Trên lượt chạy của nhóm, top-1 và thứ hạng giống hệt 50/50 chương trình khi có/không CF. Mức "+12 pp Acc@1 nhờ CF" trong bài so hai lượt sinh ràng buộc khác nhau.
2. **Điểm cộng cho dòng LLM tự đoán**: `apply_fault_line_prior` cộng 1,2 vào `fault_line` do LLM đề xuất — không thấy mô tả trong bài → ablation "không prior".
3. **DD**: log công bố cho Acc@1 38,0%, bài ghi 0,0% (mã tính mọi dòng trúng trong tập tối thiểu là hạng 1).
4. **Ground truth**: 56/250 chương trình trỏ vào dòng trống, 9 chương trình trỏ vào dòng không test fail nào chạy qua (giả thuyết: lỗi thiếu mã).
5. **Cách chấm có lợi** (mục 3.4 (i)); không có kết quả công bố cho Claude T = 0.

### 3.7 Phân tích cấu trúc benchmark

Đo mức trùng lặp / dùng chung khuôn mẫu giữa 250 chương trình (so khớp cấu trúc AST sau khi chuẩn hóa tên và hằng, cùng các họ tên như `allocate_*_cut`). Báo cáo số cụm khuôn mẫu; kiểm định thống kê có thêm phiên bản theo cụm (bootstrap theo cụm) để không coi các chương trình gần giống nhau là quan sát độc lập.

## 4. Cải tiến đề xuất (định hướng đã chốt, chi tiết để builder thiết kế)

**Ý tưởng:** SemLoc bỏ hẳn tín hiệu độ phủ, trong khi độ phủ và ràng buộc ngữ nghĩa bổ sung cho nhau — độ phủ loại được dòng mà test fail không đi qua; ràng buộc phân biệt được dòng mà cả test pass lẫn fail đều đi qua. Cải tiến (tên tạm: **CovGate**) gồm ba thành phần, mỗi thành phần tắt được để làm ablation:

1. **Cổng độ phủ:** loại khỏi danh sách ứng viên những dòng không được bất kỳ test fail nào chạy qua.
2. **Kết hợp điểm:** xếp hạng theo điểm ràng buộc, dùng điểm SBFL làm tiêu chí phá thế hòa hoặc kết hợp có trọng số (cách cụ thể do builder chọn và chỉnh trên tập dev).
3. **CF xếp hạng lại thật sự:** dùng kết quả CF (ràng buộc Primary/Secondary, không bị prune) để tính lại điểm dòng và đặt các dòng đó lên trước — điều mã gốc không làm (mục 3.6). Chi phí: không thêm lượt gọi so với SemLoc gốc; ghi thêm số lượt gọi CF có thể bỏ nếu chỉ kiểm chứng top-K qua cổng.

4. **Grounded guess (đoán có căn cứ):** chỉ giữ điểm cộng 1,2 cho dòng LLM tự đoán khi dòng đó **có bằng chứng thực thi** — được ít nhất một test fail chạy qua **và** gắn với ít nhất một ràng buộc bị vi phạm trong test fail; không có bằng chứng thì bỏ điểm cộng. Đây là thành phần nhắm thẳng vào Acc@1.

Ablation: tắt từng thành phần; thêm biến thể **bỏ điểm cộng cho dòng LLM đoán** áp cho cả SemLoc gốc lẫn CovGate.

### 4b. Đề xuất rồi kiểm chứng (PAV, Phase 5)

Bằng chứng Phase 5 cho thấy gắn thêm tín hiệu vào SemLoc (CovGate) chỉ giúp ít, còn một prompt có test fail thắng SemLoc. PAV là cải tiến chính mới: (1) **đề xuất** — prompt LLM + test fail (2c) cho tối đa 5 dòng; (2) **kiểm chứng** — với k dòng đầu, LLM đề xuất bản sửa tối thiểu tại đúng dòng đó (bộ đề xuất của `flx.verify_gt`), chạy test; dòng có bản sửa đạt mọi test được đưa lên đầu. Tham số k ∈ {2, 3}, số lần thử ∈ {1, 2}, thứ tự (theo LLM / theo kích thước bản sửa), giới hạn kích thước bản sửa ∈ {1, 2, 3, không giới hạn} — **chọn trên dev** bằng Acc@1 trung bình trên bộ gốc và bộ đã rà soát (không dùng bộ đã sửa vì bộ đó dựng bằng chính cơ chế sửa thử), rồi chạy một lần trên test và BugsInPy. Mã: `src/flx/pav.py`, `scripts/run_pav.py`, `scripts/pav_eval.py`. Nếu PAV không thắng LLM + test fail, báo cáo như kết quả âm tính ("khi LLM đã đọc test fail, chạy test xác nhận không thêm được gì").

**Phân rã độ chính xác ("grounded hay guessed", câu trả lời định lượng cho tên bài):** đo Acc@1/Acc@3 cho mọi tổ hợp bật/tắt của {điểm cộng dự đoán LLM, phổ vi phạm ràng buộc, CF xếp hạng lại, độ phủ} trên 3 lần lặp × 200 chương trình test; quy ra phần đóng góp của từng thành phần (giá trị Shapley trên các tổ hợp) kèm khoảng tin cậy bootstrap. Chạy offline trên đầu ra đã có, không thêm lượt gọi LLM.

**Quy trình đánh giá cho định vị lỗi bằng LLM (checklist):** đúc kết audit thành danh sách kiểm tra dùng lại được — xử lý hòa điểm, mẫu số cố định, kiểm chứng ground truth bằng thực thi, tách ablation các thành phần không được mô tả (ví dụ điểm cộng dự đoán), lặp và kiểm định — và áp nó cho mọi phương pháp trong bài (SBFL, LLM hỏi thẳng, LLM + độ phủ, SemLoc, CovGate) để phát hiện không chỉ gắn với một công cụ.

**Hai nguồn bằng chứng cho RQ2:**
- **Bằng chứng chính:** các lượt chạy của nhóm — SemLoc gốc và CovGate bằng Gemini 3.8 Flash qua proxy, **T = 0.8** (cấu hình tốt nhất trong bài), mức suy luận mặc định, **3 lần lặp** trên 200 chương trình tập test. CovGate dùng **cùng** constraints/violations của mỗi lượt chạy SemLoc, chỉ khác bước chấm điểm và kiểm chứng phản thực tế, nên so sánh là ghép cặp và kiểm định được. Đây là khoản tốn LLM lớn nhất của dự án; quy mô cuối cùng chốt sau khi đo quota (việc 2.1).
- **Bằng chứng phụ:** thành phần 1–2 (và ablation không prior) chấm lại trên log SemLoc đã công bố (log không có thư mục CF nên thành phần 3 chỉ đo được trên lượt chạy của nhóm) (Gemini 2.5 Pro và Claude Sonnet 4.6, T = 0 / 0.3 / 0.8, mỗi cấu hình 1 lần chạy) — không tốn lượt gọi LLM, cho thấy cải tiến không phụ thuộc mô hình; báo cáo rõ là chạy đơn, không kiểm định lặp.

Mục tiêu đo được của cải tiến: Acc@1/Acc@3 cao hơn SemLoc gốc trên tập test **và/hoặc** ít lượt gọi LLM hơn ở cùng độ chính xác. Nếu cải tiến không thắng, bài vẫn báo cáo trung thực như một kết quả âm tính kèm phân tích nguyên nhân.

## 5. Hạ tầng

- **LLM qua proxy:** `cli-proxy-api` (image `eceasy/cli-proxy-api:v8.0.28`), API kiểu OpenAI tại `http://localhost:8317/v1`, compose `infra/proxy/compose.yaml`. Tài khoản trong Docker volume `vipharmind_cli_proxy_auth`: **4 Antigravity** (Gemini, gpt-oss), **4 Codex free** (GPT luna), **1 Claude**. Cấu hình là bản sao riêng `infra/proxy/config.yaml` (không commit vì chứa khóa) của cấu hình vipharmind, đã **bỏ các quy tắc ép mức suy luận** cho model của dự án; repo vipharmind không bị sửa.
- **Phân vai mô hình** (chi tiết `infra/proxy/MODELS.md`): chính `gemini-3.8-flash-high` (upstream trả lời bằng `gemini-3.8-flash-n`, gateway ghi `served_model` mỗi lượt) cho RQ1b, RQ2, RQ3a, RQ3b; RQ3c trên tập con 50 chương trình: `claude-sonnet-5-5`, `gpt-6-luna`, `gpt-oss-120b-medium` (mã nguồn mở), `gemini-3.5-flash-lite`; `claude-sonnet-4-6` chỉ để đối chiếu tái hiện với log tác giả.
- **Mức suy luận: mặc định của nhà cung cấp cho mọi model** (quyết định của chủ dự án). Đo được: Gemini 3.8 suy nghĩ động (bài ngắn ≈ medium, prompt SemLoc trung vị ~3.450 token đầu ra, tới 478 s/lượt); Flash-Lite và Claude không suy luận; luna ≈ medium. So sánh RQ3c là "ở mặc định của từng nhà cung cấp", không phải cùng mức suy luận. Timeout gateway 600 s, lượt timeout thử lại 1 lần.
- **Nối SemLoc với proxy:** SemLoc gọi OpenAI qua `OpenAI(api_key=...)`, nên đặt `OPENAI_BASE_URL` là đủ cho nhánh OpenAI; nhánh `gemini-*` (google-genai) và `claude-*` (AnthropicVertex) gọi thẳng, cần một lớp chuyển nhỏ để mọi lượt gọi đi qua proxy. Sửa tối thiểu, giữ nguyên prompt và logic của SemLoc để không làm hỏng tính tái hiện.
- **Ghi log mọi lượt gọi LLM** (model, served model, token, thời gian, lỗi) và **cache theo nội dung + run_id** để chạy lại không tốn quota; log là một phần của dữ liệu công bố. Mỗi lần lặp = một run_id = một workdir riêng; mỗi lượt chạy phải qua `flx.run_health` (không còn lỗi LLM chưa khắc phục, không có CF lỗi) trước khi số liệu được dùng.
- Máy: WSL2, không GPU, có Python 3, pdflatex/xelatex, Docker.
- **Kiểm tra quota trước** khi lên lịch chạy lớn: đo số lượt gọi/giờ thực tế của từng tài khoản.

## 6. Sản phẩm và nơi lưu

| Sản phẩm | Ngôn ngữ | Định dạng | Vị trí |
|---|---|---|---|
| Báo cáo đầy đủ | Tiếng Việt | LaTeX theo quy cách trường: Times New Roman 13pt, lề trên 3.5 / dưới 3 / trái 2.5 / phải 2.5 cm, giãn dòng 1.5, tiêu đề chương 16 đậm, đánh số mục tối đa 4 cấp, mỗi nhóm tiểu mục ≥2 mục, hình/bảng đánh số theo chương, số trang giữa chân trang; có bìa, cam kết trung thực, mục lục, danh sách bảng/hình/viết tắt, tài liệu tham khảo theo mẫu IEEE trong hướng dẫn | `docs/report/` |
| Bài báo (báo cáo tóm tắt) | Tiếng Anh | LaTeX dạng bài báo arXiv (Introduction, Related Work, Background, Approach, Evaluation, Threats, Conclusion) | `docs/report/` (thư mục con riêng) |
| Slide báo cáo lần 1, lần 2, slide bảo vệ | Tiếng Việt | PPTX dựng từ `docs/presentation/template-vi.pptx` | `docs/presentation/` |
| Mã nguồn + dữ liệu + log LLM | — | Repo này; SemLoc gốc được đưa vào như mã bên ngoài có ghi nguồn và giấy phép | thư mục mã nguồn ở gốc repo (tên do builder đặt) |
| Gói artifact công khai | Tiếng Anh | Repo GitHub công khai `doanan293/grounded-or-guessed` (không làm DOI/Zenodo — chủ dự án quyết 09/11; bài báo chỉ dẫn link GitHub), Dockerfile chạy offline, `REPRODUCE.md` tái hiện từng bảng; gói lượt chạy + log + cache LLM (đã quét bí mật) do `scripts/export_artifact.py` tạo, đính kèm GitHub Release khi nộp | đã xong ở Phase 3 |

**Phiên bản và nhánh (chủ dự án quyết 09/11).** Viết trọn bài cuối cùng trước trên `main`; báo cáo VI và bài báo EN dùng **một nguồn LaTeX** với công tắc phiên bản `lan1` / `lan2` / `full` quyết định chương nào được đưa vào. Hai nhánh tiến độ được cắt từ `main` sau khi bài đầy đủ xong, chỉ khác công tắc và bộ slide; mã nguồn và dữ liệu giống nhau ở cả ba nhánh. Sửa theo góp ý của thầy luôn làm trên `main` rồi cắt lại nhánh.

| Nhánh | Dùng cho | Nội dung (4 nội dung thầy chấm) |
|---|---|---|
| `bao-cao-lan-1` | 18–19/11 (cần ≥2/4) | báo cáo VI bản `lan1`: nội dung 1 (tài liệu, từ khóa, nghiên cứu liên quan) + nội dung 2 (3 RQ, thiết kế, kết quả RQ1–RQ3); slide lần 1 |
| `bao-cao-lan-2` | 25–26/11 (cần ≥3/4) | báo cáo VI bản `lan2`: thêm nội dung 3 (phân tích thất bại, đóng góp, triết lý khoa học, Threats); bản nháp bài báo EN; slide lần 2 |
| `main` | nộp cuối, bảo vệ (12/2026) | đủ 4/4: báo cáo VI `full`, bài báo EN arXiv đầy đủ, slide bảo vệ |

Báo cáo đầy đủ và bài báo dùng chung số liệu, bảng, hình; nên sinh bảng/hình tự động từ kết quả thực nghiệm để hai bản luôn khớp.

## 7. Lộ trình 4 phase

Mốc của thầy: **báo cáo lần 1 ngày 18–19/11** (cần xong 2/4 nội dung), **lần 2 ngày 25–26/11** (cần 3/4), **nộp và bảo vệ tháng 12** (ngày cụ thể chưa biết — tạm đặt xong mọi thứ trước 12/12).

### Phase 1 — Tài liệu và nền tảng (làm xong 08/11)
- 1.1 Đọc sâu SemLoc (bài + mã nguồn) và 2 bài còn lại (EffiHolmes, Crash report + LLM)
- 1.2 Tìm thêm ~20 tài liệu liên quan (SBFL, MBFL, định vị lỗi bằng LLM như AutoFL/AgentFL/FlexFL, benchmark Defects4J/BugsInPy, nhiễm dữ liệu huấn luyện của LLM); chốt bộ từ khóa; lập bảng so sánh
- 1.3 Khung LaTeX cho báo cáo VI và bài báo EN, file `.bib` chung

### Phase 2 — RQ và thực nghiệm (làm xong 08–09/11)
- 2.1 Dựng proxy cho dự án, gọi thử từng họ mô hình, đo quota
- 2.2 Cài SemLoc, chạy `semloc report` tái hiện bảng từ log có sẵn (RQ1a)
- 2.3 Nối SemLoc với proxy; chạy trên tập dev để kiểm tra pipeline, chi phí và mức suy luận (chạy kiểm tra, không phải số liệu báo cáo)
- 2.4 Gắn nhãn lỗi ngữ nghĩa (mục 3.3), chia dev/test
- 2.5 Thiết kế và cài CovGate trên tập dev, đánh giá trên log có sẵn (không tốn LLM)
- 2.6 Chuẩn bị dữ liệu RQ3: SemFault-250 đổi tên, tập con BugsInPy
- 2.7 Chạy đủ lưới thực nghiệm (RQ1b, RQ2 kể cả thành phần 3, RQ3) — kế hoạch chi tiết `docs/superpowers/plans/2026-11-08-milestone2-phase2-thuc-nghiem.md`
- Chạy mẫu nhỏ chỉ để kiểm tra khói (3–5 chương trình) hoặc kiểm tra hướng ý tưởng; số liệu báo cáo luôn từ lượt chạy đầy đủ.

**Báo cáo lần 1 (18–19/11)** mang lên: tổng quan tài liệu + từ khóa, 3 RQ, phương pháp, **kết quả RQ1 (tái hiện + audit) và RQ2 đầy đủ**, RQ3 sơ bộ — vượt mức 2/4 nội dung thầy yêu cầu.

### Phase 3 — Phân tích và đóng góp (làm xong 09/11, plan `docs/superpowers/plans/2026-11-09-phase3-phan-tich-dong-gop.md`)
- 3.1 Thống kê, kiểm định, ablation, chi phí
- 3.2 Phân tích 15–20 ca thất bại, xếp nhóm nguyên nhân
- 3.3 Chốt danh sách đóng góp và phần triết lý khoa học
- 3.4 Sửa theo góp ý của thầy sau lần 1 (sau 18–19/11, làm trên `main`)
- Đã thêm (chủ dự án duyệt 09/11): baseline LLM + độ phủ chạy trên BugsInPy và trên tập đổi tên (Task 0); loại khỏi ground truth đã sửa các vị trí "sửa" ở dòng trống (13 chương trình) sau final review; phát hiện mơ hồ "đầu khối – thân khối" của Acc@1 cấp dòng; mọi con số trong tài liệu là macro sinh từ `data/` (`numbers.tex`, `numbers-vi.tex`) và được `scripts/check_claims.py` đối chiếu.

**Báo cáo lần 2 (25–26/11)** mang lên: RQ3 đầy đủ, phân tích thất bại, danh sách đóng góp và triết lý khoa học, bản nháp bài báo.

### Phase 5 — Ablation, nhãn rà soát, PAV, viết lại (09/11 → trước 18/11; plan `docs/superpowers/plans/2026-11-09-phase5-pav-viet-lai.md`)
- 5.1 Ablation độ phủ (xong): LLM + test fail không độ phủ, 3 lần × 200 test; trên BugsInPy 3 lần × 31 lỗi
- 5.2 SemFault-250 đã rà soát (xong): Fable rà 250 nhãn, nhóm duyệt 111, 5 ca sửa có bằng chứng chạy test
- 5.3 PAV: chọn tham số trên dev → chạy test (3 lần) và BugsInPy (3 lần)
- 5.4 Câu chuyện mới: SemLoc "guessed" ở hạng 1; benchmark có gần một nửa nhãn lệch dòng; một prompt có test fail (điều lập trình viên vẫn làm, nhất là với TDD) thắng pipeline, độ phủ không giúp; PAV là phiên bản "grounded" thật sự (hoặc kết quả âm tính); benchmark bão hòa khi nhãn đúng → cần lỗi thật
- 5.5 Viết lại báo cáo VI, bài báo EN, slide; review cuối; cắt lại 2 nhánh; push
- Hướng phát triển (không làm): ablation giấu tên test; định vị cấp dự án (thu hẹp từ dự án xuống hàm)

### Phase 4 — Viết trọn bài, rồi cắt 2 nhánh báo cáo (bắt đầu 09/11, trước 18/11)
- 4.0 Dàn ý chi tiết báo cáo VI + bài báo EN — chủ dự án duyệt trước khi viết
- 4.1 Báo cáo đầy đủ tiếng Việt trên `main`, có công tắc phiên bản `lan1` / `lan2` / `full`
- 4.2 Bài báo tiếng Anh (arXiv), cùng số liệu qua macro
- 4.3 Tự phản biện theo 5 chiều (đóng góp, độ rõ, sức mạnh thực nghiệm, độ đầy đủ đánh giá, độ hợp lý của thiết kế); `check_claims.py` cho mọi con số
- 4.4 Slide lần 1 (số liệu mới), slide lần 2, slide bảo vệ
- 4.5 Cắt nhánh `bao-cao-lan-1`, `bao-cao-lan-2` từ `main`; push
- 4.6 Sau mỗi buổi báo cáo: sửa theo góp ý trên `main`, cắt lại nhánh; nộp cuối tháng 12 (gói lượt chạy đính kèm GitHub Release)

## 8. Tiêu chí "đạt điểm A"

1. Đóng góp nói được trong một câu: *tái hiện độc lập SemLoc, chỉ ra hạng 1 của nó là dòng LLM đoán và kết quả phụ thuộc vào cách đánh giá và benchmark (gần một nửa nhãn lệch dòng), sửa và rà soát benchmark (SemFault-250 đã sửa / đã rà soát), cho thấy một prompt có test fail thắng pipeline còn độ phủ không giúp (ablation), đề xuất PAV — LLM đề xuất, test quyết định — và đánh giá độ bền trên lỗi thật, code đã đổi tên và nhiều họ LLM.*
2. Đánh giá trên SemFault-250 (chia dev/test) **và SemFault-250-verified** + ít nhất một nguồn lỗi thật (BugsInPy) + biến thể đổi tên; kết quả tách theo nhãn ngữ nghĩa / lộ qua độ phủ; có phân tích cấu trúc benchmark (mục 3.7).
3. Đủ các phương pháp so sánh ở mục 3.2, kể cả baseline LLM + độ phủ (2b).
4. Lặp ≥3 lần, có kiểm định thống kê và effect size.
5. Có ablation từng thành phần của CovGate.
6. Có báo cáo chi phí và biểu đồ chi phí – độ chính xác.
7. Có phân tích thất bại.
8. Có mục Threats to Validity; repo công khai có Docker và `REPRODUCE.md` tái hiện từng bảng; người khác chạy lại được (không cần DOI — chủ dự án quyết 09/11).

Thứ tự cắt khi thiếu quota/thời gian: bỏ GPT → giảm số lần lặp (không dưới 3) → thu hẹp BugsInPy. Không cắt mục 1–5.

## 9. Không làm và thất bại cần tránh

**Không làm:** tự cài lại SemLoc; lỗi hiệu năng (hướng EffiHolmes); dữ liệu doanh nghiệp; huấn luyện hay tinh chỉnh mô hình; sửa logic/prompt của SemLoc khi đo SemLoc gốc.

**Coi là thất bại dù làm xong hết:**
- Kết quả chỉ đứng được trên SemFault-250, không có bằng chứng trên lỗi thật hay code đổi tên.
- Có khẳng định trong Abstract/Introduction không có số liệu chống lưng.
- Cải tiến được chỉnh tham số trên chính tập dùng để báo cáo (rò rỉ dev/test).
- Không ai chạy lại được thí nghiệm.
- Trình bày lại SemLoc như đóng góp của nhóm; mọi phần dùng từ SemLoc phải ghi nguồn rõ ràng.

## 10. Rủi ro chính

| Rủi ro | Cách xử lý |
|---|---|
| Quota tài khoản OAuth không đủ | Đo sớm (2.1); cache mọi lượt gọi; CovGate thành phần 1–2 dùng log có sẵn; giảm lặp theo thứ tự cắt ở mục 8 |
| Mô hình qua proxy khác mô hình trong bài (Gemini 2.5 Pro, Claude Sonnet 4.6) | Ghi rõ phiên bản; đây chính là nội dung của RQ1b/RQ3c, không phải lỗi |
| Môi trường BugsInPy khó dựng | Đã dựng 31 lỗi youtube-dl (một project); nêu trong Threats |
| Mức suy luận mặc định làm chi phí và độ trễ cao (Gemini) | Timeout 600 s, cache, theo dõi `run_health`; chạy nền nhiều worker |
| CovGate không thắng | Báo cáo kết quả âm tính trung thực; nhấn đóng góp tái hiện + độ bền |
| Biến thể đổi tên làm hỏng chương trình hoặc lệch dòng lỗi | Kiểm tra tự động: test cho đúng kết quả pass/fail như bản gốc, ánh xạ lại dòng lỗi |

## 11. Quyết định của Claude (chủ dự án chưa duyệt riêng từng điểm)

- Tên tạm "CovGate" và cách chia 3 thành phần của cải tiến
- Tỉ lệ chia dev/test 50/200
- Định nghĩa khách quan của "lỗi ngữ nghĩa" ở mục 3.3
- Số lần lặp tối thiểu 3, mục tiêu 5
- QuixBugs chuyển thành tùy chọn
- Đặt hạn hoàn thành tạm là 12/12
- BugsInPy: giới hạn 3 ngày dựng môi trường, ngưỡng ≥20 lỗi chạy trọn, phương án khi dưới ngưỡng (mục 3.1)
- Bằng chứng chính của RQ2 là lượt chạy Gemini của nhóm ở T = 0.8 × 3 lần; log công bố chỉ là bằng chứng phụ (mục 4)
- CovGate thành phần 3 đổi thành "CF xếp hạng lại thật sự" và thêm ablation "không prior" sau audit (mục 3.6) — chủ dự án đã duyệt 08/11
- Báo cáo song song cách chấm của tác giả và cách chấm công bằng (mục 3.4)
- Cấu hình proxy riêng; mọi model ở mức suy luận mặc định (chủ dự án quyết 08/11)
- Kéo Phase 2 lên trước báo cáo lần 1; chạy mẫu nhỏ chỉ để kiểm tra (chủ dự án quyết 08/11)
- Thêm SemFault-250-verified, baseline LLM + độ phủ, phân tích cấu trúc benchmark, biểu đồ chi phí – độ chính xác, gói artifact (chủ dự án duyệt 08/11; DOI bỏ 09/11)
- Thêm CovGate thành phần 4 "grounded guess", phân rã độ chính xác theo thành phần (Shapley), checklist đánh giá (chủ dự án duyệt 08/11)
- 09/11: bỏ DOI/Zenodo; viết trọn bài trước rồi cắt nhánh báo cáo; thêm baseline LLM + độ phủ trên BugsInPy và tập đổi tên; thứ tự tác giả (chủ dự án quyết)
- 09/11: loại vị trí "sửa" ở dòng trống khỏi ground truth đã sửa (final review Phase 3); báo cáo thêm Acc@1 chấp nhận đầu khối/thân khối (Claude quyết, ghi trong ledger)
- Tên bài: **Grounded or Guessed: A Reproducibility Study of LLM-Based Semantic Fault Localization**; repo công khai `doanan293/grounded-or-guessed` (MIT cho mã của nhóm; SemLoc giữ Apache-2.0)

## 12. Để builder tự quyết

- Công thức kết hợp điểm cụ thể và tham số K của CovGate (chỉnh trên dev)
- Cách đổi tên/làm nhiễu bề mặt cụ thể, miễn giữ ngữ nghĩa và kiểm tra được
- Cấu trúc thư mục mã nguồn, cách tích hợp SemLoc (submodule, vendored copy…), công cụ thống kê
- Mẫu LaTeX cụ thể cho bài báo arXiv; cách dựng slide từ template
- Chọn model cụ thể trong từng họ theo danh sách proxy cung cấp

# Specs tổng quan — Tiểu luận 2KH: Định vị lỗi ngữ nghĩa dựa trên SemLoc

- Môn: IT5440 – Nguyên lý và kỹ thuật phân tích chương trình, kỳ 2026.1, ĐH Bách khoa Hà Nội
- Đề tài: **2KH** — Chương 10 "Phát hiện lỗi và định vị lỗi", hướng nghiên cứu khoa học
- Ngày viết: 08/11/2026
- Người thực hiện: chủ dự án (học viên) + Claude, làm trọn từ đầu đến cuối. Các thành viên khác trong nhóm 7 người không nhận phần việc nào (đã chốt 08/11). Danh sách tên nhóm cho trang bìa và lời cam kết sẽ do chủ dự án cung cấp khi làm báo cáo.
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

- **RQ1 — Tái hiện.** Kết quả của SemLoc có tái hiện được khi (a) tính lại từ log đã công bố và (b) chạy lại bằng mô hình hiện có của nhóm (Gemini qua proxy) không? Khoảng chênh so với bài báo là bao nhiêu, và do đâu?
- **RQ2 — Cải tiến.** Cải tiến của nhóm (mục 4) có tốt hơn SemLoc gốc về độ chính xác (Acc@k) **và** về chi phí (số lượt gọi LLM, token, thời gian) không? Mỗi thành phần của cải tiến đóng góp bao nhiêu (ablation)?
- **RQ3 — Độ bền.** Kết quả của SemLoc và của cải tiến có giữ được khi (a) chuyển sang **lỗi thật** (BugsInPy), (b) chuyển sang **code LLM khó đã thấy** (SemFault-250 bị đổi tên định danh/làm nhiễu bề mặt), và (c) đổi **họ mô hình** (Gemini ↔ Claude ↔ GPT, bản mạnh ↔ bản nhẹ) không?

Thêm một câu hỏi phụ dùng để phân loại, không tính là RQ: lỗi nào là "lỗi ngữ nghĩa" theo định nghĩa khách quan ở mục 3.3.

## 3. Thiết kế thực nghiệm

### 3.1 Benchmark

| Nguồn | Vai trò | Ghi chú |
|---|---|---|
| **SemFault-250** (của SemLoc) | Benchmark chính cho RQ1, RQ2 | Chia **dev / test** cố định (50 / 200, chia ngẫu nhiên có seed, phân tầng theo nhãn ngữ nghĩa ở mục 3.3 — benchmark không kèm nhãn miền ứng dụng theo từng chương trình) — cải tiến chỉ được thiết kế và chỉnh tham số trên dev, kết quả báo cáo trên test. |
| **SemFault-250 đổi tên** | RQ3(b) | Biến đổi giữ nguyên ngữ nghĩa: đổi tên hàm/biến/hằng sang tên vô nghĩa, xóa docstring/comment, có thể đảo thứ tự hàm phụ. Phải giữ nguyên số dòng hoặc ánh xạ lại dòng lỗi; phải kiểm tra test vẫn cho đúng kết quả pass/fail như bản gốc. |
| **BugsInPy — tập con** | RQ3(a) | Dùng hạ tầng `bip_runner.py` của SemLoc; ưu tiên 68 lỗi họ đã chạy trọn. **Log RQ3 đã công bố không dùng lại được để chấm CovGate** (382/450 file chỉ chứa lỗi; 68 file còn lại chỉ có tóm tắt, không có constraints/violations, không có dữ liệu độ phủ) → bắt buộc dựng lại môi trường. Dựng BugsInPy **ngay đầu Phase 2, giới hạn 3 ngày** (10–12/11). Ngưỡng chấp nhận: **≥20 lỗi chạy trọn** cả SBFL, SemLoc và CovGate. Nếu dưới ngưỡng: báo cáo trên số lỗi dựng được, nêu rõ trong Threats to Validity, và nhấn mạnh RQ3(b) (đổi tên) làm bằng chứng độ bền chính. |
| QuixBugs (Python) | Tùy chọn | Chỉ thêm nếu còn thời gian; không bắt buộc. |

### 3.2 Phương pháp được so sánh

1. SBFL-Ochiai, SBFL-DStar (Tarantula có sẵn trong log thì báo cáo luôn)
2. LLM hỏi thẳng (`llm_direct_fl.py` — tương ứng SemLoc† trong bài)
3. SemLoc gốc (có / không kiểm chứng phản thực tế)
4. **Cải tiến của nhóm** (mục 4), cùng các biến thể ablation

### 3.3 Định nghĩa "lỗi ngữ nghĩa" (khách quan, tự động)

Một lỗi được gắn nhãn **ngữ nghĩa** (`semantic`) nếu dòng lỗi thật được **cả test fail lẫn ít nhất một test pass** chạy qua (tính bằng coverage.py theo từng test); **lộ ra qua độ phủ** (`coverage_revealed`) nếu test fail chạy qua mà không test pass nào chạy qua; và **không được thực thi** (`not_executed`) nếu không test fail nào chạy qua dòng lỗi thật — trên SemFault-250 nhãn này gồm 65 chương trình, 56 trong đó có ground truth trỏ vào dòng trống (xem `docs/literature/benchmark-notes.md`). Kết quả báo cáo cả tập đầy đủ và tập 185 chương trình có dòng lỗi thực thi được. Mọi kết quả Acc@k được báo cáo cả tổng và tách theo hai nhãn này. Đây cũng chính là điều kiện mà SemLoc nói SBFL thất bại, nên tiêu chí khớp với bài gốc mà không phụ thuộc người gán nhãn.

### 3.4 Chỉ số

- **Độ chính xác:** Acc@1, Acc@3, Acc@5 (cấp dòng, khớp `ground_truth.json`), thứ hạng trung vị, %Susp (tỉ lệ dòng bị đánh dấu nghi ngờ) — dùng đúng định nghĩa và mã tính của SemLoc để so sánh được.
- **Chi phí:** số lượt gọi LLM, token vào/ra, thời gian chạy cho mỗi chương trình.
- **Độ ổn định:** độ lệch Acc@k giữa các lần chạy lặp.

### 3.5 Thống kê

- Mỗi cấu hình có LLM chạy lặp **ít nhất 3 lần** (mục tiêu 5 nếu quota cho phép); báo cáo trung bình ± độ lệch chuẩn.
- So sánh cặp phương pháp trên cùng tập lỗi bằng **McNemar** (đúng/sai ở Top-k) hoặc **Wilcoxon** (thứ hạng), kèm p-value và effect size.
- Không khẳng định "tốt hơn" nếu không có ý nghĩa thống kê; khi đó ghi đúng là "tương đương" hoặc "không đủ bằng chứng".

## 4. Cải tiến đề xuất (định hướng đã chốt, chi tiết để builder thiết kế)

**Ý tưởng:** SemLoc bỏ hẳn tín hiệu độ phủ, trong khi độ phủ và ràng buộc ngữ nghĩa bổ sung cho nhau — độ phủ loại được dòng mà test fail không đi qua; ràng buộc phân biệt được dòng mà cả test pass lẫn fail đều đi qua. Cải tiến (tên tạm: **CovGate**) gồm ba thành phần, mỗi thành phần tắt được để làm ablation:

1. **Cổng độ phủ:** loại khỏi danh sách ứng viên những dòng không được bất kỳ test fail nào chạy qua.
2. **Kết hợp điểm:** xếp hạng theo điểm ràng buộc, dùng điểm SBFL làm tiêu chí phá thế hòa hoặc kết hợp có trọng số (cách cụ thể do builder chọn và chỉnh trên tập dev).
3. **Kiểm chứng phản thực tế tiết kiệm:** chỉ gọi LLM vá thử cho các ràng buộc có dòng gán điểm đi qua cổng và nằm trong top-K, nhằm giảm số lượt gọi LLM.

**Hai nguồn bằng chứng cho RQ2:**
- **Bằng chứng chính:** các lượt chạy của nhóm — SemLoc gốc và CovGate bằng Gemini qua proxy, **T = 0.8** (cấu hình tốt nhất trong bài), **3 lần lặp** trên 200 chương trình tập test. CovGate dùng **cùng** constraints/violations của mỗi lượt chạy SemLoc, chỉ khác bước chấm điểm và kiểm chứng phản thực tế, nên so sánh là ghép cặp và kiểm định được. Đây là khoản tốn LLM lớn nhất của dự án; quy mô cuối cùng chốt sau khi đo quota (việc 2.1).
- **Bằng chứng phụ:** thành phần 1–2 chấm lại trên log SemLoc đã công bố (Gemini 2.5 Pro và Claude Sonnet 4.6, T = 0 / 0.3 / 0.8, mỗi cấu hình 1 lần chạy) — không tốn lượt gọi LLM, cho thấy cải tiến không phụ thuộc mô hình; báo cáo rõ là chạy đơn, không kiểm định lặp.

Mục tiêu đo được của cải tiến: Acc@1/Acc@3 cao hơn SemLoc gốc trên tập test **và/hoặc** ít lượt gọi LLM hơn ở cùng độ chính xác. Nếu cải tiến không thắng, bài vẫn báo cáo trung thực như một kết quả âm tính kèm phân tích nguyên nhân.

## 5. Hạ tầng

- **LLM qua proxy:** `cli-proxy-api` (image `eceasy/cli-proxy-api:v8.0.28`), API kiểu OpenAI tại `http://localhost:8317/v1`. Tài khoản đăng nhập nằm trong Docker volume `vipharmind_cli_proxy_auth` (hiện có 3 tài khoản Antigravity cho Gemini, 1 tài khoản Claude; tài khoản Codex cũ đã xóa). Cấu hình mẫu ở `/home/andv/personal/vipharmind/devops/cli-proxy-api/config.yaml`. Dự án tiểu luận có compose riêng, dùng lại volume và config đó, **không sửa gì trong repo vipharmind**.
- **GPT:** chủ dự án sẽ đăng nhập thêm một tài khoản Codex free (OAuth qua trình duyệt, chủ dự án tự chạy lệnh đăng nhập). GPT chỉ dùng cho RQ3(c) trên tập con; thiếu quota thì bỏ.
- **Phân vai mô hình:** Gemini là mô hình chính (RQ1, RQ2); Claude và GPT dùng cho RQ3(c) trên tập con.
- **Nối SemLoc với proxy:** SemLoc gọi OpenAI qua `OpenAI(api_key=...)`, nên đặt `OPENAI_BASE_URL` là đủ cho nhánh OpenAI; nhánh `gemini-*` (google-genai) và `claude-*` (AnthropicVertex) gọi thẳng, cần một lớp chuyển nhỏ để mọi lượt gọi đi qua proxy. Sửa tối thiểu, giữ nguyên prompt và logic của SemLoc để không làm hỏng tính tái hiện.
- **Ghi log mọi lượt gọi LLM** (model, prompt, response, token, thời gian) và **cache theo nội dung** để chạy lại không tốn quota; log này là một phần của dữ liệu công bố.
- Máy: WSL2, không GPU, có Python 3, pdflatex/xelatex, Docker.
- **Kiểm tra quota trước** khi lên lịch chạy lớn: đo số lượt gọi/giờ thực tế của từng tài khoản.

## 6. Sản phẩm và nơi lưu

| Sản phẩm | Ngôn ngữ | Định dạng | Vị trí |
|---|---|---|---|
| Báo cáo đầy đủ | Tiếng Việt | LaTeX theo quy cách trường: Times New Roman 13pt, lề trên 3.5 / dưới 3 / trái 2.5 / phải 2.5 cm, giãn dòng 1.5, tiêu đề chương 16 đậm, đánh số mục tối đa 4 cấp, mỗi nhóm tiểu mục ≥2 mục, hình/bảng đánh số theo chương, số trang giữa chân trang; có bìa, cam kết trung thực, mục lục, danh sách bảng/hình/viết tắt, tài liệu tham khảo theo mẫu IEEE trong hướng dẫn | `docs/report/` |
| Bài báo (báo cáo tóm tắt) | Tiếng Anh | LaTeX dạng bài báo arXiv (Introduction, Related Work, Background, Approach, Evaluation, Threats, Conclusion) | `docs/report/` (thư mục con riêng) |
| Slide báo cáo lần 1, lần 2, slide bảo vệ | Tiếng Việt | PPTX dựng từ `docs/presentation/template-vi.pptx` | `docs/presentation/` |
| Mã nguồn + dữ liệu + log LLM | — | Repo này; SemLoc gốc được đưa vào như mã bên ngoài có ghi nguồn và giấy phép | thư mục mã nguồn ở gốc repo (tên do builder đặt) |

Báo cáo đầy đủ và bài báo dùng chung số liệu, bảng, hình; nên sinh bảng/hình tự động từ kết quả thực nghiệm để hai bản luôn khớp.

## 7. Lộ trình 4 phase

Mốc của thầy: **báo cáo lần 1 ngày 18–19/11** (cần xong 2/4 nội dung), **lần 2 ngày 25–26/11** (cần 3/4), **nộp và bảo vệ tháng 12** (ngày cụ thể chưa biết — tạm đặt xong mọi thứ trước 12/12).

### Phase 1 — Tài liệu và nền tảng (08–14/11)
- 1.1 Đọc sâu SemLoc (bài + mã nguồn) và 2 bài còn lại (EffiHolmes, Crash report + LLM)
- 1.2 Tìm thêm ~20 tài liệu liên quan (SBFL, MBFL, định vị lỗi bằng LLM như AutoFL/AgentFL/FlexFL, benchmark Defects4J/BugsInPy, nhiễm dữ liệu huấn luyện của LLM); chốt bộ từ khóa; lập bảng so sánh
- 1.3 Khung LaTeX cho báo cáo VI và bài báo EN, file `.bib` chung

### Phase 2 — RQ và thực nghiệm (09–24/11)
- 2.1 Dựng proxy cho dự án, gọi thử từng họ mô hình, đo quota
- 2.2 Cài SemLoc, chạy `semloc report` tái hiện bảng từ log có sẵn (RQ1a)
- 2.3 Nối SemLoc với proxy, chạy SemLoc bằng Gemini trên một tập nhỏ → số liệu thử cho báo cáo lần 1
- 2.4 Gắn nhãn lỗi ngữ nghĩa (mục 3.3), chia dev/test
- 2.5 Thiết kế và cài CovGate trên tập dev, đánh giá trên log có sẵn (không tốn LLM)
- 2.6 Chuẩn bị dữ liệu RQ3: SemFault-250 đổi tên, tập con BugsInPy
- 2.7 Chạy đủ lưới thực nghiệm (RQ1b, RQ2 kể cả thành phần 3, RQ3)
- 2.8 Dự phòng 2 ngày (23–24/11)

**Báo cáo lần 1 (18–19/11)** mang lên: bảng tổng quan tài liệu + từ khóa, 3 RQ, sơ đồ phương pháp, kết quả tái hiện từ log (RQ1a) và số liệu chạy thử bằng Gemini.

### Phase 3 — Phân tích và đóng góp (22–28/11)
- 3.1 Thống kê, kiểm định, ablation, chi phí
- 3.2 Phân tích 15–20 ca thất bại, xếp nhóm nguyên nhân
- 3.3 Chốt danh sách đóng góp và phần triết lý khoa học
- 3.4 Sửa theo góp ý của thầy sau lần 1

**Báo cáo lần 2 (25–26/11)** mang lên: kết quả RQ1–RQ2 đầy đủ, RQ3 sơ bộ, danh sách đóng góp.

### Phase 4 — Viết và nộp (27/11–12/12)
- 4.1 Bài báo tiếng Anh
- 4.2 Báo cáo đầy đủ tiếng Việt
- 4.3 Tự phản biện theo 5 chiều (đóng góp, độ rõ, sức mạnh thực nghiệm, độ đầy đủ đánh giá, độ hợp lý của thiết kế); đối chiếu từng khẳng định với số liệu
- 4.4 Đóng gói mã nguồn, dữ liệu, log; hướng dẫn chạy lại
- 4.5 Slide bảo vệ; sửa theo góp ý sau lần 2

## 8. Tiêu chí "đạt điểm A"

1. Đóng góp nói được trong một câu: *tái hiện độc lập SemLoc, đề xuất CovGate kết hợp độ phủ với phổ ngữ nghĩa, và đánh giá độ bền trên lỗi thật, code đã đổi tên và nhiều họ LLM.*
2. Đánh giá trên SemFault-250 (chia dev/test) + ít nhất một nguồn lỗi thật (BugsInPy) + biến thể đổi tên; kết quả tách theo nhãn ngữ nghĩa / lộ qua độ phủ.
3. Đủ các phương pháp so sánh ở mục 3.2.
4. Lặp ≥3 lần, có kiểm định thống kê và effect size.
5. Có ablation từng thành phần của CovGate.
6. Có báo cáo chi phí.
7. Có phân tích thất bại.
8. Có mục Threats to Validity; công bố mã nguồn, dữ liệu, log LLM; người khác chạy lại được.

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
| Môi trường BugsInPy khó dựng | Dựa vào log RQ3 của SemLoc; thu hẹp tập con; nêu trong Threats |
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

## 12. Để builder tự quyết

- Công thức kết hợp điểm cụ thể và tham số K của CovGate (chỉnh trên dev)
- Cách đổi tên/làm nhiễu bề mặt cụ thể, miễn giữ ngữ nghĩa và kiểm tra được
- Cấu trúc thư mục mã nguồn, cách tích hợp SemLoc (submodule, vendored copy…), công cụ thống kê
- Mẫu LaTeX cụ thể cho bài báo arXiv; cách dựng slide từ template
- Chọn model cụ thể trong từng họ theo danh sách proxy cung cấp

# Đóng góp, triết lý khoa học và giới hạn (cập nhật Phase 5)

Mọi con số dưới đây là một macro trong `docs/report/generated/numbers-vi.tex` (sinh từ `data/` bởi `scripts/make_numbers.py`); tên macro ghi trong ngoặc vuông ngay sau số. Kiểm tra lại: `python scripts/check_claims.py docs/analysis/contributions.md`.

**Câu đóng góp (spec §8, tiêu chí 1):** Nhóm tái hiện độc lập SemLoc và chỉ ra rằng hạng 1 của nó là dòng LLM tự đoán theo một lựa chọn thiết kế không được mô tả; gần một nửa nhãn của bộ dữ liệu không trỏ đúng dòng lỗi (nhóm công bố hai bộ nhãn mới); một prompt duy nhất có kiểm thử thất bại — gần với cách nhiều lập trình viên đang làm — thắng quy trình nhiều bước và rẻ hơn khoảng bảy lần; và mọi cách thêm phức tạp mà nhóm thử, cùng phân tích tĩnh, không thêm được gì, vì kiểm thử đủ để gợi ý vị trí lỗi nhưng quá yếu để chứng minh nó.

## 1. Đóng góp

### C1. Hạng 1 của SemLoc là dòng LLM đoán
- **Khẳng định.** Điểm thưởng cho dòng LLM đoán lớn hơn mọi điểm ràng buộc, nên dòng đầu của SemLoc luôn là dòng đoán. Acc@1 của SemLoc 52,3 [`\RqTwoRepairedAllSemlocAccOneMean`] (bộ đã sửa); riêng phổ vi phạm 43,2 [`\RqTwoRepairedAllSemlocNoPriorAccOneMean`]. Trên lỗi thật, Acc@1 của SemLoc bằng đúng của riêng dòng đoán: 46,2 [`\BipAllLlmGuessAccOneMean`]. Bước vá thử chiếm 42 [`\CostCfSharePct`]% lượt gọi LLM nhưng không đổi thứ hạng nào.
- **Bác bỏ nếu** bỏ điểm thưởng mà Acc@1 không đi xuống. Ở đây: −9,1 [`\RqTwoRepairedAllSemlocNoPriorDAccOne`] điểm, CI [−16,7 [`\RqTwoRepairedAllSemlocNoPriorDAccOneLo`]; −1,9 [`\RqTwoRepairedAllSemlocNoPriorDAccOneHi`]] (bộ đã sửa); −26,2 [`\RqTwoReviewedAllSemlocNoPriorDAccOne`] (bộ đã rà soát).
- **Kèm theo (audit):** gỡ lỗi chia đôi 38,0 [`\RqOneDdAuthorAllAccOne`] theo mã chấm của tác giả, 0,0 [`\RqOneDdFairAllAccOne`] khi chấm công bằng; SBFL Acc@5 30,4 [`\RqOneSbflOchiaiAuthorAllAccFive`] so với 48,0 [`\RqOneSbflOchiaiFairAllAccFive`]; hai lỗi của bộ chạy BugsInPy.
- **Bằng chứng.** `data/rq_decomposition.csv`, `data/rq1_audit.csv`, `data/rq1_cf_identity.json`, `data/rq3_bugsinpy.csv`.

### C2. Gần một nửa nhãn của SemFault-250 không trỏ đúng dòng lỗi
- **Khẳng định.** 112 [`\LabaudAllMoved`] trên 250 [`\LabaudAllN`] nhãn gốc bị dời khi rà soát: 56 [`\LabaudAllBlank`] trên dòng trống, 7 [`\LabaudAllNonCode`] trên log/`def`/chú thích, 32 [`\LabaudAllOffByOne`] lệch một dòng, 17 [`\LabaudAllFarther`] xa hơn; 40 [`\LabaudAllExtended`] được giữ và thêm một dòng (lỗi hai dòng).
- **Hai bộ nhãn mới.** *Đã sửa* (kiểm thử quyết định): 82 [`\GtConfirmedN`] xác nhận, 46 [`\GtCorrectedN`] dời vị trí, 226 [`\GtRepairedN`] chương trình. *Đã rà soát*: LLM rà trước cả 250 nhãn, 6 [`\ReviewReviewersN`] thành viên duyệt 111 [`\ReviewHumanN`] nhãn (có xem gợi ý LLM, đồng ý ở 111 [`\ReviewAgreeN`] ca), trưởng nhóm sửa 5 [`\ReviewOverrideN`] ca có bằng chứng chạy kiểm thử; vòng rà soát bác 8 [`\ReviewCorrectedOverturnedN`] lần bộ phán định dời nhãn.
- **Nhãn lệch có thể đã có lợi cho SemLoc.** Trên nhãn gốc SemLoc hơn LLM hỏi thẳng ở Acc@3 (60,3 [`\RqTwoOriginalAllSemlocAccThreeMean`] so với 43,0 [`\RqTwoOriginalAllLlmDirectAccThreeMean`]); trên nhãn đã rà soát hai bên ngang nhau (90,0 [`\RqTwoReviewedAllSemlocAccThreeMean`] so với 90,8 [`\RqTwoReviewedAllLlmDirectAccThreeMean`]); trên nhãn đã sửa SemLoc vẫn hơn (75,4 [`\RqTwoRepairedAllSemlocAccThreeMean`] so với 62,8 [`\RqTwoRepairedAllLlmDirectAccThreeMean`]), nên kết luận này chỉ dựa trên bộ nhãn do LLM gợi ý.
- **Bằng chứng.** `data/label_audit.csv`, `data/semfault_verified_gt.json`, `data/semfault_reviewed_gt.json`, `docs/analysis/gt-review/`.
- **Duyệt mù** (60 [`\BlindBlindAllPrograms`] chương trình, mỗi ca 2 người chưa từng xem, không có gợi ý LLM): hai người chọn trùng dòng ở 37 [`\BlindBlindAllPairsAgree`]/42 [`\BlindBlindAllPairs`] cặp; 71 [`\BlindBlindAllMatchReviewed`]/84 [`\BlindBlindAllNReviewed`] câu trả lời trùng nhãn đã rà soát, 38 [`\BlindBlindAllMatchOriginal`] trùng nhãn gốc; 36 [`\BlindAnswersExcluded`]/120 [`\BlindAnswersTotal`] câu dẫn lại tệp duyệt cũ nên bị loại. Nhóm khó nhất là nhãn LLM giữ nguyên (25 [`\BlindBlindKeptMatchReviewed`]/36 [`\BlindBlindKeptNReviewed`]), toàn lỗi thiếu câu lệnh.
- **Giới hạn.** Vòng đầu người duyệt xem gợi ý; duyệt mù chỉ trên mẫu nhỏ; kết quả chính báo trên bộ gốc và bộ đã sửa.

### C3. Một prompt có kiểm thử thất bại thắng quy trình nhiều bước
- **Khẳng định.** LLM + kiểm thử thất bại hơn SemLoc ở Acc@1 trên cả ba bộ nhãn: +7,7 [`\RqTwoOriginalAllLlmTestsDAccOne`] (gốc), +10,2 [`\RqTwoRepairedAllLlmTestsDAccOne`] CI [+5,3 [`\RqTwoRepairedAllLlmTestsDAccOneLo`]; +16,0 [`\RqTwoRepairedAllLlmTestsDAccOneHi`]] (đã sửa), +12,5 [`\RqTwoReviewedAllLlmTestsDAccOne`] (đã rà soát); Acc@3 +14,5 [`\RqTwoRepairedAllLlmTestsDAccThree`] (đã sửa). Chi phí 2,0 [`\CostLlmTestsTokensK`] nghìn token mỗi chương trình so với 14,0 [`\CostSemlocTokensK`] nghìn.
- **Trên lỗi thật:** Acc@3 71,0 [`\BipAllLlmTestsAccThreeMean`] so với 53,8 [`\BipAllSemlocPriorAccThreeMean`], CI [−3,2 [`\BipAllLlmTestsDAccThreeLo`]; +36,6 [`\BipAllLlmTestsDAccThreeHi`]] còn chứa 0.
- **Bằng chứng.** `data/rq2_ours.csv`, `data/rq3_bugsinpy.csv`, `data/llm_cost.csv`.
- **Giới hạn.** Một mô hình chính; một hàm mỗi lần; tên kiểm thử của bộ dữ liệu mô tả rất rõ ý định.

### C4. Thêm phức tạp không thu hẹp được khoảng cách — và vì sao
- **Kiểm thử thất bại là tín hiệu chính:** Acc@3 +27,2 [`\AblRepairedAllTestsEffectDAccThree`] so với LLM hỏi thẳng. **Độ phủ không giúp:** Acc@3 +2,1 [`\AblRepairedAllCoverageEffectDAccThree`], Acc@1 −5,4 [`\AblRepairedAllCoverageEffectDAccOne`] CI [−9,4 [`\AblRepairedAllCoverageEffectDAccOneLo`]; −2,1 [`\AblRepairedAllCoverageEffectDAccOneHi`]].
- **CovGate** (phá hòa Ochiai): Acc@3 +3,9 [`\RqTwoRepairedAllCovgateDAccThree`], Acc@1 không đổi.
- **Đề xuất rồi kiểm chứng** (dev): cấu hình được chọn 90,7 [`\PavDevChosenReviewedAccOne`] so với bước đề xuất 90,7 [`\PavDevStageReviewedAccOne`]; cấu hình mạnh tay 79,3 [`\PavDevWorstReviewedAccOne`]. **Biểu quyết** (dev): 92,0 [`\VoteReviewedVoteAccOne`] so với 90,7 [`\VoteReviewedSingleAccOne`].
- **Phân tích tĩnh:** ruff luật mặc định trúng 1 [`\StatReviewedRuffDefaultOnFaultLine`] chương trình; ruff mọi luật trúng 25 [`\StatReviewedRuffAllOnFaultLine`], thấp hơn mức ngẫu nhiên 56,3 [`\StatReviewedRuffAllOnFaultLineByChance`]; pyrefly 0 [`\StatReviewedPyreflyOnFaultLine`].
- **Cơ chế:** bản sửa nhỏ làm mọi kiểm thử đạt ở 23,3 [`\PavmechReviewedOtherLineFixable`]% lần thử tại các dòng ứng viên không có lỗi, chỉ 42,5 [`\PavmechReviewedFaultLineFixable`]% tại dòng lỗi thật (tập dev).
- **Bằng chứng.** `data/ablation_coverage.csv`, `data/pav_dev_grid.csv`, `data/pav_mechanism.csv`, `data/vote_dev.csv`, `data/static_tools.csv`.
- **Giới hạn.** Đề xuất rồi kiểm chứng và biểu quyết chỉ đánh giá trên dev.

### C5. Bảng kiểm tra bảy mục và gói tái hiện
- Bảng kiểm (phá hòa, mẫu số cố định, nhãn kiểm chứng, loại bỏ thành phần ẩn, lặp + kiểm định, chi phí, so với một prompt có kiểm thử thất bại): `docs/literature/evaluation-checklist.md`.
- Gói tái hiện: Docker offline, nhật ký và bộ đệm lượt gọi LLM (`FLX_LLM_OFFLINE=1`), tệp duyệt nhãn của từng thành viên, mọi con số là macro. `REPRODUCE.md`.

## 2. Triết lý khoa học

1. **Kiểm thử là trọng tài — khi đủ chặt.** LLM đề xuất, kiểm thử quyết định; khi kiểm thử không đủ (lỗi hai dòng, lỗi thiếu mã, bản sửa bù trừ), nêu rõ phần nào do người duyệt quyết định.
2. **Đo đóng góp.** Phân rã và loại bỏ từng thành phần thay cho một con số tổng.
3. **Cái đơn giản là mốc bắt buộc.** Một quy trình nhiều bước phải thắng một prompt đưa kiểm thử thất bại cho LLM.
4. **Chịu bác bỏ.** Mỗi khẳng định có điều kiện bác bỏ và khoảng tin cậy; báo cáo cả kết quả âm tính.
5. **Bộ dữ liệu cũng là giả thuyết.** Nhãn phải được kiểm tra trước khi tin con số.

## 3. Giới hạn chính

- **Vòng tròn của bộ nhãn rà soát:** nhãn do LLM gợi ý, người duyệt xem gợi ý; kết quả chính báo trên bộ gốc và bộ đã sửa.
- **Tên kiểm thử "nói hộ" lỗi** và **một hàm mỗi lần**: lợi thế của prompt đơn giản có thể nhỏ hơn trên dự án thật; định vị cấp dự án chưa được đánh giá.
- **Lỗi thật ít:** 31 lỗi một dự án, khoảng tin cậy còn chứa 0.
- **Một mô hình chính**; so sánh nhiều họ mô hình chỉ trên tập con, chưa có khoảng tin cậy.

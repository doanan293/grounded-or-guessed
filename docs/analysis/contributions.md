# Đóng góp, triết lý khoa học và giới hạn (Phase 3.3)

Mọi con số dưới đây là một macro trong `docs/report/generated/numbers-vi.tex` (sinh từ `data/` bởi `scripts/make_numbers.py`); tên macro ghi trong ngoặc vuông ngay sau số. Kiểm tra lại: `python scripts/check_claims.py docs/analysis/contributions.md`.

**Câu đóng góp (spec §8, tiêu chí 1):** Nhóm tái hiện độc lập SemLoc và chỉ ra rằng phần "grounded" (bằng chứng thực thi) đóng góp ít hơn nhiều so với phần "guessed" (dòng lỗi LLM tự đoán) ở hạng 1; rằng kết quả phụ thuộc mạnh vào cách chấm điểm và vào ground truth của benchmark; nhóm sửa benchmark bằng bằng chứng thực thi, đề xuất CovGate, và cho thấy một prompt duy nhất kèm bằng chứng độ phủ vượt cả pipeline — chính xác hơn, rẻ hơn và bền hơn khi đổi tên biến.

## 1. Đóng góp

### C1. "Grounded or guessed": đo phần đóng góp của bằng chứng thực thi
- **Khẳng định.** Ở hạng 1, phần lớn độ chính xác của SemLoc đến từ dòng LLM tự đoán, không từ phổ vi phạm ràng buộc. Trên lượt chạy của nhóm (ground truth đã sửa), Acc@1 49,3 [`\DecSemlocRepairedAllAccOneFull`] = dòng đoán 28,9 [`\DecSemlocRepairedAllAccOnePhiGuess`] + phổ ngữ nghĩa 20,3 [`\DecSemlocRepairedAllAccOnePhiSpectrum`] (giá trị Shapley, CI 95% bootstrap theo cụm template). Ở top-3 thì ngược lại: phổ 44,4 [`\DecSemlocRepairedAllAccThreePhiSpectrum`] so với dòng đoán 26,8 [`\DecSemlocRepairedAllAccThreePhiGuess`]. Trên log công bố của tác giả (Claude): 42,8 [`\PubSemlocClaudeTZeroEightSemlocOriginalAllAccOneFull`] = 27,8 [`\PubSemlocClaudeTZeroEightSemlocOriginalAllAccOnePhiGuess`] + 15,0 [`\PubSemlocClaudeTZeroEightSemlocOriginalAllAccOnePhiSpectrum`].
- **Trên lỗi thật (BugsInPy, 31 lỗi):** Acc@1 của SemLoc 46,2 [`\BipAllSemlocPriorAccOneMean`] bằng đúng Acc@1 của riêng dòng đoán 46,2 [`\BipAllLlmGuessAccOneMean`]; riêng phổ ngữ nghĩa chỉ 7,5 [`\BipAllSemlocSpectrumAccOneMean`].
- **Bằng chứng.** `data/rq_decomposition.csv`, `data/rq_decomposition_published.csv`, `data/rq3_bugsinpy.csv`.
- **Điều sẽ bác bỏ nó.** Một cấu hình SemLoc mà khi bỏ điểm thưởng cho dòng đoán, Acc@1 không giảm. Trên lượt chạy của nhóm, bỏ điểm thưởng làm Acc@1 giảm −8,6 [`\RqTwoRepairedAllSemlocNoPriorDAccOne`] điểm, CI [−15,8 [`\RqTwoRepairedAllSemlocNoPriorDAccOneLo`]; −1,9 [`\RqTwoRepairedAllSemlocNoPriorDAccOneHi`]].
- **Giới hạn.** Phân rã là trò chơi hai người chơi có tổng đúng bằng SemLoc như phát hành; giá trị Shapley phụ thuộc cách định nghĩa "tắt" một thành phần. Xem C5 về sự mơ hồ dòng kề cạnh.

### C2. Một prompt có độ phủ vượt cả pipeline
- **Khẳng định.** Baseline của nhóm — một lượt gọi LLM với mã nguồn đánh dấu số test fail/pass chạy qua mỗi dòng — có Acc@3 86,7 [`\RqTwoRepairedAllLlmCoverageAccThreeMean`] so với 71,2 [`\RqTwoRepairedAllSemlocAccThreeMean`] của SemLoc: Δ +15,4 [`\RqTwoRepairedAllLlmCoverageDAccThree`] điểm, CI [+9,8 [`\RqTwoRepairedAllLlmCoverageDAccThreeLo`]; +21,3 [`\RqTwoRepairedAllLlmCoverageDAccThreeHi`]]; Acc@1 cũng hơn: Δ +4,6 [`\RqTwoRepairedAllLlmCoverageDAccOne`], CI [+1,3 [`\RqTwoRepairedAllLlmCoverageDAccOneLo`]; +8,2 [`\RqTwoRepairedAllLlmCoverageDAccOneHi`]].
- **Không chỉ nhờ lỗi lộ qua độ phủ:** trên lỗi ngữ nghĩa thuần, Acc@3 91,8 [`\RqTwoRepairedSemanticLlmCoverageAccThreeMean`] so với 77,6 [`\RqTwoRepairedSemanticSemlocAccThreeMean`].
- **Rẻ hơn:** 2,6 [`\CostLlmCoverageTokensK`] nghìn token mỗi chương trình so với 14,0 [`\CostSemlocTokensK`] nghìn; thắng SemLoc ở cả 5 họ model (`data/pareto.csv`, `pareto.pdf`).
- **Bền khi đổi tên biến:** Acc@3 đổi −0,9 [`\RenRepairedLlmCoverageDAccThree`] điểm, CI [−3,3 [`\RenRepairedLlmCoverageDAccThreeLo`]; +1,2 [`\RenRepairedLlmCoverageDAccThreeHi`]], trong khi SemLoc giảm −8,1 [`\RenRepairedSemlocDAccThree`] và riêng phổ ngữ nghĩa giảm −14,8 [`\RenRepairedSemlocNoPriorDAccThree`].
- **Trên lỗi thật:** cùng hướng — Acc@3 69,9 [`\BipAllLlmCoverageAccThreeMean`] so với 53,8 [`\BipAllSemlocPriorAccThreeMean`], Δ +16,1 [`\BipAllLlmCoverageDAccThree`], nhưng CI [−3,2 [`\BipAllLlmCoverageDAccThreeLo`]; +34,4 [`\BipAllLlmCoverageDAccThreeHi`]] còn chạm 0 với 31 lỗi.
- **Bằng chứng.** `data/rq2_ours.csv`, `data/rq3_renamed.csv`, `data/rq3_bugsinpy.csv`, `data/llm_cost.csv`.
- **Giới hạn.** Prompt baseline do nhóm thiết kế, không tinh chỉnh trên test; chỉ đo với một mức suy luận mặc định của mỗi nhà cung cấp.

### C3. Kết quả công bố phụ thuộc vào cách chấm điểm và thành phần không được mô tả
- Tái hiện khớp 13/13 cấu hình từ log công bố, nhưng: (a) điểm thưởng +1,2 cho dòng LLM đoán không có trong bài báo, bỏ đi thì Acc@1 (Claude) từ 42,8 [`\RqOneSemlocClaudeTZeroEightAuthorAllAccOne`] còn 30,0 [`\RqOneSemlocClaudeTZeroEightNoPriorFairAllAccOne`]; (b) delta debugging đạt 38,0 [`\RqOneDdAuthorAllAccOne`] trong bộ chấm của tác giả nhưng 0,0 [`\RqOneDdFairAllAccOne`] khi chấm công bằng; (c) SBFL Acc@5 bị đánh giá thấp: 30,4 [`\RqOneSbflOchiaiAuthorAllAccFive`] so với 48,0 [`\RqOneSbflOchiaiFairAllAccFive`]; (d) bước counterfactual không đổi thứ hạng nào (0/250) dù chiếm 42 [`\CostCfSharePct`]% lượt gọi LLM của SemLoc.
- Artifact còn có lỗi tái hiện: runner BugsInPy báo hạng của chính dòng LLM đoán thay vì dòng đã sửa, và để lại bytecode cũ sau bước vá thử (cùng kích thước, cùng giây) làm lỗi "biến mất" ở lượt chạy sau.
- **Bằng chứng.** `data/rq1_audit.csv`, `data/rq1_cf_identity.json`, `src/flx/bip_run.py`, `src/flx/bip_score.py`.

### C4. SemFault-250-verified: ground truth kiểm chứng bằng thực thi
- 56 [`\GtBlankN`] dòng ground truth là dòng trống và 65 [`\GtNotExecutedN`] chương trình không có test fail nào chạy tới dòng lỗi. Oracle "một bản sửa tối thiểu một dòng làm mọi test pass" (LLM chỉ đề xuất, test phân xử) cho: 82 [`\GtConfirmedN`] xác nhận, 46 [`\GtCorrectedN`] sửa vị trí, 111 [`\GtUnverifiedN`] chưa kiểm chứng, 11 [`\GtUnverifiableN`] không kiểm chứng được.
- Sửa ground truth làm Acc@1 của SemLoc tăng từ 36,8 [`\RqTwoOriginalAllSemlocAccOneMean`] lên 49,3 [`\RqTwoRepairedAllSemlocAccOneMean`]; kết luận so sánh giữa các phương pháp không đổi chiều.
- **Giới hạn quan trọng (xem §3).** Oracle chấp nhận cả bản sửa bù trừ.

### C5. Định nghĩa Acc@1 cấp dòng không ổn định trên lỗi trải hai dòng
- Trong 96 chương trình mà dòng đoán sai, 44 [`\FailRelationHeaderBodyN`] là cặp "đầu khối điều kiện – câu lệnh được bảo vệ". Chấp nhận cả hai, Acc@1 của SemLoc từ 49,3 [`\TolSemlocAccOneExact`] lên 71,8 [`\TolSemlocAccOneGuardOrBody`], của LLM + độ phủ từ 53,9 [`\TolLlmCoverageAccOneExact`] lên 76,8 [`\TolLlmCoverageAccOneGuardOrBody`]. Thứ tự giữa các phương pháp giữ nguyên.
- **Bằng chứng.** `data/failure_tolerance.csv`, `docs/analysis/failure-analysis.md`.

### C6. CovGate và checklist đánh giá
- CovGate (λ·Ochiai chọn trên dev) tăng Acc@3 +3,5 [`\RqTwoRepairedAllCovgateDAccThree`] điểm, CI [+1,3 [`\RqTwoRepairedAllCovgateDAccThreeLo`]; +6,2 [`\RqTwoRepairedAllCovgateDAccThreeHi`]], Acc@1 không đổi; riêng cổng độ phủ đã đạt Acc@3 74,6 [`\RqTwoRepairedAllGateOnlyAccThreeMean`]. "Chỉ thưởng khi có căn cứ" làm Acc@1 giảm −3,9 [`\RqTwoRepairedAllGroundedPriorOnlyDAccOne`]; CF xếp lại làm Acc@1 giảm −2,3 [`\RqTwoRepairedAllCfRerankDAccOne`]. Gắn thêm bằng chứng vào pipeline chỉ giúp ít — đối chiếu với C2.
- Checklist sáu mục (hòa điểm, mẫu số cố định, ground truth kiểm chứng, ablation thành phần ẩn, lặp + kiểm định, chi phí) áp cho mọi phương pháp: `docs/literature/evaluation-checklist.md`.

### C7. Gói tái hiện
- Docker offline dựng lại toàn bộ `data/` và mọi bảng giống từng byte từ gói lượt chạy; mọi lượt gọi LLM phát lại được từ cache (`FLX_LLM_OFFLINE=1`); mọi con số trong bài là macro sinh tự động. `REPRODUCE.md`.

## 2. Triết lý khoa học

1. **Chứng cứ thực thi là trọng tài, LLM chỉ đề xuất.** Ở mọi chỗ cần phán xử — dòng nào là lỗi, bản sửa nào đúng — nhóm để test quyết định; LLM chỉ sinh ứng viên. Đây cũng là câu hỏi của bài: SemLoc tuyên bố "neo lập luận vào thực thi", nhóm đo xem phần neo đó thực sự đóng góp bao nhiêu.
2. **Tái hiện không phải là chép lại con số.** Khớp 13/13 số công bố là điều kiện cần; điều kiện đủ là hiểu *vì sao* ra số đó — cách chấm, thành phần ẩn, lỗi của artifact. Một kết quả chỉ đứng vững khi nó còn đúng sau khi đổi cách chấm hợp lý.
3. **Đo đóng góp, không chỉ đo tổng.** Một con số Acc@1 không nói nó đến từ đâu. Phân rã Shapley và ablation từng thành phần biến câu hỏi "phương pháp có tốt không" thành "phần nào làm nó tốt".
4. **So với baseline đơn giản nhất có cùng thông tin.** Một pipeline nhiều bước chỉ đáng giá khi thắng một prompt duy nhất có cùng bằng chứng; ở đây nó thua.
5. **Mỗi khẳng định kèm điều kiện bác bỏ và khoảng tin cậy.** Lặp 3 lần, bootstrap theo chương trình và theo cụm template (không coi lần lặp là mẫu độc lập), báo cáo cả khi CI chạm 0 (BugsInPy).
6. **Benchmark cũng là giả thuyết.** Ground truth do người gán có thể sai hoặc mơ hồ; kiểm chứng nó bằng thực thi, báo cáo trên cả bản gốc và bản đã sửa, và nêu rõ giới hạn của chính oracle sửa lỗi.

## 3. Threats to Validity

- **Oracle sửa tối thiểu chấp nhận bản sửa bù trừ.** Ví dụ `gradient_clip_budget`: "sửa" ở dòng 62 bằng `norm = ... - 1` trong khi lỗi thật ở dòng 66; các khối lỗi nhiều dòng được "xác nhận" bằng cách tắt điều kiện. SemFault-250-verified vì vậy vẫn còn nhiễu; mọi kết quả được báo cáo trên cả ground truth gốc.
- **Ground truth kiểm chứng có thể thiên về phương pháp dựa trên độ phủ** (oracle cần test fail chạy tới dòng sửa). Thứ tự giữa các phương pháp giống nhau trên ground truth gốc.
- **Mơ hồ dòng kề cạnh** (C5): Acc@1 chặt phụ thuộc quy ước gán nhãn; nhóm báo cáo cả Acc@1 chấp nhận đầu khối/thân khối.
- **Lỗi thật ít và một dự án** (31 lỗi youtube-dl); hàm đích chọn từ diff của lập trình viên (lỗi của định vị cấp hàm không được đo). youtube-dl_33 còn 2 test fail do môi trường trong runner gốc của SemLoc.
- **Model và mức suy luận.** Mô hình chính (Gemini 3.8 Flash) mới hơn mô hình trong bài gốc; mỗi nhà cung cấp chạy ở mức suy luận mặc định nên RQ3c so "ở mặc định", không cùng mức suy luận; Claude qua proxy sinh ràng buộc yếu hơn log công bố (RQ1b).
- **Nhiễm dữ liệu.** Biến thể đổi tên chỉ đổi định danh và xóa chú thích; cấu trúc mã giữ nguyên nên không loại trừ hoàn toàn việc model đã thấy các template.
- **Prompt baseline do nhóm viết**, thiết kế trước khi xem kết quả test, không tinh chỉnh; một prompt khác có thể cho kết quả khác.

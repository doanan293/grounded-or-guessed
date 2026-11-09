# Báo cáo và bài báo

| Tệp | Nội dung |
|---|---|
| `bao-cao.pdf` | Báo cáo tiểu luận tiếng Việt, bản đầy đủ (bài nộp cuối kỳ) |
| `paper.pdf` | Bài báo tiếng Anh (IEEEtran, bản arXiv) |

Nhánh này (`main`) là bản đầy đủ. Hai bản báo cáo tiến độ nằm ở nhánh `bao-cao-lan-1` (18–19/11/2026) và
`bao-cao-lan-2` (25–26/11/2026), dựng từ cùng nguồn LaTeX với công tắc phiên bản `\Version` (`lan1`, `lan2`, `full`).

Dựng lại: `make -C docs/report vi-full paper` (hoặc `vi-lan1`, `vi-lan2`); `make -C docs/report check` dựng mọi phiên
bản và báo lỗi nếu còn trích dẫn/tham chiếu chưa định nghĩa hoặc số gõ tay. Mọi con số là macro trong
`generated/numbers-vi.tex` / `generated/numbers.tex`, sinh từ `data/` bởi `scripts/make_numbers.py`.

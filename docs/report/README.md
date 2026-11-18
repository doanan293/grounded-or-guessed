# Báo cáo và bài báo

| Tệp | Nội dung |
|---|---|
| `bao-cao.pdf` | Báo cáo tiểu luận tiếng Việt, bản final (bài nộp cuối kỳ) |
| `paper.pdf` | Bài báo tiếng Anh (IEEEtran, bản arXiv) |

Chỉ có một báo cáo final. Hai lần báo cáo tiến độ (18–19/11 và 25–26/11/2026) chỉ trình bày bằng slide, ở nhánh
`bao-cao-lan-1` và `bao-cao-lan-2` (`docs/presentation/`).

Dựng lại: `make -C docs/report vi paper`; `make -C docs/report check` dựng cả hai và báo lỗi nếu còn trích dẫn/tham
chiếu chưa định nghĩa hoặc số gõ tay. Mọi con số là macro trong `generated/numbers-vi.tex` / `generated/numbers.tex`,
sinh từ `data/` bởi `scripts/make_numbers.py`.

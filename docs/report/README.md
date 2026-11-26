# Báo cáo và bài báo

| Nguồn | Bản dựng (không đưa lên git) |
|---|---|
| `vi/` | `bao-cao.pdf`: báo cáo tiểu luận tiếng Việt, bản final (bài nộp cuối kỳ) |
| `paper-en/` | `paper.pdf`: bài báo tiếng Anh (IEEEtran, bản arXiv) |

Chỉ có một báo cáo final. Ba lần báo cáo tiến độ chỉ trình bày bằng slide (`docs/presentation/slide-lan-1/2/3.pptx`),
slide bảo vệ là `docs/presentation/slide-bao-ve.pptx`; dựng bằng `docs/presentation/build/make_decks.sh`. Các tệp PDF
và PPTX này là sản phẩm dựng nên nằm trong `.gitignore`; muốn gửi ai thì dựng lại rồi gửi tệp, hoặc đính vào GitHub
Release.

Dựng lại: `make -C docs/report vi paper`; `make -C docs/report check` dựng cả hai và báo lỗi nếu còn trích dẫn/tham
chiếu chưa định nghĩa hoặc số gõ tay. Mọi con số là macro trong `generated/numbers-vi.tex` / `generated/numbers.tex`,
sinh từ `data/` bởi `scripts/make_numbers.py`.

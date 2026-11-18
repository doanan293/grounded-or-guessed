# make vi | paper | all | check | clean   (one final report: vi/main.pdf; the paper: paper-en/main.pdf)
.PHONY: all vi paper check clean
all: vi paper
vi:
	cd vi && latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
paper:
	cd paper-en && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
# build both, fail on undefined citations/references or hand-typed numbers in the text (not the preamble)
check: vi paper
	! grep -E "(Citation|Reference) .* undefined" vi/main.log paper-en/main.log
	cd .. && cd .. && .venv/bin/python scripts/lint_numbers.py docs/report/vi/chapters docs/report/vi/frontmatter docs/report/paper-en/sections
clean:
	cd vi && latexmk -C main.tex; cd paper-en && latexmk -C main.tex

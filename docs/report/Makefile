# make vi-full | vi-lan1 | vi-lan2 | vi-lan3 | paper | all | check | clean
# Each Vietnamese version builds its own PDF (vi/main-<version>.pdf); the paper builds paper-en/main.pdf.
.PHONY: all vi vi-full vi-lan1 vi-lan2 vi-lan3 paper check clean
VI = cd vi && latexmk -xelatex -interaction=nonstopmode -halt-on-error
all: vi-full paper
vi: vi-full
vi-full vi-lan1 vi-lan2 vi-lan3:
	$(VI) -jobname=main-$(@:vi-%=%) -usepretex='\def\Version{$(@:vi-%=%)}' main.tex
paper:
	cd paper-en && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
# build every version, fail on undefined citations/references or hand-typed numbers in the text (not the preamble)
check: vi-lan1 vi-lan2 vi-lan3 vi-full paper
	! grep -E "(Citation|Reference) .* undefined" vi/main-lan1.log vi/main-lan2.log vi/main-lan3.log vi/main-full.log paper-en/main.log
	cd .. && cd .. && .venv/bin/python scripts/lint_numbers.py docs/report/vi/chapters docs/report/vi/frontmatter docs/report/paper-en/sections
clean:
	cd vi && for v in lan1 lan2 lan3 full; do latexmk -C -jobname=main-$$v main.tex; done; cd paper-en && latexmk -C main.tex

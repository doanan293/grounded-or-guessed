# make vi | make paper | make all | make clean
.PHONY: all vi paper clean
all: vi paper
vi:
	cd vi && latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
paper:
	cd paper-en && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
clean:
	cd vi && latexmk -C main.tex; cd paper-en && latexmk -C main.tex

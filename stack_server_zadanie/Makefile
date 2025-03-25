default: stack_try.pdf \
stack_empty.pdf \
stack_7.pdf \
stack_70.pdf \
stack_70_15.pdf \
stack_70_3.pdf \
stack_70_3_5.pdf \
stack_7_10.pdf \
stack_85.pdf

.PRECIOUS: %.t1.tex

%.pdf: %.eps
	epstopdf $(*D)/$(*F).eps

%.eps: %.ps
	ps2eps $(*D)/$(*F).ps -f -l

%.ps: %.dvi
	dvips -o $@ $(*D)/$(*F).dvi

%.dvi: %.tex
	latex $(*D)/$(*F)
	rm $(*F).aux
	rm $(*F).log

%.tex: %.py stack.template.tex numberstack.py
	python3 $(*D)/$(*F).py stack.template.tex > $@

pygments.tex: get_pygments_tex.py Makefile
	python get_pygments_tex.py > pygments.tex


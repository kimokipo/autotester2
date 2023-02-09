

exemple-allumettes:
	python main.py -t real_tester  -r exemple-13allumettes/tps/st1/  --version 1 --verbose

MD_FILES = ${wildcard *.md}
HTML_FILES = ${MD_FILES:%.md=%.html}
PDF_FILES  = ${MD_FILES:%.md=%.pdf}

PANDOC = pandoc
PANDOC_OPT = --toc -s

doc: ${HTML_FILES}

%.html: %.md
	${PANDOC} ${PANDOC_OPT} -o $@ $<

%.pdf: %.md
	${PANDOC} ${PANDOC_OPT} -o $@ $<


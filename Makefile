ACTIVATE=. venv/bin/activate
VERSION=1.0.0

venv:
	python3 -m venv venv

build/install: venv requirements.txt
	${ACTIVATE} && pip install --upgrade pip
	${ACTIVATE} && pip install -r requirements.txt
	mkdir -p build && touch build/install

install: build/install

clean:
	rm -rf venv
	rm -f install

autoformat: install
	${ACTIVATE} && yapf -i *.py --style .yapfrc

lint: install
	${ACTIVATE} && pylint *.py

test: install
	${ACTIVATE} && pytest tests
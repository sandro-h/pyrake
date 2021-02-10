ACTIVATE=. venv/bin/activate
VERSION=1.0.0

venv:
	python3 -m venv venv

build/install: venv requirements.txt
	${ACTIVATE} && pip install --upgrade pip wheel
	${ACTIVATE} && pip install -r requirements.txt
	mkdir -p build && touch build/install

install: build/install

clean-install:
	rm -rf venv install

clean:
	rm -rf */__pycache__ dist

autoformat: install
	${ACTIVATE} && yapf --in-place pyrake/*.py --style .yapfrc

check-format: install
	${ACTIVATE} && yapf --diff pyrake/*.py --style .yapfrc

lint: install
	${ACTIVATE} && pylint pyrake/*.py

test: install
	${ACTIVATE} && pytest tests

dist: clean install
	${ACTIVATE} && python setup.py sdist bdist_wheel
	echo "::set-output name=package_file::$$(cd dist && ls -1 pyrake*.whl)"

release: VERSION=$$(grep 'version=' setup.py | sed -r "s/\s+version='(.*)',\s*/\1/")
release: 
	git tag v${VERSION}
	git push origin v${VERSION}
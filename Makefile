CC=$(shell which pyinstaller)

build:
	$(CC) src/vly.py --onefile --distpath vly

clean:
	rm -frfr build/ __pycache__ vly vly.spec

format:
	black -l 79 src/*.py

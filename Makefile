.PHONY: dist

demo-output.html: demo.py pygments_better_html/__init__.py
	python demo.py

dist:
	./setup.py sdist bdist_wheel

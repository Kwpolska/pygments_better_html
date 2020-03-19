.PHONY: dist

demo-output-table.html demo-output-ol.html: demo.py pygments_better_html/__init__.py
	python demo.py

demo-output-ol.html: demo-output-table.html

dist:
	./setup.py sdist bdist_wheel

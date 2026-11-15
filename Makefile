.PHONY: run test lint clean

run:
	python app.py

test:
	python -m pytest tests/ -v

lint:
	python -m flake8 *.py --max-line-length 120

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage

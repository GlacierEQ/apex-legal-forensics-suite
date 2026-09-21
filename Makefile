.PHONY: test lint build run clean

test:
	@echo "🧪 Running backend test gate..."
	python3 -m unittest discover -s backend/tests -v
	@echo "🧪 Running frontend verification..."
	node --check frontend/package.json

lint:
	@echo "🔍 Linting codebase..."
	python3 -m py_compile backend/app/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

cd ENTER_YOUR_PROJECT_DIRECTORY_ || exit
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=10 --max-line-length=100 --statistics
mypy --ignore-missing-imports --install-types --non-interactive --exclude venv .
pycodestyle --max-line-length=100 .
pylint --disable=C0112,C0114,C0115,C0116,C0103,R1705,R0903 *.py
ruff check --output-format=github .
setup:
	pip install -r requirements.txt

run:
	python main.py

env:
	python3 -m venv env

activate:
	source env/bin/activate

deactivate:
	deactivate

help:
	@echo "List of Available Commands"
	@echo "--------------------------"
	@echo " - init-env      : installs all requirements from requirements.txt"
	@echo " - init-dev           : installs all development requirements from dev-requirements.txt"
	@echo " - flake         : runs flake8 style checks in src/*.py files"
	@echo " - clean-nb      : cleans python notebooks outputs in notebooks/*.ipynb"
	@echo " - clean-folders : cleans up all folders nb checkpoints, pycache & pytest folders"
	@echo " - interrogate   : runs interrogate on the \"src\" folder"
	@echo " - precommit     : runs clean-nb, clean-folders & interrogate"
	@echo " - all           : runs all (clean-nb + clean-folders + interrogate + flake)"

init-env:
	pip install -r requirements.txt --no-cache-dir

init-dev: init-env
	pip install -r dev-requirements.txt --no-cache-dir

flake:
	flake8 app/*.py

clean-nb:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/*.ipynb

clean-folders:
	rm -rf .ipynb_checkpoints __pycache__ .pytest_cache */.ipynb_checkpoints */__pycache__ */.pytest_cache

interrogate:
	interrogate -vv --ignore-module --ignore-init-method --ignore-private --ignore-magic --fail-under=80 app/

precommit: clean-folders interrogate

check-all: clean-nb clean-folders interrogate flake
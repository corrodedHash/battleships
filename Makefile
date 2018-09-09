PROJECTNAME=battleships

.PHONY: test coverage typing linting

test:
	python -m unittest discover

coverage:
	coverage run -m unittest discover && coverage report --skip-covered

typing:
	mypy --strict ${PROJECTNAME}

linting:
	pylint ${PROJECTNAME}

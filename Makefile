.PHONY:	black-format \
	black-format-check \
	bootstrap \
	cheeseshop \
	coverage-html \
	isort \
	isort-check \
	mypy \
	nuke-venv \
	run-tests \

PIPENV_RUN = pipenv run


black-format:
	@$(PIPENV_RUN) black krakus/ tests/ -S -l 119

black-format-check:
	@$(PIPENV_RUN) black krakus/ tests/ -S -l 119 --check -q

bootstrap: nuke-venv cheeseshop

cheeseshop:
	@pipenv install --dev

coverage-html:
	@$(PIPENV_RUN) coverage html

isort:
	@$(PIPENV_RUN) isort krakus/ tests/ --recursive -tc

isort-check:
	@$(PIPENV_RUN) isort krakus/ tests/ --recursive --check-only -tc -q

mypy:
	@$(PIPENV_RUN) mypy krakus/

nuke-venv:
	@pipenv --rm;\
	EXIT_CODE=$$?;\
	if [ $$EXIT_CODE -eq 1 ]; then\
		echo Skipping virtualenv removal;\
	fi

run-tests:
	@$(PIPENV_RUN) py.test -s --cov krakus

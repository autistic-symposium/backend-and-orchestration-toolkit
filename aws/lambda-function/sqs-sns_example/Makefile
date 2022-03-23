install:
	@python setup.py install && pip install -r requirements.txt

build:
	@/bin/bash ./scripts/build_package.sh

clean:
	@rm -rf /tmp/*.mp4 .coverage .tox build dist lib/*.pyc *.egg-info *pyc __pycache__/ ffmpeg* .pytest_cache /tmp/*mp4 /tmp/*jpg

doctoc:
	@doctoc README.md

event:
	@PYTHONPATH=$(pwd) ./scripts/create_test_event.py

invoke:
	@PYTHONPATH=$(pwd) lambda invoke -v

lint:
	@pep8 --exclude=build,venv,dist . && echo pep8: no linting errors

fixlint:
	@autopep8 --in-place *py lib/*py lib/handlers/*py lib/routes/*py tests/*py scripts/*py

test:
	@PYTHONPATH=$(pwd) py.test -v --color=yes --ignore=venv/

deploy:
	@/bin/bash scripts/deploy_lambda.sh sandbox

sbox:
	@/bin/cp .env.sample_sandbox .env

stag:
	@/bin/cp .env.sample_staging .env

prod:
	@/bin/cp .env.sample_prod .env

.PHONY: install clean doctoc lint invoke test build deploy event fixlint prod stag sbox

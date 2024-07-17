PIP=pip

.PHONY: wheel clean clean-docs build install docs build-tool

build: build-tool
	python -m build

install:
	$(PIP) install .

docs:
	$(PIP) freeze | grep -q Sphinx || $(PIP) install Sphinx
	$(MAKE) -C docs html

clean-docs:
	$(MAKE) -C docs clean

CLEAN_LIST=build rubber_docker.egg-info $(wildcard *.whl) $(wildcard rubber-docker-*.tar.gz)
clean: clean-docs
	rm -rf build $(CLEAN_LIST)

build-tool:
	$(PIP) freeze |grep -q build || $(PIP) install build
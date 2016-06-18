#!/bin/bash -e

pip freeze | grep -q Sphinx || pip install Sphinx

pushd docs
make clean
make html
popd

rm -rf docs/linux
mv docs/_build/html docs/linux

echo 'Done!'

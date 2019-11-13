#!/bin/bash
cd "$(dirname -- "$(dirname -- "$(readlink -f "$0")")")"

for cmd in flake8 isort mypy pytype pylint; do
    if [[ ! -x "$(which "$cmd")" ]]; then
        echo "Could not find $cmd. Please make sure that flake8, isort, and pylint are all installed."
        exit 1
    fi
done

flake8 neuralzero && isort --recursive --check neuralzero && mypy neuralzero && pytype --disable=not-supported-yet neuralzero && pylint neuralzero

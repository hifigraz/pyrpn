#!/usr/bin/env bash

[ -z "$1" ] && poetry run ${EDITOR} . || poetry run ${EDITOR} "$*"

#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace


celery -A dino_backend.taskapp worker -l INFO

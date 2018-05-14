#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A dino_backend.taskapp beat -l INFO

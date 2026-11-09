#!/usr/bin/env bash
set -euo pipefail
git config user.name "Jenkins CI"
git config user.email "jenkins@localhost"
git add docs
if git diff --cached --quiet; then exit 0; fi
git commit -q -m "docs: build #${BUILD_NUMBER} ${APP_VERSION} [skip ci]"
git tag -a "build-${BUILD_NUMBER}-${GIT_SHA}" -m "Build ${BUILD_NUMBER} versión ${APP_VERSION}"
if [[ "$(git remote get-url origin)" == /repos/* ]]; then
    git push origin HEAD:main --follow-tags
else
    ASKPASS="$(mktemp)"
    trap 'rm -f "$ASKPASS"' EXIT
    printf '#!/bin/sh\ncase "$1" in Username*) echo "$GIT_USER" ;; *) echo "$GIT_TOKEN" ;; esac\n' > "$ASKPASS"
    chmod 700 "$ASKPASS"
    GIT_ASKPASS="$ASKPASS" GIT_TERMINAL_PROMPT=0 git push origin HEAD:main --follow-tags
fi

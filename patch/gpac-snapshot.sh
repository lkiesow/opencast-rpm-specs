#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
cvs=$(date +%Y%m%d)

cd "$tmp"
cvs -z3 -d:pserver:anonymous@gpac.cvs.sourceforge.net:/cvsroot/gpac co -P gpac 
find . -type d -name CVS -print0 | xargs -0r rm -rf
chmod 755 gpac/configure
rm -rf gpac/extra_lib/
tar jcf "$pwd"/gpac-$cvs.tar.bz2 gpac
cd - >/dev/null

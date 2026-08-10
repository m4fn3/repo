#!/bin/sh

set -eu

packages_tmp=$(mktemp)
trap 'rm -f "$packages_tmp"' EXIT

apt-ftparchive packages ./debs > "$packages_tmp"

awk '
{
    print

    if ($0 == "Package: com.m4fn3.myrtle") {
        print "SileoDepiction: https://m4fn3.github.io/repo/web/depictions/Myrtle.json"
    } else if ($0 == "Package: com.m4fn3.k2geisland") {
        print "SileoDepiction: https://m4fn3.github.io/repo/web/depictions/K2geIsland.json"
    } else if ($0 == "Package: com.m4fn3.k2gecamen") {
        print "SileoDepiction: https://m4fn3.github.io/repo/web/depictions/K2gecamen.json"
    } else if ($0 == "Package: com.m4fn3.k2ge3air") {
        print "SileoDepiction: https://m4fn3.github.io/repo/web/depictions/K2ge3Air.json"
    }
}
' "$packages_tmp" > Packages

bzip2 -kf Packages
gzip -c Packages > Packages.gz

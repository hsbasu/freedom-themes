#! /bin/bash

INKSCAPE="inkscape"
OPTIPNG="optipng"

SRC_FILE="assets.svg"
ASSETS_DIR="."

INDEX="assets.txt"

ulimit -s 1024

render()
{
    echo Rendering $1
    $INKSCAPE --export-id=$2 \
            --export-id-only \
            --export-png=$1 $SRC_FILE >/dev/null \
    && $OPTIPNG -o7 --quiet $1
}

# check command avalibility
has_command() {
  "$1" -v $1 > /dev/null 2>&1
}

mkdir -p $ASSETS_DIR

for i in `cat $INDEX`
do
if ! [ -f $ASSETS_DIR/$i.png ]; then
    echo Rendering $ASSETS_DIR/$i.png
    render $ASSETS_DIR/$i@2.png $i &
    # allow only to execute number of jobs in parallel
    # equal to number of processors
    if [[ $(jobs -r -p | wc -l) -gt $(nproc) ]]; then
    # wait only for first job
    wait $(jobs -p)
    fi
fi
done
exit 0

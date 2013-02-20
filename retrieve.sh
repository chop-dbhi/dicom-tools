#!/bin/bash
# Link filedescriptor 10 with stdin
exec 10<&0
# stdin replaced with a file supplied as a first argument
exec < $2
let count=0

while read LINE; do
    runme="dcmqr "$1" -cmove DCMQR -q0020000D="$LINE
    echo $runme
    $runme
done

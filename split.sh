#!/bin/bash
let count=0
cd $1
moveto=$2

if [ ! -d "$moveto" ]; then
   mkdir -p $moveto
fi

for f in *
do 
  mv $f $moveto 
  let count++ 
  if [ "$count" -eq 65000 ]
  then
     break
  fi
done

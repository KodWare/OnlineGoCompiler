#! /bin/bash
cd $1
notify-send "Tamam" $1
LANG=en GOOS=$2 GOARCH=$3 go build main.go
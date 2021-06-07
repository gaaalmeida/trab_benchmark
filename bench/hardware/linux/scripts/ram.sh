#!/bin/sh

if [ $(id -u) -ne 0 ]; then
    exit 1
fi

dmidecode --type 17

#!/bin/sh
xtbin='/home/xray/knvvv/xtb/bin/xtb'
crst='/home/xray/knvvv/xtb/bin/crest'

cd $1
command -v $xtbin >/dev/null 2>&1 || { echo >&2 "Cannot find xtb binary. Exit."; exit 1; }
command -v $crst >/dev/null 2>&1 || { echo >&2 "Cannot find crest binary. Exit."; exit 1; }
$xtbin start.xyz --input xtb-control -P 1 --opt tight -g methanol > LOGFILE

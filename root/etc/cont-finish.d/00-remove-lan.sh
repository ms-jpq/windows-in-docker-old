#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


if [[ -z "$LAN_IF" ]]
then
  exit
fi


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- LAN'
printf '%s\n' '-------------------------------'


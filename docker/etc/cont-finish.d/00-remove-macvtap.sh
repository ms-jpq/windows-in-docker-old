#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


if [[ -z "$MACVTAP_IF" ]]
then
  exit
fi


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- MACVTAP'
printf '%s\n' '-------------------------------'


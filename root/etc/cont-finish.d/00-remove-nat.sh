#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


ip link set "$NAT_NAME" down
brctl delbr "$NAT_NAME"


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- NAT'
printf '%s\n' '-------------------------------'


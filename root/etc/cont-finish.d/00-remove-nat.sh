#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


ip link set "$VIRT_NAT_NAME" down
brctl delbr "$VIRT_NAT_NAME"


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- NAT'
printf '%s\n' '-------------------------------'


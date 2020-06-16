#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


ip link del "$VIRT_NAT_NAME" type bridge


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- NAT'
printf '%s\n' '-------------------------------'


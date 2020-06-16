#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


ip link del "$VIRT_NAT_NAME"
ip link del "$VIRT_NAT_NAME-nic"


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- NAT'
printf '%s\n' '-------------------------------'


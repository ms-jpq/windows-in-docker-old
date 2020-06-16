#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


virsh net-destroy "$VIRT_NAT_NAME"


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- NAT'
printf '%s\n' '-------------------------------'


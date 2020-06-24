#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


VM_IP="$(< /vmrc/ip_addr)"
route-nat --bridge "$NAT_NAME" --ip "$VM_IP" --state off
ip link set "$NAT_NAME" down
brctl delbr "$NAT_NAME"


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- NAT'
printf '%s\n' '-------------------------------'


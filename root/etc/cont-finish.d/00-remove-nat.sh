#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


ip link set "$NAT_NAME" down
brctl delbr "$NAT_NAME"


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- NAT'
printf '%s\n' '-------------------------------'


VM_IP="$(< /vmrc/ip_addr)"
VM_NET="$(< /vmrc/network)"
route-nat --bridge "$NAT_NAME" --ip "$VM_IP" --network "$VM_NET" --state off


printf '%s\n' '-------------------------------'
printf '%s\n' 'DEINIT -- IPTABLES'
printf '%s\n' '-------------------------------'


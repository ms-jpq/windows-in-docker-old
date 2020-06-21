#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


cd "/etc/sysconfig/network-scripts" || exit 1

if [[ -z "$MACVTAP_IF" ]]
then
  exit
fi


export UUID="$(uuidgen)"
TEMP="$(envsubst '${UUID},${MACVTAP_IF}' < /vmrc/ifcfg)"
printf '%s' "$TEMP" > "ifcfg-$MACVTAP_IF"


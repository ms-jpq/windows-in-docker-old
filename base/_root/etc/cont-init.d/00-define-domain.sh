#!/usr/bin/with-contenv bash

set -eu
set -o pipefail

VMDK="/config"
DOMAIN_XML="$VMDK/$VM_NAME.xml"

if [[ -f "$DOMAIN_XML" ]]
then
  virsh define "$DOMAIN_XML"
else
  hr
  >&2 echo WARNING -- VM Not Found
  >&2 echo Build VM using 'CMD :: new'
  hr
fi

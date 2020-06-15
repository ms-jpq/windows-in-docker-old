#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


TEMP="$(envsubst '${VIRT_MACVTAP_NAME}' < /vmrc/macvtap.xml)"
printf '%s' "$TEMP" > /vmrc/macvtap.xml


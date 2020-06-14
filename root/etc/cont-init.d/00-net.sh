#!/usr/bin/with-contenv bash

set -eu
set -o pipefail


ip link add link "$MACVTAP_IF" name "$MACVTAP_NAME" type macvtap

IFS=$'\n'
dev_names=($(ip -j link | jq '.[]["ifname"]' -r))
dev_index=($(ip -j link | jq '.[]["ifindex"]' -r))


found=
for idx in "${!dev_names[@]}"
do
  name="${dev_names[$idx]}"
  index="${dev_index[$idx]}"
  if [[ "$name" == "$MACVTAP_NAME" ]]
  then
    found="$index"
  fi
done


echo "----------------------------------------------"
printf '%s\n' "$found"
echo "----------------------------------------------"


TEMP="$(envsubst '${MACVTAP_NAME},${MACVTAP_IF}' < /vmrc/network.xml)"
printf '%s' "$TEMP" > /vmrc/network.xml


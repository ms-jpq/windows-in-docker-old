#!/usr/bin/env bash

set -eu
set -o pipefail


modlist=""
if grep -qs "^flags.* vmx" /proc/cpuinfo; then
  modlist="kvm_intel"
elif grep -qs "^flags.* svm" /proc/cpuinfo; then
  modlist="kvm_amd"
fi

if [ -n "$modlist" ]; then
  modprobe -b "kvm $modlist" || true
fi


mknod /dev/kvm c 10 232 || true
chown root:kvm /dev/kvm || true
chmod g+rw /dev/kvm || true


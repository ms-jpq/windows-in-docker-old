#!/usr/bin/env bash

cd / || exit 1

/usr/sbin/libvirtd &

for rc in /vmrc/**
do
  ."$rc"
done

kill %1

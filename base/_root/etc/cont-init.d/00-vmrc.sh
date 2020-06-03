#!/usr/bin/env bash

cd / || exit 1

for rc in /vmrc/**
do
  ."$rc"
done

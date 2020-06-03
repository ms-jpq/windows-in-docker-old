#!/usr/bin/env python3

from typing import List, Iterable
from subprocess import run
from sys import stderr, stdout

from psutil import net_if_addrs


def call(*args: List[str]) -> None:
  ret = run(args, stdout=stdout, stderr=stderr)
  if ret.returncode != 0:
    exit(ret.returncode)


interfaces: Iterable[str] = (name
                             for name in net_if_addrs().keys()
                             if name != "lo")

call("brctl", "addbr", "br0")
for interface in interfaces:
  call("brctl", "addif", "br0", interface)

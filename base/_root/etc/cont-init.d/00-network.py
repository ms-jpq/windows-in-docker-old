#!/usr/bin/env python3

from subprocess import run
from typing import List

from psutil import net_if_addrs


def call(*args: List[str]) -> None:
  ret = run(args)
  if ret.returncode != 0:
    exit(ret.returncode)


def main() -> None:
  interfaces: List[str] = [name
                           for name in net_if_addrs().keys()
                           if name != "lo"]
  call("brctl", "addbr", "br0")
  call("brctl", "setfd", "br0", "0")
  for interface in interfaces:
    pass
    # call("brctl", "addif", "br0", interface)


main()

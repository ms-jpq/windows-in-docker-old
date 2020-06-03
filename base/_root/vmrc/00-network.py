#!/usr/bin/env python3

from subprocess import run
from sys import stderr, stdout
from tempfile import NamedTemporaryFile
from typing import List, Iterable

from psutil import net_if_addrs


def call(*args: List[str]) -> None:
  ret = run(args, stdout=stdout, stderr=stderr)
  if ret.returncode != 0:
    exit(ret.returncode)


def write(path: str, text: str) -> None:
  with open(path, "w") as fd:
    fd.write(text)


def network_xml(interface: str) -> str:
  return f"""
  <network>
    <name>{interface}</name>
    <forward mode="bridge">
      <interface dev="{interface}"/>
    </forward>
  </network>
  """


def main() -> None:
  interfaces: Iterable[str] = (name
                               for name in net_if_addrs().keys()
                               if name != "lo")
  temp = NamedTemporaryFile()
  for name in interfaces:
    xml = network_xml(name)
    write(temp.name, xml)
    call("virsh", "net-define", temp.name)
    call("virsh", "net-start", name)
    call("virsh", "net-dumpxml", name)


main()

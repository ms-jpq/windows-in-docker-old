#!/usr/bin/env python3

from subprocess import run
from sys import stderr, stdout
from tempfile import NamedTemporaryFile
from typing import List, Iterable, Set
from pprint import pprint as pp

import libvirt
from psutil import net_if_addrs


def network_xml(interface: str) -> str:
  return f"""
  <network>
    <name>{interface}</name>
    <forward mode="bridge">
      <interface dev="{interface}"/>
    </forward>
  </network>
  """


def find_net(conn, name: str):
  try:
    return conn.networkLookupByName(name)
  except libvirt.libvirtError:
    return None


def main() -> None:
  interfaces: Iterable[str] = (name
                               for name in net_if_addrs().keys()
                               if name != "lo")
  temp = NamedTemporaryFile()
  with libvirt.open(None) as conn:
    for name in interfaces:
      if find_net(conn, name) is None:
        xml = network_xml(name)
        net = conn.networkCreateXML(xml)


main()

#!/usr/bin/env python3

from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from os import environ
from socket import AddressFamily
from subprocess import run
from sys import stderr
from typing import Any, Dict, List

from psutil import net_if_addrs


private_ranges: List[IPv4Network] = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
]


def main() -> None:
  mac_lf = environ["VIRT_MACVTAP_IF"]
  if_addrs = net_if_addrs()

  net_fam = {AddressFamily.AF_INET, AddressFamily.AF_INET6}
  addresses = (addr for addr in if_addrs[mac_lf]
               if addr.family == AddressFamily.AF_INET)
  address = next(addresses)
  if address:
    addr = address.address
    mask = address.netmask
    network = ip_network(f"{addr}/{mask}", False)

    exclusions = (exclusion
                  for pr in private_ranges
                  for exclusion in pr.address_exclude(network))
    exclusion = next(exclusions)

  else:
    print(f"ERROR! -- No IPv4 addr for {mac_lf}", file=stderr)
    exit(1)


main()


#!/usr/bin/with-contenv python3

from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from json import loads
from os import environ
from os.path import join
from shutil import get_terminal_size
from socket import AddressFamily
from subprocess import PIPE, run
from sys import stderr, stdout
from typing import Any, Dict, List, Iterable, Iterator

from psutil import net_if_addrs


_vmrc_ = "/vmrc"
_nat_rc_ = "nat.xml"


def bold_print(message: str, sep="-", file=stdout) -> None:
  _, cols = get_terminal_size()
  print(sep * cols, file=file)
  print(message, file=file)
  print(sep * cols, file=file)


def slurp(path: str) -> bytes:
  with open(path, "rb") as fd:
    return fd.read()


def spit(path: str, data: bytes) -> None:
  with open(path, "wb") as fd:
    fd.write(data)


def check_br() -> None:
  ret = run(["ip", "-j", "link", "show", "type", "bridge"], stdout=PIPE)
  if ret.returncode != 0:
    exit(ret.returncode)
  json = loads(ret.stdout.decode())
  bridges = (br["ifname"] for br in json)
  bridge = environ["VIRT_NAT_NAME"]
  if bridge in bridges:
    bold_print(f"ERROR! -- Already Exists :: {bridge}")
    exit(1)


def usable_ipv4(addr: Any) -> bool:
  return (addr.family == AddressFamily.AF_INET
          and not ip_address(addr.address).is_loopback)


def p_network(address: Any) -> IPv4Network:
  addr = address.address
  mask = address.netmask
  network = ip_network(f"{addr}/{mask}", False)
  return network


def p_networks() -> Iterable[IPv4Network]:
  if_addrs = net_if_addrs()
  for addrs in if_addrs.values():
    for addr in addrs:
      if usable_ipv4(addr):
        yield p_network(addr)


def p_non_overlapping_exclusions(networks: List[IPv4Network]) -> Iterable[IPv4Network]:
  private_ranges: List[IPv4Network] = [
      ip_network("10.0.0.0/8"),
      ip_network("172.16.0.0/12"),
      ip_network("192.168.0.0/16"),
  ]
  for private_range in private_ranges:
    for network in networks:
      for exclusion in private_range.address_exclude(network):
        if exclusion.num_addresses < 65535:
          yield exclusion


def p_non_overlapping(networks: List[IPv4Network]) -> Iterable[IPv4Network]:
  exclusions = p_non_overlapping_exclusions(networks)
  for exclusion in exclusions:
    if all(not exclusion.overlaps(network)
           for network in networks):
      yield exclusion


def envsubst(values: Dict[str, str], path: str) -> None:
  template = slurp(path)
  subst = ",".join(f"${{key}}" for key in values.keys())
  env = {**environ, **values}
  ret = run(["envsubst", subst], env=env, input=template, stdout=PIPE)
  if ret.returncode != 0:
    exit(ret.returncode)
  else:
    spit(path, ret.stdout)


def main() -> None:
  check_br()
  networks: List[IPv4Network] = [*p_networks()]
  subnet: IPv4Network = next(p_non_overlapping(networks))

  it: Iterator[IPv4Network] = subnet.hosts()
  MASK = str(subnet.netmask)
  ROUTER = str(next(it))
  BEGIN = str(next(it))
  END = str(subnet.broadcast_address - 1)

  nat_rc = join(_vmrc_, _nat_rc_)
  env = {"VIRT_NAT_NAME": environ["VIRT_NAT_NAME"],
         "MASK": MASK, "ROUTER": ROUTER,
         "BEGIN": BEGIN, "END": END}
  envsubst(env, nat_rc)


main()


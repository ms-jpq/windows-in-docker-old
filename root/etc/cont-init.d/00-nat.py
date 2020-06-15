#!/usr/bin/with-contenv python3

from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from os import environ
from os.path import join
from socket import AddressFamily
from subprocess import PIPE, run
from sys import stderr
from typing import Any, Dict, List

from psutil import net_if_addrs


_vmrc_ = "/vmrc"
_nat_rc_ = "nat.xml"


private_ranges: List[IPv4Network] = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
]


def slurp(path: str) -> bytes:
  with open(path, "rb") as fd:
    return fd.read()


def spit(path: str, data: bytes) -> None:
  with open(path, "wb") as fd:
    fd.write(data)


def usable_ipv4(addr: Any) -> bool:
  if addr.family != AddressFamily.AF_INET:
    return False
  ip = ip_address(addr.address)
  if ip.is_loopback:
    return False
  return True


def p_addrs() -> List[Any]:
  if_addrs = net_if_addrs()
  names = (name
           for name, addrs in if_addrs.items()
           if any(usable_ipv4(addr) for addr in addrs))
  mac_lf = environ.get("VIRT_NAT_IF") or next(names)
  addrs = if_addrs[mac_lf]
  return addrs


def p_exclusions(network: IPv4Network) -> IPv4Network:
  exclusions = (exclusion
                for pr in private_ranges
                for exclusion in pr.address_exclude(network)
                if exclusion.num_addresses < 65535)
  return exclusions


def envsubst(address: Any) -> None:
  addr = address.address
  mask = address.netmask
  network = ip_network(f"{addr}/{mask}", False)

  exclusions = p_exclusions(network)
  new = next(exclusions)
  it = new.hosts()

  MASK = str(new.netmask)
  ROUTER = str(next(it))
  BEGIN = str(next(it))
  END = str(new.broadcast_address - 1)

  nat_rc = join(_vmrc_, _nat_rc_)
  env = {**environ,
         "MASK": MASK, "ROUTER": ROUTER,
         "BEGIN": BEGIN, "END": END}
  subst = "${VIRT_NAT_NAME},${ROUTER},${MASK},${BEGIN},${END}"
  xml = slurp(nat_rc)
  ret = run(["envsubst", subst], env=env, input=xml, stdout=PIPE)

  if ret.returncode != 0:
    exit(ret.returncode)
  else:
    spit(nat_rc, ret.stdout)


def main() -> None:
  addrs = p_addrs()
  if not addrs:
    raise Exception("Missing IPv4 if @ $VIRT_NAT_IF")

  address = next(addr for addr in addrs
                 if addr.family == AddressFamily.AF_INET)
  if address:
    envsubst(address)

  else:
    print(f"ERROR! -- No IPv4 addr for {mac_lf}", file=stderr)
    exit(1)


main()


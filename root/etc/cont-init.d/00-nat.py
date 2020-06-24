#!/usr/bin/with-contenv python3

from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from json import loads
from os import environ
from os.path import join
from random import randint
from shutil import get_terminal_size
from socket import AddressFamily
from subprocess import PIPE, run
from sys import stderr, stdout
from typing import Any, Dict, List, Iterable, Iterator, Optional
from xml.dom import minidom


_vmdk_ = "/config"
_vmrc_ = "/vmrc"
_nat_rc_ = join(_vmrc_, "nat.xml")
_ip_rc_ = join(_vmrc_, "ip_addr")


def bold_print(message: str, sep="-", file=stdout) -> None:
  _, cols = get_terminal_size()
  print(sep * cols, file=file)
  print(message, file=file)
  print(sep * cols, file=file)


def call_into(prog: str,
              *args: List[str],
              input: bytes = None,
              env: Dict[str, str] = None) -> bytes:
  ret = run([prog, *args], input=input, env=env, stdout=PIPE)
  if ret.returncode != 0:
    exit(ret.returncode)
  else:
    return ret.stdout


def slurp(path: str) -> bytes:
  with open(path, "rb") as fd:
    return fd.read()


def spit(path: str, data: bytes) -> None:
  with open(path, "wb") as fd:
    fd.write(data)


def envsubst(values: Dict[str, str], path: str) -> None:
  template = slurp(path)
  subst = ",".join("${" + key + "}" for key in values.keys())
  env = {**environ, **values}
  out = call_into("envsubst", subst, env=env, input=template)
  spit(path, out)


def check_br() -> None:
  out = call_into("ip", "-j", "link", "show", "type", "bridge")
  bridges = loads(out.decode())
  br_names = (br["ifname"] for br in bridges)
  name = environ["NAT_NAME"]

  if name in br_names:
    bold_print(f"ERROR! -- Bridge Already Exists :: {name}")
    exit(1)


def p_networks() -> Iterable[IPv4Network]:
  out = call_into("ip", "-4", "-j", "route")
  routes = loads(out.decode())
  for route in routes:
    dst = route["dst"]
    try:
      yield ip_network(dst)
    except ValueError:
      pass


def private_subnets() -> Iterable[IPv4Network]:
  private_ranges: List[IPv4Network] = [
      ip_network("192.168.0.0/16"),
      ip_network("172.16.0.0/12"),
      ip_network("10.0.0.0/8"),
  ]
  for private_range in private_ranges:
    for i in range(16, 30):
      yield from private_range.subnets(new_prefix=i)


def p_exclude(parent: IPv4Network, child: IPv4Network) -> Iterable[IPv4Network]:
  try:
    yield from parent.address_exclude(child)
  except ValueError:
    yield parent


def p_non_overlapping_exclusions(networks: List[IPv4Network]) -> Iterable[IPv4Network]:
  for private_range in private_subnets():
    for network in networks:
      for exclusion in p_exclude(private_range, network):
        yield exclusion


def p_non_overlapping(networks: List[IPv4Network]) -> Iterable[IPv4Network]:
  exclusions = p_non_overlapping_exclusions(networks)
  for exclusion in exclusions:
    if all(not exclusion.overlaps(network)
           for network in networks):
      yield exclusion


def rand_mac() -> str:
  def mac_slot(): return format(randint(0, 255), 'x')
  mac = f"52:54:00:{mac_slot()}:{mac_slot()}:{mac_slot()}"
  return mac


def p_mac_addr(name: str) -> str:
  try:
    xml = slurp(join(_vmdk_, f"{name}.xml"))
    dom = minidom.parseString(xml)
    for interface in dom.getElementsByTagName("interface"):
      if interface.getAttribute("type") == "network":
        source = interface.getElementsByTagName("source")[0]
        mac = interface.getElementsByTagName("mac")[0]
        return mac.getAttribute("address")
    raise ValueError(f"Unable to parse XML -- Missing Mac Address\n{xml}")
  except OSError:
    pass
  else:
    return rand_mac()


def main() -> None:
  check_br()
  networks: List[IPv4Network] = [*p_networks()]
  subnet: IPv4Network = next(p_non_overlapping(networks))

  VM_NAME = environ["VM_NAME"]
  NAT_NAME = environ["NAT_NAME"]
  it: Iterator[IPv4Network] = subnet.hosts()
  MASK = str(subnet.netmask)
  ROUTER = str(next(it))
  BEGIN = str(next(it))
  VM_IP = str(next(it))
  END = str(subnet.broadcast_address - 1)
  VM_MAC = p_mac_addr(VM_NAME)

  values = {"NAT_NAME": NAT_NAME,
            "MASK": MASK, "ROUTER": ROUTER,
            "BEGIN": BEGIN, "END": END,
            "VM_MAC": VM_MAC, "VM_IP": VM_IP,
            "VM_NAME": VM_NAME}
  envsubst(values, _nat_rc_)
  spit(_ip_rc_, VM_IP.encode())
  out = call_into("route-nat",
                  "--bridge", NAT_NAME,
                  "--ip", VM_IP,
                  "--state", "on")
  print(out.decode())


main()


#!/usr/bin/with-contenv python3

from os import environ, listdir
from os.path import join
from random import randint
from re import Pattern, compile as re_compile
from subprocess import PIPE, run
from time import sleep
from typing import Dict, List


_vmrc_ = "/vmrc"
_macvtap_rc_ = "macvtap.xml"


def call(prog: str, *args: List[str]) -> None:
  ret = run([prog, *args])
  if ret.returncode != 0:
    exit(ret.returncode)


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


def new_mac() -> str:
  def fx(): return format(randint(0, 255), "x")
  return f"02:00:00:{fx()}:{fx()}:{fx()}"


def main() -> None:
  vbr_name = environ["VIRT_MACVTAP_NAME"]
  if_name = environ["VIRT_MACVTAP_IF"]
  if not if_name:
    return

  i = 0
  while True:
    ret = run(["ip", "link", "add",
               "link", if_name, "name", vbr_name,
               "type", "macvtap", "mode", "bridge"])
    if ret.returncode == 0:
      return
    elif i == 5:
      exit(1)
    else:
      i += 1
      sleep(1)

  call("ip", "link", "set", vbr_name, "address", new_mac())

  call("ip", "link", "set", vbr_name, "up")

  base = join("/sys/devices/virtual/net", vbr_name)
  re: Pattern = re_compile(r"tap\d+")
  for name in listdir(base):
    if re.match(name):
      spec = join(base, name, "dev")
      major, minor = slurp(spec).decode().split(":")

  call("mknod", join("/dev", vbr_name), "c", major, minor)

  call("ip", "link", "set", "dev", vbr_name, "up")

  macvtap_rc = join(_vmrc_, _macvtap_rc_)
  values = {
      "VIRT_MACVTAP_NAME":
      environ["VIRT_MACVTAP_NAME"],
      "VIRT_MACVTAP_IF":
      environ["VIRT_MACVTAP_IF"]}
  envsubst(values, macvtap_rc)


main()


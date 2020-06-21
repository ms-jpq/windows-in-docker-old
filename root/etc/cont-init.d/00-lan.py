#!/usr/bin/with-contenv python3

from os import environ, listdir
from os.path import join
from random import randint
from re import Pattern, compile as re_compile
from shutil import get_terminal_size
from subprocess import PIPE, run
from sys import stderr, stdout
from time import sleep
from typing import Dict, List


_vmrc_ = "/vmrc"
_lan_rc_ = "lan.xml"


def big_print(msg: str, sep="-", file=stdout) -> None:
  _, cols = get_terminal_size()
  print(sep * cols, file=file)
  print(msg, file=file)
  print(sep * cols, file=file)


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
  return
  vbr_name = environ["LAN_NAME"]
  if_name = environ["LAN_IF"]
  if not if_name:
    big_print("LAN_IF is Nil\nSkipping Initialization")
    exit(0)

  i = 0
  while True:
    ret = run(["ip", "link", "add",
               "link", if_name, "name", vbr_name,
               "type", "macvtap", "mode", "bridge"])
    if ret.returncode == 0:
      break
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

  values = {"LAN_NAME": environ["LAN_NAME"],
            "LAN_IF": environ["LAN_IF"]}
  lan_rc = join(_vmrc_, _lan_rc_)
  envsubst(values, lan_rc)


main()


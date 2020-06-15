#!/usr/bin/with-contenv python3


from os import environ
from subprocess import PIPE, run


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


def main() -> None:
  if_name = environ.get("VIRT_MACVTAP_IF")
  pass


#!/usr/bin/env python3

from os import listdir
from os.path import join, splitext
from typing import List, Iterable


_vmrc_dir_ = "/config"


def read(name: str) -> str:
  with open(name) as fd:
    return fd.read()


def is_xml(name: str) -> bool:
  _, ext = splitext(name)
  return ext == "xml"


def main() -> None:
  specs: Iterable[str] = (f
                          for name in listdir(_vmrc_dir_)
                          if is_xml(f := join(_vmrc_dir_, name)))
  for spec in specs:
    xml = read(spec)


main()

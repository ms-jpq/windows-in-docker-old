#!/usr/bin/env python3

from os.path import basename, dirname, splitext
from typing import Any, Callable, Dict, List

from jinja2 import Environment, FileSystemLoader,  StrictUndefined
from psutil import net_if_addrs


def read(name: str) -> str:
  with open(name) as fd:
    return name.read()


def write(name: str, text: str) -> None:
  with open(name, "w") as fd:
    fd.write(text)


def build_j2(src: str, filters: Dict[str, Callable] = {}) -> Environment:
  j2 = Environment(
      enable_async=True,
      trim_blocks=True,
      lstrip_blocks=True,
      undefined=StrictUndefined,
      loader=FileSystemLoader(src))
  j2.filters = {**j2.filters, **filters}
  return j2


def render_j2(dest: str, values: Dict[str, Any]) -> None:
  full, _ = splitext(dest)
  base = basename(full)
  parent = dirname(full)
  j2 = build_j2(parent)
  content = j2.get_template(dest).render(**values)
  write(full, content)


def main() -> None:
  interfaces: List[str] = [name
                           for name in net_if_addrs().keys()
                           if name != "lo"]

  render_j2("/vmrc/macvtap0.xml.j2", {"interfaces": interfaces})


main()

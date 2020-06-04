#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from multiprocessing import cpu_count
from os import chdir, popen
from subprocess import run
from sys import stderr, stdout
from typing import List, Tuple
from uuid import uuid4

from psutil import net_if_addrs

_install_dir_ = "/install"
_vmdk_dir_ = "/config"
_sound_ = "hda"
_bridge_ = ""


def parse() -> Namespace:
  parser = ArgumentParser()

  parser.add_argument("-d", "--dry", action="store_true")
  parser.add_argument("-n", "--name", required=True)
  parser.add_argument("-c", "--cpus", default=cpu_count())
  parser.add_argument("-m", "--memory", default=4000)
  parser.add_argument("-s", "--disk-size", default=100)

  parser.add_argument("--vram", default=256000)
  parser.add_argument("--bios", action="store_true", default=False)

  parser.add_argument(
      "--install-media", default=f"{_install_dir_}/windows.iso")
  parser.add_argument("--install-drivers",
                      default=f"{_install_dir_}/drivers.iso")
  parser.add_argument("--extra", default="")

  return parser.parse_args()


def install(args: Namespace) -> List[str]:
  vmdk = f"{_vmdk_dir_}/{args.name}.img"
  return f"""
    virt-install
    {"" if args.bios else "--boot uefi"}
    --noautoconsole
    --features kvm_hidden=on
    --virt-type kvm
    --os-variant=win10
    --vcpus {args.cpus},sockets=1
    --cpu host-passthrough
    --memory {args.memory}
    --controller type=scsi,model=virtio-scsi
    --disk path={vmdk},size={args.disk_size},format=raw,sparse=true,bus=scsi,discard=unmap,io=threads,cache=none
    --network bridge=br0,model=virtio
    --graphics vnc,listen=0.0.0.0
    --video qxl,ram={args.vram}
    --channel unix,target_type=virtio,name=org.qemu.guest_agent.0
    --disk {args.install_media},device=cdrom
    --disk {args.install_drivers},device=cdrom
    --qemu-commandline="-soundhw"
    --qemu-commandline="{_sound_}"
    --qemu-commandline="-uuid"
    --qemu-commandline="{uuid4()}"
    --name {args.name}
    --check disk_size=off
    {args.extra}
    {"--print-xml --dry-run" if args.dry else ""}
    """.split()


def main() -> None:
  chdir(_install_dir_)
  print("\n" * 10)
  try:
    args = parse()
    cmd = install(args)
    ret = run(cmd, stdout=stdout, stderr=stderr)
    exit(ret.returncode)
  except:
    raise
  finally:
    print("\n" * 10)


main()

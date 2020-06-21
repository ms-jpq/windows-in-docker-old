# DONT FORK IT IM NOT DONE WHY YOU FORK
# IT DOESNT WORK RIGHT NOW

# Windows in Docker | WIND

Browser > VNC > Docker > KVM > Windows

## WHY?

QEMU + KVM has a bunch of moving parts, not very user friendly.

This image is super user friendly, it comes with:

1) Browser UI

2) NAT + Lan networking out of the box

3) Literally single line install

4) Built-in Windows drivers

5) Crazy easy customizations, ie. `--cpus=9 --memory=6024 --size=120`

## Instructions

### Prerequisites

You hardware must be able to run `KVM`. (Most computer can run at least 1 layer of virtualization now days.)

### Install

Run

### Environmental Variables

#### VNC

- `-e SCR_WIDTH=1600`
- `-e SCR_HEIGHT=900`

#### noVNC UI

- `-e PATH_PREFIX=/`
- `-e RECON_DELAY=250` reconnection delay (ms)
- `-e PAGE_TITLE=KVM`

#### Virtualization

Libvirt look for `VM_NAME.xml` to boot.

- `-e VM_NAME=wind`

### Ports

- `-p 80:8080` noVNC web UI

- `-p 5900:5900` VNC

### Volumes

- `-v ./vm_data:/config`

- `-v ./install_media:/install`

Works on my machine ™.


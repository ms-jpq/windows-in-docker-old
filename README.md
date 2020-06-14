# WIND - Windows in Docker

Browser > VNC > Docker > Arch > KVM > Windows

Oh, and it uses LXD too.

## WHY?

1) I use Arch btw

2) Got this idea at 3AM

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
- `-e VNC_RESIZE=scale|remote|off` remote = rescale remote desktop, scale = stretch remote desktop
- `-e RECON_DELAY=250` reconnection delay (ms)
- `-e PAGE_TITLE=KVM`

#### Virtualization

LXD is used to solely provide a network bridge friendly to most network typology

- `-e VIRTBR_NAME=lxdbr0` will create this bridge if does it not exist

### Ports

- `-p 80:8080` noVNC web UI

- `-p 5900:5900` VNC

### Volumes

- `-v ./vm_data:/config`

- `-v ./install_media:/install`

## Disclaimer

This image is rebuilt from CI every 24 hours.

I have no time to test if Arch randomly breaks something upstream, please file an issue if something breaks.

Works on my machine ™.


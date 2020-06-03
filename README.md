# VID - VM in Docker

Docker + Windows + VNC + noVNC web UI

WHY?

So you can run Windows inside Docker inside a browser

## Usage

### Common Environmental Variables

#### VNC

- `-e SCR_WIDTH=1600`
- `-e SCR_HEIGHT=900`

#### noVNC UI

- `-e PATH_PREFIX=/`
- `-e VNC_RESIZE=scale|remote|off` remote = rescale remote desktop, scale = stretch remote desktop
- `-e RECON_DELAY=250` reconnection delay (ms)
- `-e PAGE_TITLE=🐳`

### Common Ports

- `-p 80:8080` noVNC web UI

- `-p 5900:5900` VNC

### Common Volumes

- `-v ./appconfig:/config`


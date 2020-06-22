# WORK IN PROGRESS

---

# [WIND - Windows in Docker](https://ms-jpq.github.io/windows-in-docker)

Browser > Docker > KVM > Windows

Thank you Redhat, very legal & very cool.

## WHY?

QEMU + KVM has a relatively involved setup, not very user friendly.

This image is super user friendly, it comes with:

1. Browser UI

2. Networking out of the box

3. Literally copy paste install

4. Built-in Windows drivers

5. Crazy easy customizations, ie. `--cpus=9 --memory=6024 --size=120`

## Preview

![preview1 img](https://raw.githubusercontent.com/ms-jpq/windows-in-docker/gates/preview/scr.png)

![preview2 img](https://raw.githubusercontent.com/ms-jpq/windows-in-docker/gates/preview/drivers.png)

## Instructions

### Prerequisites

You hardware must be able to run `KVM`. (Most computer can run at least 1 layer of virtualization now days.)

### Install

Run the command below, and head to Firefox at port 8080 to finish installation

```sh
docker -it --rm \
  --privileged \
  -v /lib/modules:/lib/modules:ro \
  -p 8080:65080 \
  -v /vm_image_dir:/config \
  -v /iso_dir:/install \
  msjpq/kvm-windows new <windows.iso>
```

**Add `--bios`, if your windows version is old**

`<windows.iso>` will eject after first poweroff, you will find the generated libvirt manifest under `/config`.

Run the command below to finish installation, and for future usage.

```sh
docker -it --rm \
  --privileged \
  -v /lib/modules:/lib/modules:ro \
  -p 8080:65080 \
  -v /vm_image_dir:/config \
  msjpq/kvm-windows
```

### Drivers

You will need to manually install some of drivers, (VirtIO is annoying like that).

#### Essential

1. The harddrive drivers will need to be installed before first reboot.

2. The ethernet drivers will need to be installed after first login under Device Manager.

#### Whatever

Things like `qxl`, or `balloon` can also be installed under Device Manager. Not really important though.

**All drivers are included with the default install, under `D:/` or `E:/` drive.**

#### Customization

Additional flags to pass onto `new <image name> <flag> <flag> ...`

| Flag        | Default  | Option                                                                    |
| ----------- | -------- | ------------------------------------------------------------------------- |
| `--bios`    | `False`  | Boot `bios` instead of `uefi`                                             |
| `-os`       | `win10`  | Windows distro                                                            |
| `--cpus`    | `#cores` | Number of virtual cpus                                                    |
| `--memory`  | `4000`   | (MB)                                                                      |
| `--vram`    | `256`    | (MB)                                                                      |
| `--size`    | `100`    | (GB)                                                                      |
| `--dry-run` | `False`  | Dry run                                                                   |
| `--extra`   | `None`   | Extra args for [`virt-install`](https://linux.die.net/man/1/virt-install) |

### Environmental Variables

#### Browser UI

- `-e PATH_PREFIX=/`
- `-e VNC_RESIZE=scale|off`
- `-e RECON_DELAY=250` reconnection delay (ms)

#### Virtualization

Libvirt look for `VM_NAME.xml` to boot.

`new` will create `VM_NAME.xml` and `VM_NAME.img`.

- `-e VM_NAME=wind`

### Ports

- `-p 8080:65080` noVNC web UI

- `-p 5900:65059` VNC

### Volumes

Libvirt manifests are stored in`/config`, along with VM images.

- `-v ./vm_data:/config`

You need to supply your own `windows.iso`, for obvious reasons.

- `-v ./install_media:/install`

### Disclaimer

Works on my machine ™.


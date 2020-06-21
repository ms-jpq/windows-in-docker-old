FROM msjpq/kvm-windows-build:latest AS build
FROM ubuntu:focal

ARG S6_VER="2.0.0.1"
ARG NO_VNC_VER="1.1.0"
ARG WEB_SOCK_VER="0.9.0"

RUN mkdir /_install


## S6 Overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_VER}/s6-overlay-amd64.tar.gz /_install
RUN tar xzf /_install/s6-overlay-amd64.tar.gz -C / --exclude="./bin" && \
    tar xzf /_install/s6-overlay-amd64.tar.gz -C /usr ./bin
ENV S6_BEHAVIOUR_IF_STAGE2_FAILS=2
ENTRYPOINT ["/init"]


## KVM-QEMU
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
    qemu-kvm \
    ovmf \
    libvirt-daemon \
    libvirt-clients \
    virt-top \
    virtinst \
    iptables \
    ebtables \
    dnsmasq \
    dmidecode \
    iproute2 \
    bridge-utils
RUN groupadd --system kvm && \
    useradd -U -s /usr/sbin/nologin -d /var/lib/libvirt         libvirt-qemu && \
    useradd -U -s /usr/sbin/nologin -d /var/lib/libvirt/dnsmasq libvirt-dnsmasq
EXPOSE 65059


## NOVNC
ADD https://github.com/novnc/noVNC/archive/v${NO_VNC_VER}.zip /_install
ADD https://github.com/novnc/websockify/archive/v${WEB_SOCK_VER}.zip /_install
RUN cd /_install && \
    apt install -y unzip nginx gettext-base python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install numpy && \
    unzip v${NO_VNC_VER}.zip && \
    unzip v${WEB_SOCK_VER}.zip && \
    mv noVNC-${NO_VNC_VER} /novnc && \
    mv websockify-${WEB_SOCK_VER} /novnc/utils/websockify
ENV PATH_PREFIX=/ \
    VNC_RESIZE=scale \
    RECON_DELAY=250 \
    PAGE_TITLE=KVM
EXPOSE 65080


## Dependencies
COPY --from=build /usr/share/virtio/ /drivers/
COPY root /
ENV S6_CMD_WAIT_FOR_SERVICES=1 \
    NAT_NAME=windbr0 \
    VM_NAME=wind
VOLUME ["/config", "/install"]


## Cleanup
RUN apt autoremove -y && \
    apt clean && \
    rm -r /_install


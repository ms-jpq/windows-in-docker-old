FROM archlinux:latest

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


# ## KVM-QEMU
# RUN apt update && \
#     apt install -y \
#     qemu-kvm \
#     ovmf \
#     libvirt-daemon \
#     libvirt-clients \
#     virt-top \
#     virtinst
# RUN groupadd --system kvm && \
#     useradd -U -s /usr/sbin/nologin -d /var/lib/libvirt         libvirt-qemu && \
#     useradd -U -s /usr/sbin/nologin -d /var/lib/libvirt/dnsmasq libvirt-dnsmasq
# EXPOSE 5900


# ## Bridging
# RUN apt install -y \
#     iptables \
#     dnsmasq \
#     bridge-utils


# ## NOVNC
# ADD https://github.com/novnc/noVNC/archive/v${NO_VNC_VER}.zip /_install
# ADD https://github.com/novnc/websockify/archive/v${WEB_SOCK_VER}.zip /_install
# RUN cd /_install && \
#     apt install -y unzip python2 nginx gettext-base && \
#     unzip v${NO_VNC_VER}.zip && \
#     unzip v${WEB_SOCK_VER}.zip && \
#     mv noVNC-${NO_VNC_VER} /novnc && \
#     mv websockify-${WEB_SOCK_VER} /novnc/utils/websockify && \
#     ln -s /usr/bin/python2 /usr/bin/python
# ENV PATH_PREFIX=/ \
#     VNC_RESIZE=scale \
#     RECON_DELAY=250 \
#     PAGE_TITLE=KVM
# EXPOSE 8080


# ## Build Dependencies
# ADD https://raw.githubusercontent.com/LuRsT/hr/master/hr /usr/local/bin
# RUN chmod +x /usr/local/bin/hr && \
#     apt install -y python3 python3-pip && \
#     pip3 install \
#     jinja2 \
#     psutil \
#     libvirt-python
# COPY _root /
# ENV S6_CMD_WAIT_FOR_SERVICES=1 \
#     VM_NAME=wind
# VOLUME ["/config", "/install"]



# # Cleanup
# RUN apt autoremove -y && \
#     apt clean && \
#     rm -r /_install


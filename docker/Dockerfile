FROM fedora:latest


ARG S6="https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.3/s6-overlay-amd64-installer"


RUN dnf install -y \
    wget \
    dbus-daemon \
    cockpit \
    cockpit-machines && \
    dnf clean all && \
    rm -rf /tmp/*


RUN wget "${S6}" --output-document /tmp/s6 && \
    chmod +x /tmp/s6 && \
    /tmp/s6 / && \
    rm -rf /tmp/*
ENV S6_KEEP_ENV=1 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2
ENTRYPOINT ["/init"]


WORKDIR /srv/run
COPY . /


RUN printf '%s' 'root:docker!' | chpasswd

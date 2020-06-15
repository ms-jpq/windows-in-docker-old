FROM archlinux:latest

## AUR
RUN pacman -Sy --noconfirm \
    base-devel git
COPY build /


## Drivers
RUN git clone --depth=1 https://aur.archlinux.org/virtio-win.git && \
    cd virtio-win && \
    chgrp nobody "$PWD" && \
    chmod g+ws "$PWD" && \
    sudo -u nobody makepkg --install --nodeps --noconfirm


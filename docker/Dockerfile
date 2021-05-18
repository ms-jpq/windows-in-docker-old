FROM fedora:latest


ARG S6="https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.1/s6-overlay-amd64-installer"
ARG WOK="https://github.com/kimchi-project/wok/releases/download/3.0.0/wok-3.0.0-0.fc31.noarch.rpm"
ARG REQ="https://raw.githubusercontent.com/kimchi-project/kimchi/3.0.0/requirements-FEDORA.txt"
ARG KIM="https://github.com/kimchi-project/kimchi/releases/download/3.0.0/kimchi-3.0.0-0.fc31.noarch.rpm"


WORKDIR /tmp
RUN dnf install -y \
    wget \
    python3-pip


RUN wget "$S6" --output-document s6 && \
    wget "$WOK" --output-document wok.rpm && \
    wget "$REQ" --output-document requirements.txt && \
    wget "$KIM" --output-document kimchi.rpm


RUN ./s6 && \
    pip3 install --requiremnet requirements.txt && \
    dnf install -y wok.rpm kimchi.rpm

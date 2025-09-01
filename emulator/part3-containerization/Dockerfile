FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    retroarch \
    libgl1-mesa-dri \
    mesa-vulkan-drivers \
    libglu1-mesa \
    libx11-6 libxext6 libxi6 libxrandr2 libxcursor1 libxrender1 libxfixes3 \
    pulseaudio-utils \
    udev ca-certificates \
    xdg-utils \
    x11-xserver-utils \
    mesa-utils \
    mesa-utils-extra \
  && rm -rf /var/lib/apt/lists/*

ARG UID=1000
ARG GID=1000
#RUN groupadd -g ${GID} app && useradd -m -u ${UID} -g ${GID} app
# -l prevents lastlog/faillog writes which can bloat the image
RUN groupadd -g ${GID} app && useradd -l -m -u ${UID} -g ${GID} app
USER app
WORKDIR /home/app

RUN mkdir -p /home/app/roms /home/app/bios /home/app/saves /home/app/system /home/app/config

ENV XDG_CONFIG_HOME=/home/app/config
ENV PULSE_SERVER=unix:/run/user/1000/pulse/native

CMD ["retroarch", "--version"]

# Raspberry Pi Emulator DevOps

A portfolio-friendly Pi 5 project that shows **DevOps + CI/CD** around a containerized RetroArch emulator, plus a **monitoring stack** (Prometheus, Grafana, node-exporter, cAdvisor).

---

## Quickstart (Emulator • Pi 5 / ARM64)

**Prereqs:** Docker + Docker Compose on your Pi.

```bash
# allow X11 apps to open windows (once per login/session)
DISPLAY=:0 xhost +local:

# host ROM folders (mounted to /roms in the container)
mkdir -p ~/ROMs/{gb,snes,genesis}

# run a game (software profile is rock-solid on Pi 5)
make play-gb      PROFILE=software ROM='roms/gb/YourGame.gb'
make play-snes    PROFILE=software ROM='roms/snes/YourGame.sfc'
make play-genesis PROFILE=software ROM='roms/genesis/YourGame.md'
```

### Profiles
- `software` → uses llvmpipe (no `/dev/dri`), most compatible on Pi 5  
- `gpu` → binds `/dev/dri` (experimental on Pi 5 due to Mesa mismatch)

### Volumes & Paths
- Host `~/ROMs/{gb,snes,genesis}` → container `/roms/...`  
- Saves/config: `./data/saves`, `./data/config` (git-ignored)

### Common Issues
- No window? Run `DISPLAY=:0 xhost +local:` and try `PROFILE=software`.  
- `/dev/dri` perm errors on `gpu`? Put your numeric `video`/`render` GIDs under `group_add` in `docker-compose.yml`.  
- Audio: Pulse socket is mounted; ALSA `snd_seq` warnings are harmless.

---

## CI / CD

- **Lint:** Hadolint (`failure-threshold: error`)  
- **Security:** Trivy filesystem scan (fails on High/Critical)  
- **Build:** ARM64 buildx + QEMU smoke (`retroarch --version`)  
- **Publish:** push a tag `v*` to publish to GHCR:
  ```
  ghcr.io/elvin-rivera23/raspberry-pi-emulator-devops/retroarch:<tag>
  ```

**Release flow**
```bash
git tag -a v0.1.1 -m "cores + play targets + X11/Pulse mounts"
git push origin v0.1.1
```

---

## Monitoring Stack (Prometheus + Grafana)

Containerized observability for a Raspberry Pi 5:
- **node-exporter** (Pi system metrics)
- **cAdvisor** (container metrics)
- **Prometheus** (scrapes & stores)
- **Grafana** (dashboards)

Run:
```bash
cd monitoring
docker compose up -d
```

---

## Dev Tips

- `make smoke` / `make smoke PROFILE=gpu` → bring up and print versions.  
- `make cores` → list installed libretro cores inside the container.  
- Switch image source without editing YAML:
  ```bash
  make smoke IMAGE=ghcr.io/elvin-rivera23/raspberry-pi-emulator-devops/retroarch:latest
  ```
- ROMs are **never** tracked by git; `.gitignore` protects config/saves too.

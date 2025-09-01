PROFILE ?= software
SERVICE := $(if $(filter $(PROFILE),gpu),retroarch-gpu,retroarch-soft)
DC := docker compose
IMAGE ?= retroarch:local
GAMBATTE ?= /usr/lib/aarch64-linux-gnu/libretro/gambatte_libretro.so
SNES9X   ?= /usr/lib/aarch64-linux-gnu/libretro/snes9x_libretro.so
GENESIS  ?= /usr/lib/aarch64-linux-gnu/libretro/genesis_plus_gx_libretro.so


.PHONY: up down logs ps smoke gui cores play-gb play-snes play-genesis clean

up:
	IMAGE=$(IMAGE) COMPOSE_PROFILES=$(PROFILE) $(DC) up -d --remove-orphans
	@echo "Profile: $(PROFILE) -> Service: $(SERVICE)"

down:
	$(DC) down

logs:
	$(DC) logs -f $(SERVICE)

ps:
	$(DC) ps

smoke: up
	$(DC) exec $(SERVICE) bash -lc "retroarch --version"
	$(DC) ps

gui: up
	$(DC) exec $(SERVICE) bash -lc "retroarch"


# List installed cores inside the container (always succeed)
cores: up
	$(DC) exec $(SERVICE) bash -lc 'for d in /usr/lib/*/libretro /usr/lib/libretro; do [ -d "$$d" ] && echo "--- $$d" && ls -1 "$$d"; done || true'

# ---- Play targets (quotes handle spaces in filenames)
# Usage: make play-gb ROM=roms/gb/YourGame.gb
play-gb: up
	@if [ -z "$(ROM)" ]; then echo "Usage: make play-gb ROM=roms/gb/YourGame.gb"; exit 2; fi
	$(DC) exec $(SERVICE) bash -lc "retroarch -L $(GAMBATTE) \"/roms/gb/$(notdir $(ROM))\""

# Usage: make play-snes ROM=roms/snes/YourGame.sfc
play-snes: up
	@if [ -z "$(ROM)" ]; then echo "Usage: make play-snes ROM=roms/snes/YourGame.sfc"; exit 2; fi
	$(DC) exec $(SERVICE) bash -lc "retroarch -L $(SNES9X) \"/roms/snes/$(notdir $(ROM))\""

# Usage: make play-genesis ROM=roms/genesis/YourGame.md
play-genesis: up
	@if [ -z "$(ROM)" ]; then echo "Usage: make play-genesis ROM=roms/genesis/YourGame.md"; exit 2; fi
	$(DC) exec $(SERVICE) bash -lc "retroarch -L $(GENESIS) \"/roms/genesis/$(notdir $(ROM))\""

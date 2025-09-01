PROFILE ?= software
SERVICE := $(if $(filter $(PROFILE),gpu),retroarch-gpu,retroarch-soft)
DC := docker compose

.PHONY: up down logs ps smoke gui

up:
	COMPOSE_PROFILES=$(PROFILE) $(DC) up -d --remove-orphans
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

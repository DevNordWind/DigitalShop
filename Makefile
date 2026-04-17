COMPOSE = docker compose -f docker/docker-compose.yml

polling-up:
	$(COMPOSE) --profile polling up -d

polling-down:
	$(COMPOSE) --profile polling down

polling-logs:
	$(COMPOSE) logs -f bot-polling

webhook-up:
	$(COMPOSE) --profile webhook up -d

webhook-down:
	$(COMPOSE) --profile webhook down

webhook-logs:
	$(COMPOSE) logs -f bot-webhook

payment-up:
	$(COMPOSE) --profile payment up -d

payment-down:
	$(COMPOSE) --profile payment down

payment-logs:
	$(COMPOSE) logs -f payment-webhook

full-up:
	$(COMPOSE) --profile webhook --profile payment up -d

full-down:
	$(COMPOSE) --profile webhook --profile payment down

build:
	$(COMPOSE) build

ps:
	$(COMPOSE) ps

.PHONY: \
	polling-up polling-down polling-logs \
	webhook-up webhook-down webhook-logs \
	payment-up payment-down payment-logs \
	full-up full-down \
	build ps
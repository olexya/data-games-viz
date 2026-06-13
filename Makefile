# Makefile — pilotage de la plateforme data-games-viz (macOS / Linux)
# Équivalent Windows : make.ps1 (PowerShell)
# Usage : make <cible>   (make help pour la liste)

COMPOSE ?= docker compose
E2E := tests/e2e/test_platform.py

.DEFAULT_GOAL := help
.PHONY: help up down restart logs ps test clean urls

help: ## Affiche cette aide
	@echo "Cibles disponibles :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS=":.*?## "} {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

up: ## Démarre toute la plateforme en arrière-plan
	@echo "⏳ Premier lancement : prévoir 3-5 min (pull des images, installs, ingestion Steam, build dbt + Evidence)."
	@echo "   'make up' bloque tant que la 1re ingestion n'est pas finie (Evidence attend le loader)."
	@echo "   Les lancements suivants sont bien plus rapides. Suivi : 'make logs'."
	$(COMPOSE) up -d
	@$(MAKE) --no-print-directory urls

down: ## Arrête la plateforme (conserve les données)
	$(COMPOSE) down

restart: down up ## Redémarre la plateforme

reload: ## Force le rechargement des données Steam (ignore la fraîcheur)
	FORCE_RELOAD=true $(COMPOSE) up -d --force-recreate loader
	@echo "Rechargement des données déclenché. Suivi : make logs"

logs: ## Suit les logs de tous les services (Ctrl+C pour quitter)
	$(COMPOSE) logs -f

ps: ## État des conteneurs
	$(COMPOSE) ps

test: ## Lance les tests e2e (si la suite locale est présente)
	@if [ -f "$(E2E)" ]; then \
		python3 "$(E2E)"; \
	else \
		echo "Suite e2e absente ($(E2E)) — non publiée (locale)."; \
	fi

clean: ## Arrête tout ET supprime les volumes + données locales
	$(COMPOSE) down -v
	rm -rf docker-data

urls: ## Affiche les URLs d'accès
	@echo "Evidence : http://localhost:3000"
	@echo "Kestra   : http://localhost:8080  (admin@kestra.io / Kestra1234!)"
	@echo "Postgres : localhost:5432"

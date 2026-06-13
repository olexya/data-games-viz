# make.ps1 — pilotage de la plateforme data-games-viz (Windows / PowerShell)
# Équivalent du Makefile (macOS / Linux).
# Usage : .\make.ps1 <cible>        ex. .\make.ps1 up
#         (si l'exécution de scripts est bloquée :
#          powershell -ExecutionPolicy Bypass -File .\make.ps1 up)

param([string]$Target = "help")
$ErrorActionPreference = "Stop"
$E2E = "tests/e2e/test_platform.py"

function Show-Urls {
    Write-Host "Evidence : http://localhost:3000"
    Write-Host "Kestra   : http://localhost:8080  (admin@kestra.io / Kestra1234!)"
    Write-Host "Postgres : localhost:5432"
}

function Show-Help {
    Write-Host "Cibles disponibles :"
    Write-Host "  up        Démarre toute la plateforme en arrière-plan"
    Write-Host "  down      Arrête la plateforme (conserve les données)"
    Write-Host "  restart   Redémarre la plateforme"
    Write-Host "  reload    Force le rechargement des données Steam"
    Write-Host "  logs      Suit les logs de tous les services (Ctrl+C pour quitter)"
    Write-Host "  ps        État des conteneurs"
    Write-Host "  test      Lance les tests e2e (si la suite locale est présente)"
    Write-Host "  clean     Arrête tout ET supprime les volumes + données locales"
    Write-Host "  urls      Affiche les URLs d'accès"
}

switch ($Target.ToLower()) {
    "up"      {
        Write-Host "⏳ Premier lancement : prévoir 3-5 min (pull des images, installs, ingestion Steam, build dbt + Evidence)."
        Write-Host "   'up' bloque tant que la 1re ingestion n'est pas finie (Evidence attend le loader)."
        Write-Host "   Les lancements suivants sont bien plus rapides. Suivi : .\make.ps1 logs"
        docker compose up -d; Show-Urls
    }
    "down"    { docker compose down }
    "restart" { docker compose down; docker compose up -d; Show-Urls }
    "reload"  {
        $env:FORCE_RELOAD = "true"
        docker compose up -d --force-recreate loader
        Remove-Item Env:FORCE_RELOAD
        Write-Host "Rechargement des données déclenché. Suivi : .\make.ps1 logs"
    }
    "logs"    { docker compose logs -f }
    "ps"      { docker compose ps }
    "test"    {
        if (Test-Path $E2E) { python $E2E }
        else { Write-Host "Suite e2e absente ($E2E) — non publiée (locale)." }
    }
    "clean"   { docker compose down -v; if (Test-Path "docker-data") { Remove-Item -Recurse -Force "docker-data" } }
    "urls"    { Show-Urls }
    default   { Show-Help }
}

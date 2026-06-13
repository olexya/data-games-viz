-- Initialisation idempotente de la base/rôle Kestra.
-- Ne s'exécute qu'au premier init (pgdata vide), mais rendu ré-exécutable sans erreur.
\getenv DB KESTRA_POSTGRES_DB
\getenv USER KESTRA_POSTGRES_USER
\getenv PASSWORD KESTRA_POSTGRES_PASSWORD

-- Crée le rôle s'il n'existe pas
SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', :'USER', :'PASSWORD')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = :'USER')\gexec

-- Crée la base s'il n'existe pas (CREATE DATABASE hors transaction via \gexec)
SELECT format('CREATE DATABASE %I OWNER %I', :'DB', :'USER')
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'DB')\gexec

GRANT ALL PRIVILEGES ON DATABASE :"DB" TO :"USER";

\c :DB
GRANT ALL ON SCHEMA public TO :"USER";

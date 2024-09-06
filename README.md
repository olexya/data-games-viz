# Steam Stat
An application to understand statistique of [Steam](https://store.steampowered.com)

The application using [Kestra](https://kestra.io), [dbt](https://www.getdbt.com), [Evidence](https://evidence.dev) and [PostgreSQL](postgresql.org/)
## Installation
Download : Using git
```sh
42sh> git clone git@github.com:olexya/data-games-viz.git
```
Start : Using Docker
```sh
42sh> docker-compose up -d
```

## Viewing
Once installed, you can view the application by opening your browser at [localhost:3000](localhost:3000). Enjoy exploring Steam statistics!

## Achitecture
architecture des composants

## Study
(image data infrastructure open sources)
- [Ingestion and Transport](docs/architecture/ingestion_and_transport.md)
- [Storage](docs/architecture/storage.md)
- [Query and Processing](docs/architecture/storage.md)
- [Analysis and Output](docs/architecture/analysis_and_output.md)
- [Platform Management](docs/architecture/platform_management.md)

## Content
For information on the types of content available in the application, see:
[Content](docs/content.md)

## Credit
Special thanks to [Kestra](https://kestra.io), [dbt](https://www.getdbt.com), [Evidence](https://evidence.dev) and [PostgreSQL](postgresql.org/) for their contributions to this project.

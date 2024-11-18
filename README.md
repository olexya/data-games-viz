# Data Games Viz

Welcome to the Composable Data Platform project repository. This project was developed as part of an internship program with the primary objectives of:
- Identifying open source solutions available in the market for building a composable data platform (note: this list may not be exhaustive due to the vast number of solutions). (https://github.com/olexya/oss-data-tools-landscape)
- Demonstrating the functionality of these solutions through a simple example implementation

## Market Study

### Navigating the Open-Source Data Landscape
In today's data-driven world, a myriad of open-source solutions are available for processing, analyzing, and managing data. This abundance of options, while providing great flexibility and power, can also be overwhelming for businesses trying to select the right tools for their specific needs.

### The Challenge of Choice
The open-source community has developed numerous solutions for various aspects of data handling, including:
- Ingestion and Transport
- Storage
- Query and Processing
- Analysis and Output
- Platform Management

Github : https://github.com/olexya/oss-data-tools-landscape

While this diversity is a testament to the innovation in the field, it can make the decision-making process complex and time-consuming for organizations looking to build or enhance their data infrastructure.

## A working prototype
An application to understand statistique of [Steam](https://store.steampowered.com)

The application using [Kestra](https://kestra.io), [dbt](https://www.getdbt.com), [Evidence](https://evidence.dev) and [PostgreSQL](postgresql.org/)

### To launch the application

#### Download
Using git:
```sh
git clone https://github.com/olexya/data-games-viz.git
cd data-games-viz
```

#### Deployment
Start the application using Docker:
```sh
docker-compose up -d
```
The initial setup may take 3-5 minutes depending on your internet connection.

[More documentation](docs/usecase/content.md)

## Credit
Special thanks to [Kestra](https://kestra.io), [dbt](https://www.getdbt.com), [Evidence](https://evidence.dev) and [PostgreSQL](postgresql.org/) for their contributions to this project.
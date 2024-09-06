**Data Ingestion and Transport Tools**

With the help of my colleagues, I was able to compile a list of tools that fall under the category of data ingestion and transport. Here are some of the tools we've found:

- [Airbyte](https://github.com/airbytehq/airbyte) - Airbyte is an open-source platform for extracting data from various sources. It offers a range of connectors and APIs for automating data integration.
- [Meltano](https://github.com/meltano) - Meltano is an open-source platform for managing data pipelines. It allows users to extract, transform, and load data across multiple sources and destinations.
- [Singer IO](https://github.com/singer-io) - Singer IO is a Python library for building data integration pipelines. It provides a range of connectors for extracting data from various sources.

These tools are designed to automate the process of retrieving data from various sources. During my study, I was able to test Airbyte and found it to be a powerful tool for querying data. However, for my example infrastructure, I preferred using Python to retrieve the data because it allowed me to format the received data in a simpler SQL format.

I have tested Metabase, Matplotlib, Grafana, Superset, and Evidence. All of these tools share a similar approach, but function differently.

Matplotlib is a Python module for creating graphs. However, it requires building the entire visualization platform from scratch.

On the other hand, Superset and Metabase guide users through a powerful tool. While they can be a bit heavy to install, the advantage is that they cater to an audience that cannot develop.

Evidence is an tool with an interface that only serves to visualize data. It requires writing Markdown files containing SQL queries to create reports.

For example, I chose Evidence for my open-source project because it's easy to use and highly customizable.

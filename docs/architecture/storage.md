Here is the translation in English, replacing links with GitHub links and adding descriptions to each tool:

On the storage side, there are numerous storage and access engines available. The ones I've referenced are as follows:

- [Avro](https://github.com/apache/avro) - a data serialization system that enables efficient storage and processing of large datasets.
- [Debezium](https://github.com/debezium/debezium) - a distributed platform for Change Data Capture (CDC) that captures row-level changes from various databases and streams them to Kafka.
- [Delta Lake](https://github.com/delta-io/delta) - an open-source storage layer designed to make big data more accessible by providing a simple, SQL-based interface for querying and processing large datasets.
- [Hudi](https://github.com/apache/hudi) - an open-source data warehousing framework that provides fast and efficient storage and retrieval of large-scale datasets.
- [Iceberg](https://github.com/apache/iceberg) - a scalable, high-performance platform for storing and querying large-scale datasets, designed to be used with distributed computing frameworks like Spark.
- [Paimon](https://github.com/paimon-io/paimon) - an open-source data warehousing framework that provides fast and efficient storage and retrieval of large-scale datasets.
- [Parquet](https://github.com/apache/parquet-format) - a columnar storage format designed to store and process large-scale datasets efficiently, particularly for big data analytics workloads.
- [PostgreSQL](https://github.com/postgres/postgres) - an open-source relational database management system that provides robust support for SQL-based queries and transactions.

During my testing of the tools in the next step ([query_and_processing.md](query_and_processing.md)), I noticed that PostgreSQL was used in another tool that I'm planning to use. Therefore, my choice is to go with this tool.
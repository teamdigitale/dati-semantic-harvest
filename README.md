# Dati Semantic Harvest

This repository provides a github workflow that:

1. harvest sqlite data from a list of repositories (see `harvest.yml` workflow);
1. aggregates the harvested data into a vocabularies.db;
1. publishes the vocabularies.db so that it can be used by the Data API
   published via [dati-semantic-csv-apis](https://github.com/par-tec/dati-semantic-csv-apis).

The workflow is triggered by a schedule (every 24h) and by pull requests to the `main` branch.

Here is the link to the latest [vocabularies.db](https://github.com/par-tec/dati-semantic-harvest/raw/refs/heads/harvest/vocabularies.db).

## Testing

You can test this workflow locally using [act](https://github.com/nektos/act) and the `harvest` branch, which is used by the workflow to store the harvested data. For example:

```bash
act -j harvest
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this repository.

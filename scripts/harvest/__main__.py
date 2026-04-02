import argparse
import json
import logging

from .catalog import Catalog, remote_resource_exists


URL_TRANSLATIONS = (
    (
        "https://raw.githubusercontent.com/italia/dati-semantic-assets/master/VocabolariControllati/",
        "https://github.com/EricaCandido/dati-semantic-assets/raw/refs/heads/assets/VocabolariControllati/",
        # "https://raw.githubusercontent.com/teamdigitale/dati-semantic-csv-apis/assets/assets/controlled-vocabularies/",
    ),
    (
        "https://raw.githubusercontent.com/InailUfficio5/inail-ndc/main/",
        "https://raw.githubusercontent.com/teamdigitale/dati-semantic-csv-apis/assets/",
    ),
    (
        "https://raw.githubusercontent.com/INPS-it/NDC/main/",
        "https://raw.githubusercontent.com/teamdigitale/dati-semantic-csv-apis/assets/",
    ),
    (
        "https://github.com/istat/ndc-ontologie-vocabolari-controllati/tree/main/assets/controlled-vocabularies/economy/",
        "https://raw.githubusercontent.com/teamdigitale/dati-semantic-csv-apis/main/assets/controlled-vocabularies/",
    ),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List remote repositories from the harvest catalog."
    )
    parser.add_argument(
        "sparql_url",
        help="SPARQL endpoint URL used to load the catalog.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format for the repository list.",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        help="Logging level for catalog loading and validation.",
    )
    parser.add_argument(
        "--filter",
        help="Filter repositories by a specific keyword.",
    )
    return parser


def list_remote_repositories(
    catalog: Catalog, filter_keyword: str | None = None
) -> list[str]:
    repositories = set()

    def _get_items():
        for item in catalog.items():
            url_value = item.get("turtleDownloadUrl")
            if isinstance(url_value, list):
                yield from url_value
            elif isinstance(url_value, str):
                yield url_value

    items: set[str] = {
        url for url in _get_items() if not filter_keyword or filter_keyword in url
    }
    for url in items:
        logging.warning(f"Processing repository URL: {url}")

        for src, dst in URL_TRANSLATIONS:
            url = url.replace(src, dst)
        db_url = url[:-4] + ".db"
        if remote_resource_exists(db_url):
            repositories.add(db_url)
    return sorted(repositories)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.WARNING))

    catalog = Catalog(args.sparql_url)
    repositories = list_remote_repositories(catalog, filter_keyword=args.filter)

    if args.format == "text":
        for repository in repositories:
            print(repository)
    else:
        print(json.dumps(repositories, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

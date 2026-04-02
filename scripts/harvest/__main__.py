import argparse
import json
import logging

from .catalog import Catalog, get_value, remote_resource_exists


URL_TRANSLATIONS = (
    (
        "https://raw.githubusercontent.com/italia/dati-semantic-assets/master/VocabolariControllati",
        "https://raw.githubusercontent.com/teamdigitale/dati-semantic-csv-apis/assets/assets/controlled-vocabularies",
    ),
    (
        "https://raw.githubusercontent.com/InailUfficio5/inail-ndc/main/",
        "https://raw.githubusercontent.com/teamdigitale/dati-semantic-csv-apis/assets",
    ),
    (
        "https://raw.githubusercontent.com/INPS-it/NDC/main/",
        "https://raw.githubusercontent.com/teamdigitale/dati-semantic-csv-apis/assets",
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
    return parser


def list_remote_repositories(catalog: Catalog) -> list[str]:
    repositories = set()
    for node in catalog.items():
        if url := node.get("turtleDownloadUrl"):
            url = get_value(url)
            for src, dst in URL_TRANSLATIONS:
                url = url.replace(src, dst)
            if remote_resource_exists(url):
                repositories.add(url)
    return sorted(repositories)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.WARNING))

    catalog = Catalog(args.sparql_url)
    repositories = list_remote_repositories(catalog)

    if args.format == "text":
        for repository in repositories:
            print(repository)
    else:
        print(json.dumps(repositories, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

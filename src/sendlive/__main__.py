"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """sendlive."""


if __name__ == "__main__":
    main(prog_name="sendlive")  # pragma: no cover

"""Run TAMP Server Manager using `python -m tampp` or the `tampp` command."""

from tampp.main import TamppServer


def main() -> None:
    """Start the TAMP application."""
    TamppServer().run()


if __name__ == "__main__":
    main()

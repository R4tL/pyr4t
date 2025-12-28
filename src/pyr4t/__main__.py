"""Main module for the Pyr4t CLI."""

from .cli import build_parser


def main():
    """Main entry point for the Pyr4t CLI program."""

    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

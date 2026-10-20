"""Command line interface for FileFlow."""
from __future__ import annotations

import argparse
import logging
import sys

from .organizer import organize_directory

logger = logging.getLogger("fileflow")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fileflow",
        description="Automatically organize a messy folder into categorized subfolders.",
    )
    parser.add_argument(
        "directory", 
        help="Path to the folder you want to organize"
    )
    parser.add_argument(
        "-d", "--dry-run", 
        action="store_true", 
        help="Show what would be moved without actually moving files"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable debug logging"
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )

    try:
        summary = organize_directory(args.directory, dry_run=args.dry_run)
    except Exception as exc:
        logger.error("Error: %s", exc)
        return 1

    if not summary:
        logger.info("No files found to organize.")
        return 0

    logger.info("--- Organization Summary ---")
    for category, count in summary.items():
        logger.info("%s: %d file(s)", category, count)
    
    if args.dry_run:
        logger.info("This was a dry run. No files were actually moved.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
"""Core logic for sorting files into categorized folders."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

# Define categories and their file extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".html", ".css", ".json", ".sh", ".bat"],
}


def _get_category(file_path: Path) -> str:
    """Determine the category folder for a given file based on its extension."""
    ext = file_path.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def _safe_move(source: Path, destination_folder: Path) -> Path:
    """Move a file safely, renaming it if a file with the same name already exists."""
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination = destination_folder / source.name
    
    # If file exists, add a number to the filename
    counter = 1
    while destination.exists():
        stem = source.stem
        ext = source.suffix
        destination = destination_folder / f"{stem}_{counter}{ext}"
        counter += 1
        
    shutil.move(str(source), str(destination))
    return destination


def organize_directory(target_dir: str | Path, dry_run: bool = False) -> dict:
    """
    Organize files in the target directory into categorized subfolders.
    
    Args:
        target_dir: The path to the messy folder.
        dry_run: If True, only prints what would happen without moving files.
        
    Returns:
        A dictionary summarizing the moved files.
    """
    path = Path(target_dir)
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Invalid directory: {target_dir}")

    summary = {}
    
    # Iterate through all files in the directory (ignoring subfolders)
    for item in path.iterdir():
        if item.is_file():
            category = _get_category(item)
            dest_folder = path / category
            
            if dry_run:
                logger.info("[DRY RUN] Would move %s -> %s/", item.name, category)
            else:
                try:
                    new_path = _safe_move(item, dest_folder)
                    logger.info("Moved: %s -> %s", item.name, new_path.relative_to(path))
                except Exception as exc:
                    logger.error("Failed to move %s: %s", item.name, exc)
                    continue

            summary[category] = summary.get(category, 0) + 1

    return summary
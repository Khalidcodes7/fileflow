"""Tests for FileFlow organizer logic."""
from pathlib import Path
import pytest

from fileflow.organizer import organize_directory, _get_category


def test_get_category():
    """Test that file extensions map to the correct categories."""
    assert _get_category(Path("photo.JPG")) == "Images"
    assert _get_category(Path("document.pdf")) == "Documents"
    assert _get_category(Path("script.py")) == "Scripts"
    assert _get_category(Path("unknown.xyz")) == "Other"


def test_organize_directory(tmp_path):
    """Test that files are actually moved into category folders."""
    # 1. Setup a fake messy folder using pytest's tmp_path
    (tmp_path / "image1.jpg").touch()
    (tmp_path / "image2.png").touch()
    (tmp_path / "report.pdf").touch()
    (tmp_path / "random.xyz").touch()

    # 2. Run the organizer
    summary = organize_directory(tmp_path)

    # 3. Check the results
    assert summary == {"Images": 2, "Documents": 1, "Other": 1}
    
    # Check that the folders were created
    assert (tmp_path / "Images").is_dir()
    assert (tmp_path / "Documents").is_dir()
    assert (tmp_path / "Other").is_dir()

    # Check that files were moved
    assert (tmp_path / "Images" / "image1.jpg").exists()
    assert (tmp_path / "Documents" / "report.pdf").exists()
    assert (tmp_path / "Other" / "random.xyz").exists()


def test_organize_handles_duplicates(tmp_path):
    """Test that if two files have the same name, it renames one instead of deleting."""
    # Create two files with the same name in different places, move them to same folder
    (tmp_path / "image.jpg").touch()
    
    # We'll run the organizer once
    organize_directory(tmp_path)
    
    # Now create another file with the same name in the root
    (tmp_path / "image.jpg").touch()
    
    # Run it again
    organize_directory(tmp_path)
    
    # Both files should exist in the Images folder (one renamed to image_1.jpg)
    assert (tmp_path / "Images" / "image.jpg").exists()
    assert (tmp_path / "Images" / "image_1.jpg").exists()
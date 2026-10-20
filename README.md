# FileFlow

> Automatically organize a messy folder into categorized subfolders — with one command.

[![CI](https://github.com/Khalidcodes7/fileflow/actions/workflows/ci.yml/badge.svg)](https://github.com/Khalidcodes7/fileflow/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FileFlow** is a Python automation tool designed to instantly clean up chaotic directories (like your Downloads or Desktop folder). 

It scans a target directory, identifies file types by their extension, creates categorized subfolders (Images, Documents, Scripts, etc.), and safely moves the files into their new homes.

---

## ✨ Features

- 🗂️ **Automatic Sorting** — Sorts files into Images, Documents, Videos, Audio, Archives, and Scripts.
- 🛡️ **Safe Moving** — If a file with the same name already exists in the destination, it automatically renames the new file (e.g., `image_1.jpg`) instead of overwriting it.
- 👁️ **Dry Run Mode** — Preview exactly what will happen without actually moving any files.
- 🖥️ **CLI** — Easy to run from the terminal.
- 🧪 **Tested** — Reliable logic with pytest and GitHub Actions CI.

---

## 📦 Installation

```bash
git clone https://github.com/Khalidcodes7/fileflow.git
cd fileflow
pip install -e ".[dev]"

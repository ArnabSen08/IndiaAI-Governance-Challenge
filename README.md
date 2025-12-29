# Smart Desktop Organizer 🗂️

**"I hate manually organizing my messy Downloads folder, so I built this."**

A Python automation script that intelligently organizes files in any directory by type and date, turning chaos into clean, structured folders.

## The Problem

We've all been there - your Downloads folder has 500+ files, your Desktop is cluttered with screenshots, documents, and random files from months ago. Manually organizing them takes forever and is mind-numbingly boring.

## The Solution

This script automatically:
- 📁 Sorts files by type (Images, Documents, Videos, etc.)
- 📅 Creates date-based subfolders (2024-12, 2024-11, etc.)
- 🏷️ Handles duplicate files intelligently
- 📊 Provides a detailed organization report
- ⚡ Processes hundreds of files in seconds

## Features

- **Smart File Type Detection**: Recognizes 50+ file extensions
- **Date-Based Organization**: Groups files by month/year
- **Duplicate Handling**: Renames duplicates instead of overwriting
- **Dry Run Mode**: Preview changes before applying
- **Detailed Reporting**: Shows what was moved where
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-desktop-organizer.git
cd smart-desktop-organizer

# Install dependencies
pip install -r requirements.txt

# Run with dry-run to preview changes
python organizer.py --path "C:\Users\YourName\Downloads" --dry-run

# Actually organize the files
python organizer.py --path "C:\Users\YourName\Downloads"
```

## Usage Examples

```bash
# Organize Downloads folder
python organizer.py --path "~/Downloads"

# Organize with custom output directory
python organizer.py --path "~/Downloads" --output "~/Organized"

# Preview changes without moving files
python organizer.py --path "~/Downloads" --dry-run

# Organize only files older than 30 days
python organizer.py --path "~/Downloads" --older-than 30
```

## File Organization Structure

```
Organized/
├── Images/
│   ├── 2024-12/
│   │   ├── screenshot1.png
│   │   └── photo.jpg
│   └── 2024-11/
├── Documents/
│   ├── 2024-12/
│   │   ├── report.pdf
│   │   └── notes.docx
├── Videos/
├── Audio/
├── Archives/
└── Others/
```

## How Kiro Accelerated Development

This project was built with significant assistance from Kiro AI:

- **Rapid Prototyping**: Kiro helped structure the project and write the core logic in minutes
- **Error Handling**: Suggested robust error handling patterns for file operations
- **Cross-Platform Compatibility**: Ensured the script works across different operating systems
- **Code Organization**: Helped structure the code into clean, maintainable modules
- **Testing Strategy**: Suggested comprehensive test cases and edge case handling

## Requirements

- Python 3.7+
- Standard library only (no external dependencies for core functionality)

## License

MIT License - Feel free to use and modify!

## Contributing

Found a bug or want to add a feature? Pull requests welcome!
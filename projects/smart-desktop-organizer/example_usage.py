#!/usr/bin/env python3
"""
Example usage and demo script for Smart Desktop Organizer
"""

import os
import tempfile
from pathlib import Path
from organizer import FileOrganizer
import shutil

def create_demo_files():
    """Create a temporary directory with sample files for demonstration."""
    demo_dir = Path(tempfile.mkdtemp(prefix="desktop_organizer_demo_"))
    
    # Sample files to create
    sample_files = [
        "vacation_photo.jpg",
        "meeting_notes.pdf",
        "presentation.pptx",
        "song.mp3",
        "video_tutorial.mp4",
        "project_code.py",
        "archive_backup.zip",
        "screenshot.png",
        "document.docx",
        "spreadsheet.xlsx",
        "random_file.txt",
        "installer.exe"
    ]
    
    print(f"📁 Creating demo files in: {demo_dir}")
    
    # Create sample files
    for filename in sample_files:
        file_path = demo_dir / filename
        file_path.write_text(f"This is a sample {filename} file for demonstration.")
        print(f"   Created: {filename}")
    
    return demo_dir

def run_demo():
    """Run a complete demonstration of the organizer."""
    print("🚀 Smart Desktop Organizer Demo")
    print("=" * 40)
    
    # Create demo files
    demo_dir = create_demo_files()
    
    try:
        print(f"\n📋 Files before organization:")
        for file in demo_dir.iterdir():
            if file.is_file():
                print(f"   {file.name}")
        
        # Run dry-run first
        print(f"\n🔍 Running dry-run preview...")
        organizer = FileOrganizer(
            source_path=demo_dir,
            output_path=demo_dir / "Organized_Demo",
            dry_run=True
        )
        organizer.organize_files()
        
        # Ask user if they want to proceed
        response = input("\n❓ Proceed with actual organization? (y/n): ")
        if response.lower() == 'y':
            print(f"\n📁 Organizing files...")
            organizer = FileOrganizer(
                source_path=demo_dir,
                output_path=demo_dir / "Organized_Demo",
                dry_run=False
            )
            organizer.organize_files()
            
            print(f"\n📂 Final directory structure:")
            organized_dir = demo_dir / "Organized_Demo"
            if organized_dir.exists():
                for root, dirs, files in os.walk(organized_dir):
                    level = root.replace(str(organized_dir), '').count(os.sep)
                    indent = ' ' * 2 * level
                    print(f"{indent}{os.path.basename(root)}/")
                    subindent = ' ' * 2 * (level + 1)
                    for file in files:
                        print(f"{subindent}{file}")
        
    finally:
        # Cleanup
        print(f"\n🧹 Cleaning up demo directory...")
        shutil.rmtree(demo_dir)
        print("✅ Demo complete!")

if __name__ == "__main__":
    run_demo()
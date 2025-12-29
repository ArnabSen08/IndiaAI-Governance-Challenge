#!/usr/bin/env python3
"""
Smart Desktop Organizer
A Python script that automatically organizes files by type and date.
"""

import os
import shutil
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import json

class FileOrganizer:
    """Main class for organizing files by type and date."""
    
    # File type mappings
    FILE_TYPES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico', '.raw'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.java', '.php', '.rb', '.go', '.rs'],
        'Executables': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg', '.app']
    }
    
    def __init__(self, source_path, output_path=None, dry_run=False, older_than_days=None):
        self.source_path = Path(source_path)
        self.output_path = Path(output_path) if output_path else self.source_path / "Organized"
        self.dry_run = dry_run
        self.older_than_days = older_than_days
        self.stats = defaultdict(int)
        self.moved_files = []
        
    def get_file_type(self, file_path):
        """Determine the file type category based on extension."""
        extension = file_path.suffix.lower()
        
        for category, extensions in self.FILE_TYPES.items():
            if extension in extensions:
                return category
        return 'Others'
    
    def get_file_date_folder(self, file_path):
        """Get the date-based folder name for a file."""
        try:
            # Use modification time
            timestamp = file_path.stat().st_mtime
            date = datetime.fromtimestamp(timestamp)
            return f"{date.year}-{date.month:02d}"
        except:
            # Fallback to current date if file stat fails
            return datetime.now().strftime("%Y-%m")
    
    def should_process_file(self, file_path):
        """Check if file should be processed based on age criteria."""
        if not self.older_than_days:
            return True
            
        try:
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            cutoff_time = datetime.now() - timedelta(days=self.older_than_days)
            return file_time < cutoff_time
        except:
            return True
    
    def get_unique_filename(self, target_path):
        """Generate a unique filename if target already exists."""
        if not target_path.exists():
            return target_path
            
        base = target_path.stem
        extension = target_path.suffix
        parent = target_path.parent
        counter = 1
        
        while True:
            new_name = f"{base}_{counter}{extension}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def organize_files(self):
        """Main method to organize files."""
        print(f"🔍 Scanning: {self.source_path}")
        print(f"📁 Output: {self.output_path}")
        
        if self.dry_run:
            print("🔍 DRY RUN MODE - No files will be moved")
        
        # Create output directory if it doesn't exist
        if not self.dry_run:
            self.output_path.mkdir(exist_ok=True)
        
        # Process all files in source directory
        for file_path in self.source_path.iterdir():
            if file_path.is_file() and self.should_process_file(file_path):
                self.process_file(file_path)
        
        self.print_summary()
    
    def process_file(self, file_path):
        """Process a single file."""
        try:
            # Skip hidden files and system files
            if file_path.name.startswith('.') or file_path.name.startswith('~'):
                return
            
            file_type = self.get_file_type(file_path)
            date_folder = self.get_file_date_folder(file_path)
            
            # Create target directory structure
            target_dir = self.output_path / file_type / date_folder
            target_path = target_dir / file_path.name
            
            # Handle duplicates
            target_path = self.get_unique_filename(target_path)
            
            if not self.dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(target_path))
            
            # Track statistics
            self.stats[file_type] += 1
            self.moved_files.append({
                'original': str(file_path),
                'new': str(target_path),
                'type': file_type,
                'date': date_folder
            })
            
            print(f"📄 {file_path.name} → {file_type}/{date_folder}/")
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
    
    def print_summary(self):
        """Print organization summary."""
        print("\n" + "="*50)
        print("📊 ORGANIZATION SUMMARY")
        print("="*50)
        
        total_files = sum(self.stats.values())
        print(f"Total files processed: {total_files}")
        
        if self.dry_run:
            print("(This was a dry run - no files were actually moved)")
        
        print("\nFiles by category:")
        for category, count in sorted(self.stats.items()):
            print(f"  {category}: {count} files")
        
        # Save detailed report
        if not self.dry_run and self.moved_files:
            report_path = self.output_path / "organization_report.json"
            with open(report_path, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'total_files': total_files,
                    'stats': dict(self.stats),
                    'moved_files': self.moved_files
                }, f, indent=2)
            print(f"\n📋 Detailed report saved: {report_path}")

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Smart Desktop Organizer")
    parser.add_argument('--path', required=True, help='Path to directory to organize')
    parser.add_argument('--output', help='Output directory (default: PATH/Organized)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without moving files')
    parser.add_argument('--older-than', type=int, help='Only process files older than N days')
    
    args = parser.parse_args()
    
    # Validate source path
    source_path = Path(args.path)
    if not source_path.exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        return
    
    if not source_path.is_dir():
        print(f"❌ Error: Path '{args.path}' is not a directory")
        return
    
    # Create organizer and run
    organizer = FileOrganizer(
        source_path=args.path,
        output_path=args.output,
        dry_run=args.dry_run,
        older_than_days=args.older_than
    )
    
    print("🚀 Starting Smart Desktop Organizer...")
    organizer.organize_files()
    print("✅ Organization complete!")

if __name__ == "__main__":
    main()
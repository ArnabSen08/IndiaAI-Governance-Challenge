#!/usr/bin/env python3
"""
Test script for Smart Desktop Organizer
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from organizer import FileOrganizer

class TestFileOrganizer(unittest.TestCase):
    """Test cases for FileOrganizer class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.output_dir = self.test_dir / "organized"
        
        # Create test files
        self.test_files = {
            'image.jpg': 'Images',
            'document.pdf': 'Documents', 
            'video.mp4': 'Videos',
            'song.mp3': 'Audio',
            'archive.zip': 'Archives',
            'script.py': 'Code',
            'unknown.xyz': 'Others'
        }
        
        for filename in self.test_files.keys():
            (self.test_dir / filename).write_text("test content")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_file_type_detection(self):
        """Test file type categorization."""
        organizer = FileOrganizer(self.test_dir, self.output_dir, dry_run=True)
        
        for filename, expected_type in self.test_files.items():
            file_path = self.test_dir / filename
            detected_type = organizer.get_file_type(file_path)
            self.assertEqual(detected_type, expected_type, 
                           f"File {filename} should be categorized as {expected_type}")
    
    def test_dry_run_mode(self):
        """Test that dry run doesn't move files."""
        organizer = FileOrganizer(self.test_dir, self.output_dir, dry_run=True)
        organizer.organize_files()
        
        # Files should still be in original location
        for filename in self.test_files.keys():
            self.assertTrue((self.test_dir / filename).exists(), 
                          f"File {filename} should still exist in dry run")
        
        # Output directory should not be created in dry run
        self.assertFalse(self.output_dir.exists(), 
                        "Output directory should not exist after dry run")
    
    def test_actual_organization(self):
        """Test actual file organization."""
        organizer = FileOrganizer(self.test_dir, self.output_dir, dry_run=False)
        organizer.organize_files()
        
        # Check that files were moved to correct categories
        for filename, expected_type in self.test_files.items():
            # Find the file in the organized structure
            type_dir = self.output_dir / expected_type
            self.assertTrue(type_dir.exists(), 
                          f"Category directory {expected_type} should exist")
            
            # File should be in some date subfolder
            found = False
            for date_dir in type_dir.iterdir():
                if date_dir.is_dir() and (date_dir / filename).exists():
                    found = True
                    break
            
            self.assertTrue(found, f"File {filename} should be organized in {expected_type}")
    
    def test_duplicate_handling(self):
        """Test handling of duplicate filenames."""
        # Create duplicate files
        (self.test_dir / "duplicate.txt").write_text("original")
        
        # Simulate a duplicate by pre-creating the target
        from datetime import datetime
        date_folder = datetime.now().strftime("%Y-%m")
        target_dir = self.output_dir / "Documents" / date_folder
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "duplicate.txt").write_text("existing")
        
        # Now organize - should create duplicate_1.txt
        organizer = FileOrganizer(self.test_dir, self.output_dir, dry_run=False)
        organizer.organize_files()
        
        # Both files should exist
        self.assertTrue((target_dir / "duplicate.txt").exists())
        self.assertTrue((target_dir / "duplicate_1.txt").exists())

if __name__ == '__main__':
    unittest.main()
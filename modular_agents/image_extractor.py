# modular_agents/image_extractor.py
import os
import sys
import zipfile
import tempfile
import shutil
import subprocess
from typing import List

class ImageExtractor:
    """
    Extracts images from comic book archives (.cbr, .cbz).
    """
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def extract_images_to_temp(self, comic_path: str) -> List[str]:
        """
        Extracts images from a comic book file to the temporary directory for analysis only.
        """
        if not os.path.exists(comic_path):
            raise FileNotFoundError(f"Comic file not found: {comic_path}")

        image_paths = []
        
        # Method 1: Try as ZIP/CBZ
        try:
            with zipfile.ZipFile(comic_path, 'r') as archive:
                for file_info in archive.infolist():
                    if file_info.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        archive.extract(file_info, self.temp_dir)
                        image_paths.append(os.path.join(self.temp_dir, file_info.filename))
            if image_paths:
                image_paths.sort()
                return image_paths
        except zipfile.BadZipFile:
            pass  # Not a zip file, try next method

        # Method 2: Try system unar command
        try:
            subprocess.run(['unar', '-o', self.temp_dir, comic_path], capture_output=True, text=True, check=True)
            for root, _, files in os.walk(self.temp_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        image_paths.append(os.path.join(root, file))
            if image_paths:
                image_paths.sort()
                return image_paths
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass # unar not found or failed, try next method

        # If all methods fail, raise an exception
        raise Exception("All extraction methods failed.")

    def extract_images(self, comic_path: str, output_dir: str) -> List[str]:
        """
        Extracts images from a comic book file to a specified output directory.
        """
        if not os.path.exists(comic_path):
            raise FileNotFoundError(f"Comic file not found: {comic_path}")

        image_paths = []
        
        # Method 1: Try as ZIP/CBZ
        try:
            with zipfile.ZipFile(comic_path, 'r') as archive:
                for file_info in archive.infolist():
                    if file_info.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        archive.extract(file_info, output_dir)
                        image_paths.append(os.path.join(output_dir, file_info.filename))
            if image_paths:
                image_paths.sort()
                return image_paths
        except zipfile.BadZipFile:
            pass  # Not a zip file, try next method

        # Method 2: Try system unar command
        try:
            subprocess.run(['unar', '-o', output_dir, comic_path], capture_output=True, text=True, check=True)
            for root, _, files in os.walk(output_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        image_paths.append(os.path.join(root, file))
            if image_paths:
                image_paths.sort()
                return image_paths
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass # unar not found or failed, try next method

        # If all methods fail, raise an exception
        raise Exception("All extraction methods failed.")

    def cleanup(self):
        """
        Cleans up the temporary directory.
        """
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python image_extractor.py <path_to_comic_file> <output_directory>")
        sys.exit(1)

    comic_file_path = sys.argv[1]
    output_dir_path = sys.argv[2]
    os.makedirs(output_dir_path, exist_ok=True)
    
    extractor = ImageExtractor()
    try:
        extracted_image_paths = extractor.extract_images(comic_file_path, output_dir_path)
        for path in extracted_image_paths:
            print(path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        extractor.cleanup()
import os
import tempfile


class TempResxFiles:
    """Helper class to manage temporary resx files for testing."""

    def __init__(self):
        self.temp_files = []

    def create_temp_resx(self, content):
        """
        Create a temporary resx file with given content for testing.

        Args:
            content: XML content for the resx file

        Returns:
            Path to the temporary file
        """
        fd, path = tempfile.mkstemp(suffix='.resx')
        os.write(fd, content.encode('utf-8'))
        os.close(fd)
        self.temp_files.append(path)
        return path

    def cleanup(self):
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)

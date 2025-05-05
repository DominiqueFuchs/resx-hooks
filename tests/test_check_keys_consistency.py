import unittest

from resx_hooks.resx_parser import find_missing_keys, parse_resx_file
from tests.helpers import TempResxFiles


class TestCheckKeysConsistency(unittest.TestCase):
    def setUp(self):
        self.temp_files = TempResxFiles()

    def tearDown(self):
        self.temp_files.cleanup()

    def test_parser_finds_missing_keys(self):
        complete_resx_content = """<?xml version="1.0" encoding="utf-8"?>
<root>
  <data name="Welcome" xml:space="preserve">
    <value>Welcome to our application</value>
  </data>
  <data name="Goodbye" xml:space="preserve">
    <value>Goodbye</value>
  </data>
  <data name="Error" xml:space="preserve">
    <value>An error occurred</value>
  </data>
</root>"""

        missing_key_resx_content = """<?xml version="1.0" encoding="utf-8"?>
<root>
  <data name="Welcome" xml:space="preserve">
    <value>Welcome to our application</value>
  </data>
  <data name="Error" xml:space="preserve">
    <value>An error occurred</value>
  </data>
</root>"""

        complete_resx = self.temp_files.create_temp_resx(
            complete_resx_content)
        missing_goodbye_resx = self.temp_files.create_temp_resx(
            missing_key_resx_content)

        parsed_data = {
            complete_resx: parse_resx_file(complete_resx),
            missing_goodbye_resx: parse_resx_file(missing_goodbye_resx)
        }

        missing_keys = find_missing_keys(parsed_data)

        self.assertIn(missing_goodbye_resx, missing_keys)
        self.assertEqual(
            set(['Goodbye']),
            missing_keys[missing_goodbye_resx]
        )


if __name__ == '__main__':
    unittest.main()

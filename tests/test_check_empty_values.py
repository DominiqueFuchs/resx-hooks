import unittest

from resx_hooks.check_empty_values import find_empty_values
from tests.helpers import TempResxFiles


class TestCheckEmptyValues(unittest.TestCase):
    def setUp(self):
        self.temp_files = TempResxFiles()

    def tearDown(self):
        self.temp_files.cleanup()

    def test_find_empty_values(self):
        with_empty_values = """<?xml version="1.0" encoding="utf-8"?>
<root>
  <data name="Welcome" xml:space="preserve">
    <value>Welcome to our application</value>
  </data>
  <data name="Goodbye" xml:space="preserve">
    <value></value>
  </data>
  <data name="Error" xml:space="preserve">
    <value>   </value>
  </data>
  <data name="Success" xml:space="preserve">
    <value>Operation was successful</value>
  </data>
</root>"""

        no_empty_values = """<?xml version="1.0" encoding="utf-8"?>
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
  <data name="Success" xml:space="preserve">
    <value>Operation was successful</value>
  </data>
</root>"""

        empty_resx_path = self.temp_files.create_temp_resx(with_empty_values)
        full_resx_path = self.temp_files.create_temp_resx(no_empty_values)

        empty_keys = find_empty_values(empty_resx_path)
        self.assertEqual(set(empty_keys), {"Goodbye", "Error"})

        empty_keys = find_empty_values(full_resx_path)
        self.assertEqual(empty_keys, [])


if __name__ == '__main__':
    unittest.main()

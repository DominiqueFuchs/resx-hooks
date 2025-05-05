import unittest

from resx_hooks.check_placeholders import \
    check_placeholder_consistency, find_placeholders
from tests.helpers import TempResxFiles


class TestCheckPlaceholders(unittest.TestCase):
    def setUp(self):
        self.temp_files = TempResxFiles()

    def tearDown(self):
        self.temp_files.cleanup()

    def test_find_placeholders(self):
        placeholders = find_placeholders("Hello {0}, your score is {1:N2}")
        self.assertEqual(placeholders, {"0", "1"})

        placeholders = find_placeholders("Hello %s, your score is %d")
        self.assertEqual(placeholders, {"s", "d"})

        placeholders = find_placeholders("Hello {0}, your score is %d")
        self.assertEqual(placeholders, {"0", "d"})

        placeholders = find_placeholders("Hello World")
        self.assertEqual(placeholders, set())

    def test_placeholder_consistency_check(self):
        en_resx_content = """<?xml version="1.0" encoding="utf-8"?>
<root>
  <data name="Welcome" xml:space="preserve">
    <value>Welcome {0}, to our application!</value>
  </data>
  <data name="Goodbye" xml:space="preserve">
    <value>Goodbye {0}, see you again!</value>
  </data>
  <data name="Error" xml:space="preserve">
    <value>Error: {0} occurred at {1}</value>
  </data>
</root>"""

        fr_resx_content = """<?xml version="1.0" encoding="utf-8"?>
<root>
  <data name="Welcome" xml:space="preserve">
    <value>Bienvenue {0}, à notre application!</value>
  </data>
  <data name="Goodbye" xml:space="preserve">
    <value>Au revoir {0}, à bientôt!</value>
  </data>
  <data name="Error" xml:space="preserve">
    <value>Erreur: {1} s'est produite</value>
  </data>
</root>"""

        en_path = self.temp_files.create_temp_resx(en_resx_content)
        fr_path = self.temp_files.create_temp_resx(fr_resx_content)

        inconsistencies = check_placeholder_consistency([en_path, fr_path])
        self.assertTrue(len(inconsistencies) > 0)
        self.assertIn(fr_path, inconsistencies)
        self.assertIn('Error', inconsistencies[fr_path])

        expected_placeholders = {"0", "1"}
        found_placeholders = {"1"}
        self.assertEqual(
            inconsistencies[fr_path]['Error']['expected'],
            list(expected_placeholders))
        self.assertEqual(
            set(inconsistencies[fr_path]['Error']['found']),
            found_placeholders)

    def test_no_inconsistencies(self):
        resx_content = """<?xml version="1.0" encoding="utf-8"?>
<root>
  <data name="Welcome" xml:space="preserve">
    <value>Welcome {0}, to our application!</value>
  </data>
  <data name="Goodbye" xml:space="preserve">
    <value>Goodbye {0}, see you again!</value>
  </data>
</root>"""

        path1 = self.temp_files.create_temp_resx(resx_content)
        path2 = self.temp_files.create_temp_resx(resx_content)

        inconsistencies = check_placeholder_consistency([path1, path2])
        self.assertEqual(len(inconsistencies), 0)


if __name__ == '__main__':
    unittest.main()

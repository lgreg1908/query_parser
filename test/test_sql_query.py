import unittest
import sqlparse
from pathlib import Path
import sys

path_to_append: Path = Path.cwd().resolve().parent
sys.path.append(str(path_to_append))

from sql_query import SqlQuery
from test_cases.test_case import TestCase, load_test_cases
from typing import List


class TestSqlQuery(unittest.TestCase):
    _directory_test_cases = "test_cases"

    def setUp(self):
        self.test_cases: List[TestCase] = load_test_cases(self._directory_test_cases)
        self.sql_query = SqlQuery()

    def test_set_query_empty(self):
        with self.assertRaises(ValueError):
            self.sql_query.set_query("")

    def test_clear_cache(self):
        self.sql_query.set_query("SELECT * FROM table")
        tree_before_clearing = self.sql_query.create_tree()
        self.sql_query.clear_cache()
        tree_after_clearing = self.sql_query.create_tree()
        self.assertNotEqual(tree_before_clearing, tree_after_clearing)

    # def test_tree_to_dict(self):
    #     for case in self.test_cases:
    #         with self.subTest(name=case.name, query=case.query):
    #             self.sql_query.set_query(case.query)
    #             tree_dict = self.sql_query.tree_to_dict()
    #             self.assertEqual(tree_dict, case.expected)

if __name__ == '__main__':
    unittest.main()

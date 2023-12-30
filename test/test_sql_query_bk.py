import unittest
import sqlparse
from pathlib import Path
import sys

path_to_append: Path = Path.cwd().resolve().parent
sys.path.append(str(path_to_append))

from sql_query import SqlQuery
from test_cases.test_case import TestCase, load_test_cases


class TestSqlQuery(unittest.TestCase):
    _directory_test_cases = "test_cases"

    def setUp(self):
        self.simple_query = "SELECT * FROM users"
        self.complex_query = "SELECT name, age FROM People WHERE age > 30"
        self.test_cases = load_test_cases(self._directory_test_cases)
        self.sql_query = SqlQuery()

    def test_set_query_with_normalization(self):
        self.sql_query.set_query(self.simple_query)
        self.assertEqual(self.sql_query.raw_query, self.simple_query)
        self.assertIsNotNone(self.sql_query.normalized_query)
        self.assertIsNone(self.sql_query.tree)

    def test_set_query_without_normalization(self):
        self.sql_query.set_query(self.complex_query, normalize=False)
        self.assertEqual(self.sql_query.raw_query, self.complex_query)
        self.assertIsNotNone(self.sql_query.tree)
        self.assertIsNone(self.sql_query.normalized_query)


    def test_create_tree(self):
        self.sql_query.set_query(self.simple_query)
        tree = self.sql_query.create_tree()
        self.assertIsNotNone(tree)
        # Check the structure of the tree
        expected_structure = sqlparse.parse(self.simple_query)[0].tokens
        self.assertEqual(tree, expected_structure)

    def test_clear_cache(self):
        self.sql_query.set_query(self.simple_query)
        tree_before_clearing = self.sql_query.create_tree()
        self.sql_query.clear_cache()
        tree_after_clearing = self.sql_query.create_tree()
        self.assertNotEqual(tree_before_clearing, tree_after_clearing)

    def test_flatten_tree(self):
        self.sql_query.set_query(self.complex_query)
        flat_tree = self.sql_query.flatten_tree()
        # Expected flattened tree
        expected_flat_tree = [token.normalized for token in sqlparse.parse(self.complex_query)[0].flatten()]
        self.assertEqual(flat_tree, expected_flat_tree)

    def test_tree_to_dict(self):
        for case in self.test_cases:
            with self.subTest(query=case["query"]):
                self.sql_query.set_query(case["query"])
                tree_dict = self.sql_query.tree_to_dict()
                self.assertEqual(tree_dict, case["expected"])


if __name__ == '__main__':
    unittest.main()

import unittest
import sqlparse
from token_processor import TokenProcessor
from test_cases import test_cases

class TestTokenProcessor(unittest.TestCase):

    def setUp(self):
        self.simple_query = "SELECT * FROM users"
        self.complex_query = "SELECT name, age FROM People WHERE age > 30"
        self.simple_tokens = sqlparse.parse(self.simple_query)[0].tokens
        self.complex_tokens = sqlparse.parse(self.complex_query)[0].tokens
        self.processor = TokenProcessor()

    def test_process_simple_query(self):
        result = self.processor.process(self.simple_tokens)
        # Expected result for simple query tokens
        expected = [
            {"type": "DML", "value": "SELECT", "is_group": False},
            {"type": "Wildcard", "value": "*", "is_group": False},
            {"type": "Keyword", "value": "FROM", "is_group": False},
            {"type": "Identifier", "value": "users", "is_group": False}
        ]
        self.assertEqual(result, expected)

    def test_process_complex_query(self):
        result = self.processor.process(self.complex_tokens)
        # Expected result for complex query tokens
        expected = [
            {"type": "DML", "value": "SELECT", "is_group": False},
            {"type": "IdentifierList", "value": "name, age", "is_group": True, "children": [
                {"type": "Identifier", "value": "name", "is_group": False},
                {"type": "Identifier", "value": "age", "is_group": False}
            ]},
            {"type": "Keyword", "value": "FROM", "is_group": False},
            {"type": "Identifier", "value": "People", "is_group": False},
            {"type": "Where", "value": "WHERE age > 30", "is_group": True, "children": [
                {"type": "Comparison", "value": "age > 30", "is_group": False}
            ]}
        ]
        self.assertEqual(result, expected)

    def test_process_empty_tokens(self):
        result = self.processor.process([])
        self.assertEqual(result, [])

    def test_process_invalid_tokens(self):
        with self.assertRaises(TypeError):
            self.processor.process(None)

    def test_process_nested_tokens(self):
        nested_query = "SELECT * FROM (SELECT id FROM users)"
        nested_tokens = sqlparse.parse(nested_query)[0].tokens
        result = self.processor.process(nested_tokens)

        expected = [
            {"type": "DML", "value": "SELECT", "is_group": False},
            {"type": "Wildcard", "value": "*", "is_group": False},
            {"type": "Keyword", "value": "FROM", "is_group": False},
            {"type": "Subselect", "value": "(SELECT id FROM users)", "is_group": True, "children": [
                {"type": "DML", "value": "SELECT", "is_group": False},
                {"type": "Identifier", "value": "id", "is_group": False},
                {"type": "Keyword", "value": "FROM", "is_group": False},
                {"type": "Identifier", "value": "users", "is_group": False}
            ]}
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

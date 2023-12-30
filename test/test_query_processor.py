import unittest
import sqlparse
from query_processor import QueryProcessor
from test_cases import test_cases

class TestQueryProcessor(unittest.TestCase):

    def setUp(self):
        self.simple_query = "SELECT * FROM users"
        self.complex_query = "select name, age from People where age > 30"

    def test_init(self):
        processor_simple = QueryProcessor(self.simple_query)
        processor_complex = QueryProcessor(self.complex_query)

        self.assertEqual(processor_simple.query, self.simple_query)
        self.assertEqual(processor_complex.query, self.complex_query)

    def test_normalize_query(self):
        processor = QueryProcessor(self.complex_query)
        normalized_query = processor.normalize_query()

        # The expected result should be a properly formatted version of the complex query
        expected = "SELECT name, age\nFROM People\nWHERE age > 30"
        self.assertEqual(normalized_query, expected)

    def test_normalize_query_failure(self):
        # Testing normalization with a bad query
        bad_query = "SELEC * FORM"
        processor = QueryProcessor(bad_query)

        with self.assertRaises(ValueError) as context:
            processor.normalize_query()
        self.assertTrue("Error while normalizing the query" in str(context.exception))

    def test_parse_query(self):
        processor = QueryProcessor(self.simple_query)
        parsed = processor.parse_query()

        # The expected result should be a token list of the simple query
        expected = sqlparse.parse(self.simple_query)[0].tokens
        self.assertEqual(parsed, expected)

    def test_parse_query_failure(self):
        # Testing parsing with a bad query
        bad_query = "SELECT FROM without_table"
        processor = QueryProcessor(bad_query)

        with self.assertRaises(ValueError) as context:
            processor.parse_query()
        self.assertTrue("Error while parsing the query" in str(context.exception))

if __name__ == '__main__':
    unittest.main()

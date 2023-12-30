import sqlparse
from sqlparse.sql import Token
from typing import List


class QueryProcessor:
    def __init__(self, query: str):
        """
        Initialize the QueryProcessor with a SQL query.

        Parameters:
        query (str): The SQL query to be processed.

        Raises:
        ValueError: If the input query is not a valid string.
        """
        if not isinstance(query, str):
            raise ValueError("Query must be a string")
        self.query = query

    def normalize_query(self) -> str:
        """
        Normalize the SQL query.

        Returns:
        str: The normalized SQL query.

        Raises:
        ValueError: If there's an error during normalization.
        """
        try:
            return sqlparse.format(self.query, reindent=True, keyword_case='upper', strip_whitespace=True)
        except Exception as e:
            raise ValueError(f"Error while normalizing the query: {e}")

    def parse_query(self) -> List[Token]:
        """
        Parse the SQL query.

        Returns:
        List[Token]: A list of tokens obtained from parsing the query.

        Raises:
        ValueError: If there's an error during parsing or if the query is empty.
        """
        try:
            parsed = sqlparse.parse(self.query)
            if not parsed:
                raise ValueError("Failed to parse the query")
            return parsed[0].tokens
        except Exception as e:
            raise ValueError(f"Error while parsing the query: {e}")

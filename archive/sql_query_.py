import sqlparse
from sqlparse.sql import Token, TokenList

from typing import List, Dict, Optional
from functools import lru_cache



class QueryProcessor:
    def __init__(self, query: str):
        self.query = query

    def normalize_query(self) -> str:
        try:
            return sqlparse.format(self.query, reindent=True, keyword_case='upper', strip_whitespace=True)
        except Exception as e:
            raise ValueError(f"Error while normalizing the query: {e}")

    def parse_query(self) -> List[Token]:
        try:
            parsed = sqlparse.parse(self.query)
            if not parsed:
                raise ValueError("Failed to parse the query")
            return parsed[0].tokens
        except Exception as e:
            raise ValueError(f"Error while parsing the query: {e}")

class TokenProcessor:
    def process(self, tokens: List[Token]) -> List[Dict]:
        result = []
        for token in tokens:
            if isinstance(token, TokenList):
                children = self.process(token.tokens)
                result.append({
                    "type": type(token).__name__,
                    "value": token.normalized,
                    "is_group": True,  # Add the is_group tag.
                    "children": children
                })
            else:
                result.append({
                    "type": token.ttype,
                    "value": token.normalized,
                    "is_group": False  # Add the is_group tag.
                })
        return result

class SqlQuery:
    def __init__(self):
        self.raw_query = None
        self.normalized_query = None
        self.tree: Optional[List[Token]] = None

    def set_query(self, query: str, normalize: bool = True):
        self.clear_cache()  # Clear the cache before processing a new query.
        if not query:
            raise ValueError("Query cannot be empty")
        self.raw_query = query
        if normalize:
            processor = QueryProcessor(query)
            self.normalized_query = processor.normalize_query()
            self.tree = None
        else:
            processor = QueryProcessor(query)
            self.tree = processor.parse_query()
            self.normalized_query = None

    @lru_cache(maxsize=None)
    def create_tree(self) -> List[Token]:
        if not self.raw_query:
            raise ValueError("No query set")

        if self.tree is None:
            processor = QueryProcessor(self.raw_query)
            self.tree = processor.parse_query()

        return self.tree

    def clear_cache(self):
        """
        Clear the LRU cache used for create_tree.
        """
        self.create_tree.cache_clear()

    def flatten_tree(self, tokens: Optional[List[Token]] = None) -> List[str]:
        if tokens is None:
            tokens = self.create_tree()

        flat_tokens = []
        for token in tokens:
            if isinstance(token, TokenList):
                flat_tokens.extend(self.flatten_tree(token.tokens))
            else:
                flat_tokens.append(token.normalized)
        return flat_tokens

    def tree_to_dict(self, tokens=None) -> Dict:
        if tokens is None:
            tokens = self.create_tree()

        token_processor = TokenProcessor()
        return {"type": "ROOT", "children": token_processor.process(tokens)}

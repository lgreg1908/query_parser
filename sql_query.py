from typing import List, Dict, Optional
from query_processor import QueryProcessor
from token_processor import TokenProcessor
from sqlparse.sql import Token, TokenList


class SqlQuery:
    def __init__(self):
        """
        Initialize the SqlQuery class.
        """
        self.raw_query = None
        self.normalized_query = None
        self.tree: Optional[List[Token]] = None

    def set_query(self, query: str, normalize: bool = True):
        """
        Set the SQL query for processing.

        Parameters:
        query (str): The SQL query to be set.
        normalize (bool): If True, normalize the query; otherwise, parse it directly.

        Raises:
        ValueError: If the query is empty.
        """
        if not query:
            raise ValueError("Query cannot be empty")
        
        self.raw_query = query
        processor = QueryProcessor(query)

        if normalize:
            self.normalized_query = processor.normalize_query()
            self.tree = None
        else:
            self.tree = processor.parse_query()
            self.normalized_query = None

    def create_tree(self) -> List[Token]:
        """
        Create a tree structure from the SQL query.

        Returns:
        List[Token]: A list of tokens representing the tree structure of the query.

        Raises:
        ValueError: If no query is set.
        """
        if not self.raw_query:
            raise ValueError("No query set")
        if not self.normalized_query:
            processor = QueryProcessor(self.raw_query)
            self.normalized_query = processor.normalize_query()
        if self.tree is None:
            processor = QueryProcessor(self.normalized_query)
            self.tree = processor.parse_query()
        return self.tree

    def flatten_tree(self) -> List[str]:
        """
        Flatten the tree structure into a list of token strings.

        Parameters:
        tokens (Optional[List[Token]]): The list of tokens to flatten. If None, uses the current tree.

        Returns:
        List[str]: A list of token strings.
        """
        flat_tokens = []
        for token in self.tree:
            if isinstance(token, TokenList):
                flat_tokens.extend(self.flatten_tree(token.tokens))
            else:
                flat_tokens.append(token.normalized)
        return flat_tokens

    def tree_to_dict(self) -> Dict:
        """
        Convert the token tree into a dictionary format.

        Parameters:
        tokens (Optional[List[Token]]): The list of tokens to convert. If None, uses the current tree.

        Returns:
        Dict: A dictionary representation of the token tree.
        """
        token_processor = TokenProcessor()
        return {"type": "ROOT", "children": token_processor.process(self.tree)}

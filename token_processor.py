from typing import List, Dict
from sqlparse.sql import Token, TokenList


class TokenProcessor:
    def process(self, tokens: List[Token]) -> List[Dict]:
        """
        Process a list of tokens into a structured format.

        Parameters:
        tokens (List[Token]): The list of tokens to process.

        Returns:
        List[Dict]: A list of dictionaries representing the processed tokens.

        Raises:
        ValueError: If the tokens list is empty or not a list.
        """
        if not isinstance(tokens, list) or not tokens:
            raise ValueError("Tokens must be a non-empty list")

        result = []
        for token in tokens:
            if isinstance(token, TokenList):
                children = self.process(token.tokens)
                result.append({
                    "type": type(token).__name__,
                    "value": token.normalized,
                    "is_group": True,
                    "children": children
                })
            else:
                result.append({
                    "type": token.ttype,
                    "value": token.normalized,
                    "is_group": False
                })
        return result

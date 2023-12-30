import sqlparse
import logging
from typing import List, Optional, Iterator

class SQLToken:
    """
    Represents a basic SQL token.

    Attributes
    ----------
    token_type : sqlparse.tokens.TokenType
        The type of the SQL token.
    value : str
        The string value of the token.
    """
    def __init__(self, token_type: sqlparse.tokens._TokenType, value: str):
        self.token_type = token_type
        self.value = value

    def __str__(self) -> str:
        """Return the string representation of the SQL token."""
        return f"{self.token_type}: {self.value}"

    def __repr__(self) -> str:
        """Return a detailed string representation of the SQL token for debugging."""
        return f"<SQLToken type={self.token_type}, value={self.value}>"

class SQLNode:
    """
    Represents a node in the SQL query tree.

    Attributes
    ----------
    token : Optional[SQLToken]
        The SQL token associated with this node. Can be None for structural nodes.
    children : List[SQLNode])
        The list of child nodes.
    """
    def __init__(self, token: Optional[SQLToken] = None):
        self.token = token
        self.children: List[SQLNode] = []

    def add_child(self, child: 'SQLNode'):
        """Add a child node to this node."""
        self.children.append(child)

    def __str__(self, indent: str = "") -> str:
        """Return the string representation of the SQL node and its children."""
        node_str = indent + str(self.token) + "\n" if self.token else ""
        for child in self.children:
            node_str += child.__str__(indent + "  ")
        return node_str

    def find_tokens(self, token_type: sqlparse.tokens._TokenType) -> List[SQLToken]:
        """
        Find all tokens of a specific type in the subtree rooted at this node.

        Arguments
        ---------
        token_type : sqlparse.tokens.TokenType
            The token type to search for.

        Returns
        -------
        List[SQLToken]
            A list of SQLToken instances matching the specified type.
        """
        found_tokens = []
        if self.token and self.token.token_type == token_type:
            found_tokens.append(self.token)
        for child in self.children:
            found_tokens.extend(child.find_tokens(token_type))
        return found_tokens

    def get_depth(self) -> int:
        """Calculate the maximum depth of the subtree rooted at this node."""
        if not self.children:
            return 1
        return 1 + max(child.get_depth() for child in self.children)

    def count_nodes(self) -> int:
        """Count the total number of nodes in the subtree rooted at this node."""
        return 1 + sum(child.count_nodes() for child in self.children)

    def __iter__(self) -> Iterator['SQLNode']:
        """Iterate over this node and all its descendants."""
        yield self
        for child in self.children:
            yield from child

    def __getitem__(self, key):
        """Return the child node at the specified index."""
        return self.children[key]

    def __repr__(self) -> str:
        """Return a detailed string representation of the SQL node for debugging."""
        return f"<SQLNode token={self.token}, children={len(self.children)}>"

class SQLQueryTree:
    """
    Represents the entire SQL query tree.

    Attributes
    ----------
    sql_query : str
        The SQL query string used to build the tree.
    root : SQLNode
        The root node of the SQL query tree.
    """
    def __init__(self, sql_query: str):
        self.sql_query = sql_query
        self.root: SQLNode = self._build_tree(sqlparse.parse(sql_query)[0])

    def _build_tree(self, parsed_query: sqlparse.sql.Statement) -> SQLNode:
        """
        Build the SQL query tree from a parsed SQL statement.

        Arguments
        ---------
        parsed_query : sqlparse.sql.Statement
            The parsed SQL statement.

        Returns
        -------
        SQLNode
            The root node of the SQL query tree.

        Raises
            ValueError: If the SQL query is invalid or parsing fails.
        """
        if not parsed_query:
            raise ValueError("Invalid SQL query provided")

        root = SQLNode()
        for token in parsed_query.tokens:
            if isinstance(token, sqlparse.sql.Token):
                node = SQLNode(SQLToken(token.ttype, token.value))
                root.add_child(node)
            elif isinstance(token, (sqlparse.sql.Parenthesis, sqlparse.sql.Statement)):
                node = SQLNode()
                root.add_child(node)
                node.children.append(self._build_tree(token))
        print("Node:", node)
        print("Children:", node.children)
        return root
    
    def get_depth(self) -> int:
        """
        Calculate the maximum depth of the SQL query tree.

        Returns:
            int: The maximum depth of the tree.
        """
        return self._get_depth_recursive(self.root)

    def _get_depth_recursive(self, node: SQLNode) -> int:
        """
        Helper method to recursively calculate the depth of the tree.

        Args:
            node (SQLNode): The current node being processed.
            current_depth (int): The depth of the current node.

        Returns:
            int: The depth of the tree rooted at the current node.
        """
        if not node.children:
            return 1
        return  1 + max(self._get_depth_recursive(child) for child in node.children)

    def __str__(self) -> str:
        """Return the string representation of the entire SQL query tree."""
        return self.root.__str__()

    def __len__(self) -> int:
        """Return the total number of nodes in the SQL query tree."""
        return self.root.count_nodes()

    def __iter__(self) -> Iterator[SQLNode]:
        """Iterate over all nodes in the SQL query tree."""
        return iter(self.root)

    def __getitem__(self, key):
        """Return the child node of the root at the specified index."""
        return self.root[key]

    def __repr__(self) -> str:
        """Return a detailed string representation of the SQL query tree for debugging."""
        return f"<SQLQueryTree root={repr(self.root)}>"

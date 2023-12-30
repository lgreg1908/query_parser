from dataclasses import dataclass
from pathlib import Path
import json
from typing import List


@dataclass
class TestCase:
    query: str
    name: str
    expected: dict


def load_test_cases(directory) -> List[TestCase]:
    test_cases = []

    # Create Path objects for the sql and expected directories
    sql_directory = Path(directory) / 'sql'
    expected_directory = Path(directory) / 'expected'

    # Get a list of SQL files in the sql directory
    sql_files = [f for f in sql_directory.glob('*.sql')]

    for sql_file in sql_files:
        # Extract the base name (without extension)
        base_name = sql_file.stem

        sql_path = sql_file
        json_path = expected_directory / f'{base_name}.json'

        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found for SQL file: {sql_file}")

        with open(sql_path, 'r') as sql_file:
            query = sql_file.read()

        with open(json_path, 'r') as json_file:
            expected = json.load(json_file)

        # Create a test case instance and append to the list
        test_case = TestCase(query=query, name=base_name, expected=expected)
        test_cases.append(test_case)

    return test_cases

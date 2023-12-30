WITH cte AS (
    SELECT col1 FROM table1
    UNION
    SELECT col2 FROM table2
    )
    SELECT * FROM cte
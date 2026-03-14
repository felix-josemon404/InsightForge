from sqlalchemy import text
from db import engine

def execute_sql(query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query))

        # If the query returns rows (SELECT)
        if result.returns_rows:
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]

    # If it's INSERT / UPDATE / DELETE
        else:
            conn.commit()
            return []
    



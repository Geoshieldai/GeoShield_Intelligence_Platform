"""
GeoShield Metadata Database
"""

from pathlib import Path
import sqlite3


DB_PATH = Path("database/geoshield.db")


class MetadataDatabase:

    def __init__(self):

        DB_PATH.parent.mkdir(
            exist_ok=True
        )

        self.connection = sqlite3.connect(DB_PATH)

        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(

            product_id TEXT PRIMARY KEY,

            provider TEXT,

            name TEXT,

            publication_date TEXT,

            origin_date TEXT,

            footprint TEXT
        )
        """)

        self.connection.commit()

    def insert(self, metadata: dict):

        self.cursor.execute("""
        INSERT OR REPLACE INTO products
        VALUES(
            ?,?,?,?,?,?
        )
        """, (

            metadata["product_id"],

            metadata["provider"],

            metadata["name"],

            metadata["publication_date"],

            metadata["origin_date"],

            metadata["footprint"]

        ))

        self.connection.commit()
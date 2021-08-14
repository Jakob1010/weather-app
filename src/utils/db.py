from contextlib import contextmanager
import psycopg2
import io
from sqlalchemy import create_engine

class WarehouseConnection:
    def __init__(
        self, db: str, user: str, password: str, host: str, port: int
    ):
        self.conn_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
    

    @contextmanager
    def managed_cursor(self):
        self.engine = create_engine(self.conn_url)
        self.conn = self.engine.raw_connection()
        self.curr = self.conn.cursor()
        try: 
            yield self.curr
        finally:
            self.conn.commit()
            self.curr.close()
            self.conn.close()
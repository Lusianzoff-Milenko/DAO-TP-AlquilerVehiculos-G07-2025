# python
import os
import sqlite3
import contextlib
import threading

from config.database import SingletonMeta


class Database(metaclass=SingletonMeta):
    def __init__(self, db_path: str | None = None):
        if getattr(self, "_initialized", False):
            return
        self._db_path = db_path or os.getenv("config/alquiler_vehiculos_data_base.db")
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._lock = threading.Lock()
        self._initialized = True

    def get_connection(self) -> sqlite3.Connection:
        return self._conn

    def get_cursor(self) -> sqlite3.Cursor:
        return self._conn.cursor()

    @contextlib.contextmanager
    def transaction(self):
        with self._lock:
            cur = self._conn.cursor()
            try:
                yield cur
                self._conn.commit()
            except:
                self._conn.rollback()
                raise
            finally:
                cur.close()

    def close(self):
        with self._lock:
            try:
                self._conn.close()
            except:
                pass
            finally:
                self._initialized = False
                type(self)._instances.pop(type(self), None)

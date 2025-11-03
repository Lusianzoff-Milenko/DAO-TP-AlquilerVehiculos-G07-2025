# python
import os
import sqlite3
import contextlib
import threading

from config.database import SingletonMeta


class Database(metaclass=SingletonMeta):
    def __init__(self, db_path: str | None = None):
        # idempotent init for singleton
        if getattr(self, "_initialized", False):
            return

        env_path = os.getenv("./alquiler_vehiculos_data_base")
        self._db_path = db_path or env_path or os.path.join(os.getcwd(), "./alquiler_vehiculos_data_base.db")

        # Ensure directory exists if path includes directories
        dirpath = os.path.dirname(self._db_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

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

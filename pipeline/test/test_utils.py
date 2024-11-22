import pytest
from pathlib import Path
from ..utils import initialize_database, reset_enviroment


def test_initialize_database(tmp_path):
    db_fp = Path(tmp_path / "test.db")
    test_db_fp = f"sqlite:///{db_fp}"
    initialize_database(conn_str=test_db_fp)
    assert db_fp.exists(), "Failed to initialise database."


def test_reset_enviroment(tmp_path):
    fp = Path(tmp_path / "test.txt")
    fp.touch()
    reset_enviroment(str(fp))
    assert not fp.exists(), "Failed to reset environment (removing the db)"

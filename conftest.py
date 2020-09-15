import pathlib
import pytest
import uuid


@pytest.fixture
def database_file(tmp_path):
    return tmp_path.joinpath(str(uuid.uuid4()))

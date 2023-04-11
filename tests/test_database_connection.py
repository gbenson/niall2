from lambda_function import Robot


def test_service_name(mock_database):
    """The database service name is "dynamodb"."""
    list(Robot().generate())
    assert mock_database._tables[0]._resource._service_name == "dynamodb"


def test_table_name(mock_database):
    """The database table name is "Niall2"."""
    list(Robot().generate())
    assert mock_database._tables[0]._name == "Niall2"


def test_lazy_loading_1(mock_database):
    """The database connection is not established unless required."""
    Robot()
    assert len(mock_database._tables) == 0


def test_lazy_loading_2(mock_database):
    """The database connection is established when required."""
    list(Robot().generate())
    assert len(mock_database._tables) == 1
    assert mock_database._tables[0]._load_count == 1


def test_persistence(mock_database):
    """The database connection persists across invocations."""
    lambda_handler = Robot()
    list(lambda_handler.generate())
    list(lambda_handler.generate())
    assert len(mock_database._tables) == 1
    assert mock_database._tables[0]._load_count == 1

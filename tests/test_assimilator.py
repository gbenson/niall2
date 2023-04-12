import pytest

from lambda_function import Robot


@pytest.mark.parametrize(
    "tokens,expect_num_updates",
    (([], 1),
     (["hello", "niall"], 3),
     ))
def test_num_updates(mock_database, tokens, expect_num_updates):
    """The result of storing N tokens is N + 1 table updates."""
    Robot().store(tokens)
    assert len(mock_database._tables[0]._updates) == expect_num_updates


@pytest.mark.parametrize(
    "update_index,expect_key",
    ((0, {"From": "_", "To": "hello"}),
     (1, {"From": "hello", "To": "niall"}),
     (2, {"From": "niall", "To": "_"}),
     ))
def test_updates(mock_database, update_index, expect_key):
    Robot().store(["hello", "niall"])
    update = mock_database._tables[0]._updates[update_index]
    assert update == {
        "ExpressionAttributeValues": {
            ":one": 1,
        },
        "Key": expect_key,
        "UpdateExpression": "ADD Weight :one",
    }

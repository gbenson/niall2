import pytest

from lambda_function import Robot


def test_generation(mock_database):
    """The result of our deterministic generation is as expected."""
    assert list(Robot().generate()) == ["hello", "gary"]


def test_num_queries(mock_database):
    """The expected number of queries were executed."""
    list(Robot().generate())
    assert len(mock_database._tables[0]._queries) == 3


@pytest.mark.parametrize(
    "query_index,expect_kce",
    ((0, "From = _"),
     (1, "From = hello"),
     (2, "From = gary"),
     ))
def test_queries(mock_database, query_index, expect_kce):
    list(Robot().generate())
    query = mock_database._tables[0]._queries[query_index]
    assert len(query) == 1
    [[key, value]] = query.items()
    assert key == "KeyConditionExpression"
    kce = value.get_expression()
    kce = kce["format"].format(
        kce["values"][0].name,
        *kce["values"][1:],
        operator=kce["operator"])
    assert kce == expect_kce

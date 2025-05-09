import pytest

from helpers.cluster import ClickHouseCluster

cluster = ClickHouseCluster(__file__)

node1 = cluster.add_instance("node1", with_zookeeper=True)
node2 = cluster.add_instance(
    "node2",
    with_zookeeper=True,
    image="clickhouse/clickhouse-server",
    tag="23.3",
    with_installed_binary=True,
)


@pytest.fixture(scope="module")
def start_cluster():
    try:
        cluster.start()

        yield cluster
    finally:
        cluster.shutdown()


def test_different_versions(start_cluster):
    assert (
        node1.query(
            "SELECT uniqExact(x) FROM (SELECT version() as x from remote('node{1,2}', system.one)) settings serialize_query_plan = 0"
        )
        == "2\n"
    )

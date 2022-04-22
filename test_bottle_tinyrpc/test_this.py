import pytest

from tinyrpc.protocols.jsonrpc import JSONRPCError


def test_bottle_tinyrpc_basic_functionality(test_client):
    assert test_client.foo(1, 2) == 3
    assert test_client.bar("Bar", ["wat", "hello"], {"foo": "bar"}) == "wat"
    with pytest.raises(JSONRPCError):
        test_client.nonesuch(1)

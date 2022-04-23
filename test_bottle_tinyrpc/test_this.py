import pytest

from tinyrpc.protocols.jsonrpc import JSONRPCError
from tinyrpc.protocols.msgpackrpc import MSGPACKRPCProtocol, MSGPACKRPCError


def test_bottle_tinyrpc_basic_functionality(test_client):
    assert test_client.foo(1, 2) == 3
    assert test_client.bar("Bar", ["wat", "hello"], {"foo": "bar"}) == "wat"
    with pytest.raises(JSONRPCError):
        test_client.nonesuch(1)

    with pytest.raises(JSONRPCError):
        test_client.fails("foo")


@pytest.mark.parametrize("tinyrpc_protocol", [MSGPACKRPCProtocol])
@pytest.mark.parametrize("tinyrpc_mimetype", ["application/x-msgpack"])
def test_bottle_msgpack_basic_functionality(test_client, tinyrpc_protocol, tinyrpc_mimetype):
    assert test_client.foo(1, 2) == 3
    assert test_client.bar("Bar", ["wat", "hello"], {"foo": "bar"}) == "wat"
    with pytest.raises(MSGPACKRPCError):
        test_client.nonesuch(1)

    with pytest.raises(MSGPACKRPCError):
        test_client.fails("foo")
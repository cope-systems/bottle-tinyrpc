import pytest
from webtest import TestApp
from bottle import Bottle
from tinyrpc.transports import ClientTransport
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc import RPCClient

from bottle_tinyrpc import TinyRPCPlugin


class WebtestTransport(ClientTransport):
    def __init__(self, app: TestApp, endpoint):
        self.app = app
        self.endpoint = endpoint

    def send_message(self, message: bytes, expect_reply: bool = True) -> bytes:
        r = self.app.post(self.endpoint, params=message, content_type="application/json-rpc")
        if expect_reply:
            return r.body


@pytest.fixture
def endpoint():
    return "/"


@pytest.fixture
def tinyrpc_protocol():
    return JSONRPCProtocol


@pytest.fixture
def tinyrpc_mimetype():
    return "application/json"


@pytest.fixture
def tinyrpc_plugin(endpoint, tinyrpc_protocol, tinyrpc_mimetype):
    plugin = TinyRPCPlugin(
        endpoint,
        protocol=tinyrpc_protocol(),
        mimetype=tinyrpc_mimetype
    )

    @plugin.public
    def foo(a, b):
        return a + b

    @plugin.public
    def bar(a, b, c):
        return "wat"

    @plugin.public
    def fails(a):
        raise IOError("huh")

    return plugin


@pytest.fixture
def bottle_app():
    return Bottle()


@pytest.fixture
def test_app(bottle_app, tinyrpc_plugin):
    bottle_app.install(tinyrpc_plugin)
    return TestApp(bottle_app)


@pytest.fixture
def webtest_transport(test_app, endpoint):
    return WebtestTransport(test_app, endpoint)


@pytest.fixture
def test_client(webtest_transport, tinyrpc_protocol):
    rpc_client = RPCClient(tinyrpc_protocol(), webtest_transport)
    remote_server = rpc_client.get_proxy()
    return remote_server

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import graph_pb2 as graph__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in graph_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class GraphStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getAllVertices = channel.unary_unary(
                '/Graph.Graph/getAllVertices',
                request_serializer=graph__pb2.Empty.SerializeToString,
                response_deserializer=graph__pb2.getAllResponse.FromString,
                _registered_method=True)
        self.getAllEdges = channel.unary_unary(
                '/Graph.Graph/getAllEdges',
                request_serializer=graph__pb2.Empty.SerializeToString,
                response_deserializer=graph__pb2.getAllResponse.FromString,
                _registered_method=True)
        self.addVertex = channel.unary_unary(
                '/Graph.Graph/addVertex',
                request_serializer=graph__pb2.Vertex.SerializeToString,
                response_deserializer=graph__pb2.Response.FromString,
                _registered_method=True)
        self.addEdge = channel.unary_unary(
                '/Graph.Graph/addEdge',
                request_serializer=graph__pb2.Edge.SerializeToString,
                response_deserializer=graph__pb2.EdgeResponse.FromString,
                _registered_method=True)
        self.removeVertex = channel.unary_unary(
                '/Graph.Graph/removeVertex',
                request_serializer=graph__pb2.Vertex.SerializeToString,
                response_deserializer=graph__pb2.Response.FromString,
                _registered_method=True)
        self.removeEdge = channel.unary_unary(
                '/Graph.Graph/removeEdge',
                request_serializer=graph__pb2.Edge.SerializeToString,
                response_deserializer=graph__pb2.Response.FromString,
                _registered_method=True)
        self.hasVertex = channel.unary_unary(
                '/Graph.Graph/hasVertex',
                request_serializer=graph__pb2.Vertex.SerializeToString,
                response_deserializer=graph__pb2.YesNo.FromString,
                _registered_method=True)
        self.hasEdge = channel.unary_unary(
                '/Graph.Graph/hasEdge',
                request_serializer=graph__pb2.Edge.SerializeToString,
                response_deserializer=graph__pb2.YesNo.FromString,
                _registered_method=True)
        self.getNeighbors = channel.unary_unary(
                '/Graph.Graph/getNeighbors',
                request_serializer=graph__pb2.Vertex.SerializeToString,
                response_deserializer=graph__pb2.getAllResponse.FromString,
                _registered_method=True)
        self.hasPath = channel.unary_unary(
                '/Graph.Graph/hasPath',
                request_serializer=graph__pb2.EdgeList.SerializeToString,
                response_deserializer=graph__pb2.YesNo.FromString,
                _registered_method=True)
        self.getPath = channel.unary_unary(
                '/Graph.Graph/getPath',
                request_serializer=graph__pb2.Edge.SerializeToString,
                response_deserializer=graph__pb2.Multiple.FromString,
                _registered_method=True)
        self.shortestPath = channel.unary_unary(
                '/Graph.Graph/shortestPath',
                request_serializer=graph__pb2.Edge.SerializeToString,
                response_deserializer=graph__pb2.Multiple.FromString,
                _registered_method=True)
        self.printGraph = channel.unary_unary(
                '/Graph.Graph/printGraph',
                request_serializer=graph__pb2.Empty.SerializeToString,
                response_deserializer=graph__pb2.getAllResponse.FromString,
                _registered_method=True)
        self.Shutdown = channel.unary_unary(
                '/Graph.Graph/Shutdown',
                request_serializer=graph__pb2.Empty.SerializeToString,
                response_deserializer=graph__pb2.Response.FromString,
                _registered_method=True)


class GraphServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getAllVertices(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getAllEdges(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addVertex(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addEdge(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeVertex(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def removeEdge(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def hasVertex(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def hasEdge(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getNeighbors(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def hasPath(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getPath(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def shortestPath(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def printGraph(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Shutdown(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GraphServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getAllVertices': grpc.unary_unary_rpc_method_handler(
                    servicer.getAllVertices,
                    request_deserializer=graph__pb2.Empty.FromString,
                    response_serializer=graph__pb2.getAllResponse.SerializeToString,
            ),
            'getAllEdges': grpc.unary_unary_rpc_method_handler(
                    servicer.getAllEdges,
                    request_deserializer=graph__pb2.Empty.FromString,
                    response_serializer=graph__pb2.getAllResponse.SerializeToString,
            ),
            'addVertex': grpc.unary_unary_rpc_method_handler(
                    servicer.addVertex,
                    request_deserializer=graph__pb2.Vertex.FromString,
                    response_serializer=graph__pb2.Response.SerializeToString,
            ),
            'addEdge': grpc.unary_unary_rpc_method_handler(
                    servicer.addEdge,
                    request_deserializer=graph__pb2.Edge.FromString,
                    response_serializer=graph__pb2.EdgeResponse.SerializeToString,
            ),
            'removeVertex': grpc.unary_unary_rpc_method_handler(
                    servicer.removeVertex,
                    request_deserializer=graph__pb2.Vertex.FromString,
                    response_serializer=graph__pb2.Response.SerializeToString,
            ),
            'removeEdge': grpc.unary_unary_rpc_method_handler(
                    servicer.removeEdge,
                    request_deserializer=graph__pb2.Edge.FromString,
                    response_serializer=graph__pb2.Response.SerializeToString,
            ),
            'hasVertex': grpc.unary_unary_rpc_method_handler(
                    servicer.hasVertex,
                    request_deserializer=graph__pb2.Vertex.FromString,
                    response_serializer=graph__pb2.YesNo.SerializeToString,
            ),
            'hasEdge': grpc.unary_unary_rpc_method_handler(
                    servicer.hasEdge,
                    request_deserializer=graph__pb2.Edge.FromString,
                    response_serializer=graph__pb2.YesNo.SerializeToString,
            ),
            'getNeighbors': grpc.unary_unary_rpc_method_handler(
                    servicer.getNeighbors,
                    request_deserializer=graph__pb2.Vertex.FromString,
                    response_serializer=graph__pb2.getAllResponse.SerializeToString,
            ),
            'hasPath': grpc.unary_unary_rpc_method_handler(
                    servicer.hasPath,
                    request_deserializer=graph__pb2.EdgeList.FromString,
                    response_serializer=graph__pb2.YesNo.SerializeToString,
            ),
            'getPath': grpc.unary_unary_rpc_method_handler(
                    servicer.getPath,
                    request_deserializer=graph__pb2.Edge.FromString,
                    response_serializer=graph__pb2.Multiple.SerializeToString,
            ),
            'shortestPath': grpc.unary_unary_rpc_method_handler(
                    servicer.shortestPath,
                    request_deserializer=graph__pb2.Edge.FromString,
                    response_serializer=graph__pb2.Multiple.SerializeToString,
            ),
            'printGraph': grpc.unary_unary_rpc_method_handler(
                    servicer.printGraph,
                    request_deserializer=graph__pb2.Empty.FromString,
                    response_serializer=graph__pb2.getAllResponse.SerializeToString,
            ),
            'Shutdown': grpc.unary_unary_rpc_method_handler(
                    servicer.Shutdown,
                    request_deserializer=graph__pb2.Empty.FromString,
                    response_serializer=graph__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Graph.Graph', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Graph.Graph', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Graph(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getAllVertices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/getAllVertices',
            graph__pb2.Empty.SerializeToString,
            graph__pb2.getAllResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getAllEdges(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/getAllEdges',
            graph__pb2.Empty.SerializeToString,
            graph__pb2.getAllResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def addVertex(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/addVertex',
            graph__pb2.Vertex.SerializeToString,
            graph__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def addEdge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/addEdge',
            graph__pb2.Edge.SerializeToString,
            graph__pb2.EdgeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def removeVertex(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/removeVertex',
            graph__pb2.Vertex.SerializeToString,
            graph__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def removeEdge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/removeEdge',
            graph__pb2.Edge.SerializeToString,
            graph__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def hasVertex(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/hasVertex',
            graph__pb2.Vertex.SerializeToString,
            graph__pb2.YesNo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def hasEdge(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/hasEdge',
            graph__pb2.Edge.SerializeToString,
            graph__pb2.YesNo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getNeighbors(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/getNeighbors',
            graph__pb2.Vertex.SerializeToString,
            graph__pb2.getAllResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def hasPath(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/hasPath',
            graph__pb2.EdgeList.SerializeToString,
            graph__pb2.YesNo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getPath(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/getPath',
            graph__pb2.Edge.SerializeToString,
            graph__pb2.Multiple.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def shortestPath(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/shortestPath',
            graph__pb2.Edge.SerializeToString,
            graph__pb2.Multiple.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def printGraph(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/printGraph',
            graph__pb2.Empty.SerializeToString,
            graph__pb2.getAllResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Shutdown(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Graph.Graph/Shutdown',
            graph__pb2.Empty.SerializeToString,
            graph__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
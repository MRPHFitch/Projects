import threading
import grpc
from concurrent import futures
import logging
import broker_pb2
import broker_pb2_grpc

logging.basicConfig(
    filename="graph.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
class Broker(broker_pb2_grpc.BrokerServicer):
    def __init__(self):
        # Create channels to communicate with multiple graph servers
        self.server_channels = [grpc.insecure_channel('localhost:50051'),
                                grpc.insecure_channel('localhost:50055')]
        self.server_stubs = [broker_pb2_grpc.GraphStub(channel)
                             for channel in self.server_channels]
        self.stopEvent = threading.Event()

    def getServerStub(self, vertex):
        # Simple hash function to distribute vertices among servers
        return self.server_stubs[hash(vertex) % len(self.server_stubs)]

    ''' PATH ALGORITHMS HANDLED BY THE BROKER '''

    def hasPath(self, request, context):
        print("FINDING PATH...")
        edges = request.edges
        vn = edges[-1]
        print("LAST NODE {}".format(vn))
        counter = 0
        for i in range(len(edges) - 1):
            current_vertex = edges[i]
            next_vertex = edges[i + 1]
            stub = self.getServerStub(current_vertex.vert)
            has_vertex_response = stub.hasVertex(broker_pb2.Vertex(vert=current_vertex.vert))
            if not has_vertex_response.tf:
                logging.warning("Path does not exist. Vertex {} does not exist.".format(current_vertex.vert))
                print("PATH DOES NOT EXIST. NODE {} DOES NOT EXIST.".format(current_vertex.vert))
                return broker_pb2.YesNo(tf=False)
            has_next_vertex_response = stub.hasVertex(broker_pb2.Vertex(vert=next_vertex.vert))
            if not has_next_vertex_response.tf:
                logging.warning("Path does not exist. Vertex {} does not exist.".format(next_vertex.vert))
                print("PATH DOES NOT EXIST. NODE {} DOES NOT EXIST.".format(next_vertex.vert))
                return broker_pb2.YesNo(tf=False)
            edge = broker_pb2.Edge(start=broker_pb2.Vertex(vert=current_vertex.vert),
                                   to=broker_pb2.Vertex(vert=next_vertex.vert))
            logging.info(f"Checking edge: {edge.start.vert} -> {edge.to.vert}")
            has_edge_response = stub.hasEdge(edge)
            if not has_edge_response.tf:
                logging.warning("Path does not exist. Edge from {} to {} does not exist.".format(
                    current_vertex.vert, next_vertex.vert))
                print(f"PATH DOES NOT EXIST. EDGE {current_vertex.vert} -> {next_vertex.vert} DOES NOT EXIST.")
                return broker_pb2.YesNo(tf=False)
            counter += 1
        print("FOUND PATH: {}".format(edges))
        return broker_pb2.YesNo(tf=True)

    def shortestPath(self, request, context):
        vs = request.start.vert
        vd = request.to.vert
        print("\nFINDING SHORTEST PATH...")
        stub = self.getServerStub(vs)
        point1 = broker_pb2.Vertex(vert=vs)
        point2 = broker_pb2.Vertex(vert=vd)
        reply1 = stub.hasVertex(point1)
        reply2 = stub.hasVertex(point2)
        if reply1.tf == False:
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs))
            return broker_pb2.Multiple(message="Vertex {} does not exist")
        if reply2.tf == False:
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd))
            return broker_pb2.Multiple(message="Vertex {} does not exist.")
        queue = [(vs, [vs])]
        visited = set()
        while queue:
            current, path = queue.pop(0)
            if current == vd:
                print("SHORTEST PATH FOUND: {}.".format(path))
                theWay = [broker_pb2.Vertex(vert=v) for v in path]
                return broker_pb2.Multiple(edges=broker_pb2.EdgeList(edges=theWay))
            visited.add(current)
            neighbors_response = stub.getNeighbors(broker_pb2.Vertex(vert=current))
            for neighbor in neighbors_response.response:
                if neighbor not in visited and neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))
        print("PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd))
        return broker_pb2.Multiple(message="Path does not exist.")

    ''' FUNCTIONS HANDLED BY THE SERVER '''
    def addVertex(self, request, context):
        stub = self.getServerStub(request.vert)
        return stub.addVertex(request)

    def addEdge(self, request, context):
        stub = self.getServerStub(request.start.vert)
        return stub.addEdge(request)

    def removeVertex(self, request, context):
        stub = self.getServerStub(request.vert)
        return stub.removeVertex(request)

    def removeEdge(self, request, context):
        stub = self.getServerStub(request.start.vert)
        return stub.removeEdge(request)

    def hasVertex(self, request, context):
        stub = self.getServerStub(request.vert)
        return stub.hasVertex(request)

    def hasEdge(self, request, context):
        stub = self.getServerStub(request.start.vert)
        return stub.hasEdge(request)

    def getAllVertices(self, request, context):
        responses = []
        for stub in self.server_stubs:
            response = stub.getAllVertices(request)
            responses.extend(response.response)
        return broker_pb2.getAllResponse(response=responses)

    def getAllEdges(self, request, context):
        responses = []
        for stub in self.server_stubs:
            response = stub.getAllEdges(request)
            responses.extend(response.response)
        return broker_pb2.getAllResponse(response=responses)

    def getNeighbors(self, request, context):
        stub = self.getServerStub(request.vert)
        return stub.getNeighbors(request)

    def Shutdown(self, request, context):
        print("Broker received shutdown request.")
        for stub in self.server_stubs:
            stub.Shutdown(broker_pb2.Empty())
        print("Shutting down broker.")
        self.stopEvent.set()
        return broker_pb2.Response(message="We are shutting down now.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    broker_instance = Broker()
    broker_pb2_grpc.add_BrokerServicer_to_server(broker_instance, server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("BROKER SERVER STARTED ON PORT 50052")
    broker_instance.stopEvent.wait()
    server.stop(3)
    print("I have shutdown. Goodbye.")

if __name__ == '__main__':
    serve()
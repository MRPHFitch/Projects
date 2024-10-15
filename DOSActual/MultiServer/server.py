from concurrent import futures
import logging
import sys
import threading
import broker_pb2
import broker_pb2_grpc
import grpc

logging.basicConfig(
    filename = "graph.log",
    filemode = "w",
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.DEBUG
)
class Graph(broker_pb2_grpc.GraphServicer):
    def __init__(self, stops):
        self.graph = {}  # Dictionary to store the graph
        self.stopEvent=stops
        logging.info("Graph is initialized.")
        
    def getAllVertices(self, request, context):
        print(f"All vertices: {self.graph.keys()}")
        vertices=list(self.graph.keys())
        logging.info(f"All vertices: {self.graph.keys()}")
        return broker_pb2.getAllResponse(response=vertices)

    def getAllEdges(self, request, context):
        print(f"All Edges: {self.graph.values()}")
        edges=[]
        for vertex, neighbors in self.graph.items():
            for neighbor in neighbors:
                edges.append(f"{vertex}->{neighbor}")
        logging.info(f"All edges: {self.graph.values()}")
        return broker_pb2.getAllResponse(response=edges)

    def addVertex(self, request, context):
        v=request.vert
        if v in self.graph:
            logging.warning(f"Failed to add vertex {v}, as it already exists.")
            return broker_pb2.Response(message="Fail: Vertex already exists.")
        self.graph[v] = []
        logging.info(f"Vertex {v} is added successfully.")
        return broker_pb2.Response(message="Success: Vertex added.")

    def addEdge(self, request, context):
        v0=request.start.vert
        v1=request.to.vert
        #If a vertex is not in the graph, add it, then create the edge
        if v0 not in self.graph:
            self.addVertex(broker_pb2.Vertex(vert=v0), context)
        if v1 not in self.graph:
            self.addVertex((broker_pb2.Vertex(vert=v1)), context)
        #If the edge already exists, don't add it
        if v1 in self.graph[v0]:
            return broker_pb2.Response(message="Fail: Edge already exists.")
        #Finally, add that edge
        self.graph[v0].append(v1)
        return broker_pb2.Response(message="Success: Edge added.")

    def removeVertex(self, request, context):
        v=request.vert
        if v not in self.graph:
            return broker_pb2.Response(message="Fail: Vertex does not exist.")
        #Check if the given vertex has any neighbors
        nReq=broker_pb2.Vertex(vert=v)
        neighbors=self.getNeighbors(nReq, context)
        #If the point does not have any neighbors, remove the vertex
        if neighbors.response:
            return broker_pb2.Response(message=f"Vertex {v} could not be removed. It had friends.")
        del self.graph[v]
        return broker_pb2.Response(message="Success: Vertex removed")

    def removeEdge(self, request, context):
        v0=request.start.vert
        v1=request.to.vert
        if v0 not in self.graph or v1 not in self.graph[v0]:
            logging.warning(f"Failed to remove edge ({v0}, {v1}), as it does not exist.")
            return broker_pb2.Response(message="Fail: Edge does not exist.")
        self.graph[v0].remove(v1)
        logging.info(F"Edge ({v0}, {v1}) is removed successfully.")
        return broker_pb2.Response(message="Success: Edge removed.")

    def hasVertex(self, request, context):
        v=request.vert
        if (v in self.graph):
            logging.info(F"Vertex {v} exists.")
            return broker_pb2.YesNo(tf=True)
        else:
            logging.info(f"Vertex {v} does not exist.")
            return broker_pb2.YesNo(tf=False)

    def hasEdge(self, request, context):
        v0=request.start.vert
        v1=request.to.vert
        if(v0 in self.graph and v1 in self.graph[v0]):
            logging.info(f"Edge ({v0}, {v1}) exists.")
            return broker_pb2.YesNo(tf=True)
        else:
            logging.info(f"Edge ({v0}, {v1}) does not exists.")
            return broker_pb2.YesNo(tf=False)

    def getNeighbors(self, request, context):
        point=request.vert
        if point in self.graph:
            neighbors = self.graph[point]
            logging.info(f"Neighbors of {point} are: {neighbors}")
            print(f"Neighbors of {point} are: {neighbors}")
        else:
            logging.info(f"No neighbors found from {point}")
            print(f"{point} has no friends. No neighbors found.")
        return broker_pb2.getAllResponse(response=neighbors)

    def printGraph(self):
        #print("PRINTING GRAPH...") 
        #print("")
        logging.info("PRINTING GRAPH...")
        logging.debug(f"Graph structures : {self.graph}")
        visuals=[]
        for vertex, neighbors in self.graph.items():
            for neighbor in neighbors:
                visuals.append(f"{vertex}->{neighbor}")
        return broker_pb2.getAllResponse(response=visuals)
    
    def Shutdown(self, request, context):
        print("Shutting down now.")
        self.stopEvent.set()
        return(broker_pb2.Response(message="Goodbye."))
             
def serve(port, stops):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    broker_pb2_grpc.add_GraphServicer_to_server(Graph(stops), server)
    server.add_insecure_port(f'[::]:{port}')  # Listen on port 50051 for broker 
    server.start()
    print(f"Graph server started on port {port}")
    stops.wait()
    print("Are we here?")
    server.stop(2)
    print("I have shutdown. Goodbye.")

if __name__ == '__main__':
    if len(sys.argv) !=2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port=sys.argv[1]
    stopEvent=threading.Event()
    serve(port,stopEvent)
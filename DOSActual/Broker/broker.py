import threading
import grpc 
from concurrent import futures 
import logging
import broker_pb2 # includes broker definitions 
import broker_pb2_grpc # includes broker definitions 

logging.basicConfig(
    filename = "graph.log",
    filemode = "w",
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.DEBUG
)

class Broker(broker_pb2_grpc.BrokerServicer):
    
    def __init__(self):

        # create channel to communicate with graph server
        self.server_channel = grpc.insecure_channel('localhost:50051')
        self.server_stub = broker_pb2_grpc.GraphStub(self.server_channel)  # Create server stub
        self.stopEvent=threading.Event()

    ''' PATH ALGORITHMS HANDLED BY THE BROKER '''

    # hasPath breaks up the algorithm into separate function calls to the server 
    def hasPath(self, request, context):

        print("FINDING PATH...")
        edges=request.edges     
        vn = edges[-1]
        print("LAST NODE {}".format(vn))

        # iterate through the list 
        # for each vertex (has_vertex), 
        # check if proceeding vertex + corresponding edge exists (has_edge)
        counter = 0
        for i in range(len(edges) - 1): 
            
            current_vertex = edges[i]
            next_vertex = edges[i + 1]

            # Check if the current vertex exists
            has_vertex_response = self.server_stub.hasVertex(broker_pb2.Vertex(vert=current_vertex.vert))
            if not has_vertex_response.tf:
                logging.warning("Path does not exist. Vertex {} does not exist.".format(current_vertex.vert))
                print("PATH DOES NOT EXIST. NODE {} DOES NOT EXIST.".format(current_vertex.vert))
                return broker_pb2.YesNo(tf=False)

            # Check if the next vertex exists
            has_next_vertex_response = self.server_stub.hasVertex(broker_pb2.Vertex(vert=next_vertex.vert))
            if not has_next_vertex_response.tf:
                logging.warning("Path does not exist. Vertex {} does not exist.".format(next_vertex.vert))
                print("PATH DOES NOT EXIST. NODE {} DOES NOT EXIST.".format(next_vertex.vert))
                return broker_pb2.YesNo(tf=False)

            # Check if the edge between the current and next vertex exists
            edge = broker_pb2.Edge(start=broker_pb2.Vertex(vert=current_vertex.vert),
                                to=broker_pb2.Vertex(vert=next_vertex.vert))
            logging.info(f"Checking edge: {edge.start.vert} -> {edge.to.vert}")
            has_edge_response = self.server_stub.hasEdge(edge)

            if not has_edge_response.tf:
                logging.warning("Path does not exist. Edge from {} to {} does not exist.".format(
                    current_vertex.vert, next_vertex.vert))
                print(f"PATH DOES NOT EXIST. EDGE {current_vertex.vert} -> {next_vertex.vert} DOES NOT EXIST.")
                return broker_pb2.YesNo(tf=False)

            counter += 1

        # If the loop completes, the path exists
        print("FOUND PATH: {}".format(edges))
        return broker_pb2.YesNo(tf=True)


    def getPath(self, request, context):
        
        vs=request.start.vert
        vd=request.to.vert

        print("\nGETTING PATH...")

        response1=self.server_stub.hasVertex(broker_pb2.Vertex(vert=vs))
        response2=self.server_stub.hasVertex(broker_pb2.Vertex(vert=vd))

        if(response1.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs))
            return broker_pb2.Multiple(message="Vertex {} does not exist.")

        if(response2.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd))
            return broker_pb2.Multiple(message="Vertex {} does not exist.")

        # storing current vertex and current path in a stack
        # current path will only be initialized with the starting vertex 
        # current vertex is updated with each stack pop 
        stack = [(vs, [vs])]

        while stack:
            
            current, path = stack.pop()

            # final vertex has been reached
            if current == vd:
                print("PATH FOUND: {}".format(path))
                theWay=[broker_pb2.Vertex(vert=v) for v in path]
                return broker_pb2.EdgeList(edges=theWay)

            # find all neighbors of current vertex using server function 
            neighbors_response = self.server_stub.getNeighbors(broker_pb2.Vertex(vert=current))            
            for neighbor in neighbors_response.response:
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))

        print("PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd))
        return broker_pb2.Multiple(message="Path does not exist.") 



    def shortestPath(self, request, context):
        
        vs=request.start.vert
        vd=request.to.vert 

        print("\nFINDING SHORTEST PATH...")
        
        point1=broker_pb2.Vertex(vert=vs)
        point2=broker_pb2.Vertex(vert=vd)

        print(f"Checking existence of vertex: {vs}")
        print(f"Checking existence of vertex: {vd}")
        reply1=self.server_stub.hasVertex(point1)
        reply2=self.server_stub.hasVertex(point2)


        if(reply1.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs))
            return broker_pb2.Multiple(message="Vertex {} does not exist")

        if(reply2.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd))
            return broker_pb2.Multiple(message="Vertex {} does not exist.")

        queue = [(vs, [vs])] # reference self.get_path()
        visited = set() 

        while queue:
            current, path = queue.pop(0) # first element popped (not last)

            # final vertex has been reached
            if current == vd:
                print("SHORTEST PATH FOUND: {}.".format(path))
                theWay=[broker_pb2.Vertex(vert=v) for v in path]
                return broker_pb2.Multiple(edges=broker_pb2.EdgeList(edges=theWay))

            visited.add(current)

            # find all neighbors of current vertex
            neighbors_response = self.server_stub.getNeighbors(broker_pb2.Vertex(vert=current))
            for neighbor in neighbors_response.response:
                if neighbor not in visited and neighbor not in path:
                    queue.append((neighbor, path + [neighbor]))

        print("PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd))
        return broker_pb2.Multiple(message="Path does not exist.") 


    ''' FUNCTIONS HANDLED BY THE SERVER ''' 
    def addVertex(self, request, context):
        return self.server_stub.addVertex(request)

    def addEdge(self, request, context):
        return self.server_stub.addEdge(request)

    def removeVertex(self, request, context):
        return self.server_stub.removeVertex(request)

    def removeEdge(self, request, context):
        return self.server_stub.removeEdge(request)

    def hasVertex(self, request, context):
        return self.server_stub.hasVertex(request)

    def hasEdge(self, request, context):
        return self.server_stub.hasEdge(request)

    def getAllVertices(self, request, context):
        return self.server_stub.getAllVertices(request)

    def getAllEdges(self, request, context):
        return self.server_stub.getAllEdges(request)

    def getNeighbors(self, request, context):
        return self.server_stub.getNeighbors(request)

    def Shutdown(self, request, context):
        print("Broker received shutdown request.")
        # Forward shutdown to the server
        self.server_stub.Shutdown(broker_pb2.Empty())
        print("Shutting down broker.")
        self.stopEvent.set()
        return broker_pb2.Response(message="We are shutting down now.")
    

def serve():
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    broker_instance = Broker()  # create instance of broker
    broker_pb2_grpc.add_BrokerServicer_to_server(broker_instance, server)
    server.add_insecure_port('[::]:50052')  # Listen on port 50052 for client
    server.start()
    print("BROKER SERVER STARTED ON PORT 50052")
    broker_instance.stopEvent.wait()
    server.stop(3)
    print("I have shutdown. Goodbye.")

if __name__ == '__main__':
    serve()

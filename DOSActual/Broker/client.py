import sys 
import logging
import grpc
import broker_pb2
import broker_pb2_grpc

logging.basicConfig(level=logging.INFO)

''' client parses input file and sends requests to the server '''
class Graph():
     def __init__(self):
        self.graph = {}  # Dictionary to store the graph
        logging.info("Graph is initialized.")

def client(input):
    
    # connect to gRPC server on localhost port 50052
    channel = grpc.insecure_channel('localhost:50052')  # Connect to Broker
    stub = broker_pb2_grpc.BrokerStub(channel)

    logging.info(f"Processing file : {input}")

    try:
        with open(input, 'r') as infile:
            for line in infile:
                command = line.strip()

                if command.startswith("add-vertex"):
                    vertex = command.split("<")[1].replace('>', '')
                    response = stub.addVertex(broker_pb2.Vertex(vert=vertex))
                    logging.info(f"Add Vertex {vertex}: {response.message}")
                    print(f"Add Vertex {vertex}: {response.message}")

                elif command.startswith("add-edge"):

                    #parsing vertices of edge
                    vertices = command.split("<")[1].split(", ")
                    v0 = vertices[0]
                    v1 = vertices[1].replace('>', '')
                    ()
                    
                    try:
                        response = stub.addEdge(broker_pb2.Edge(start=broker_pb2.Vertex(vert=v0),
                                        to=broker_pb2.Vertex(vert=v1)))
                        logging.info(response.edges)
                        print(f"Edge {v0} -> {v1}: {response.edges}")
                    except grpc.RpcError as e:
                        logging.error(f"gRPC failed: {e.details()}")
                        print(f"gRPC failed: {e.details()}")


                elif command.startswith("get-all-vertices"):
                    response = stub.getAllVertices(broker_pb2.Empty()) #empty message 
                    logging.info(f"All Vertices of graph: {response.response}") #gets all response

                elif command.startswith("get-all-edges"):
                    response = stub.getAllEdges(broker_pb2.Empty())
                    logging.info(f"All Edges of graph: {response.response}")

                elif command.startswith("remove-vertex"):
                    vertex = command.split("<")[1].replace('>', '')
                    response = stub.removeVertex(broker_pb2.Vertex(vert=vertex))
                    logging.info(f"Remove Vertex {vertex}: {response.message}")

                elif command.startswith("remove-edge"):

                    # parsing vertices of edge 
                    vertices = command.split("<")[1].split(", ")
                    v0 = vertices[0]
                    v1 = vertices[1].replace('>', '')

                    response = stub.removeEdge(broker_pb2.Edge(
                        start = broker_pb2.Vertex(vert = v0),
                        to = broker_pb2.Vertex(vert = v1)
                    ))
                    logging.info(f"Remove Edge <{v0},{v1}>: {response.message}")

                elif command.startswith("has-vertex"):

                    #Parse to get the vertex and check if it exists
                    vertex = command.split("<")[1].replace('>', '')
                    response = stub.hasVertex(broker_pb2.Vertex(vert = vertex))
                    if(response.tf==True):
                        logging.info(f"Vertex {vertex} exists.")
                    else:
                        logging.info(f"Vertex {vertex} exists.")

                elif command.startswith("has-edge"):

                    # parsing vertices of edge 
                    vertices = command.split("<")[1].split(", ")
                    v0 = vertices[0]
                    v1 = vertices[1].replace('>', '')

                    response = stub.hasEdge(broker_pb2.Edge(
                        start = broker_pb2.Vertex(vert = v0),
                        to = broker_pb2.Vertex(vert = v1)
                    ))
                    if(response.tf==True):
                        logging.info(f"Edge <{v0}, {v1}> exists.")
                    else:
                        logging.info(f"Edge <{v0}, {v1}> does not exists.")

                elif command.startswith("get-neighbors"):
                    #parse to get the vertex and check if it has neighbors
                    vertex = command.split("(")[1].replace(')', '')
                    response = stub.getNeighbors(broker_pb2.Vertex(vert = vertex))
                    print(f"Neighbors of Vertex {vertex}: {response.response}")

                # NEED TO TEST THIS 
                elif command.startswith("has-path"):

                    vertices = command.split("<")[1].split(", ")
                    vd = vertices[-1].replace(">", "")
                    vertices[-1] = vd
                    objects=[broker_pb2.Vertex(vert=v) for v in vertices]
                    response = stub.hasPath(broker_pb2.EdgeList(edges = objects))
                    if(response.tf==True):
                        logging.info(f"Path < {' , '.join(vertices)} > exists:")
                        print(f"Path < {' , '.join(vertices)} > exists:")
                    else:
                        print("Path does not exist.")

                elif command.startswith("get-path"):
                    # parsing vertices of path 
                    vertices = command.split("<")[1].split(", ")
                    vs = vertices[0]
                    vd = vertices[1].replace('>','')

                    response = stub.getPath(broker_pb2.Edge(
                        start = broker_pb2.Vertex(vert = vs),
                        to = broker_pb2.Vertex(vert = vd)
                    ))
                    logging.info(f"Path from {vs} to {vd}: {response.edges}")

                elif command.startswith("get-shortest-path"):
                    vertices = command.split("<")[1].split(", ")
                    vs = vertices[0]
                    vd = vertices[1].replace('>','')

                    response = stub.shortestPath(broker_pb2.Edge(
                        start = broker_pb2.Vertex(vert = vs),
                        to = broker_pb2.Vertex(vert = vd)
                    ))
                    if(response.HasField('edges')):
                        logging.info(f"SHORTEST PATH: ({vs}, {vd}): {response.edges}")

                else:
                    logging.info(f"Unknown command: {command}")

    except FileNotFoundError:
        logging.info(f"ERROR: {input} NOT FOUND.")
    response=stub.Shutdown(broker_pb2.Empty())
    print(response)


def main(): 
    
    if len(sys.argv) != 2:
        logging.error("Incorrect number of arguments. Expected 1 argument for input file.")
        print("Expected args: python3 <script>.py <input_file>")
        sys.exit(1)
    
    graph = Graph()
    
    input_file = sys.argv[1]

    logging.info(f"Finding input file: {input_file}")
    graph=client(input_file)
    


if __name__ == '__main__':
    main()

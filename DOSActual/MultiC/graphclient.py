import sys 
import logging
import grpc
import graph_pb2 # module generated using protobuf
import graph_pb2_grpc # generated using protobuf

''' client parses input file and sends requests to the server '''
def client(input):
    
    # connect to gRPC server on localhost port 50051
    channel = grpc.insecure_channel('localhost:50051')
    stub = graph_pb2_grpc.GraphStub(channel)
    
    stub.ClientConnect(graph_pb2.Empty())

    logging.info(f"Processing file : {input}")

    try:
        #Try to open the file to process
        with open(input, 'r') as infile:
            for line in infile:
                command = line.strip()
                #Check what command the file indicates and call the correct function
                if command.startswith("add-vertex"):
                    #Parse command out of the file
                    vertex = command.split("<")[1].replace('>', '')
                    response = stub.addVertex(graph_pb2.Vertex(vert=vertex))
                    logging.info(f"Add Vertex {vertex}: {response.message}")
                    print(f"Add Vertex {vertex}: {response.message}")
                elif command.startswith("add-edge"):
                    #parsing vertices of edge
                    vertices = command.split("<")[1].split(", ")
                    v0 = vertices[0]
                    v1 = vertices[1].replace('>', '')
                    ()
                    try:
                        #Convert the given vertices into the necessary Edge Object to call gRPC function
                        response = stub.addEdge(graph_pb2.Edge(start=graph_pb2.Vertex(vert=v0),
                                        to=graph_pb2.Vertex(vert=v1)))
                        logging.info(response.edges)
                        print(f"Edge {v0} -> {v1}: {response.edges}")
                    except grpc.RpcError as e:
                        logging.error(f"gRPC failed: {e.details()}")
                        print(f"gRPC failed: {e.details()}")
                elif command.startswith("get-all-vertices"):
                    response = stub.getAllVertices(graph_pb2.Empty()) #No parameters required for function 
                    #Log the response returned by the function
                    logging.info(f"All Vertices of graph: {response.response}") 
                elif command.startswith("get-all-edges"):
                    response = stub.getAllEdges(graph_pb2.Empty()) #No parameters required for function
                    #Log the response returned by the function
                    logging.info(f"All Edges of graph: {response.response}")
                elif command.startswith("remove-vertex"):
                    vertex = command.split("<")[1].replace('>', '')
                    response = stub.removeVertex(graph_pb2.Vertex(vert=vertex))
                    logging.info(f"Remove Vertex {vertex}: {response.message}")
                elif command.startswith("remove-edge"):
                    # parsing vertices of edge 
                    vertices = command.split("<")[1].split(", ")
                    v0 = vertices[0]
                    v1 = vertices[1].replace('>', '')
                    #Convert vertices from file into Edge Object and call function
                    response = stub.removeEdge(graph_pb2.Edge(
                        start = graph_pb2.Vertex(vert = v0),
                        to = graph_pb2.Vertex(vert = v1)
                    ))
                    logging.info(f"Remove Edge <{v0},{v1}>: {response.message}")
                elif command.startswith("has-vertex"):
                    #Parse to get the vertex and check if it exists
                    vertex = command.split("<")[1].replace('>', '')
                    response = stub.hasVertex(graph_pb2.Vertex(vert = vertex))
                    #Access the message returned and compare for results
                    if(response.tf==True):
                        logging.info(f"Vertex {vertex} exists.")
                    else:
                        logging.info(f"Vertex {vertex} exists.")
                elif command.startswith("has-edge"):
                    # parsing vertices of edge 
                    vertices = command.split("<")[1].split(", ")
                    v0 = vertices[0]
                    v1 = vertices[1].replace('>', '')
                    #Convert vertices from file into Edge Object and call function
                    response = stub.hasEdge(graph_pb2.Edge(
                        start = graph_pb2.Vertex(vert = v0),
                        to = graph_pb2.Vertex(vert = v1)
                    ))
                    #Access the message returned and compare for results
                    if(response.tf==True):
                        logging.info(f"Edge <{v0}, {v1}> exists.")
                    else:
                        logging.info(f"Edge <{v0}, {v1}> does not exists.")

                elif command.startswith("get-neighbors"):
                    #parse to get the vertex and check if it has neighbors
                    vertex = command.split("(")[1].replace(')', '')
                    response = stub.getNeighbors(graph_pb2.Vertex(vert = vertex))
                    print(f"Neighbors of Vertex {vertex}: {response.response}")
                elif command.startswith("has-path"):
                    vertices = command.split("<")[1].split(", ")
                    vd = vertices[-1].replace(">", "")
                    vertices[-1] = vd
                    objects=[graph_pb2.Vertex(vert=v) for v in vertices] #Create list of vertices
                    response = stub.hasPath(graph_pb2.EdgeList(edges = objects))
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
                    response = stub.shortestPath(graph_pb2.Edge(
                        start = graph_pb2.Vertex(vert = vs),
                        to = graph_pb2.Vertex(vert = vd)
                    ))
                    logging.info(f"Path from {vs} to {vd}: {response.edges}")
                elif command.startswith("get-shortest-path"):
                    vertices = command.split("<")[1].split(", ")
                    vs = vertices[0]
                    vd = vertices[1].replace('>','')
                    response = stub.shortestPath(graph_pb2.Edge(
                        start = graph_pb2.Vertex(vert = vs),
                        to = graph_pb2.Vertex(vert = vd)
                    ))
                    if(response.HasField('edges')):
                        logging.info(f"SHORTEST PATH: ({vs}, {vd}): {response.edges}")
                else:
                    logging.info(f"Unknown command: {command}")
    except FileNotFoundError:
        logging.info(f"ERROR: {input} NOT FOUND.")
    response=stub.Shutdown(graph_pb2.Empty())
    print(response)


def main(): 
    if len(sys.argv) != 2:
        logging.error("Incorrect number of arguments. Expected 1 argument for input file.")
        print("Expected args: python3 <script>.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    logging.info(f"Finding input file: {input_file}")
    client(input_file)
    
if __name__ == '__main__':
    main()
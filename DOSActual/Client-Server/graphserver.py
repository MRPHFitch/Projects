from concurrent import futures
import logging
import threading
import graph_pb2
import graph_pb2_grpc
import grpc

logging.basicConfig(
    filename = "graph.log",
    filemode = "w",
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.DEBUG
)
class Graph(graph_pb2_grpc.GraphServicer):
    def __init__(self):
        self.graph = {}  # Dictionary to store the graph
        self.stopEvent=stopEvent
        logging.info("Graph is initialized.")
        
    def getAllVertices(self, request, context):
        print(f"All vertices: {self.graph.keys()}")
        vertices=list(self.graph.keys())
        logging.info(f"All vertices: {self.graph.keys()}")
        return graph_pb2.getAllResponse(response=vertices)

    def getAllEdges(self, request, context):
        print(f"All Edges: {self.graph.values()}")
        edges=[]
        for vertex, neighbors in self.graph.items():
            for neighbor in neighbors:
                edges.append(f"{vertex}->{neighbor}")
        logging.info(f"All edges: {self.graph.values()}")
        return graph_pb2.getAllResponse(response=edges)

    def addVertex(self, request, context):
        v=request.vert
        if v in self.graph:
            logging.warning(f"Failed to add vertex {v}, as it already exists.")
            return graph_pb2.Response(message="Fail: Vertex already exists.")
        self.graph[v] = []
        logging.info(f"Vertex {v} is added successfully.")
        return graph_pb2.Response(message="Success: Vertex added.")

    def addEdge(self, request, context):
        v0=request.start.vert
        v1=request.to.vert
        #If a vertex is not in the graph, add it, then create the edge
        if v0 not in self.graph:
            self.addVertex(graph_pb2.Vertex(vert=v0), context)
        if v1 not in self.graph:
            self.addVertex((graph_pb2.Vertex(vert=v1)), context)
        #If the edge already exists, don't add it
        if v1 in self.graph[v0]:
            return graph_pb2.Response(message="Fail: Edge already exists.")
        #Finally, add that edge
        self.graph[v0].append(v1)
        return graph_pb2.Response(message="Success: Edge added.")

    def removeVertex(self, request, context):
        v=request.vert
        if v not in self.graph:
            return graph_pb2.Response(message="Fail: Vertex does not exist.")
        #Check if the given vertex has any neighbors
        nReq=graph_pb2.Vertex(vert=v)
        neighbors=self.getNeighbors(nReq, context)
        #If the point does not have any neighbors, remove the vertex
        if neighbors.response:
            return graph_pb2.Response(message=f"Vertex {v} could not be removed. It had friends.")
        del self.graph[v]
        return graph_pb2.Response(message="Success: Vertex removed")

    def removeEdge(self, request, context):
        v0=request.start.vert
        v1=request.to.vert
        #Make sure the vertices exist before removing
        if v0 not in self.graph or v1 not in self.graph[v0]:
            logging.warning(f"Failed to remove edge ({v0}, {v1}), as it does not exist.")
            return graph_pb2.Response(message="Fail: Edge does not exist.")
        #Remove, log, and return message of success.
        self.graph[v0].remove(v1)
        logging.info(F"Edge ({v0}, {v1}) is removed successfully.")
        return graph_pb2.Response(message="Success: Edge removed.")

    def hasVertex(self, request, context):
        v=request.vert
        if (v in self.graph):
            logging.info(F"Vertex {v} exists.")
            return graph_pb2.YesNo(tf=True)
        else:
            logging.info(f"Vertex {v} does not exist.")
            return graph_pb2.YesNo(tf=False)

    def hasEdge(self, request, context):
        v0=request.start.vert
        v1=request.to.vert
        if(v0 in self.graph and v1 in self.graph[v0]):
            logging.info(f"Edge ({v0}, {v1}) exists.")
            return graph_pb2.YesNo(tf=True)
        else:
            logging.info(f"Edge ({v0}, {v1}) does not exists.")
            return graph_pb2.YesNo(tf=False)

    def getNeighbors(self, request, context):
        point=request.vert
        #If the vertex exists, create a list of all the vertices next to given vertex
        if point in self.graph:
            neighbors = self.graph[point]
            logging.info(f"Neighbors of {point} are: {neighbors}")
            print(f"Neighbors of {point} are: {neighbors}")
        else:
            logging.info(f"No neighbors found from {point}")
            print(f"{point} has no friends. No neighbors found.")
        return graph_pb2.getAllResponse(response=neighbors)

    def hasPath(self, request, context):  
        edges=request.edges     
        
        print("FINDING PATH...")
        vn = edges[-1]
        print("LAST NODE {}".format(vn))

        # iterate through the list 
        # for each vertex (has_vertex), 
        # check if proceeding vertex + corresponding edge exists (has_edge)
        counter = 0
        for node in edges:
            i=0
            
            if(self.hasVertex(node, context) == False):
                logging.warning("Path does not exist.")
                print("PATH DOES NOT EXIST. NODE {} DOES NOT EXIST.".format(node))
                return graph_pb2.YesNo(tf=False)
            
            # prevent out of bounds error
            if(counter < len(edges)-1): 
               
                next_node = edges[counter + 1]
                edge=graph_pb2.Edge(start=graph_pb2.Vertex(vert=node.vert),
                                    to=graph_pb2.Vertex(vert=next_node.vert))
                logging.info(f"Check on edge: {edge.start.vert}, {edge.to.vert}")
                print(f"Checking edge: {edge.start.vert} -> {edge.to.vert}")

                if(self.hasVertex(next_node, context) == False):
                    print("PATH DOES NOT EXIST. PROCEEDING NODE {} DOES NOT EXIST.".format(next_node))
                    return graph_pb2.YesNo(tf=False)

                if(self.hasEdge(edge, context) == False):
                    print("PATH DOES NOT EXIST. EDGE <{},{}> DOES NOT EXIST.".format(node, next_node))
                    return graph_pb2.YesNo(tf=False) 
            else: 
                print("LAST VERTEX {} HAS BEEN REACHED.".format(node))
            counter += 1
            i+=1
        
        print("FOUND PATH: {}".format(edges))
        counter = 0
        return graph_pb2.YesNo(tf=True)

    def getPath(self, request, context):
        #Get all the necessary Objects ready for the other function calls
        vs=request.start.vert
        vd=request.to.vert
        point1=graph_pb2.Vertex(vert=vs)
        point2=graph_pb2.Vertex(vert=vd)
        print("\nGETTING PATH...")
        response1=self.hasVertex(point1,context)
        response2=self.hasVertex(point2,context)
        if(response1.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs))
            return graph_pb2.Multiple(message="Vertex {} does not exist.")
        if(response2.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd))
            return graph_pb2.Multiple(message="Vertex {} does not exist.")

        # storing current vertex and current path in a stack
        # current path will only be initialized with the starting vertex 
        # current vertex is updated with each stack pop 
        stack = [(vs, [vs])]

        while stack:
            
            current, path = stack.pop()

            # final vertex has been reached
            if current == vd:
                print("PATH FOUND: {}".format(path))
                theWay=[graph_pb2.Vertex(vert=v) for v in path]
                return graph_pb2.EdgeList(edges=theWay)

            # find all neighbors of current vertex
            for neighbor in self.graph[current]:
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))

        print("PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd))
        return graph_pb2.Multiple(message="Path does not exist.")

    def shortestPath(self, request, context):
        vs=request.start.vert
        vd=request.to.vert 
        print("\nFINDING SHORTEST PATH...")
        point1=graph_pb2.Vertex(vert=vs)
        point2=graph_pb2.Vertex(vert=vd)
        reply=self.hasVertex(point1,context)
        query=self.hasVertex(point2,context)

        if(reply.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs))
            return graph_pb2.Multiple(message="Vertex {} does not exist")
        if(query.tf == False): 
            print("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd))
            return graph_pb2.Multiple(message="Vertex {} does not exist.")

        queue = [(vs, [vs])] # reference self.get_path()
        visited = set() 

        while queue:
            current, path = queue.pop(0) # first element popped (not last)

            # final vertex has been reached
            if current == vd:
                print("SHORTEST PATH FOUND: {}.".format(path))
                theWay=[graph_pb2.Vertex(vert=v) for v in path]
                return graph_pb2.Multiple(edges=graph_pb2.EdgeList(edges=theWay))


            visited.add(current)

            # find all neighbors of current vertex
            for neighbor in self.graph[current]:

                if (neighbor not in visited) and (neighbor not in path): 
                    queue.append((neighbor, path + [neighbor]))

        print("PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd))
        return graph_pb2.Multiple(message="Path does not exist.")

    def __str__(self):
        return str(self.graph)
    
    def printGraph(self):
        logging.info("PRINTING GRAPH...")
        logging.debug(f"Graph structures : {self.graph}")
        visuals=[]
        for vertex, neighbors in self.graph.items():
            for neighbor in neighbors:
                visuals.append(f"{vertex}->{neighbor}")
        return graph_pb2.getAllResponse(response=visuals)
    
    def Shutdown(self, request, context):
        print("Shutting down now.")
        self.stopEvent.set()
        return(graph_pb2.Response(message="Goodbye."))
        
        
def serve():
    #Set up the server-client connection
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    global stopEvent
    stopEvent=threading.Event()
    graph_pb2_grpc.add_GraphServicer_to_server(Graph(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    stopEvent.wait()
    #Give a 2 second buffer after receiving shutdown message before stopping
    server.stop(2)
    print("I have shutdown. Goodbye.")


if __name__ == '__main__':
    serve()
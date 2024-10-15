import sys
import logging
import json
import time
import threading
import os
start_time = time.time()
commands = 0

#   Command incrementer
def command_increment():
    global commands
    commands += 1

logging.basicConfig(
    filename = "graph.log",
    filemode = "w",
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.DEBUG
)

class Graph:
    def __init__(self):
        command_increment()
        # Dictionary to store the graph
        self.graph = {}
        logging.debug("Graph is initialized.")
        self.output_file = None  
        logging.info("Output file created.")
    
    def open_output_file(self, file_name):
        command_increment()
        self.output_file = open(file_name, 'w')  # Open the file and assign it to the class member

    def write_to_file(self, content):
        command_increment()
        if self.output_file:
            self.output_file.write(content + '\n')

    def close_output_file(self):
        command_increment()
        if self.output_file:
            self.output_file.close()
    
    def getAllV(self):
        command_increment()
        self.write_to_file(f"All vertices: {self.graph.keys()}")
        logging.debug(f"All vertices: {self.graph.keys()}")
        return self.graph.keys
        
    def getAllE(self):
        command_increment()
        self.write_to_file(f"All Edges: {self.graph.values()}")
        logging.debug(f"All edges: {self.graph.values()}")
        return self.graph.values()

    def add_vertex(self, v):
        logging.info(f"Adding vertex : {v}")
        if not v.strip():
            logging.error(f"Failed as vertex name cannot be empty.")
            command_increment()
            return "Fail: Vertex name cannot be empty."
        #If the vertex is already in the graph, don't add it
        if v in self.graph:
            # log:
            logging.warning(f"Failed to add vertex {v}, as it already exists.")
            command_increment()
            return "Fail: Vertex already exists."
        #Otherwise, add the vertex to the graph
        self.graph[v] = []
        logging.info(f"Vertex {v} is added successfully.")
        self.write_to_file(f"Vertex {v} is added successfully.")
        command_increment()
        return "Success: Vertex added."

    def add_edge(self, v0, v1):
        logging.info(f"Adding edge: ({v0}, {v1})")
        #If the vertex is empty, return fail
        if not v0.strip() or not v1.strip():
            logging.debug(f"Failed as vertex name cannot be empty.")
            command_increment()
            return "Fail: Vertex name cannot be empty"
        #If a vertex is not in the graph, add it, then create the edge
        if v0 not in self.graph:
            self.add_vertex(v0)
        if v1 not in self.graph:
            self.add_vertex(v1)
        #If the edge already exists, don't add it
        if v1 in self.graph[v0]:
            logging.warning(f"Failed to add edge ({v0},{v1}), as edge already exists.")
            command_increment()
            return "Fail: Edge already exists."
        #Finally, add that edge
        self.graph[v0].append(v1)
        logging.info(f"Edge ({v0}, {v1}) is added successfully.")
        self.write_to_file(f"Edge ({v0}, {v1}) added")
        command_increment()
        return "Success: Edge added."

    def remove_vertex(self, v):
        logging.info(f"Removing vertex: {v}")
        #If the vertex is empty, return fail
        if not v.strip():
            logging.error(f"Failed as vertex name cannot be empty.")
            command_increment()
            return "Fail: Vertex name cannot be empty"
        
        if v not in self.graph:
            logging.error(f"Failed to remove vertex {v} as it does not exist.")
            command_increment()
            return "Fail: Vertex does not exist."
        #Check if the given vertex has any neighbors
        neighbors=self.getNeighbors(v)
        #If the point does not have any neighbors, remove the vertex
        if len(neighbors) == 0:
            self.graph.pop(v)
            for key in self.graph:
                self.graph[key] = [i for i in self.graph[key] if i != v]
            
            logging.info(f"Vertex {v} is removed successfully.")
            self.write_to_file(f"Vertex {v} removed.")   
            command_increment()         
            return "Success: Vertex removed."
        #If the point has neighbors, it cannot be removed
        else:
            logging.warning(f"Vertex {v} could not be removed.")
            command_increment()
            return "Fail: Vertex could not be removed. It had friends."

    def remove_edge(self, v0, v1):
        logging.info(f"Removing edge: ({v0}, {v1})")
        #If the edge doesn't exist, you can't remove it
        if v0 not in self.graph or v1 not in self.graph[v0]:
            logging.error(f"Failed to remove edge ({v0}, {v1}), as it does not exist.")
            command_increment()
            return "Fail: Edge does not exist."
        self.graph[v0].remove(v1)
        logging.info(F"Edge ({v0}, {v1}) is removed successfully.")
        self.write_to_file(f"Edge ({v0}, {v1}) removed successfully.")
        return "Success: Edge removed."

    def has_vertex(self, v):
        logging.info(f"Looking for vertex {v})")
        if (v in self.graph):
            logging.info(f"Vertex {v} is found.")
            self.write_to_file(f"Vertex {v} exists.")
            command_increment()
            return "Success: Vertex {} found.".format(v)
        
        self.write_to_file(f"Vertex {v} does not exisit.")        
        logging.warning(f"Vertex {v} does not exist.")
        command_increment()
        return "Fail: Vertex {} does not exist.".format(v)

    def has_edge(self, v0, v1):
        logging.info(f"Looking for edge ({v0}, {v1})")
        if(v0 in self.graph and v1 in self.graph[v0]):
            logging.info("Edge ({}, {}) is found.".format(v0,v1))
            self.write_to_file(f"Edge ({v0}, {v1}) exists.")
            command_increment()
            return "Success: Edge ({},{}) found.".format(v0,v1)
        
        self.write_to_file(f"Edge ({v0}, {v1}) does not exist.")
        logging.warning("Edge ({}, {}) does not exists.".format(v0,v1))
        command_increment()
        return "Fail: Edge ({},{}) does not exist.".format(v0,v1)
        
    def getNeighbors(self, node):
        command_increment()
        logging.info(f"Getting neighbors of {node})")
        #If node is in graph return neighbors
        if node in self.graph:
            neighbors=self.graph[node]
            self.write_to_file(f"Neighbors of {node} are: {neighbors}")
            logging.debug(f"Neighbors of {node} are: {neighbors}")
            return neighbors
        
        #If node not in graph return empty array
        else:
            self.write_to_file(f"{node} has no friends. No neighbors found.")
            logging.warning(f"No neighbors found from {node}")
            return []

    def has_path(self, edges):       
        logging.debug(f"Finding path for {edges}")
        """
        iterate through the list 
        for each vertex (has_vertex), 
        check if proceeding vertex + corresponding edge exists (has_edge)
        """
        counter = 0
        for node in edges:
            
            if(self.has_vertex(node) == "Fail: Vertex {} does not exist.".format(node)): 
                self.write_to_file(f"Path does not exist. Node {node} does not exist")
                logging.error("PATH DOES NOT EXIST. NODE {} DOES NOT EXIST.".format(node))
                command_increment()
                return "PATH DOES NOT EXIST. NODE {} DOES NOT EXIST.".format(node)
            
            # prevent out of bounds error
            if(counter < len(edges)-1): 
               
                next_node = edges[counter + 1]

                if(self.has_vertex(next_node) == "Fail: Vertex {} does not exist.".format(next_node)):
                    self.write_to_file(f"PATH DOES NOT EXIST. PROCEEDING NODE {next_node} DOES NOT EXIST.")
                    logging.error("PATH DOES NOT EXIST. PROCEEDING NODE {} DOES NOT EXIST.".format(next_node))
                    command_increment()
                    return "PATH DOES NOT EXIST. PROCEEDING NODE {} DOES NOT EXIST.".format(next_node)

                if(self.has_edge(node, next_node) == "Fail: Edge ({},{}) does not exist.".format(node, next_node)):
                    self.write_to_file(f"PATH DOES NOT EXIST. EDGE <{node}, {next_node}> DOES NOT EXIST.")
                    logging.info("PATH DOES NOT EXIST. EDGE <{},{}> DOES NOT EXIST.".format(node, next_node))
                    command_increment()
                    return "PATH DOES NOT EXIST. EDGE <{},{}> DOES NOT EXIST.".format(node, next_node) 
                
            else: 
                logging.debug("LAST VERTEX {} HAS BEEN REACHED.".format(node))
                command_increment()
                print("LAST VERTEX {} HAS BEEN REACHED.".format(node))

            counter += 1

        self.write_to_file(f"Found path {edges}.")
        logging.info("FOUND PATH: {}".format(edges))
        command_increment()
        return "FOUND PATH: {}".format(edges)

    def get_path(self, vs, vd):
        logging.info("\nGETTING PATH ({},{})...".format(vs, vd))
        if(self.has_vertex(vs) == "Fail: Vertex {} does not exist.".format(vs)): 
            self.write_to_file(f"NO PATH FOUND. VERTEX {vs} DOES NOT EXIST.")
            logging.error("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs))
            command_increment()
            return "NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs)
        
        if(self.has_vertex(vd) == "Fail: Vertex {} does not exist.".format(vd)):
            self.write_to_file(f"NO PATH FOUND. VERTEX {vd} DOES NOT EXIST.")
            logging.error("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd))
            command_increment()
            return "NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd)

        """
        storing current vertex and current path in a stack
        current path will only be initialized with the starting vertex 
        current vertex is updated with each stack pop 
        """
        stack = [(vs, [vs])]

        while stack:
            
            current, path = stack.pop()

            # final vertex has been reached
            if current == vd:
                self.write_to_file(f"Path found: {path}")
                logging.info("PATH FOUND: {}".format(path))
                command_increment()
                return "PATH FOUND: {}".format(path)

            # find all neighbors of current vertex
            for neighbor in self.graph[current]:
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))
                    #command_increment()

        self.write_to_file(f"Path <{vs}, ..., {vd}> does not exist")
        logging.warning("PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd))
        command_increment()
        return "PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd)


    def get_shortest_path(self, vs, vd): 
        logging.debug(f"Finding shortest path for {vs} ... {vd}")
        
        if(self.has_vertex(vs) == "Fail: Vertex {} does not exist.".format(vs)): 
            self.write_to_file(f"No path found. Vertex {vs} does not exist")
            logging.error("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs))
            command_increment()
            return "Fail: NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vs)
        
        if(self.has_vertex(vd) == "Fail: Vertex {} does not exist.".format(vd)): 
            self.write_to_file(f"No path found. Vertex {vd} does not exist")
            logging.error("NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd))
            command_increment()
            return "Fail: NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd)

        queue = [(vs, [vs])] # reference self.get_path()
        visited = set() 

        while queue:
            current, path = queue.pop(0) # first element popped (not last)

            # final vertex has been reached
            if current == vd:
                self.write_to_file(f"Shortest path found: {path}")
                logging.info("SHORTEST PATH FOUND: {}.".format(path))
                command_increment()
                return "Success: SHORTEST PATH FOUND: {}.".format(path)

            visited.add(current)

            # find all neighbors of current vertex
            for neighbor in self.graph[current]:

                if (neighbor not in visited) and (neighbor not in path): 
                    queue.append((neighbor, path + [neighbor]))
                    #command_increment()

        self.write_to_file(f"Path {vs} ... {vd} does not exist")
        logging.warning("PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd))
        command_increment()
        return "Fail: PATH <{}, ..., {}> DOES NOT EXIST.".format(vs, vd)

    def __str__(self):
        command_increment()
        return str(self.graph)
    
    #Print out the graph semi-aesthetically
    def print_graph(self):
        command_increment()
        logging.debug("PRINTING GRAPH...")
        logging.debug(f"Graph structures : {self.graph}")
        self.write_to_file("Graph:")
        self.write_to_file(json.dumps(self.graph, indent=4))
            
    def process_file(self, input_file):
        #Get the input file ready to read
        logging.info(f"Processing file : {input_file}")
        try:
            with open(input_file) as infile:
                for line in infile:
                    command = line.strip()
                    logging.debug(f"Processing command: {command}")
                    if command.startswith("add-vertex"):
                        vertex = command.split("<")[1].replace('>','')
                        self.add_vertex(vertex)

                    elif command.startswith("add-edge"):
                        # parsing vertices of edge
                        vertices = command.split("<")[1].split(", ")
                        v0 = vertices[0]
                        v1 = vertices[1].replace('>','')
                        self.add_edge(v0, v1)

                    elif command.startswith("get-all-vertices"):
                        #Print out all the keys in the dictionary
                        self.getAllV()
                    
                    elif command.startswith("get-all-edges"):
                        #Print out all of the edges in the dictionary
                        self.getAllE()

                    elif command.startswith("remove-vertex"):
                        vertex = command.split("<")[1].replace('>','')
                        self.remove_vertex(vertex)

                    elif command.startswith("remove-edge"):
                        # parsing vertices of edge 
                        vertices = command.split("<")[1].split(", ")
                        v0 = vertices[0]
                        v1 = vertices[1].replace('>','')
                        self.remove_edge(v0, v1)

                    elif command.startswith("has-vertex"):
                        #Parse to get the vertex and check if it exists
                        vertex = command.split("<")[1].replace('>','')
                        self.has_vertex(vertex)

                    elif command.startswith("has-edge"):
                        # parsing vertices of edge 
                        vertices = command.split("<")[1].split(", ")
                        v0 = vertices[0]
                        v1 = vertices[1].replace('>','')
                        self.has_edge(v0, v1)
                    
                    elif command.startswith("get-neighbors"):
                        #parse to get the vertex and check if it has neighbors
                        point=command.split("(")[1].replace(')','')
                        self.getNeighbors(point)

                    elif command.startswith("has-path"): 
                        vertices = command.split("<")[1].split(", ")
                        vd = vertices[-1].replace(">", "")
                        vertices[-1] = vd  
                        self.has_path(vertices)                 
                    
                    elif command.startswith("get-path"): 
                        # parsing vertices of path 
                        vertices = command.split("<")[1].split(", ")
                        vs = vertices[0]
                        vd = vertices[1].replace('>','')
                        self.get_path(vs, vd)

                    elif command.startswith("get-shortest-path"):
                        # parsing vertices of path 
                        vertices = command.split("<")[1].split(", ")
                        vs = vertices[0]
                        vd = vertices[1].replace('>','')
                        self.get_shortest_path(vs, vd)

                    else:
                        self.write_to_file("INVALID COMMAND.")
                        logging.error(f"Invalid command")
        except FileNotFoundError:
            logging.error(f"Error {input_file} not found.")
            self.write_to_file(f"File has not been found.")

        except Exception as e:
            logging.exception(f"Error processing file {input_file}: {e}")
            self.write_to_file(f"An error has occured {e}")

#   Records throughput in 0.005 intervals in a seperate thread.
def printit():
    global commands
    input_file = sys.argv[1]
    threading.Timer(0.005, printit).start()
    elapsed_time = time.time() - start_time
    with open(f"{input_file}_throughput.csv", "a") as file:
        file.write(f"{commands},{elapsed_time}\n")
        commands = 0

def main(): 
    if len(sys.argv) != 3:
        logging.error("Incorrect number of arguments. Expected 1 argument for input file.")
        print("Usage: python script.py <input_file> outputFileName.txt")
        sys.exit(1)
    graph = Graph()

    input_file = sys.argv[1]
    logging.debug(f"FINDING INPUT FILE WITH FILENAME: " + input_file)

    #   Start throughput measurer
    if os.path.isfile(f"{input_file}_throughput.csv"):
        os.remove(f"{input_file}_throughput.csv")
    timer_thread = threading.Timer(0.005, printit)
    timer_thread.daemon = True  # Make the timer a daemon thread
    timer_thread.start()

    output_file = sys.argv[2]
    graph.open_output_file(output_file)
    logging.info(f"Opening output file: {output_file}")

    graph.process_file(input_file)
    graph.close_output_file()

    #   Ensure threads finishes
    time.sleep(0.005)
    timer_thread.join()

    #   Record end time
    end_time = time.time()

    #   Write Additional info
    if os.path.isfile(f"{input_file}_benchmark.csv"):
        os.remove(f"{input_file}_benchmark.csv")
    with open(f"{input_file}_benchmark.csv", "w") as file:
        file.write(f"BENCHMARK \n")
        file.write(f"Start Time: {start_time}\n")
        file.write(f"End Time: {end_time}\n")
        file.write(f"Latency: {end_time - start_time}\n")

if __name__ == "__main__":
    main()
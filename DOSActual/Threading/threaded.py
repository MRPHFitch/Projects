import sys
import logging
import threading
import json
sems=threading.Semaphore()
import time
import os

sems=threading.Semaphore()
start_time = time.time()
commands = 0

# Command incrementer
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
        self.graph = {}  # Dictionary to store the graph
        logging.info("Graph is initialized.")
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
        if self.output_file:
            self.output_file.close()
        
    def getAllV(self):
        self.write_to_file(f"All vertices: {self.graph.keys()}")
        logging.info(f"All vertices: {self.graph.keys()}")
        command_increment()
        return self.graph.keys()

    def getAllE(self):
        self.write_to_file(f"All Edges: {self.graph.values()}")
        logging.info(f"All edges: {self.graph.values()}")
        command_increment()
        return self.graph.values()

    def add_vertex(self, v):
        #Lock down access to all functions, add the vertex, then release the lock.
        sems.acquire()
        logging.info(f"Adding vertex : {v}")
        if not v.strip():
            logging.warning(f"Cannot add empty vertex.")
            sems.release()
            command_increment()
            return "Fail: Vertex name cannot be empty."
        
        if v in self.graph:
            logging.warning(f"Failed to add vertex {v}, as it already exists.")
            sems.release()
            command_increment()
            return "Fail: Vertex already exists."

        self.graph[v] = []
        self.write_to_file(f"Vertex {v} is added successfully.")
        logging.info(f"Vertex {v} is added successfully.")
        sems.release()
        command_increment()
        return "Success: Vertex added."

    def add_edge(self, v0, v1):
        logging.info(f"Adding edge: ({v0}, {v1})")
        #If a vertex is not in the graph, add it, then create the edge
        if v0 not in self.graph:
            if(self.add_vertex(v0) == "Fail: Vertex name cannot be empty."):
                logging.warning("Cannot add empty vertex.")
                command_increment()
                return "Fail: Vertex name cannot be empty."
            
        #Make sure that an actual vertex was sent    
        if v1 not in self.graph:
            if(self.add_vertex(v1) == "Fail: Vertex name cannot be empty."):
                logging.warning("Cannot add empty vertex.")
                command_increment()
                return "Fail: Vertex name cannot be empty."
        #Can't add an Edge that already exists    
        if v1 in self.graph[v0]:
            logging.warning("Edge already exists.")
            command_increment()
            return "Fail: Edge already exists."

        sems.acquire()
        self.graph[v0].append(v1) # add edge
        logging.info(f"Edge ({v0}, {v1}) added")
        self.write_to_file(f"Edge ({v0}, {v1}) added")
        sems.release()
        command_increment()
        return "Success: Edge added."

    def remove_vertex(self, v):
        logging.info(f"Removing vertex: {v}")
        if not v.strip():
            logging.warning("Cannot remove empty vertex")
            command_increment()
            return "Fail: Vertex name cannot be empty"
        
        if v not in self.graph:
            logging.warning("Vertex does not exist")
            command_increment()
            return "Fail: Vertex does not exist."
        
        neighbors=self.getNeighbors(v)
        #If the point does not have any neighbors, remove the vertex
        sems.acquire()
        if not neighbors:
            self.graph.pop(v)
            for key in self.graph:
                self.graph[key] = [i for i in self.graph[key] if i != v]

            logging.info(f"Vertex {v} removed.")
            self.write_to_file(f"Vertex {v} removed.")
            sems.release()
            command_increment()
            return f"Success: Vertex {v} removed."
        
        logging.warning("Cannot remove a vertex with neighbors")
        sems.release()
        command_increment()
        return f"Fail: Vertex {v} could not be removed. It had friends."

    def remove_edge(self, v0, v1):
        logging.info(f"Removing edge: ({v0}, {v1})")
        sems.acquire()
        #Can only remove what already exists
        if v0 not in self.graph or v1 not in self.graph[v0]:
            logging.warning(f"Failed to remove edge ({v0}, {v1}), as it does not exist.")
            sems.release()
            command_increment()
            return "Fail: Edge does not exist."
        #Since it exists, remove it
        self.graph[v0].remove(v1)
        logging.info(f"Edge ({v0}, {v1}) is removed successfully.")
        self.write_to_file(f"Edge ({v0}, {v1}) removed successfully.")
        sems.release()
        command_increment()
        return "Success: Edge removed."

    def has_vertex(self, v):
        logging.info(f"Looking for vertex {v})")
        sems.acquire()
        if (v in self.graph):
            logging.info(f"Vertex {v} exists.")
            self.write_to_file(f"Vertex {v} exists.")
            sems.release()
            command_increment()
            return f"Success: Vertex {v} found."
        
        logging.info(f"Vertex {v} does not exist.")
        self.write_to_file(f"Vertex {v} does not exisit.")
        sems.release()
        command_increment()
        return f"Fail: Vertex {v} does not exist."

    def has_edge(self, v0, v1):
        logging.info(f"Looking for edge ({v0}, {v1})")
        sems.acquire
        if(v0 in self.graph and v1 in self.graph[v0]): 
            logging.info(f"Edge ({v0}, {v1}) exists.")
            self.write_to_file(f"Edge ({v0}, {v1}) exists.")
            sems.release()
            command_increment()
            return f"Success: Edge ({v0}, {v1}) found."
    
        logging.info(f"Edge ({v0}, {v1}) does not exists.")
        self.write_to_file(f"Edge ({v0}, {v1}) does not exist.")
        sems.release()
        command_increment()
        return f"Fail: Edge ({v0}, {v1}) does not exist."

    def getNeighbors(self, point):
        logging.info(f"Getting neighbors of {point})")
        sems.acquire()
        #If the point has any next to it, add it to a list
        if point in self.graph:
            neighbors = self.graph[point]
            logging.info(f"Neighbors of {point} are: {neighbors}")
            self.write_to_file(f"Neighbors of {point} are: {neighbors}")
        else:
            logging.info(f"No neighbors found from {point}")
            self.write_to_file(f"{point} has no friends. No neighbors found.")
       
        command_increment()
        sems.release()
        return neighbors

    def has_path(self, edges): 
        sems.acquire()      
        logging.info(f"Finding path for {edges}")

        # check if proceeding vertex + corresponding edge exists (has_edge)
        counter = 0
        for node in edges:
            if(self.has_vertex(node) == f"Fail: Vertex {node} does not exist."): 
                logging.warning(f"Path does not exist. Node {node} does not exist")
                self.write_to_file(f"Path does not exist. Node {node} does not exist")
                sems.release()
                command_increment()
                return f"PATH DOES NOT EXIST. NODE {node} DOES NOT EXIST."
                       
            # prevent out of bounds error
            if(counter < len(edges)-1): 
               
                next_node = edges[counter + 1]
                if(self.has_vertex(next_node) == f"Fail: Vertex {next_node} does not exist."):
                    logging.warning(f"PATH DOES NOT EXIST. PROCEEDING NODE {next_node} DOES NOT EXIST.")
                    self.write_to_file(f"PATH DOES NOT EXIST. PROCEEDING NODE {next_node} DOES NOT EXIST.")
                    sems.release()
                    command_increment()
                    return f"PATH DOES NOT EXIST. PROCEEDING NODE {next_node} DOES NOT EXIST."
                
                if(self.has_edge(node, next_node) == f"Fail: Edge ({node}, {next_node}) does not exist."):
                    logging.warning(f"PATH DOES NOT EXIST. EDGE <{node}, {next_node}> DOES NOT EXIST.")
                    self.write_to_file(f"PATH DOES NOT EXIST. EDGE <{node}, {next_node}> DOES NOT EXIST.")
                    sems.release()
                    command_increment()
                    return f"PATH DOES NOT EXIST. EDGE <{node}, {next_node}> DOES NOT EXIST."
            else: 
                command_increment()
                logging.info(f"LAST VERTEX {node} HAS BEEN REACHED.")
            counter += 1
        
        logging.info(f"Found path {edges}.")
        self.write_to_file(f"Found path {edges}.")
        sems.release()
        command_increment()
        return "FOUND PATH: {}".format(edges)

    def get_path(self, vs, vd):
        sems.acquire()
        logging.info(f"Getting path: {vs} ... {vd}.")

        if(self.has_vertex(vs) == f"Fail: Vertex {vs} does not exist."):
            logging.info(f"No path found, Vertex {vs} does not exist.") 
            self.write_to_file(f"NO PATH FOUND. VERTEX {vs} DOES NOT EXIST.")
            sems.release()
            command_increment()
            return f"NO PATH FOUND. VERTEX {vs} DOES NOT EXIST."
        
        if(self.has_vertex(vd) == f"Fail: Vertex {vd} does not exist."): 
            logging.info(f"No path found. Vertex {vd} does not exist")
            self.write_to_file(f"NO PATH FOUND. VERTEX {vd} DOES NOT EXIST.")
            sems.release()
            command_increment()
            return "NO PATH FOUND. VERTEX {} DOES NOT EXIST.".format(vd)

        # storing current vertex and current path in a stack
        # current path will only be initialized with the starting vertex 
        # current vertex is updated with each stack pop 
        stack = [(vs, [vs])]
        while stack:
            
            current, path = stack.pop()

            if current == vd:
                logging.info(f"Path found: {path}")
                self.write_to_file(f"Path found: {path}")
                sems.release()
                command_increment()
                return f"PATH FOUND: {path}"

            for neighbor in self.graph[current]:
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))

        logging.warning(f"Path <{vs}, ..., {vd}> does not exist")
        self.write_to_file(f"Path <{vs}, ..., {vd}> does not exist")
        sems.release()
        command_increment()
        return f"PATH <{vs}, ..., {vd}> DOES NOT EXIST."

    def get_shortest_path(self, vs, vd): 
        logging.info(f"Finding shortest path for {vs} ... {vd}")
        sems.acquire()

        if(self.has_vertex(vs) == f"Fail: Vertex {vs} does not exist."): 
            logging.warning(f"No path found. Vertex {vs} does not exist")
            self.write_to_file(f"No path found. Vertex {vs} does not exist")
            sems.release()
            command_increment()
            return f"Fail: NO PATH FOUND. VERTEX {vs} DOES NOT EXIST."
        
        if(self.has_vertex(vd) == f"Fail: Vertex {vd} does not exist."): 
            logging.warning(f"No path found. Vertex {vd} does not exist")
            self.write_to_file(f"No path found. Vertex {vd} does not exist")
            sems.release()
            command_increment()
            return f"Fail: NO PATH FOUND. VERTEX {vd} DOES NOT EXIST."

        queue = [(vs, [vs])] # reference self.get_path()
        visited = set() 

        while queue:
            current, path = queue.pop(0) 

            if current == vd:
                logging.info(f"Shortest path found: {path}")
                self.write_to_file(f"Shortest path found: {path}")
                sems.release()
                command_increment()
                return f"Success: SHORTEST PATH FOUND: {path}."

            visited.add(current)

            # find all neighbors of current vertex
            for neighbor in self.graph[current]:

                if (neighbor not in visited) and (neighbor not in path): 
                    queue.append((neighbor, path + [neighbor]))

        logging.warning(f"Path {vs} ... {vd} does not exist")
        self.write_to_file(f"Path {vs} ... {vd} does not exist")
        sems.release()
        command_increment()
        return f"Fail: PATH <{vs}, ..., {vd}> DOES NOT EXIST."

    def __str__(self):
        command_increment()
        return str(self.graph)
    
    #Print the graph out in a semi-aesthetically way
    def print_graph(self):
        logging.info("PRINTING GRAPH...")
        logging.debug(f"Graph structures : {self.graph}")
        self.write_to_file("Graph:")
        command_increment()
        self.write_to_file(json.dumps(self.graph, indent=4))
            
    def process_file(self, input_file):
        logging.info(f"Processing file : {input_file}")
        #Parse the file to get the appropriate commands out, then call that function using a thread
        try:
            with open(input_file) as inFile:
                threads=[]
                for line in inFile:
                    command = line.strip()
                    logging.debug(f"Processing command: {command}")
                    if command.startswith("add-vertex"):
                        vertex = command.split("<")[1].replace('>','')
                        thread1=threading.Thread(target=self.add_vertex, args=(vertex,))
                        thread1.start()
                        threads.append(thread1)

                    elif command.startswith("add-edge"):
                        vertices = command.split("<")[1].split(", ")
                        v0 = vertices[0]
                        v1 = vertices[1].replace('>','')
                        thread2=threading.Thread(target=self.add_edge, args=(v0, v1))
                        thread2.start()
                        threads.append(thread2)

                    elif command.startswith("get-all-vertices"):
                        self.getAllV()

                    elif command.startswith("get-all-edges"):
                        self.getAllE()

                    elif command.startswith("remove-vertex"):
                        vertex = command.split("<")[1].replace('>','')
                        thread3=threading.Thread(target=self.remove_vertex, args=(vertex,))
                        thread3.start()
                        threads.append(thread3)

                    elif command.startswith("remove-edge"):
                        vertices = command.split("<")[1].split(", ")
                        v0 = vertices[0]
                        v1 = vertices[1].replace('>','')
                        thread4=threading.Thread(target=self.remove_edge, args=(v0, v1))
                        thread4.start()
                        threads.append(thread4)

                    elif command.startswith("has-vertex"):
                        vertex = command.split("<")[1].replace('>','')
                        thread5=threading.Thread(target=self.has_vertex, args=(vertex,))
                        thread5.start()
                        threads.append(thread5)

                    elif command.startswith("has-edge"):
                        vertices = command.split("<")[1].split(", ")
                        v0 = vertices[0]
                        v1 = vertices[1].replace('>','')
                        thread6=threading.Thread(target=self.has_edge, args=(v0, v1))
                        thread6.start()
                        threads.append(thread6)

                    elif command.startswith("get-neighbors"):
                        point= command.split("(")[1].replace(')','')
                        thread7=threading.Thread(target=self.getNeighbors, args=(point,))
                        thread7.start()
                        threads.append(thread7)

                    elif command.startswith("has-path"): 
                        vertices = command.split("<")[1].split(", ")
                        vd = vertices[-1].replace(">", "")
                        vertices[-1] = vd                   
                        thread8=threading.Thread(target=self.has_path, args=(vertices,))
                        thread8.start()
                        threads.append(thread8)

                    elif command.startswith("get-path"):
                        vertices = command.split("<")[1].split(", ")
                        vs = vertices[0]
                        vd = vertices[1].replace('>','')
                        thread9=threading.Thread(target=self.get_path, args=(vs, vd))
                        thread9.start()
                        threads.append(thread9)

                    elif command.startswith("get-shortest-path"):
                        vertices = command.split("<")[1].split(", ")
                        vs = vertices[0]
                        vd = vertices[1].replace('>','')
                        thread10=threading.Thread(target=self.get_shortest_path, args=(vs, vd))
                        thread10.start()
                        threads.append(thread10)

                    else:
                        logging.error(f"Invalid command: {command}")
                        self.write_to_file("INVALID COMMAND.")

                for thread in threads:
                    thread.join()
        #Tell user if the file couldn't be found or there was an error with the file.
        except FileNotFoundError:
            logging.error(f"Error {input_file} not found.")
            self.write_to_file("File has not been found.")

        except Exception as e:
            logging.error(f"Error processing file {input_file}: {e}") 
            self.write_to_file(f"An error has occurred: {e}")

    # Records throughput in 0.001 intervals in a separate thread.
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
    logging.info(f"Finding input file: {input_file}")

    # Start throughput measurer
    if os.path.isfile(f"{input_file}_throughput.csv"):
        os.remove(f"{input_file}_throughput.csv")
    timer_thread = threading.Timer(0.005, printit)
    timer_thread.daemon = True  # Make the timer a daemon thread
    timer_thread.start()

    output_file = sys.argv[2]
    graph.open_output_file(output_file)
    logging.info(f"Opening output file: {output_file}")

    graph.process_file(input_file)

    graph.print_graph()

    # Ensure threads finishes
    time.sleep(0.005)
    timer_thread.join()

    # Record end time
    end_time = time.time()

    # Write Additional info
    if os.path.isfile(f"{input_file}_benchmark.csv"):
        os.remove(f"{input_file}_benchmark.csv")
    with open(f"{input_file}_benchmark.csv", "w") as file:
        file.write(f"BENCHMARK \n")
        file.write(f"Start Time: {start_time}\n")
        file.write(f"End Time: {end_time}\n")
        file.write(f"Latency: {end_time - start_time}\n")
    graph.close_output_file()

if __name__ == "__main__":
    main()
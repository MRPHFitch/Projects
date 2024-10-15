import pytest
from program1 import Graph  

def test_add_vertex():
    g = Graph()
    assert g.add_vertex("A") == "Success: Vertex added."
    assert g.add_vertex("A") == "Fail: Vertex already exists."
    assert g.add_vertex(" ") == "Fail: Vertex name cannot be empty."

def test_add_edge():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    assert g.add_edge(" ", "E") == "Fail: Vertex name cannot be empty"
    assert g.add_edge("E", " ") == "Fail: Vertex name cannot be empty"
    assert g.add_edge("A", "B") == "Success: Edge added."
    assert g.add_edge("A", "B") == "Fail: Edge already exists."
    assert g.add_edge("A", "C") == "Success: Edge added."
    assert g.add_edge("D", "B") == "Success: Edge added."

def test_remove_vertex():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")
    assert g.remove_vertex(" ") == "Fail: Vertex name cannot be empty"
    assert g.remove_vertex("C") == "Fail: Vertex does not exist."
    assert g.remove_vertex("A") == "Fail: Vertex could not be removed. It had friends."
    assert g.remove_vertex("B") == "Success: Vertex removed."
    assert g.has_edge("A", "B") == "Fail: Edge (A,B) does not exist."
    assert g.remove_vertex("A") == "Success: Vertex removed."
    assert g.has_vertex("B") == "Fail: Vertex B does not exist."
    assert g.has_vertex("A") == "Fail: Vertex A does not exist."

def test_remove_edge():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")
    assert g.add_edge(" ", "E") == "Fail: Vertex name cannot be empty"
    assert g.add_edge("E", " ") == "Fail: Vertex name cannot be empty"
    assert g.remove_edge("A", "B") == "Success: Edge removed."
    assert g.remove_edge("A", "B") == "Fail: Edge does not exist."
    assert g.has_edge("A", "B") == "Fail: Edge (A,B) does not exist."

def test_has_vertex():
    g = Graph()
    g.add_vertex("A")
    assert g.has_vertex("A") == "Success: Vertex A found."
    assert g.has_vertex("B") == "Fail: Vertex B does not exist."

def test_has_edge():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")
    assert g.has_edge("A", "B") == "Success: Edge (A,B) found."
    assert g.has_edge("B", "A") == "Fail: Edge (B,A) does not exist."
    assert g.has_edge("A", "C") == "Fail: Edge (A,C) does not exist."

def test_get_neighbors():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_edge("A","B")
    g.add_edge("A","C")
    
    assert g.getNeighbors("A") == ["B", "C"]
    assert g.getNeighbors("B") == []
    assert g.getNeighbors("C") == []

def test_has_path():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    g.add_edge("A","B")
    g.add_edge("B","C")
    g.add_edge("C","D")
    assert g.has_path("ABCD") == "FOUND PATH: ABCD"
    assert g.has_path("DABC") == "PATH DOES NOT EXIST. EDGE <D,A> DOES NOT EXIST."

def test_get_path():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    g.add_vertex("F")
    g.add_edge("A","B")
    g.add_edge("A","C")
    g.add_edge("A","D")
    g.add_edge("B","D")
    g.add_edge("B","F")
    assert g.get_path("A", "D") == "PATH FOUND: ['A', 'D']"
    assert g.get_path("A", "1") == "NO PATH FOUND. VERTEX 1 DOES NOT EXIST."
    assert g.get_path("G", "A") == "NO PATH FOUND. VERTEX G DOES NOT EXIST."
    assert g.get_path("D", "A") == "PATH <D, ..., A> DOES NOT EXIST."
    assert g.get_path("A", "F") == "PATH FOUND: ['A', 'B', 'F']"
    
def test_get__shortest_path():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    g.add_vertex("F")
    g.add_edge("A","B")
    g.add_edge("A","C")
    g.add_edge("A","D")
    g.add_edge("B","D")
    g.add_edge("B","F")
    assert g.get_shortest_path("A", "D") == "Success: SHORTEST PATH FOUND: ['A', 'D']."
    assert g.get_shortest_path("A", "E") == "Fail: NO PATH FOUND. VERTEX E DOES NOT EXIST."
    assert g.get_shortest_path("D", "A") == "Fail: PATH <D, ..., A> DOES NOT EXIST."
    assert g.get_shortest_path("A", "F") == "Success: SHORTEST PATH FOUND: ['A', 'B', 'F']."

if __name__ == "__main__":
    pytest.main()

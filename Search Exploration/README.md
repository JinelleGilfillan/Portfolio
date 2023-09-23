# Search

Search is an integral part of AI. It helps in problem solving across a wide variety of domains where a solution isn’t immediately clear.  This project implements several graph search algorithms with the goal of solving bi-directional and tri-directional search.

### The Files

1. **__submission.py__**: Where the implentation is for _PriorityQueue_, _Breadth First Search_, _Uniform Cost Search_, _A* Search_, _Bi-directional Search_, Tri-directional Search_
2. **_search_submission_tests.py_**: Sample tests to validate the searches locally.
3. **_search_unit_tests.py_**: More detailed tests that run searches from all possible pairs of nodes in the graph
4. **_search_submission_tests_grid.py_**: Tests searches on uniform grid and highlights path and explored nodes.
5. **_romania_graph.pickle_**: Serialized graph files for Romania.
6. **_atlanta_osm.pickle_**: Serialized graph files for Atlanta (optional for robust testing for Race!).
7. **_explorable_graph.py_**: A wrapper around `networkx` that tracks explored nodes. **FOR DEBUGGING ONLY**
9. **_visualize_graph.py_**: Module to visualize search results. 
10. **_osm2networkx.py_**: Module used by visualize graph to read OSM networks. 


#### A note on visualizing results for the Atlanta graph:

The Atlanta graph is too big to display within a Python window like Romania. As a result, when you run the bidirectional tests in **_search_submission_tests.py_**, it generates a JSON file in the GeoJSON format. To see the graph, you can upload it to a private GitHub Gist or use [this](http://geojson.io/) site.
If you want to see how **_visualize_graph.py_** is used, take a look at the class TestBidirectionalSearch in **_search_submission_tests.py_**

## The Goal

The goal of this project is to implement several informed search algorithms that will calculate a driving route between two points in Romania with a minimal time and space cost.

I used an undirected network representing a map of Romania (and an optional Atlanta graph used for the Race!).

#### Option 1: Bidirectional uniform-cost search

Implement bidirectional uniform-cost search. This requires starting the search at both the start and end states.

`bidirectional_ucs()` returns the path from the start node to the goal node (as a list of nodes).

#### Option 2: Bidirectional A* search

Implement bidirectional A* search.

`bidirectional_a_star()` returns the path from the start node to the goal node, as a list of nodes.

#### Option 3: Tridirectional UCS search

Implement tridirectional search in the naive way: starting from each goal node, perform a uniform-cost search and keep
expanding until two of the three searches meet. This should be one continuous path that connects all three nodes.

`tridirectional_search()` returns a path between all three nodes. 

#### Option 4: Upgraded Tridirectional search

Tridirectional search implemented in such a way as to consistently improve on the
performance of the previous implementation. This means consistently exploring fewer nodes during the search in order
to reduce runtime. 

`tridirectional_upgraded()` returns a path between all three nodes.
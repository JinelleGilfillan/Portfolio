# coding=utf-8

import heapq
import os
import pickle
import math


class PriorityQueue(object):
    """
    A queue structure where each element is served in order of priority.

    Elements in the queue are popped based on the priority with higher priority
    elements being served before lower priority elements.  If two elements have
    the same priority, they will be served in the order they were added to the
    queue.

    Traditionally priority queues are implemented with heaps, but there are any
    number of implementation options.

    (Hint: take a look at the module heapq)

    Attributes:
        queue (list): Nodes added to the priority queue.
    """

    def __init__(self):
        """Initialize a new Priority Queue."""

        self.queue = []
        self.count = 0

    def pop(self):
        """
        Pop top priority node from queue.

        Returns:
            The node with the highest priority.
        """

        return heapq.heappop(self.queue)

    def remove(self, node_id):
        """
        Remove a node from the queue.

        This is a hint, you might require this in ucs,
        however, if you choose not to use it, you are free to
        define your own method and not use it.

        Args:
            node_id (int): Index of node in queue.
        """

        raise NotImplementedError

    def __iter__(self):
        """Queue iterator."""

        return iter(sorted(self.queue))

    def __str__(self):
        """Priority Queue to string."""

        return 'PQ:%s' % self.queue

    def append(self, node):
        """
        Append a node to the queue.

        Args:
            node: Comparable Object to be added to the priority queue.
        """

        self.count += 1
        if len(node) > 1:
            val = (node[0], self.count, node[1])
        else:
            val = (node, self.count)
        heapq.heappush(self.queue, val)
        
    def __contains__(self, key):
        """
        Containment Check operator for 'in'

        Args:
            key: The key to check for in the queue.

        Returns:
            True if key is found in queue, False otherwise.
        """

        return key in [n[0] for n in self.queue]

    def __eq__(self, other):
        """
        Compare this Priority Queue with another Priority Queue.

        Args:
            other (PriorityQueue): Priority Queue to compare against.

        Returns:
            True if the two priority queues are equivalent.
        """

        return self.queue == other.queue

    def size(self):
        """
        Get the current size of the queue.

        Returns:
            Integer of number of items in queue.
        """

        return len(self.queue)

    def clear(self):
        """Reset queue to empty (no nodes)."""

        self.queue = []

    def top(self):
        """
        Get the top item in the queue.

        Returns:
            The first item stored in teh queue.
        """

        return self.queue[0]
        
    def end(self):
        """
        Get the top item in the queue.

        Returns:
            The first item stored in teh queue.
        """

        return self.queue[-1]


def breadth_first_search(graph, start, goal):
    """
    Warm-up exercise: Implement breadth-first-search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """    
    
    if start == goal:
        return []
    
    frontier = PriorityQueue()
    path = []
    
    frontier.append((0, start))
    
    i = 0
    explored_list = []
    
    while i < 20:
        if frontier.size() == 0:
            break
        
        ret_val = frontier.pop()
        path = (ret_val[-1])
        item_list = []
        
        if path[-1][-1] == goal:
            return [char for char in path]
        
        #add neighbors to frontier
        if explored_list.count(path[-1][-1]) == 0:
            neigh_list = graph[path[-1][-1]]
            explored_list.append(path[-1][-1])
            #print (explored_list)
            for item, val in neigh_list.items():
                for item2, val2 in val.items():
                    item_list.append((val2, item))
                    item_list.sort(reverse=True)
                    
            for x in range(len(item_list)):
                if explored_list.count(item_list[x][-1]) == 0:
                    fitem = str(path) + str(item_list[x][-1])
                    if item_list[x][-1] == goal:
                        return [char for char in fitem]
                    frontier.append((len(path),fitem))
       
    

def uniform_cost_search(graph, start, goal):
    """
    Warm-up exercise: Implement uniform_cost_search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """

    if start == goal:
        return []
    
    frontier = PriorityQueue()
    path = []
    
    frontier.append((0, start))
    
    i = 0
    explored_list = []
    
    while i < 20:
        if frontier.size() == 0:
            break
        
        ret_val = frontier.pop()
        path = (ret_val[-1])
        value = (ret_val[0])
        item_list = []
        
        path_vals = path.split(",")
        
        if path_vals[-1] == goal:
            return path.split(",")
        
        #add neighbors to frontier
        if explored_list.count(path_vals[-1]) == 0:
            neigh_list = graph[path_vals[-1]]
            explored_list.append(path_vals[-1])
            #print (explored_list)
            for item, val in neigh_list.items():
                for item2, val2 in val.items():
                    item_list.append((item, val2))
                    item_list.sort()
                    
            for x in range(len(item_list)):
                if explored_list.count(item_list[x][0]) == 0:
                    fitem = str(path) +","+ str(item_list[x][0])
                    fval = value + item_list[x][-1]
                    frontier.append((fval,fitem))


def null_heuristic(graph, v, goal):
    """
    Null heuristic used as a base line.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        v (str): Key for the node to calculate from.
        goal (str): Key for the end node to calculate to.

    Returns:
        0
    """

    return 0


def euclidean_dist_heuristic(graph, v, goal):
    """
    Warm-up exercise: Implement the euclidean distance heuristic.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        v (str): Key for the node to calculate from.
        goal (str): Key for the end node to calculate to.

    Returns:
        Euclidean distance between `v` node and `goal` node
    """

    math_val = ((graph.nodes[goal]['pos'][0]-graph.nodes[v]['pos'][0])**2) + ((graph.nodes[goal]['pos'][1]-graph.nodes[v]['pos'][1])**2)
    return (math.sqrt(math_val))


def a_star(graph, start, goal, heuristic=euclidean_dist_heuristic):
    """
    Warm-up exercise: Implement A* algorithm.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """

    if start == goal:
        return []
    
    frontier = PriorityQueue()
    path = []
    
    frontier.append((0, start))
    
    i = 0
    explored_list = []
    
    while i < 20:
        if frontier.size() == 0:
            break
        
        ret_val = frontier.pop()
        path = (ret_val[-1])
        value = (ret_val[0])
        item_list = []
        
        path_vals = path.split(",")
        
        if path_vals[-1] == goal:
            return path.split(",")
        
        #add neighbors to frontier
        if explored_list.count(path_vals[-1]) == 0:
            neigh_list = graph[path_vals[-1]]
            explored_list.append(path_vals[-1])
            #print (explored_list)
            for item, val in neigh_list.items():
                for item2, val2 in val.items():
                    item_list.append((item, val2))
                    item_list.sort()
                    
            for x in range(len(item_list)):
                if explored_list.count(item_list[x][0]) == 0:
                    fitem = str(path) +","+ str(item_list[x][0])
                    fval = (value + item_list[x][-1] - heuristic(graph, path[-1][-1], goal)) + heuristic(graph, item_list[x][0], goal)
                    
                    frontier.append((fval,fitem))


def bidirectional_ucs(graph, start, goal):
    """
    Exercise 1: Bidirectional Search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """

    if start == goal:
        return []
    
    start_frontier = PriorityQueue()
    goal_frontier = PriorityQueue()
    final_frontier = PriorityQueue()
    path = []
    half_path = []
    nodes = 0
    
    start_frontier.append((0, start))
    goal_frontier.append((0, goal))
    
    i = 0
    start_explored_list = []
    goal_explored_list = []
    
    while i < 20:
        if start_frontier.size() != 0:
            ret_val = start_frontier.pop()
            path = (ret_val[-1])
            value = (ret_val[0])
            item_list = []
            
            path_vals = path.split(",")
            
            if len(path_vals) > 1:
                index_val = 1
            else:
                index_val = 0
            
            if path_vals[index_val] == goal:
                print ("nodes explored: " + str(nodes))
                return path.split(",")
            elif path_vals[-1] == goal:
                final_frontier.append((value, path))
            else:
                half_path.append((value, path))
                half_path.sort()
            
            for m in range(len(half_path)):
                if m >= len(half_path):
                        break
                test_path = half_path[m][-1].split(",")
                test_half = [item for item in half_path if item[-1] == half_path[m][-1].replace(","+str(test_path[-1]),"")]
                print (test_half)
                
                if half_path[m] == test_half:
                        print ("path is popped")
                        half_path.pop(m)
            
            #add neighbors to frontier
            if start_explored_list.count(path_vals[-1]) == 0:# and goal_explored_list.count(path_vals[-1]) == 0:
                neigh_list = graph[path_vals[-1]]
                nodes += 1
                start_explored_list.append(path_vals[-1])
                #print (explored_list)
                for item, val in neigh_list.items():
                    for item2, val2 in val.items():
                        item_list.append((item, val2))
                        item_list.sort()
                        
                for x in range(len(item_list)):
                    if start_explored_list.count(item_list[x][0]) == 0:
                        fitem = str(path) +","+ str(item_list[x][0])
                        fval = value + item_list[x][-1]
                        start_frontier.append((fval,fitem))
        
        if len(half_path) != 0:
            for a in range(len(half_path)):
                for b in range(len(half_path)):
                    patha = half_path[a][-1].split(",")
                    pathb = half_path[b][-1].split(",")
                    vala = half_path[a][0]
                    valb = half_path[b][0]
                    
                    if patha[-1] == pathb[-1]:
                        path_string = str(patha) + str(pathb.reverse())
                        path_list = path_string.split(",")
                        path_list = list(dict.fromkeys(path_list))
                        path_string = ""
                        path_string.join(path_list)
                        val_string = vala + valb
                        final_frontier.append((val_string, path_string))
        
        if final_frontier.size() != 0:
            best = final_frontier.top()
            best_path = best[-1]
            best_val = best[0]
        else:
            best_val = math.inf
            
        if start_frontier.size() != 0:
            starts = start_frontier.top()
            starts_val = starts[0]
        else:
            if len(half_path) > 0:
                starts_val = half_path[0][0]
            else:
                starts_val = 0
        
        if goal_frontier.size() != 0:
            goals = goal_frontier.top()
            goals_val = goals[0]
        else:
            if len(half_path) > 0:
                goals_val = half_path[0][0]
            else:
                goals_val = 0
        
        
        if starts_val + goals_val >= best_val:
            print ("nodes explored: " + str(nodes))
            return best_path.split(",")
            
            
        ###################goal frontier######################
        
        if goal_frontier.size() != 0:
            ret_val = goal_frontier.pop()
            path = (ret_val[-1])
            value = (ret_val[0])
            item_list = []
            
            path_vals = path.split(",")
            
            if len(path_vals) > 1:
                index_val = 1
            else:
                index_val = 0
                
            if path_vals[index_val] == goal and path_vals[0] == start:
                print ("nodes explored: " + str(nodes))
                return path.split(",")
            elif path_vals[-1] == start:
                final_frontier.append((value, path))
            else:
                half_path.append((value, path))
                half_path.sort()
                print(half_path)
            
            for m in range(len(half_path)):
                if m >= len(half_path):
                        break
                test_path = half_path[m][-1].split(",")
                test_half = [item for item in half_path if item[-1] == half_path[m][-1].replace(","+str(test_path[-1]),"")]
                print (test_half)
                
                if half_path[m] == test_half:
                        print ("path is popped")
                        half_path.pop(m)
            
            #add neighbors to frontier
            if goal_explored_list.count(path_vals[-1]) == 0:# and start_explored_list.count(path_vals[-1]) == 0:
                neigh_list = graph[path_vals[-1]]
                nodes += 1
                goal_explored_list.append(path_vals[-1])
                #print (explored_list)
                for item, val in neigh_list.items():
                    for item2, val2 in val.items():
                        item_list.append((item, val2))
                        item_list.sort()
                        
                for x in range(len(item_list)):
                    if goal_explored_list.count(item_list[x][0]) == 0:
                        fitem = str(path) +","+ str(item_list[x][0])
                        fval = value + item_list[x][-1]
                        goal_frontier.append((fval,fitem))
        print(half_path)
        if len(half_path) != 0:
            for a in range(len(half_path)):
                for b in range(len(half_path)):
                    patha = half_path[a][-1].split(",")
                    pathb = half_path[b][-1].split(",")
                    vala = half_path[a][0]
                    valb = half_path[b][0]
                    
                    print(patha)
                    print(pathb)
                    if patha[-1] == pathb[-1]:
                        path_list = patha.split(",") + pathb.split(",").reverse()
                        list = list(OrderedDict.fromkeys(path_list))
                        path_string = ""
                        path_string.join(list)
                        val_string = vala + valb
                        final_frontier.append((val_string, path_string))
        
        print (final_frontier)
        if final_frontier.size() != 0:
            best = final_frontier.top()
            best_path = best[-1]
            best_val = best[0]
        else:
            best_val = math.inf
            
        if start_frontier.size() != 0:
            starts = start_frontier.top()
            starts_val = starts[0]
        else:
            if len(half_path) > 0:
                starts_val = half_path[0][0]
            else:
                starts_val = 0
        
        if goal_frontier.size() != 0:
            goals = goal_frontier.top()
            goals_val = goals[0]
        else:
            if len(half_path) > 0:
                goals_val = half_path[0][0]
            else:
                goals_val = 0
        
        
        if starts_val + goals_val >= best_val:
            return best_path.split(",")
                        

def bidirectional_a_star(graph, start, goal,
                         heuristic=euclidean_dist_heuristic):
    """
    Exercise 2: Bidirectional A*.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """

    if start == goal:
        return []
    
    start_frontier = PriorityQueue()
    goal_frontier = PriorityQueue()
    start_path = []
    goal_path = []
    final_path = []
    start_explored_list = []
    start_vals = []
    start_p_vals = []
    goal_explored_list = []
    goal_vals = []
    goal_p_vals = []
    path = ""
    
    start_frontier.append((0, start))
    goal_frontier.append((0, goal))
    start_exp_front = [start]
    goal_exp_front = [goal]
    last_node_val = 0
    
    i = 0
    
    #print ("start: " + str(start))
    #print ("goal: " + str(goal))
    
    #start node frontier search
    
    while i < 20:
        
        best_val = math.inf
        test_val = 0.0
        print (final_path)   
        for a in range(len(final_path)):
            for b in range(len(final_path)):
                test_patha = final_path[a][-1].split(",")
                test_pathb = final_path[b][-1].split(",")
                #print ("a: " + str(test_patha))
                #print ("b: " + str(test_pathb))
                #print (final_path)
                if test_patha[0] == start and test_patha[1] == goal:
                    path = final_path[a][-1]
                    #print(graph.explored_nodes)
                    #print("list " + str(path))
                    return path.split(",")
                if test_pathb[0] == start and test_pathb[1] == goal:
                    path = final_path[b][-1]
                    #print(graph.explored_nodes)
                    #print("list " + str(path))
                    return path.split(",")
                if test_patha[0] == start and test_patha[-1] == goal:
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif test_pathb[0] == start and test_pathb[-1] == goal:
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_patha[-1] == test_pathb[0]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1] + "," + final_path[b][-1]
        
        if goal_frontier.size() == 0:
            #move on
            oval = math.inf - 1
            other = ["random", "list"]
        else:
            other = goal_frontier.top()
            oval = other[0] #- heuristic(graph, start, other[-1].split(",")[0])
            
        if start_frontier.size() == 0:
            value = math.inf - 1
            ret_val = ["random", "list"]
        else:
            ret_val = start_frontier.top()
            value = ret_val[0] #- heuristic(graph, ret_val[-1].split(",")[-1], goal)
        
        s_min_list = []
        g_min_list = []
        for l in range(len(final_path)):
            if final_path[l][-1][0] == start:
                s_min_list.append(final_path[l][0])
            elif final_path[l][-1][-1] == goal:
                g_min_list.append(final_path[l][0])
            
        if len(s_min_list) > 0:
            s_min_val = min(s_min_list)
        else:
            s_min_val = 0
            
        if len(g_min_list) > 0:
            g_min_val = min(g_min_list)
        else:
            g_min_val = 0
        
        #print("s min val " + str(s_min_val))
        #print("g min val " + str(g_min_val))
        if ret_val[-1] == start + "," + goal or other[-1] == start + "," + goal:
            #continue to add path to path_list
            dummy_variable = 0
        elif value + g_min_val >= best_val and oval + s_min_val >= best_val:
            path_list = path.split(",")
            path_list = list(dict.fromkeys(path_list))
            #print(graph.explored_nodes)
            #print("list " + str(path_list))
            return path_list
        
        if value + g_min_val < best_val:
            ret_val = start_frontier.pop()
            
            start_path = (ret_val[-1])
            value = (ret_val[0])
            item_list = []


            path_vals = start_path.split(",")
            start_exp_front.append(path_vals[-1])
            start_vals.append(value)
            start_p_vals.append(start_path)
            
            
            
            index = start_p_vals.index(start_path)
            s_path = start_p_vals[index]
            value2 = start_vals[index] - heuristic(graph,path_vals[-1],goal)
            if s_path != start:
                final_path.append((value2, 1, s_path))
                #print (start_path.replace(","+str(start_path[-1]),""))
                #print (final_path)
                for m in range(len(final_path)):
                    #print (m)
                    #print (len(final_path))
                    if m >= len(final_path):
                        break
                    #print (final_path[m])
                    if final_path[m].count(start_path.replace(","+str(start_path[-1]),"")) > 0:
                        #print ("path is popped")
                        final_path.pop(m)
            
            #add neighbors to frontier
            if start_explored_list.count(path_vals[-1]) == 0 and goal_explored_list.count(path_vals[-1]) == 0:
                neigh_list = graph[path_vals[-1]]
                start_explored_list.append(path_vals[-1])
                for item, val in neigh_list.items():
                    for item2, val2 in val.items():
                        item_list.append((item, val2))
                        item_list.sort()
                        
                for x in range(len(item_list)):
                    if start_explored_list.count(item_list[x][0]) == 0:
                        if start_path == start and item_list[x][0] == goal:
                            #print ("neighbor case start")
                            return [start_path, item_list[x][0]]
                        fitem = str(start_path) +","+ str(item_list[x][0])
                        if x == 0:
                            fval = value + item_list[x][-1] + heuristic(graph, item_list[x][0], goal)
                        else:
                            fval = (value + item_list[x][-1] - heuristic(graph, item_list[x-1][0], goal)) + heuristic(graph, item_list[x][0], goal)
                        start_frontier.append((fval,fitem))
                    
            
    #goal node frontier search

        for a in range(len(final_path)):
            for b in range(len(final_path)):
                test_patha = final_path[a][-1].split(",")
                test_pathb = final_path[b][-1].split(",")
                #print (final_path)
                #print ("a: " + str(test_patha))
                #print ("b: " + str(test_pathb))
                if test_patha[0] == start and test_patha[1] == goal:
                    path = final_path[a][-1]
                    #print(graph.explored_nodes)
                    #print("list " + str(path))
                    return path.split(",")
                if test_pathb[0] == start and test_pathb[1] == goal:
                    path = final_path[b][-1]
                    #print(graph.explored_nodes)
                    #print("list2 " + str(path))
                    return path.split(",")
                if test_patha[0] == start and test_patha[-1] == goal:
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif test_pathb[0] == start and test_pathb[-1] == goal:
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_patha[-1] == test_pathb[0]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1] + "," + final_path[b][-1]

        if goal_frontier.size() == 0:
            #move on
            oval = math.inf - 1
            other = ["random", "list"]
        else:
            other = goal_frontier.top()
            oval = other[0] #- heuristic(graph, start, other[-1].split(",")[0])
            
        if start_frontier.size() == 0:
            value = math.inf - 1
            ret_val = ["random", "list"]
        else:
            ret_val = start_frontier.top()
            value = ret_val[0] #- heuristic(graph, ret_val[-1].split(",")[-1], goal)
        
        s_min_list = []
        g_min_list = []
        for l in range(len(final_path)):
            if final_path[l][-1][0] == start:
                s_min_list.append(final_path[l][0])
            elif final_path[l][-1][-1] == goal:
                g_min_list.append(final_path[l][0])
            
        if len(s_min_list) > 0:
            s_min_val = min(s_min_list)
        else:
            s_min_val = 0
            
        if len(g_min_list) > 0:
            g_min_val = min(g_min_list)
        else:
            g_min_val = 0
        
        #print("s min val " + str(s_min_val))
        #print("g min val " + str(g_min_val))
        if ret_val[-1] == start + "," + goal or other[-1] == start + "," + goal:
            #continue to add path to path_list
            dummy_variable = 0
        elif value + g_min_val >= best_val and oval + s_min_val >= best_val:
            path_list = path.split(",")
            path_list = list(dict.fromkeys(path_list))
            #print(graph.explored_nodes)
            #print("list3 " + str(path_list))
            return path_list

        if goal_frontier.size() == 0:
            #continue through loop
            test_val = 0
        else:
         
            if oval + s_min_val < best_val:
                ret_val = goal_frontier.pop()
                
                goal_path = (ret_val[-1])
                value = (ret_val[0])
                item_list = []
       
                path_vals = goal_path.split(",")
                goal_exp_front.append(path_vals[0])
                goal_vals.insert(0, value)
                goal_p_vals.insert(0, goal_path)
              
                index = goal_p_vals.index(goal_path)
                value2 = goal_vals[index] - heuristic(graph, start, path_vals[0])
                g_path = goal_p_vals[index]
                if g_path != goal:
                    final_path.append((value2, 2, g_path))
                    for m in range(len(final_path)):
                    #print (m)
                    #print (len(final_path))
                        if m >= len(final_path):
                            break
                    #print (final_path[m])
                        if final_path[m].count(goal_path.replace(str(goal_path[0])+",","")) > 0:
                            #print ("path is popped")
                            final_path.pop(m)
                
                #add neighbors to frontier
                if goal_explored_list.count(path_vals[-1]) == 0 and start_explored_list.count(path_vals[-1]) == 0:
                    neigh_list = graph[path_vals[-1]]
                    goal_explored_list.append(path_vals[-1])
                    for item, val in neigh_list.items():
                        for item2, val2 in val.items():
                            item_list.append((item, val2))
                            item_list.sort()
                            
                    for x in range(len(item_list)):
                        if goal_explored_list.count(item_list[x][0]) == 0:
                            if item_list[x][0] == start and goal_path == goal:
                                #print ("neighbor case goal")
                                return [item_list[x][0], goal_path]
                            fitem = str(item_list[x][0]) +","+ str(goal_path)
                            if x == 0:
                                fval = value + item_list[x][-1] + heuristic(graph, start, item_list[x][0])
                            else:
                                fval = value + item_list[x][-1] - heuristic(graph, start, item_list[x-1][0]) + heuristic(graph, start, item_list[x][0])
                            goal_frontier.append((fval,fitem))
                        
                        
                        
                        
                        
                        

def tridirectional_search(graph, goals):
    """
    Exercise 3: Tridirectional UCS Search

    See README.MD for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        goals (list): Key values for the 3 goals

    Returns:
        The best path as a list from one of the goal nodes (including both of
        the other goal nodes).
    """
    if goals[0] == goals[1]:
        return []
    
    g1_frontier = PriorityQueue()
    g2_frontier = PriorityQueue()
    g3_frontier = PriorityQueue()
    g1_path = []
    g2_path = []
    g3_path = []
    final_path = []
    g1_explored_list = []
    g1_vals = []
    g1_p_vals = []
    g2_explored_list = []
    g2_vals = []
    g2_p_vals = []
    g3_explored_list = []
    g3_vals = []
    g3_p_vals = []
    path = ""
    TRI_path = []
    
    g1_frontier.append((0, goals[0]))
    g2_frontier.append((0, goals[1]))
    g3_frontier.append((0, goals[2]))
    g1_exp_front = [goals[0]]
    g2_exp_front = [goals[1]]
    g3_exp_front = [goals[2]]
    last_node_val = 0
    
    i = 0
    
    #print ("start: " + str(start))
    #print ("goal: " + str(goal))
    
    #start node frontier search
    
    while i < 20:
        
        best_val = math.inf
        test_val = 0.0
        
        for a in range(len(final_path)):
            for b in range(len(final_path)):
                test_patha = final_path[a][-1].split(",")
                test_pathb = final_path[b][-1].split(",")
                #print ("a: " + str(test_patha))
                #print ("b: " + str(test_pathb))
                #print (final_path)
                
                if (test_patha[0] == goals[0] and test_patha[-1] == goals[1]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif (test_patha[0]==goals[0] and test_patha[-1]==goals[2]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif (test_patha[0]==goals[1] and test_patha[-1]==goals[2]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif test_pathb[0] == goals[0] and test_pathb[-1] == goals[1]:
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_pathb[0]==goals[0] and test_pathb[-1]==goals[2]):
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_pathb[0]==goals[1] and test_pathb[-1]==goals[2]):
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_patha[-1] == test_pathb[0]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1] + "," + final_path[b][-1]
                elif (test_patha[0] == test_pathb[0] and final_path[a][-2] != final_path[b][-2]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        reverse_list = final_path[a][-1].split(",").reverse()
                        reverse_string = []
                        for n in range(len(reverse_string)):
                            reverse_string.join(str(reverse_list[n]) +",")
                        path = reverse_string + "," + final_path[b][-1]
        
        if g2_frontier.size() == 0:
            #move on
            oval = math.inf - 1
            other = ["random", "list"]
        else:
            other = g2_frontier.top()
            oval = other[0]
            
        if g1_frontier.size() == 0:
            value = math.inf - 1
            ret_val = ["random", "list"]
        else:
            ret_val = g1_frontier.top()
            value = ret_val[0]
            
        if g3_frontier.size() == 0:
            tval = math.inf-1
            third = ["random", "list"]
        else:
            third = g3_frontier.top()
            tval = third[0]
        
        min_list = []
        
        for l in range(len(final_path)):
            min_list.append(final_path[l][0])
            
            
        if len(min_list) > 0:
            min_val = min(min_list)
        else:
            min_val = 0
            
        
        #print("s min val " + str(s_min_val))
        #print("g min val " + str(g_min_val))
        if value + min_val >= best_val and oval + min_val >= best_val and tval + min_val >= best_val:
            path_list = path.split(",")
            path_list = list(dict.fromkeys(path_list))
            #print(graph.explored_nodes)
            #print("list " + str(path_list))
            print ("1 return happening")
            TRI_path.append(path_list)
            print (TRI_path)
            for a in range(len(TRI_path)):
                for b in range(len(TRI_path)):
                    patha = TRI_path[a]
                    pathb = TRI_path[b]
                    if patha != pathb:
                        if patha[0] == pathb[0] or patha[-1] == pathb[-1]:
                            joined = []
                            joined.append(patha[0])
                            joined.append(patha[-1])
                            joined.append(pathb[-1])
                            print(list(dict.fromkeys(joined)))
                            return list(dict.fromkeys(joined))
        
        if value + min_val < best_val:
            ret_val = g1_frontier.pop()
            
            g1_path = (ret_val[-1])
            value = (ret_val[0])
            item_list = []


            path_vals = g1_path.split(",")
            g1_exp_front.append(path_vals[-1])
            g1_vals.append(value)
            g1_p_vals.append(g1_path)
            
            
            
            index = g1_p_vals.index(g1_path)
            value2 = g1_vals[index]
            g1_path = g1_p_vals[index]
            if g1_path != goals[0]:
                final_path.append((value2, 1, g1_path))
                #print (start_path.replace(","+str(start_path[-1]),""))
                #print (final_path)
                for m in range(len(final_path)):
                    #print (m)
                    #print (len(final_path))
                    if m >= len(final_path):
                        break
                    #print (final_path[m])
                    if final_path[m].count(g1_path.replace(","+str(g1_path[-1]),"")) > 0:
                        #print ("path is popped")
                        final_path.pop(m)
            
            #add neighbors to frontier
            if g1_explored_list.count(path_vals[-1]) == 0 and g2_explored_list.count(path_vals[-1]) == 0 and g3_explored_list.count(path_vals[-1]) == 0:
                neigh_list = graph[path_vals[-1]]
                g1_explored_list.append(path_vals[-1])
                for item, val in neigh_list.items():
                    for item2, val2 in val.items():
                        item_list.append((item, val2))
                        item_list.sort()
                        
                for x in range(len(item_list)):
                    if g1_explored_list.count(item_list[x][0]) == 0:
                        if g1_path == goals[0] and item_list[x][0] == goals[1]:
                            #print ("neighbor case start")
                            print ("2 return happening")
                            TRI_path.append([g1_path, item_list[x][0]])
                            print (TRI_path)
                        if g1_path == goals[0] and item_list[x][0] == goals[2]:
                            print ("3 return happening")
                            print (str(g1_path) + " = " + str(goals[0]))
                            print (str(item_list[x][0]) + " = " + str(goals[2]))
                            print ([g1_path, item_list[x][0]])
                            TRI_path.append([g1_path, item_list[x][0]])
                            print (TRI_path)
                        fitem = str(g1_path) +","+ str(item_list[x][0])
                        fval = value + item_list[x][-1]
                        g1_frontier.append((fval,fitem))
                        print(g1_frontier)
            
    #goal node frontier search

        for a in range(len(final_path)):
            for b in range(len(final_path)):
                test_patha = final_path[a][-1].split(",")
                test_pathb = final_path[b][-1].split(",")
                #print (final_path)
                #print ("a: " + str(test_patha))
                #print ("b: " + str(test_pathb))
                if (test_patha[0] == goals[0] and test_patha[-1] == goals[1]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif (test_patha[0]==goals[0] and test_patha[-1]==goals[2]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif (test_patha[0]==goals[1] and test_patha[-1]==goals[2]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif test_pathb[0] == goals[0] and test_pathb[-1] == goals[1]:
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_pathb[0]==goals[0] and test_pathb[-1]==goals[2]):
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_pathb[0]==goals[1] and test_pathb[-1]==goals[2]):
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_patha[-1] == test_pathb[0]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1] + "," + final_path[b][-1]
                elif (test_patha[0] == test_pathb[0] and final_path[a][-2] != final_path[b][-2]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        reverse_list = final_path[a][-1].split(",").reverse()
                        reverse_string = []
                        for n in range(len(reverse_string)):
                            reverse_string.join(str(reverse_list[n]) +",")
                        path = reverse_string + "," + final_path[b][-1]

        if g2_frontier.size() == 0:
            #move on
            oval = math.inf - 1
            other = ["random", "list"]
        else:
            other = g2_frontier.top()
            oval = other[0]
            
        if g1_frontier.size() == 0:
            value = math.inf - 1
            ret_val = ["random", "list"]
        else:
            ret_val = g1_frontier.top()
            value = ret_val[0]
            
        if g3_frontier.size() == 0:
            tval = math.inf-1
            third = ["random", "list"]
        else:
            third = g3_frontier.top()
            tval = third[0]
        
        min_list = []
        
        for l in range(len(final_path)):
            min_list.append(final_path[l][0])
            
            
        if len(min_list) > 0:
            min_val = min(min_list)
        else:
            min_val = 0
        
        
        #print("s min val " + str(s_min_val))
        #print("g min val " + str(g_min_val))
        if value + min_val >= best_val and oval + min_val >= best_val and tval + min_val >= best_val:
            path_list = path.split(",")
            path_list = list(dict.fromkeys(path_list))
            #print(graph.explored_nodes)
            #print("list " + str(path_list))
            print ("4 return happening")
            TRI_path.append(path_list)
            print (TRI_path)

        if g2_frontier.size() == 0:
            #continue through loop
            test_val = 0
        else:
         
            if oval + min_val < best_val:
                ret_val = g2_frontier.pop()
                
                g2_path = (ret_val[-1])
                value = (ret_val[0])
                item_list = []
       
                path_vals = g2_path.split(",")
                g2_exp_front.append(path_vals[0])
                g2_vals.insert(0, value)
                g2_p_vals.insert(0, g2_path)
              
                index = g2_p_vals.index(g2_path)
                value2 = g2_vals[index]
                g2_path = g2_p_vals[index]
                if g2_path != goals[1]:
                    final_path.append((value2, 2, g2_path))
                    for m in range(len(final_path)):
                    #print (m)
                    #print (len(final_path))
                        if m >= len(final_path):
                            break
                    #print (final_path[m])
                        if final_path[m].count(g2_path.replace(str(g2_path[0])+",","")) > 0:
                            #print ("path is popped")
                            final_path.pop(m)
                
                #add neighbors to frontier
                if g2_explored_list.count(path_vals[-1]) == 0 and g1_explored_list.count(path_vals[-1]) == 0 and g3_explored_list.count(path_vals[-1]) == 0:
                    neigh_list = graph[path_vals[-1]]
                    g2_explored_list.append(path_vals[-1])
                    for item, val in neigh_list.items():
                        for item2, val2 in val.items():
                            item_list.append((item, val2))
                            item_list.sort()
                            
                    for x in range(len(item_list)):
                        if g2_explored_list.count(item_list[x][0]) == 0:
                            if item_list[x][0] == goals[0] and g2_path == goals[1]:
                                #print ("neighbor case goal")
                                print ("5 return happening")
                                TRI_path.append([item_list[x][0], g2_path])
                                print (TRI_path)
                            if item_list[x][0] == goals[2] and g2_path == goals[1]:
                                #print ("neighbor case goal")
                                print ("6 return happening")
                                return [item_list[x][0], g2_path]
                            fitem = str(item_list[x][0]) +","+ str(g2_path)
                            fval = value + item_list[x][-1]
                            g2_frontier.append((fval,fitem))
                            print(g2_frontier)
                            
                            
     #goal2 node frontier search

        for a in range(len(final_path)):
            for b in range(len(final_path)):
                test_patha = final_path[a][-1].split(",")
                test_pathb = final_path[b][-1].split(",")
                #print (final_path)
                #print ("a: " + str(test_patha))
                #print ("b: " + str(test_pathb))
                if (test_patha[0] == goals[0] and test_patha[-1] == goals[1]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif (test_patha[0]==goals[0] and test_patha[-1]==goals[2]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif (test_patha[0]==goals[1] and test_patha[-1]==goals[2]):
                    test_val = final_path[a][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1]
                elif test_pathb[0] == goals[0] and test_pathb[-1] == goals[1]:
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_pathb[0]==goals[0] and test_pathb[-1]==goals[2]):
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_pathb[0]==goals[1] and test_pathb[-1]==goals[2]):
                    test_val = final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[b][-1]
                elif (test_patha[-1] == test_pathb[0]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        path = final_path[a][-1] + "," + final_path[b][-1]
                elif (test_patha[0] == test_pathb[0] and final_path[a][-2] != final_path[b][-2]):
                    test_val = final_path[a][0] + final_path[b][0]
                    if test_val < best_val:
                        best_val = test_val
                        reverse_list = final_path[a][-1].split(",").reverse()
                        reverse_string = []
                        for n in range(len(reverse_string)):
                            reverse_string.join(str(reverse_list[n]) +",")
                        path = reverse_string + "," + final_path[b][-1]

        if g2_frontier.size() == 0:
            #move on
            oval = math.inf - 1
            other = ["random", "list"]
        else:
            other = g2_frontier.top()
            oval = other[0]
            
        if g1_frontier.size() == 0:
            value = math.inf - 1
            ret_val = ["random", "list"]
        else:
            ret_val = g1_frontier.top()
            value = ret_val[0]
            
        if g3_frontier.size() == 0:
            tval = math.inf-1
            third = ["random", "list"]
        else:
            third = g3_frontier.top()
            tval = third[0]
        
        min_list = []
        
        for l in range(len(final_path)):
            min_list.append(final_path[l][0])
            
            
        if len(min_list) > 0:
            min_val = min(min_list)
        else:
            min_val = 0
        
        
        #print("s min val " + str(s_min_val))
        #print("g min val " + str(g_min_val))
        if value + min_val >= best_val and oval + min_val >= best_val and tval + min_val >= best_val:
            path_list = path.split(",")
            path_list = list(dict.fromkeys(path_list))
            #print(graph.explored_nodes)
            #print("list " + str(path_list))
            print ("7 return happening")
            TRI_path.append(path_list)
            print (TRI_path)

        if g3_frontier.size() == 0:
            #continue through loop
            test_val = 0
        else:
         
            if tval + min_val < best_val:
                ret_val = g3_frontier.pop()
                
                g3_path = (ret_val[-1])
                value = (ret_val[0])
                item_list = []
       
                path_vals = g3_path.split(",")
                g3_exp_front.append(path_vals[0])
                g3_vals.insert(0, value)
                g3_p_vals.insert(0, g3_path)
              
                index = g3_p_vals.index(g3_path)
                value2 = g3_vals[index]
                g3_path = g3_p_vals[index]
                if g3_path != goals[2]:
                    final_path.append((value2, 3, g3_path))
                    for m in range(len(final_path)):
                    #print (m)
                    #print (len(final_path))
                        if m >= len(final_path):
                            break
                    #print (final_path[m])
                        if final_path[m].count(g3_path.replace(str(g3_path[0])+",","")) > 0:
                            #print ("path is popped")
                            final_path.pop(m)
                
                #add neighbors to frontier
                if g3_explored_list.count(path_vals[-1]) == 0 and g1_explored_list.count(path_vals[-1]) == 0 and g2_explored_list.count(path_vals[-1]) == 0:
                    neigh_list = graph[path_vals[-1]]
                    g3_explored_list.append(path_vals[-1])
                    for item, val in neigh_list.items():
                        for item2, val2 in val.items():
                            item_list.append((item, val2))
                            item_list.sort()
                            
                    for x in range(len(item_list)):
                        if g3_explored_list.count(item_list[x][0]) == 0:
                            if item_list[x][0] == goals[0] and g3_path == goals[2]:
                                #print ("neighbor case goal")
                                print ("8 return happening")
                                TRI_path.append([item_list[x][0], g3_path])
                                print (TRI_path)
                            if item_list[x][0] == goals[1] and g2_path == goals[2]:
                                #print ("neighbor case goal")
                                print ("9 return happening")
                                return [item_list[x][0], g3_path]
                            fitem = str(item_list[x][0]) +","+ str(g3_path)
                            fval = value + item_list[x][-1]
                            g3_frontier.append((fval,fitem))  
                            print(g3_frontier)
                        
                              
                        
                        
def tridirectional_upgraded(graph, goals, heuristic=euclidean_dist_heuristic):
    """
    Exercise 4: Upgraded Tridirectional Search

    See README.MD for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        goals (list): Key values for the 3 goals
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path as a list from one of the goal nodes (including both of
        the other goal nodes).
    """
    raise NotImplementedError


def return_your_name():
    """Return your name from this function"""
    return "Jinelle Gilfillan"


def custom_heuristic(graph, v, goal):
    """
       Feel free to use this method to try and work with different heuristics and come up with a better search algorithm.
       Args:
           graph (ExplorableGraph): Undirected graph to search.
           v (str): Key for the node to calculate from.
           goal (str): Key for the end node to calculate to.
       Returns:
           Custom heuristic distance between `v` node and `goal` node
       """

pass

# Extra Credit: Your best search method for the race
def custom_search(graph, start, goal, data=None):
    """
    Race!: Implement your best search algorithm here to compete against the
    other student agents.

    If you implement this function and submit your code to bonnie, you'll be
    registered for the Race!

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        data :  Data used in the custom search.
            Will be passed your data from load_data(graph).
            Default: None.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """

    raise NotImplementedError



def load_data(graph, time_left):
    """
    Feel free to implement this method. We'll call it only once 
    at the beginning of the Race, and we'll pass the output to your custom_search function.
    graph: a networkx graph
    time_left: function you can call to keep track of your remaining time.
        usage: time_left() returns the time left in milliseconds.
        the max time will be 10 minutes.

    * To get a list of nodes, use graph.nodes()
    * To get node neighbors, use graph.neighbors(node)
    * To get edge weight, use graph.get_edge_weight(node1, node2)
    """

    # nodes = graph.nodes()
    return None
 
def haversine_dist_heuristic(graph, v, goal):
    """
    Note: This provided heuristic is for the Atlanta race.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        v (str): Key for the node to calculate from.
        goal (str): Key for the end node to calculate to.

    Returns:
        Haversine distance between `v` node and `goal` node
    """

    #Load latitude and longitude coordinates in radians:
    vLatLong = (math.radians(graph.nodes[v]["pos"][0]), math.radians(graph.nodes[v]["pos"][1]))
    goalLatLong = (math.radians(graph.nodes[goal]["pos"][0]), math.radians(graph.nodes[goal]["pos"][1]))

    #Now we want to execute portions of the formula:
    constOutFront = 2*6371 #Radius of Earth is 6,371 kilometers
    term1InSqrt = (math.sin((goalLatLong[0]-vLatLong[0])/2))**2 #First term inside sqrt
    term2InSqrt = math.cos(vLatLong[0])*math.cos(goalLatLong[0])*((math.sin((goalLatLong[1]-vLatLong[1])/2))**2) #Second term
    return constOutFront*math.asin(math.sqrt(term1InSqrt+term2InSqrt)) #Straight application of formula

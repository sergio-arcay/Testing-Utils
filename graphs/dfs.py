""" Depth-First-Search algorithm
"""


def dfs(node, graph, _trail=None):
    """ Standard implementation of DFS.

    Functionality:
        Passing through every node from the given origin. Print every reachable node.

    Algorithm:
        Depth First Search (DPS).

    Method:
        Recursive method. Iterate over each node in the given graph until passing along all the possible branches.

    Graph:
        {
            <node_1>: [<reachable_node_1_from_node_1>, <reachable_node_2_from_node_1>, ...],
            <node_2>: [<reachable_node_1_from_node_2>, ...],
            ...
        }

    Return:
        None. Just print the passing nodes.

    """

    # Initialize the recursive function variables.
    if _trail is None:
        _trail = list()

    # If current node was not visited in this branch yet.
    if node not in _trail:

        # Print the current state
        print("{} -> {}".format(_trail, node))

        # Add the new node to the current branch trail
        _trail.append(node)

        # Get all the current node neighbours and call this function again with each one.
        for neighbour in graph[node]:
            dfs(neighbour, graph, _trail.copy())


def dfs_to_destination(origin, destination, graph, _trail=None, _results=None):
    """ DFS with destination node.

    Functionality:
        Find all the possible paths from the given origin node to the given destination node.

    Algorithm:
        Depth First Search (DPS).

    Method:
        Recursive method. Iterate over each node in the given graph until passing along all the possible branches.

    Graph:
        {
            <node_1>: [<reachable_node_1_from_node_1>, <reachable_node_2_from_node_1>, ...],
            <node_2>: [<reachable_node_1_from_node_2>, ...],
            ...
        }

    Return:
        Resulting branches. A list with all the branches valid to reach the given destination.

    """

    # Initialize the recursive function variables.
    if _trail is None:
        _trail = list()
    if _results is None:
        _results = list()

    # If current node was not visited in this branch yet.
    if origin not in _trail:

        # Print the current state
        # print("{} -> {}".format(_trail, origin))

        # Append the new node to the branch trail.
        _trail.append(origin)

        # If the new node is the desired destination, append the branch trail to the results and finish the branch.
        if origin == destination:
            _results.append(_trail.copy())
            del _trail
            return _results

        # Get all the current node neighbours and call this function again with each one.
        for neighbour in graph[origin]:
            _results = dfs_to_destination(neighbour, destination, graph, _trail.copy(), _results)

        # Once is over, return the results.
        return _results

    # If current node is already in the trail (was already visited), finish the current branch.
    else:
        del _trail
        return _results


def dfs_to_destination_with_costs(origin, destination, max_cost, graph, _trail=None, _results=None):
    """ DFS with destination node and a specific cost for each link.

    Functionality:
        Find all the possible paths from the given origin node to the given destination node and with a maximum cost.

    Algorithm:
        Depth First Search (DPS).

    Method:
        Recursive method. Iterate over each node in the given graph until passing along all the possible branches.

    Graph:
        {
            <node_1>: {
                reachable_node_1_from_node_1: <cost_to_reachable_node_1_from_node_1>,
                reachable_node_2_from_node_1: <cost_to_reachable_node_2_from_node_1>,
                ...
            },
            <node_2>: {
                reachable_node_1_from_node_2: <cost_to_reachable_node_1_from_node_2>,
                ...
            },
            ...
        }

    Return:
        Resulting branches and their path costs. A list with all the branches valid to reach the given destination with
        the given maximum cost.

    """

    # Initialize the recursive function variables.
    if _trail is None:
        _trail = list()
    if _results is None:
        _results = list()

    # Calculate the resulting path cost after appending the new node
    new_path_cost = \
        sum((graph[n1][n2] for n1, n2 in zip(_trail, _trail[1:])), graph[_trail[-1]][origin]) if _trail else 0

    # If current node was not visited in this branch yet and the resulting path cost does not turn to be too high.
    if origin not in _trail and new_path_cost <= max_cost:

        # Print the current state
        # print("{} -> {}".format(_trail, origin))

        # Append the new node to the branch trail.
        _trail.append(origin)

        # If the new node is the desired destination, append the branch trail to the results and finish the branch.
        if origin == destination:
            _results.append((_trail.copy(), new_path_cost))
            del _trail
            return _results

        # Get all the current node neighbours and call this function again with each one.
        for neighbour in graph[origin]:
            _results = dfs_to_destination_with_costs(neighbour, destination, max_cost, graph, _trail.copy(), _results)

        # Once is over, return the results.
        return _results

    # If current node is already in the trail (was already visited), finish the current branch.
    else:
        del _trail
        return _results


# TODO Nodes with an individual priority value? This algorithm could be finished once an acceptable total priority
#  was reached.


if __name__ == '__main__':

    graph_with_reachable_nodes = {
        "5": ["3", "7"],
        "3": ["2", "4"],
        "7": ["8"],
        "2": [],
        "4": ["8"],
        "8": ["7"]
    }

    graph_with_node_costs = {
        "2": {},
        "3": {"2": 1, "4": 1},
        "4": {"8": 1},
        "5": {"3": 1, "7": 1},
        "7": {"8": 1},
        "8": {"7": 1}
    }

    results = dfs_to_destination_with_costs("5", "8", 3, graph_with_node_costs)
    print("DFS to a given destination and maximum cost => {}".format(results))

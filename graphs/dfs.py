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


if __name__ == '__main__':

    test_graph = {
        "5": ["3", "7"],
        "3": ["2", "4"],
        "7": ["8"],
        "2": [],
        "4": ["8"],
        "8": ["7"]
    }

    results = dfs_to_destination("5", "2", test_graph)
    print("DFS to a given destination => {}".format(results))

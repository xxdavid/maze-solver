from enum import Enum
from typing import List, Optional, Tuple
from common import Coordinates


class Node:
    def __init__(self, coordinates: Coordinates):
        self.coordinates: Coordinates = coordinates

    def __repr__(self):
        return self.__str__()


class GraphNode(Node):
    class State(Enum):
        FRESH = 1
        OPEN = 2
        CLOSE = 3

    def __init__(self, coordinates: Coordinates):
        super().__init__(coordinates)
        self.state: self.State = self.State.FRESH
        self.neighbours: List['GraphNode'] = []

    def add_neighbour(self, neighbour: 'GraphNode'):
        self.neighbours.append(neighbour)

    def to_tree_node(self, predecessor: 'TreeNode') -> 'TreeNode':
        return TreeNode(self.coordinates, predecessor)

    def to_root_node(self) -> 'TreeNode':
        return TreeNode(self.coordinates, None)

    def __str__(self):
        return f"GraphNode: [{self.coordinates.x}, {self.coordinates.y}] {self.state}"


class TreeNode(Node):
    def __init__(self, coordinates: Coordinates, predecessor: Optional['TreeNode']):
        super().__init__(coordinates)
        self.predecessor: Optional['TreeNode'] = predecessor

    def __str__(self):
        return f"TreeNode: [{self.coordinates.x}, {self.coordinates.y}]"


def graph_to_tree(root: GraphNode) -> List[TreeNode]:
    tree: List[TreeNode] = [root.to_root_node()]

    queue: List[Tuple[GraphNode, TreeNode]] = [(root, root.to_root_node())]
    root.state = root.State.OPEN

    while len(queue) > 0:
        current = queue.pop(0)
        current_graph_node: GraphNode = current[0]
        predecessor: TreeNode = current[1]
        current_tree_node = current_graph_node.to_tree_node(predecessor)
        for neighbour in current_graph_node.neighbours:
            if neighbour.state == neighbour.State.FRESH:
                neighbour.state = neighbour.State.OPEN
                queue.append((neighbour, current_tree_node))
                tree.append(neighbour.to_tree_node(current_tree_node))
        current_graph_node.state = current_graph_node.State.CLOSE

    return tree


def path_to_root(end_node: TreeNode) -> List[Coordinates]:
    path: List[Coordinates] = [end_node.coordinates]
    node = end_node

    while node.predecessor is not None:
        predecessor = node.predecessor
        path.insert(0, predecessor.coordinates)
        node = predecessor

    return path

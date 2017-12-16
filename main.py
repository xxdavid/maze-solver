#!/usr/bin/env python3
import sys
from PIL import Image
import numpy as np

from graph import GraphNode, graph_to_tree, path_to_root
from common import Coordinates
from typing import Dict, List, Tuple


class MazeSolver:
    def __init__(self, image: Image, out_filename: str):
        self.image: Image = image
        self.size = self.image.size
        self.pixels = self.image_to_pixel_matrix()
        self.out_filename = out_filename

    def solve(self):
        gates = self.find_gates()
        graph = self.pixels_to_graph()
        start_node = next(node for node in graph if node.coordinates == gates[0])
        tree = graph_to_tree(start_node)
        end_node = next(node for node in tree if node.coordinates == gates[1])
        path = path_to_root(end_node)
        self.draw(path)

    def image_to_pixel_matrix(self):
        size = self.image.size
        array = np.array([x // 255 for x in self.image.getdata(1)])
        return array.reshape(size[1], size[0]).transpose()

    def find_gates(self) -> Tuple[Coordinates, Coordinates]:
        gates: List[Coordinates] = []

        # find horizontal gates
        for x in range(0, self.size[0]):
            for y in [0, self.size[1] - 1]:
                if self.pixels[x, y]:
                    gates.append(Coordinates(x, y))

        # find vertical gates
        for x in [0, self.size[0] - 1]:
            for y in range(0, self.size[1]):
                if self.pixels[x, y]:
                    gates.append(Coordinates(x, y))

        return gates[0], gates[-1]

    def pixels_to_graph(self) -> List[GraphNode]:
        nodes: Dict[Coordinates, GraphNode] = {}
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                if self.pixels[x, y]:
                    coords = Coordinates(x, y)
                    node = GraphNode(coords)
                    nodes[coords] = node

        for coords, node in nodes.items():
            # negative is for up and left, positive for down and right
            for direction in [-1, +1]:
                # 0 is for y (up and down), 1 for x (left and right)
                for axis in [0, 1]:
                    look_coords = Coordinates(
                        coords.x + abs(axis - 1) * direction,
                        coords.y + axis * direction
                    )
                    if look_coords in nodes:
                        node.add_neighbour(nodes[look_coords])

        return list(nodes.values())

    def draw(self, path: List[Coordinates]):
        pixel_map = self.image.load()
        for coords in path:
            pixel_map[coords.x, coords.y] = 150
        self.image.save(self.out_filename)


if __name__ == '__main__':
    input_filename: str = sys.argv[1]
    if len(sys.argv) < 3:
        output_filename = input_filename.rsplit(".", 1)[0] + "-path" + ".png"
    else:
        output_filename = sys.argv[2]
    MazeSolver(Image.open(input_filename), output_filename).solve()

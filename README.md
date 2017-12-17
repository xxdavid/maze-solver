# Maze solver
Just a very basic Python maze solver based on breadth-first search. It takes an input image of a maze and outputs the image with an optimal path drawn.
The output is written to a file specified or to `${input_file}-path`.

Run it with:
```bash
./main.py input_file [output_file]
```

## Limitations
* the maze must have black borders with white “gates” (start/end) in them
* the algorithm is pixel based and optimal results are achieved only on images where 1 pixel corresponds to 1 “block”

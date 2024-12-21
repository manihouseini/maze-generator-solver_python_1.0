# randomized depth first search

## Recursive implementation

The depth-first search algorithm of maze generation is frequently implemented using backtracking. This can be described with a following recursive routine:

    1. Given a current cell as a parameter
    2. Mark the current cell as visited
    3. While the current cell has any unvisited neighbour cells
        a. Choose one of the unvisited neighbours
        b. Remove the wall between the current cell and the chosen cell
        c. Invoke the routine recursively for the chosen cell
    which is invoked once for any initial cell in the area.

## Iterative implementation

A disadvantage of the first approach is a large depth of recursion – in the worst case, the routine may need to recur on every cell of the area being processed, which may exceed the maximum recursion stack depth in many environments. As a solution, the same backtracking method can be implemented with an explicit stack, which is usually allowed to grow much bigger with no harm.

    1. Choose the initial cell, mark it as visited and push it to the stack
    2. While the stack is not empty
        a. Pop a cell from the stack and make it a current cell
        b. If the current cell has any neighbours which have not been visited
            i. Push the current cell to the stack
            ii. Choose one of the unvisited neighbours
            iii. Remove the wall between the current cell and the chosen cell
            iv. Mark the chosen cell as visited and push it to the stack

# A star algorithom

What A\* Search Algorithm does is that at each step it picks the node according to a value-‘f’ which is a parameter equal to the sum of two other parameters – ‘g’ and ‘h’. At each step it picks the node/cell having the lowest ‘f’, and process that node/cell.

    g = the movement cost to move from the starting point to a given square on the grid, following the path generated to get there.

    h = the estimated movement cost to move from that given square on the grid to the final destination. This is often referred to as the heuristic

which is nothing but a kind of smart guess. We really don’t know the actual distance until we find the path, because all sorts of things can be in the way (walls, water, etc.).

    1.  Initialize the open list
    2.  Initialize the closed list
        put the starting node on the open list (you can leave its f at zero)

    3.  while the open list is not empty
        a) find the node with the least f on
       the open list, call it "q"

        b) pop q off the open list

        c) generate q's 8 successors and set their parents to q

        d) for each successor
            i) if successor is the goal, stop search

            ii) else, compute both g and h for successor
            successor.g = q.g + distance between successor and q
            successor.h = distance from goal to
            successor (This can be done using many ways, we will discuss three heuristics - Manhattan, Diagonal and Euclidean Heuristics)
            successor.f = successor.g + successor.h

            iii) if a node with the same position as successor is in the OPEN list which has a lower f than successor, skip this successor

            iV) if a node with the same position as
            successor  is in the CLOSED list which has
            a lower f than successor, skip this successor
            otherwise, add  the node to the open list
        end (for loop)

        e) push q on the closed list
    end (while loop)

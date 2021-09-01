# Value-iteration---A-star-algorithms-
This is an implementation of _Value Iteration_ and _A-star_ algorithms aiming to find the optimal path in a Grid World environment.

## Problem description
Supposing that an agent acts in the below enviroment, its goal is to find the optimal path from "Start" grid to positive (+1) exit.

<img src="https://github.com/george22294/Value-iteration---A-star-algorithms-/blob/main/problem%20description/grid_world.png">

The agent can move one grid per time (up, down right, left). But, when it decides the direction of its move, the actual result is non-deterministically determined. There is a certain probability distribution for this actual result which is:
- 0.8 to move to the desired grid
- 0.2 to move in vertical direction in relation with its desired movement

The movement to any grid has a cost of -0.04, except for the two exit grids:
- +1 for the "good" exit
- -1 for the "bad" exit

## Value Iteration
Given that there is a well-defined set of states (girds), a reward function (the above costs), a set of possible actions (possible movements) and a transition model (probability  distribution), we can use the [_Value Iteration_ algorithm](https://en.wikipedia.org/wiki/Markov_decision_process#Value_iteration) to get the _expected utility_ per state. 

By running the "iteration_value.py" script you can get the _expected utilies_ as an _xlsx_ file in the "utilities" directory. In this directory, there are already some files that were created by running the algorithm for different values of _γ_ parameter (a parameter of the algorithm equation): 0.9, 0.6, 0.2. The results are presented in the below image:

<img src="https://github.com/george22294/Value-iteration---A-star-algorithms-/blob/main/results/value_iteration/values.PNG">

You can also choose a different value for _γ_ (range 0.0 - 1.0), alternative starting point, grid size, exit points, reward function, transition model and walls location by changing their values in the "iteration_value.py" script where there are usefull comments.

## A-star
Given the aforementioned _expected utilities_ (let denote them with _U(s)_ where _s_ is a valid state), we can define a heuristic function for [_A-star_ algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) as:
_h(s) = -U(s)_

The resulting values using 0.9, 0.6, 0.2 _γ_ values are shown below:

<img src="https://github.com/george22294/Value-iteration---A-star-algorithms-/blob/main/results/a_star/heuristic_values.png">

Based on the +0.04 transition cost, the real transition costs from the "Start" grid were computed to be:

<img src="https://github.com/george22294/Value-iteration---A-star-algorithms-/blob/main/results/a_star/real_costs.PNG">

In this way, the heuristic values can be considered _valid_, because none of them overestimate the real costs.

After running, the "astar.py" script we can get the optimal path according to the specified _γ_ value (you can change this value in the code) as an _xlsx_ file in  "paths_from_A_star" directory. In order to run this script, it is needed to exist the corresponding _xlsx_ file (with the _expected utilities_) in "utilities" directory. 

The resulting paths for 0.9, 0.6, 0.2 _γ_ values are:

<img src="https://github.com/george22294/Value-iteration---A-star-algorithms-/blob/main/results/a_star/calculated_paths.png">

We can observe that as the value of _γ_ reducing (e.g 0.2), it is harder for the agent to expand the path towards the grid which finally will lead to the optimal path. This happens because agent becomes more "greedy" as _γ_ reducing. Nevertheless, the paths that are produced are all the same due to the _validity_ of the heuristic function which ensures that the optimal path will be found.

## Dependencies
To run the two scripts the below libraries are needed:
- NumPy 1.19.2
- XlsxWriter 1.3.7



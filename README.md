# This is a simulation of Conway's Game of Life

## Game interaction
Click on the grid to change it's color. Press Space to run step by step.

## Module usage:

```
import game_of_life as game
game.game_of_life()
```
This will open an empty grid.
To specify the initial grid state:
```
game.game_of_life(grid=grid_state)
```
where grid_state is a 2D numpy array.

To turn off the GUI, make a certain number of steps:
```
game.game_of_life(grid=grid_state, graphics=False, make_steps=3)
```
where make_steps - the number of steps to compute, until the function will return the grid's state.

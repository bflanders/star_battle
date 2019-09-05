# star_battle

When I battle stars, I win. 

## Star Battle

This game is a constraint problem somewhat related to [Sudoku](https://github.com/bflanders/sudoku_boards/). I wrote a solver for it. 

The game is based on [this Braingle site](https://www.braingle.com/games/starbattle/). Rules: place two stars in each region and so that there is only two stars in each column and row. 

The algorithm is basically: do a depth first search of all decision branches. If you're not careful (and I wasn't in the beginning), you may find yourself looping around a structure that is not supposed to have loops. The key is to find an order to your choices. 

My insight was to first come up with a list of all valid two-square selections for each region. Then you can select pairs in order (region 0, 1, 2, ... etc.). What I found was faster was to order your selection based on number of squares in each region (ascending order). That way your depth first search is on a shallower tree, at least in the "top" part of the tree. 


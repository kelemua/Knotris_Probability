# Knotris_Probability
This repository houses the code for the Python probability simulations for the game Knotris. To play the game, check out izook.github.io/knotris/! To learn about the game mechanics, read our Math Horizons article, Knotris: A Game Inspired by Knot Theory at https://www.tandfonline.com/doi/full/10.1080/10724117.2020.1809238.
  - Fill Hole 
      - Contains functions that calculate the probability of filling a hole in Knotris 
  - Fill Row
      - Executes the filling a row alogrithm where:
         - Given a bag of knot mosaic tiles
         - Rows are assembled using all possible permutations and rotations of tiles from the bag
         - Only the suitaly connected rows are kept
         - Outputs the unique lower boundary condition of the realizable suitably connected row and respective frequency
      - The purpose of this was to determine how constraints on the tile bag impacted gameplay. 

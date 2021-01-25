# Knotris_Probability
This repository houses the code for the Python probability simulations for the game Knotris. To play the game, check out izook.github.io/knotris/! To learn about the game mechanics, read our Math Horizons article, Knotris: A Game Inspired by Knot Theory at https://www.tandfonline.com/doi/full/10.1080/10724117.2020.1809238.

  -Filling a Row Files
      - Execute the Filling a Row alogrithm where:
         - Given a bag of knot mosaic tiles
         - Rows are assembled using all possible permutations and rotations of tiles from the bag
         - Only the suitaly connected rows are kept
         - Outputs the unique lower boundary condition of the realizable suitably connected row and respective frequency
      - The purpose of this was to determine how constraints on the tile bag impacted gameplay. 
        - Filling a Row Alogrithm--Gamebag: applies the algorithm to the gamebag
        - Filling a Row Algorithm--6-&7-Tile Bags: applies the algorithm to 6-&7-Tiel Bags 
  - Fill Hole
      - Calculate the probability of filling a hole in Knotris 
        - The probability of 1 through 3 tile hole types where are all edges are determined are complete
        - I'm stil working on:
            - Some of the hole 3 tile hole types with free edges
            - Calculating both the randumb and smart probability for filling holes 
            - Creating an some interface so a user can enter a hole type in a more user friendly way and the probability of filling the hole is returned 

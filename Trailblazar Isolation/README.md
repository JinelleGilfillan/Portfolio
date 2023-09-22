# Trailblazer Isolation

This project implements game playing agents for a variant of the game Isolation.

## Noteable Files
1. `isolation.py`: Includes the `Board` class and a function for printing out a game as text. 
2. `notebook.ipynb`: The code to implement the required methods for the agents.
3. `player_submission_tests.py`: Sample tests to validate the agents locally.
4. `test_players.py`: Contains 2 player types to test agents locally:
    - `RandomPlayer` - chooses a legal move randomly from among the available legal moves
    - `HumanPlayer` - allows *YOU* to play against the AI in terminal (else use `InteractiveGame` in jupyter)
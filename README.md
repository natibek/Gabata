# Gabata Project

This is an implementation of the Gabata (Mancala) game using the Ethiopian rule set. The project uses python to
implement game rules and create a bot. The user interface is designed using Tkinter and there is a version already
available that uses pygame as a first draft. This has slight issues with the UI which don't affect game play (but are annoying).

# Gabata Rules

The game is for 2 players. Each player has their side of the board with 6 playable slots and 1 deposit slot.

At the beginning of the game each player has 4 marbles in their playable slots.
Player 1 starts.

The current player can choose any of their playable slots to start a move. To make a move pick up all the marbles from
the chosen playable slot and start dropping one into the next slots (not including opponents deposit slot) going counter
clockwise.

(Note: where you land is where you place the last marble!!)

- If you land on your deposit slot, it is still your turn.
- If you land in any of your opponents playable slots, it is their turn.
- If you land on your own side in a non-empty playable slot, pick up the marbles from the slot and continue the same
  process.
- If you land on your own side in an empty slot,
  - If the opponent slot symmetrically opposite from your landing slot is not empty, pick up the last marble, add to said opponent slot, pick up all the marbles,
    and continue from said opponents side.
  - If the opponent slot symmetrically opposite from your landing slot is empty, it is your opponent's turn.

The Player with more marbles in their deposit slot wins.

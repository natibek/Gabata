class Node:
    """
    Node class for the creation of tree nodes for bot
    """

    def __init__(self, board, depth):
        """
        Node objects are instantiated with a board, depth, children, move_made,
        and value (score) attributes

        move_made (int): stores the move made to result in the nodes state
        value (int): stores score of the on the board for the final state

        Inputs:
            board (Board): current board
            depth (int): depth of node within the tree
        """
        self.board = board
        self.depth = depth

        if len(board.sequence) == 1:
            self.player = board.sequence[-1]
        else:
            self.player = board.sequence[-2]

        self.children = []
        self.move_made = None  # move made to result in board state
        self.value = None

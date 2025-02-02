from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
import math
from math import log, sqrt

# Tree size of 1000 required
num_nodes = 50
explore_constant = 2

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """

    # While the game is still alive 
    while not board.is_ended(state):
        # Return node if there are untried actions
        if node.untried_actions:
            return node, state

        # Establish bot and opponent
        current_player = board.current_player(state)
        is_opponent = (current_player != bot_identity)

        # Select the best child based on UCB score
        best_child = max(
            node.child_nodes.values(),
            key=lambda child: ucb(child, is_opponent),
            default=None
        )

        # Move to the best child node or return if no children exist
        if best_child:
            node = best_child
            state = board.next_state(state, node.parent_action)
        else:
            break

    return node, state

def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node: The added child node
        state: The state associated with that node

    """

    # Start with an untried action
    action = node.untried_actions.pop()
    
    # Next game state
    next_state = board.next_state(state, action)
    
    # Create a new child node
    child = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
    
    # Add the new child node to the current node
    node.child_nodes[action] = child
    return child, next_state


def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """

    """ Perform a limited rollout. """

    # Rollout as long as game goes on 
    while not board.is_ended(state):
        # Choose an action and play it if it is legal
        legal_actions = board.legal_actions(state)
        action = choice(legal_actions)
        # Next game state
        state = board.next_state(state, action)
    
    return state

def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    # While true 
    while node is not None:
        # Update visit count
        node.visits += 1
        # Bot wins - add it
        if won:
            node.wins += 1
        # Back to parent node
        node = node.parent

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """

    # If node hasn't been visited
    if node.visits == 0:
        return float("inf")
    
    # Node win rate
    win_rate = node.wins / node.visits

    # Adjust win rate if last action was performed by opponent
    if is_opponent:
        win_rate = 1 - win_rate

    # UCB Function 
    return win_rate + explore_constant * sqrt(log(node.parent.visits) / node.visits)

def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree
    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    """
    # Best action based on number of visits
    best_action = max(
        # Starts with root node and navigates through each child node and their respective visits
        root_node.child_nodes.items(), 
        key=lambda 
        item: item[1].visits
        )[0]
    return best_action

def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Do MCTS - This is all you!
        # ...

        # Selection: Traverse Nodes 
        node, state = traverse_nodes(node, board, state, bot_identity)

        # Expansion: Expand Leaf 
        if node.untried_actions:
            node, state = expand_leaf(node, board, state)

        # Simulation: Rollout 
        final_state = rollout(board, state)

        # Backpropagation: Update Simulation Result
        won = is_win(board, final_state, bot_identity)
        backpropagate(node, won)

    # Return best action
    best_action = get_best_action(root_node)
    
    print(f"Action chosen: {best_action}")
    return best_action
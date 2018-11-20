import time

from Move import Move
from Node import *


class MCTS:

    def __init__(self, statemanager, initial_state, target_policy, default_policy, tree_policy, M=10):
        self.statemanager = statemanager
        self.root = initial_state
        self.tree = Node(self.root)
        self.M = M
        self.policy = target_policy
        self.default_policy = default_policy
        self.tree_policy = tree_policy

    # Estimating the value of a leaf node in the tree by doing a rollout simulation using
    # the default policy from the leaf node’s state to a final state.
    def leaf_evaluation(self, node):
        wins = 0
        losses = 0

        initial_state = node.content
        start_time = time.time()
        time_limit = 5
        for i in range(self.M):  # num rollouts
            #if time.time()-start_time > time_limit: break
            state = initial_state.__copy__()
            current_node : Node= node
            while not self.statemanager.is_final_state(state):
                if len(self.statemanager.get_moves(state)) == 0: break
                move = self.default_policy.chose(state, self.statemanager.get_moves(state),
                                                 initial_state.initial_player)
                state = self.statemanager.do_move(state, move)
                # next = current_node.addChild(move, state)
                # current_node = next

            if self.statemanager.is_win(state, initial_state.initial_player):  # state.winnerF() == self.root.player:
                wins += 1
            else:
                losses += 1

            self.backpropagation(current_node, (wins - losses) / (wins + losses))

        return (wins - losses) / (wins + losses)

    def pick_action(self, state):
        self.root = Node(state)
        for i in range(self.M):
            self.tree_search(self.root)

        ratings = sorted(self.root.edges, key=lambda edge: edge.quality(), reverse=True)
        print([r.quality() for r in ratings])
        return ratings[0].content

    # Traversing the tree from the root to a leaf node by using the tree policy
    def tree_search(self, node):

        if len(node.edges) != len(self.statemanager.get_moves(node.content)):  # and not self.statemanager.is_final_state(node.content):
            # print("Expanding",node)
            self.node_expansion(node)  # Expand nodes one layer
            # node.visits += 1
            for edge in node.edges:  # Get all the moves / edges
                to_node = edge.toNode
                evaluation = self.leaf_evaluation(to_node)  # evaluate each to-node, aka the new nodes
                self.backpropagation(to_node, evaluation)  # Backpropagate

        choices = [e.content for e in node.edges]

        choice :Move= self.tree_policy.chose(node, choices, node.content.initial_player)
        node.visits +=1
        choice.visits+=1

        return choice

    # Generating some or all child states of a parent state, and then connecting the tree
    # node housing the parent state (a.k.a. parent node) to the nodes housing the child states (a.k.a. child
    # nodes).
    def node_expansion(self, node):
        moves = self.statemanager.get_moves(node.content)
        for m in moves:
            if m not in list(map(lambda edge: edge.content, node.edges)):
                node.addChild(m, m.result)

    # Passing the evaluation of a final state back up the tree, updating relevant data (see
    # course lecture notes) at all nodes and edges on the path from the final state to the tree root.
    def backpropagation(self, node, evaluation):

        while node.parent:
            node.visits += 1
            parent = node.parent
            edge_to = parent.getEdgeTo(node)
            edge_to.content.reward += evaluation
            edge_to.content.visits += 1
            node = parent

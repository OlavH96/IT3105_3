import random
import time

import numpy as np

from Move import Move
from Node import *
from TrainingCase import *
from TrainingCase import __create_training_case__


class MCTS:

    def __init__(self, statemanager, initial_state, target_policy, default_policy, tree_policy, M=10):
        self.initial_state = initial_state
        self.statemanager = statemanager
        self.root = initial_state
        self.tree = Node(self.root)
        self.M = M
        self.target_policy = target_policy
        self.default_policy = default_policy  # aka Behaviour policy
        self.tree_policy = tree_policy

    # Estimating the value of a leaf node in the tree by doing a rollout simulation using
    # the default policy from the leaf node’s state to a final state.
    def leaf_evaluation(self, node):

        initial_state = node.content

        state: HEX = initial_state.__copy__()

        while not self.statemanager.is_final_state(state):

            epsilon = 0.1

            if random.random() < epsilon:  # do random choice
                move = random.choice(self.statemanager.get_moves(state))
            else:
                move = self.default_policy.chose(state, self.statemanager.get_moves(state),
                                                 initial_state.initial_player)
            state = self.statemanager.do_move(state, move)

        if self.statemanager.is_win(state, initial_state.initial_player):
            return 1
        else:
            return -1

    def pick_action(self, state, replay_buffer):
        self.root = state
        time_limit = 5 # 5 seconds
        time_start = time.time()
        for i in range(self.M):
            self.tree_search(self.root)
            if time.time() - time_start > time_limit: break

        dist = self.root.get_visit_count_distribution()
        training_case: TrainingCase = __create_training_case__(self.root.content, dist)
        replay_buffer.add(training_case)

        # for e in self.root.edges:
        #     print(e)
        reverse = True
        #reverse = state.content.player == self.initial_state.player
        ratings = sorted(self.root.edges, key=lambda edge: edge.content.visits, reverse=reverse)
        #print([r.content.visits for r in ratings])

        self.tree = self.root
        return ratings[0]

    # Traversing the tree from the root to a leaf node by using the tree policy
    def tree_search(self, node):

        if len(node.edges) == 0:  # found leaf
            self.node_expansion(node)  # Expand nodes one layer
            eval: float = self.leaf_evaluation(node)
            self.backpropagation(node, eval)

        else:  # Use tree policy to chose next node
            choices = [e.content for e in node.edges]

            choice: Move = self.tree_policy.chose(node, choices, node.content.initial_player)
            child = node.getChildByEdge(choice)
            #self.root = child
            self.tree_search(child)  # continue

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

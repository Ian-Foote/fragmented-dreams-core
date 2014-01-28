from collections import defaultdict, namedtuple
from random import randrange

from . import exceptions


class Board:
    def __init__(self, worlds=None, edges=None):
        if worlds is None:
            worlds = ()
        self.worlds = {world.node: world for world in worlds}

        self.neighbours = defaultdict(set)
        if edges is not None:
            for edge in edges:
                self.add_edge(edge)

    def add_edge(self, edge):
        x, y = edge
        self.neighbours[x].add(y)
        self.neighbours[y].add(x)

    def remove_edge(self, edge):
        x, y = edge
        self.neighbours[x].remove(y)
        self.neighbours[y].remove(x)


ResourcesBase = namedtuple(
    'ResourcesBase', ['metal', 'biomass', 'energy', 'exotic', 'level'])


class Resources(ResourcesBase):
    def __new__(cls, metal=0, biomass=0, energy=0, exotic=0, level=0):
        return super().__new__(cls, metal, biomass, energy, exotic, level)

    @classmethod
    def random_world(cls, total=None):
        if total is None:
            total = randrange(1, 7)

        resources = [0, 0, 0, 0]
        for i in range(total):
            resources[randrange(4)] += 1

        metal, biomass, energy, exotic = resources
        return super().__new__(cls, metal, biomass, energy, exotic, level=0)

    @classmethod
    def terraformed(cls):
        resources = [1, 1, 1, 1]
        resources[randrange(4)] += 1
        resources[randrange(4)] += 1
        metal, biomass, energy, exotic = resources
        return super().__new__(cls, metal, biomass, energy, exotic, level=1)

    @classmethod
    def neutral_homeworld(cls):
        resources = [1, 1, 1, 1]
        resources[randrange(4)] += 1
        resources[randrange(4)] += 1
        metal, biomass, energy, exotic = resources
        return super().__new__(cls, metal, biomass, energy, exotic, level=2)

    @classmethod
    def player_homeworld(cls):
        resources = [2, 2, 2, 2]
        resources[randrange(4)] += 1
        resources[randrange(4)] += 1
        metal, biomass, energy, exotic = resources
        return super().__new__(cls, metal, biomass, energy, exotic, level=3)


class World:
    def __init__(self, node, fleets=None):
        if fleets is None:
            fleets = randrange(8)

        self.node = node
        self.fleets = fleets
        self.resources = Resources.random_world()
        self.player = 0
        self.shield = False

    @classmethod
    def player_homeworld(cls, node, fleets=20, *, player):
        obj = cls(node, fleets=fleets)
        obj.resources = Resources.player_homeworld()
        obj.player = player
        return obj


class Player:
    def __init__(self, player=1):
        self.player = player
        self.metal = 0
        self.biomass = 0
        self.energy = 0
        self.exotic = 0

    def controls_world(self, board, world):
        try:
            world = board.worlds[world]
        except KeyError:
            msg = 'World {} does not exist!'.format(world)
            raise exceptions.InvalidWorldError(msg)

        return world.player == self

    def valid_destination(self, board, start, world):
        try:
            board.worlds[world]
        except KeyError:
            msg = 'Destination world {} does not exist.'.format(world)
            raise exceptions.InvalidWorldError(msg)

        return world not in board.neighbours[start]

    def tannhauser(self, board, start, destination):
        if self.exotic < 5:
            msg = 'Tannhauser special has not been researched.'
            raise exceptions.NotResearchedError(msg)

        if not self.controls_world(board, start):
            msg = 'You must control the start world {}.'.format(start)
            raise exceptions.InvalidTargetError(msg)

        if not self.valid_destination(board, start, destination):
            msg = ('Destination world {} is already connected '
                   'to the start world {}.'.format(start, destination))
            raise exceptions.InvalidDestinationError(msg)

        board.add_edge((start, destination))
        self.exotic = 0

    def terraform(self, board, world):
        if self.biomass < 5:
            msg = 'Terraforming special has not been researched.'
            raise exceptions.NotResearchedError(msg)

        if not self.controls_world(board, world):
            msg = 'You must control the target world {}.'.format(world)
            raise exceptions.InvalidTargetError(msg)

        world = board.worlds[world]
        world.resources = Resources.terraformed()
        self.biomass = 0

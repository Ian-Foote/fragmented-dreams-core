import pytest

from core.core import Board, Player, World
from core import exceptions


def test_player():
    player = Player()
    assert player.player == 1
    assert player.metal == 0
    assert player.biomass == 0
    assert player.energy == 0
    assert player.exotic == 0


class TestControlsWorld:
    def test_controls_world(self):
        player = Player()
        worlds = [World.player_homeworld((0, 1), player=player)]
        board = Board(worlds)

        assert player.controls_world(board, (0, 1)) is True

    def test_uncontrolled(self):
        player = Player()
        worlds = [World((0, 0))]
        board = Board(worlds)

        assert player.controls_world(board, (0, 0)) is False

    def test_nonexistent(self):
        player = Player()
        board = Board()

        with pytest.raises(exceptions.InvalidWorldError):
            player.controls_world(board, (0, 1))


class TestValidDestination:
    def test_valid_destination(self):
        player = Player()
        worlds = [
            World.player_homeworld((0, 1), player=player),
            World((0, 2)),
        ]
        board = Board(worlds)

        assert player.valid_destination(board, (0, 1), (0, 2)) is True

    def test_invalid_destination(self):
        player = Player()
        worlds = [
            World((0, 0)),
            World.player_homeworld((0, 1), player=player),
        ]
        edges = {((0, 0), (0, 1))}
        board = Board(worlds, edges)

        assert player.valid_destination(board, (0, 1), (0, 0)) is False

    def test_destination_nonexistent(self):
        player = Player()
        worlds = [
            World.player_homeworld((0, 1), player=player),
        ]
        board = Board(worlds)

        with pytest.raises(exceptions.InvalidWorldError):
            player.valid_destination(board, (0, 1), (0, 0))


class TestTannhauser:
    def test_tannhauser(self):
        player = Player()
        player.exotic = 5
        worlds = [
            World((0, 0)),
            World.player_homeworld((0, 1), player=player),
            World((0, 2)),
        ]
        edges = {((0, 0), (0, 1)), ((0, 0), (0, 2))}
        board = Board(worlds, edges)

        player.tannhauser(board, start=(0, 1), destination=(0, 2))
        assert (0, 2) in board.neighbours[(0, 1)]
        assert player.exotic == 0

    def test_insufficient_resources(self):
        player = Player()
        player.exotic = 4
        worlds = [
            World((0, 0)),
            World.player_homeworld((0, 1), player=player),
            World((0, 2)),
        ]
        edges = {((0, 0), (0, 1)), ((0, 0), (0, 2))}
        board = Board(worlds, edges)

        with pytest.raises(exceptions.NotResearchedError):
            player.tannhauser(board, start=(0, 1), destination=(0, 2))

    def test_does_not_control_start(self):
        player = Player()
        player.exotic = 5
        worlds = [
            World((0, 0)),
            World.player_homeworld((0, 1), player=player),
            World((0, 2)),
        ]
        edges = {((0, 0), (0, 1)), ((0, 0), (0, 2))}
        board = Board(worlds, edges)

        with pytest.raises(exceptions.InvalidTargetError):
            player.tannhauser(board, start=(0, 2), destination=(0, 1))

    def test_worlds_connected(self):
        player = Player()
        player.exotic = 5
        worlds = [
            World((0, 0)),
            World.player_homeworld((0, 1), player=player),
            World((0, 2)),
        ]
        edges = {((0, 0), (0, 1)), ((0, 0), (0, 2))}
        board = Board(worlds, edges)

        with pytest.raises(exceptions.InvalidDestinationError):
            player.tannhauser(board, start=(0, 1), destination=(0, 0))


class TestTerraforming:
    def test_terraform(self):
        player = Player()
        player.biomass = 5
        world = World((0, 0))
        world.player = player
        board = Board([world])

        player.terraform(board, (0, 0))
        assert world.resources.level == 1
        assert player.biomass == 0

    def test_insufficient_resources(self):
        player = Player()
        player.biomass = 4
        world = World((0, 0))
        world.player = player
        board = Board([world])

        with pytest.raises(exceptions.NotResearchedError):
            player.terraform(board, (0, 0))

    def test_not_controlled_world(self):
        player = Player()
        player.biomass = 5
        board = Board([World((0, 0))])

        with pytest.raises(exceptions.InvalidTargetError):
            player.terraform(board, (0, 0))

    def test_homeworld(self):
        player = Player()
        player.biomass = 5
        world = World.player_homeworld((0, 0), player=player)
        board = Board([world])

        with pytest.raises(exceptions.InvalidTargetError):
            player.terraform(board, (0, 0))


class TestDefenceNet:
    def test_defence_net(self):
        player = Player()
        player.metal = 5
        world = World((0, 0))
        world.player = player
        board = Board([world])

        player.defence_net(board, (0, 0))
        assert world.shield is True
        assert player.metal == 0

    def test_insufficient_resources(self):
        player = Player()
        player.metal = 4
        world = World((0, 0))
        world.player = player
        board = Board([world])

        with pytest.raises(exceptions.NotResearchedError):
            player.defence_net(board, (0, 0))

    def test_already_exists(self):
        player = Player()
        player.metal = 5
        world = World((0, 0))
        world.shield = True
        world.player = player
        board = Board([world])

        with pytest.raises(exceptions.InvalidTargetError):
            player.defence_net(board, (0, 0))

    def test_not_controlled_world(self):
        player = Player()
        player.metal = 5
        world = World((0, 0))
        board = Board([world])

        with pytest.raises(exceptions.InvalidTargetError):
            player.defence_net(board, (0, 0))


class TestStellarBomb:
    def test_stellar_bomb(self):
        player = Player()
        player.energy = 5

        world = World((0, 1), fleets=8)
        worlds = [World.player_homeworld((0, 0), player=player), world]
        edges = [((0, 0), (0, 1))]
        board = Board(worlds, edges)

        player.stellar_bomb(board, (0, 1))
        assert world.fleets == 4
        assert player.energy == 0

    def test_insufficient_resources(self):
        player = Player()
        player.energy = 4

        world = World((0, 1))
        worlds = [World.player_homeworld((0, 0), player=player), world]
        edges = [((0, 0), (0, 1))]
        board = Board(worlds, edges)

        with pytest.raises(exceptions.NotResearchedError):
            player.stellar_bomb(board, (0, 1))

    def test_controlled_target(self):
        player = Player()
        player.energy = 5
        homeworld = World.player_homeworld((0, 0), player=player)
        target = World((0, 1))
        target.player = player
        edges = [((0, 0), (0, 1))]

        board = Board([homeworld, target], edges)

        with pytest.raises(exceptions.InvalidTargetError):
            player.stellar_bomb(board, (0, 0))

    def test_invalid_target(self):
        player = Player()
        player.energy = 5

        world = World((0, 2))
        worlds = [
            World.player_homeworld((0, 0), player=player),
            World((0, 1)),
            world,
        ]
        edges = [((0, 0), (0, 1)), ((0, 1), (0, 2))]
        board = Board(worlds, edges)

        with pytest.raises(exceptions.InvalidTargetError):
            player.stellar_bomb(board, (0, 2))

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


def test_tannhauser():
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


def test_tannhauser_insufficient_resources():
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


def test_tannhauser_player_does_not_control_start():
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


def test_tannhauser_worlds_connected():
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


def test_player_controls_world():
    player = Player()
    worlds = [World.player_homeworld((0, 1), player=player)]
    board = Board(worlds)

    assert player.controls_world(board, (0, 1)) is True


def test_player_controls_world_false():
    player = Player()
    worlds = [World((0, 0))]
    board = Board(worlds)

    assert player.controls_world(board, (0, 0)) is False


def test_player_controls_world_nonexistent():
    player = Player()
    board = Board()

    with pytest.raises(exceptions.InvalidWorldError):
        player.controls_world(board, (0, 1))


def test_player_valid_destination():
    player = Player()
    worlds = [
        World.player_homeworld((0, 1), player=player),
        World((0, 2)),
    ]
    board = Board(worlds)

    assert player.valid_destination(board, (0, 1), (0, 2)) is True


def test_player_invalid_destination():
    player = Player()
    worlds = [
        World((0, 0)),
        World.player_homeworld((0, 1), player=player),
    ]
    edges = {((0, 0), (0, 1))}
    board = Board(worlds, edges)

    assert player.valid_destination(board, (0, 1), (0, 0)) is False


def test_player_valid_destination_nonexistent():
    player = Player()
    worlds = [
        World.player_homeworld((0, 1), player=player),
    ]
    board = Board(worlds)

    with pytest.raises(exceptions.InvalidWorldError):
        player.valid_destination(board, (0, 1), (0, 0))


def test_terraform():
    player = Player()
    player.biomass = 5
    world = World((0, 0))
    world.player = player
    board = Board([world])

    player.terraform(board, (0, 0))
    assert world.resources.level == 1
    assert player.biomass == 0


def test_terraform_insufficient_resources():
    player = Player()
    player.biomass = 4
    world = World((0, 0))
    world.player = player
    board = Board([world])

    with pytest.raises(exceptions.NotResearchedError):
        player.terraform(board, (0, 0))


def test_terraform_not_controlled_world():
    player = Player()
    player.biomass = 5
    board = Board([World((0, 0))])

    with pytest.raises(exceptions.InvalidTargetError):
        player.terraform(board, (0, 0))

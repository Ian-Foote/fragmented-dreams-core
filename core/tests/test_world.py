from core.core import Player, World


def test_world():
    node = (0, 0)
    fleets = 5
    world = World(node, fleets)
    assert world.node == node
    assert world.fleets == fleets
    assert world.resources.level == 0
    assert world.shield is False


def test_world_random_fleets():
    node = (0, 0)
    world = World(node)
    assert 0 <= world.fleets <= 7


def test_player_homeworld():
    node = (3, 2)
    player = Player()
    world = World.player_homeworld(node, player=player)
    assert world.node == node
    assert world.fleets == 20
    assert world.resources.level == 3
    assert world.player == player

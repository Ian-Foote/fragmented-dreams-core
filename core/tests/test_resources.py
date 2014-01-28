from core.core import Resources


def test_resources():
    resources = Resources(metal=2, biomass=1, energy=0, exotic=0)
    assert resources.metal == 2
    assert resources.biomass == 1
    assert resources.energy == 0
    assert resources.exotic == 0
    assert resources.level == 0


def test_resources_default():
    resources = Resources()
    assert resources.metal == 0
    assert resources.biomass == 0
    assert resources.energy == 0
    assert resources.exotic == 0
    assert resources.level == 0


def test_resources_random_world():
    random_world = Resources.random_world()
    *resources, level = random_world
    assert random_world.level == 0
    assert 1 <= sum(resources) <= 6


def test_resources_random_world_total():
    total_resources = 4
    random_world = Resources.random_world(total=total_resources)
    *resources, level = random_world
    assert sum(resources) == total_resources


def test_resources_terraformed():
    terraformed = Resources.terraformed()
    *resources, level = terraformed
    assert terraformed.level == 1
    assert sum(resources) == 6
    assert min(resources) == 1


def test_resources_neutral_homeworld():
    neutral_homeworld = Resources.neutral_homeworld()
    *resources, level = neutral_homeworld
    assert neutral_homeworld.level == 2
    assert sum(resources) == 6
    assert min(resources) == 1


def test_resources_player_homeworld():
    player_homeworld = Resources.player_homeworld()
    *resources, level = player_homeworld
    assert player_homeworld.level == 3
    assert sum(resources) == 10
    assert min(resources) == 2

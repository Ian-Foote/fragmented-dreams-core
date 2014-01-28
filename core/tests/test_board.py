from core.core import Board, World


def test_empty_board():
    board = Board()
    assert board.worlds == {}
    assert board.neighbours == {}


def test_board_nodes():
    worlds = [World((0, 0)), World((0, 1)), World((0, 2))]
    board = Board(worlds=worlds)
    assert board.worlds == {world.node: world for world in worlds}


def test_board_neighbours():
    edges = {((0, 0), (0, 1)), ((0, 1), (0, 2))}
    board = Board(edges=edges)
    assert board.neighbours[(0, 1)] == {(0, 0), (0, 2)}


def test_board_add_edge():
    edges = {((0, 0), (0, 1))}
    board = Board(edges=edges)

    new_edge = ((0, 0), (0, 2))
    board.add_edge(new_edge)
    assert board.neighbours[(0, 0)] == {(0, 1), (0, 2)}


def test_board_remove_edge():
    edges = {((0, 0), (0, 1)), ((0, 1), (0, 2))}
    board = Board(edges=edges)

    old_edge = ((0, 0), (0, 1))
    board.remove_edge(old_edge)
    assert board.neighbours[(0, 0)] == set()

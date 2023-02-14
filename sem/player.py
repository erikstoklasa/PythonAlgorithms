from array import ArrayType, array
import draw as Drawer
import sys
import random
import copy
import os
import base as Base
from typing import List, Tuple, Dict

# implement you player here. If you need to define some classes, do it also here. Only this file is to be submitted to Brute.
# define all functions here


class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self, board, name, color)
        self.algorithmName = "BorekStavitel"

    actions = ["lldd", "dlld", "ddll", "lddl", "dldl", "ldld"]

    def move(self):
        """return list of moves:
        []  ... if the player cannot move
        [ [r1,c1,piece1], [r2,c2,piece2] ... [rn,cn,piece2] ] -place tiles to positions (r1,c1) .. (rn,cn)
        """
        game_finished = self.board_is_full()
        if game_finished:
            return []

        next_move_list = []
        output = []

        list_of_placed_cells = self.get_placed_cells()  # chosen cell coords
        for ri, ci in list_of_placed_cells:
            next_move_list = self.get_list_of_next_moves(ri, ci)
            if not next_move_list:
                next_move_list = self.get_list_of_next_moves(
                    ri, ci, try_all_directions=True
                )
            if next_move_list:
                for mRi, mCi, cell_type in next_move_list:
                    moveToAppend = [mRi, mCi, cell_type]
                    output.append(moveToAppend)
                return output

        return []

    def get_list_of_next_moves(
        self, ri: int, ci: int, try_all_directions: bool = False
    ) -> List[Tuple[int, int, str]]:
        next_moves: List[Tuple[int, int, str]] = []

        forced_moves = self.get_forced_moves()
        if forced_moves == -1:
            return []
        if forced_moves and len(forced_moves) > 0:
            print("doing forced moves", forced_moves)
            return self.filter_duplicite_moves(forced_moves)

        cell: str = self.board[ri][ci]
        if try_all_directions:
            directions = range(4)
        else:
            directions = self.get_my_direcitons_for_cell(cell, self.myColor)
        possible_moves: List[Tuple[int, int, str]] = []
        for d in directions:
            riCh, ciCh = self.neighbors[d]
            newRi = ri + riCh
            newCi = ci + ciCh
            if self.inside(newRi, newCi) and self.is_free_space(newRi, newCi):
                direction_to_connect: int = self.my2other[d]
                if try_all_directions:
                    cell_type_candidates = self.tiles
                else:
                    cell_type_candidates: List[str] = self.get_cells_which_connect_to(
                        direction_to_connect, self.myColor
                    )
                for ctc in cell_type_candidates:
                    if self.can_place_cell_neighbors_check(
                        ctc, newRi, newCi
                    ):  
                        possible_moves.append((newRi, newCi, ctc))
                    else:
                        print("Can't place", newRi, newCi, ctc)
        if len(possible_moves) > 0:
            next_moves.append(random.choice(possible_moves))
            modified_board = self.get_moddified_board(self.board, next_moves)
            forced_moves = self.get_forced_moves(modified_board)
            if forced_moves == -1:
                return []
            if forced_moves:
                print("appending forced moves", forced_moves)
                next_moves.extend(forced_moves)
        if len(next_moves) > 0:
            print("doing a normal move", next_moves)
        return self.filter_duplicite_moves(next_moves)

    def filter_duplicite_moves(self, moves_list):
        for move in moves_list:
            while moves_list.count(move) > 1:
                moves_list.remove(move)
        return moves_list

    def get_forced_moves(self, board=None):  # -> List[Tuple[int, int, str]]
        if not board:
            board = self.board
        forced_moves: List[Tuple[int, int, str]] = []
        i_p_map: List[List[Dict[str, int]]] = self.get_incoming_paths_map(board)
        for ri in range(len(i_p_map)):
            for ci in range(len(i_p_map[ri])):
                if (
                    i_p_map[ri][ci]["l"] == 2 or i_p_map[ri][ci]["d"] == 2
                ) and self.is_free_space(ri, ci, board):
                    # find compatible cells which connect to the neighbors
                    for tile in self.tiles:
                        if self.can_place_cell_neighbors_check(tile, ri, ci, board):
                            forced_moves.append((ri, ci, tile))
                            break
                    if len(forced_moves) > 0:
                        # lastForcedMove = forced_moves[len(forced_moves) - 1]
                        modified_board = self.get_moddified_board(board, forced_moves)
                        f_m_for_modified_board = self.get_forced_moves(modified_board)
                        if f_m_for_modified_board == -1:
                            return -1
                        # checking for already existing SAME actions
                        for moveToAdd in f_m_for_modified_board:
                            if moveToAdd not in forced_moves:
                                forced_moves.append(moveToAdd)
                if i_p_map[ri][ci]["l"] > 2 or i_p_map[ri][ci]["d"] > 2:
                    return -1

        return forced_moves

    def get_moddified_board(self, board, action_list):
        modified_board = copy.deepcopy(board)
        for ri, ci, cell in action_list:
            modified_board[ri][ci] = cell
        return modified_board

    def get_incoming_paths_map(self, board=None) -> List[List[Dict[str, int]]]:
        if not board:
            board = self.board
        i_p_map: List[List[Dict[str, int]]] = [
            [{}] * len(board[0]) for _ in range(len(board))
        ]

        for ri in range(len(board)):
            for ci in range(len(board[ri])):
                cell_stats: Dict[str, int] = self.get_incoming_paths_for_cell(
                    ri, ci, board
                )
                i_p_map[ri][ci] = cell_stats

        return i_p_map

    def get_incoming_paths_for_cell(
        self, ri: int, ci: int, board=None
    ) -> Dict[str, int]:
        if not board:
            board = self.board
        light_incoming_count: int = 0
        dark_incoming_count: int = 0
        for direction in range(4):
            riCh, ciCh = self.neighbors[direction]
            newRi = ri + riCh
            newCi = ci + ciCh
            direction_to_connect = self.my2other[direction]
            if self.inside(newRi, newCi) and not self.is_free_space(
                newRi, newCi, board
            ):
                neighbour_cell = board[newRi][newCi]
                if neighbour_cell[direction_to_connect] == "l":
                    light_incoming_count += 1
                elif neighbour_cell[direction_to_connect] == "d":
                    dark_incoming_count += 1
        return {"l": light_incoming_count, "d": dark_incoming_count}

    def can_place_cell_neighbors_check(
        self, cell_type: str, ri: int, ci: int, board=None
    ) -> bool:
        if not board:
            board = self.board
        if ri == 3 and ci == 10:
            print("brpt")
        for direction in range(4):
            direction_to_connect: int = self.my2other[direction]
            riCh, ciCh = self.neighbors[direction]
            newRi = ri + riCh
            newCi = ci + ciCh
            if self.inside(newRi, newCi):
                current_neighbor = board[newRi][newCi]
                space_is_free: bool = self.is_free_space(newRi, newCi, board)
                cells_connect: bool = (
                    current_neighbor[direction_to_connect] == cell_type[direction]
                )
                if (not space_is_free) and (not cells_connect):
                    return False
        return True

    def get_cells_which_connect_to(self, direction: int, color: str) -> List[str]:
        cells: List[str] = []
        for tile in self.tiles:
            if tile[direction] == color:
                cells.append(tile)
        return cells

    def is_free_space(self, ri: int, ci: int, board=None) -> bool:
        if not board:
            board = self.board
        return board[ri][ci] == "none"

    def get_my_direcitons_for_cell(self, cell, color: str) -> List[int]:
        output: List[int] = []
        for i in range(len(cell)):
            if cell[i] == color:
                output.append(i)
        return output

    def get_placed_cells(self) -> List[Tuple[int, int]]:
        placed_cells: List[Tuple[int, int]] = []

        for ri in range(len(self.board)):
            for ci in range(len(self.board[ri])):
                if self.board[ri][ci] != "none":
                    placed_cells.append((ri, ci))

        return placed_cells

    def board_is_full(self):
        for ri in range(len(self.board)):
            for ci in range(len(self.board[ri])):
                if self.board[ri][ci] == "none":
                    return False
        return True


if __name__ == "__main__":
    # call you functions from this block:

    boardRows = 10
    boardCols = boardRows
    board = [["none"] * boardCols for _ in range(boardRows)]

    board[boardRows // 2][boardCols // 2] = random.choice(
        [
            "lldd",
            "dlld",
            "ddll",
            "lddl",
            "dldl",
            "ldld",
        ]
    )
    board = [
        [
            "lldd",
            "dlld",
            "lldd",
            "dldl",
            "dldl",
            "dlld",
            "ldld",
            "lddl",
            "dldl",
            "dldl",
            "dlld",
            "lldd",
        ],
        [
            "ldld",
            "ldld",
            "ldld",
            "lldd",
            "dldl",
            "ddll",
            "ldld",
            "lldd",
            "dldl",
            "dlld",
            "lddl",
            "ddll",
        ],
        [
            "ldld",
            "ldld",
            "ldld",
            "ldld",
            "lldd",
            "dlld",
            "ldld",
            "none",
            "none",
            "none",
            "none",
            "none",
        ],
        [
            "ddll",
            "ldld",
            "lddl",
            "ddll",
            "lddl",
            "ddll",
            "lddl",
            "none",
            "none",
            "none",
            "none",
            "none",
        ],
        [
            "dlld",
            "lddl",
            "dldl",
            "dlld",
            "lldd",
            "dlld",
            "lldd",
            "dldl",
            "dldl",
            "dlld",
            "lddl",
            "none",
        ],
        [
            "ddll",
            "lldd",
            "dlld",
            "none",
            "none",
            "ldld",
            "ldld",
            "lldd",
            "dlld",
            "lddl",
            "dlld",
            "none",
        ],
        [
            "lldd",
            "ddll",
            "none",
            "none",
            "none",
            "ddll",
            "lddl",
            "ddll",
            "lddl",
            "dlld",
            "lddl",
            "none",
        ],
        [
            "none",
            "none",
            "none",
            "none",
            "dldl",
            "dldl",
            "dlld",
            "lldd",
            "dlld",
            "lddl",
            "dldl",
            "none",
        ],
        [
            "none",
            "none",
            "none",
            "none",
            "none",
            "dldl",
            "ddll",
            "ldld",
            "ldld",
            "lldd",
            "none",
            "none",
        ],
        [
            "none",
            "none",
            "none",
            "none",
            "none",
            "lldd",
            "dlld",
            "lddl",
            "ddll",
            "none",
            "none",
            "none",
        ],
        [
            "none",
            "none",
            "none",
            "none",
            "none",
            "ddll",
            "lddl",
            "dlld",
            "lldd",
            "none",
            "none",
            "none",
        ],
        [
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
            "none",
        ],
    ]

    d = Drawer.Drawer()

    p1 = Player(board, "player1", "l")
    p2 = Player(board, "player2", "d")

    # test game. We assume that both player play correctly. In Brute/Tournament case, more things will be checked
    # like types of variables, validity of moves, etc...

    idx = 0
    gameDir = "zgame-" + str(hash((random.randint(0, 1000), random.randint(0, 1000))))
    os.makedirs(gameDir)
    while True:
        print(idx)
        # call player for his move
        rmove = p1.move()

        # rmove is: [ [r1,c1,tile1], ... [rn,cn,tile] ]
        # write to board of both players
        for move in rmove:
            row, col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile

        # make png with resulting board

        d.draw(p1.board, f"{gameDir}" + "/move-{:04d}.png".format(idx))
        idx += 1

        if len(rmove) == 0:
            print("End of game")
            break
        p1, p2 = p2, p1  # switch players

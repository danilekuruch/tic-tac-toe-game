from enum import Enum
from dataclasses import dataclass
from abc import ABC
import string


class GameRole(Enum):
    O = 0
    X = 1


class BasePlayer(ABC):
    role: GameRole


@dataclass(frozen=True)
class PlayerO(BasePlayer):
    role = GameRole.O


@dataclass(frozen=True)
class PlayerX(BasePlayer):
    role = GameRole.X


class WinSolution:
    def __init__(self, solution):
        self.board_cells: tuple[BoardCell, BoardCell, BoardCell] = solution


class BoardCell:
    def __init__(self, row: int, col: int):
        self.row: int = row
        self.col: int = col
        self.role = None


class GameBoard:
    def __init__(self):
        self.cells = [BoardCell(x, y) for x in range(3) for y in range(3)]


class TicTacToeGame:

    def __init__(self):
        self.board = GameBoard()
        self.player1: PlayerX = PlayerX()
        self.player2: PlayerO = PlayerO()

        self.current_player_move = self.player1
        self.win_solutions: list[WinSolution] = []
        self._define_win_solutions()

    def _define_win_solutions(self):
        solutions = [
            # horizontal solutions
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            # vertical solutions
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            # cross solutions
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0)),
        ]
        for solution in solutions:
            board_cells = [
                self.get_board_cell(row, col)
                for row, col in solution
            ]
            self.win_solutions.append(WinSolution(tuple(board_cells)))

    def check_solution(self, win_solution: WinSolution, player: BasePlayer):
        return all(
            point.role == player.role
            for point in win_solution.board_cells
        )

    def parse_player_move(self, player_input: str):
        player_move = player_input.strip().split(" ")

        if len(player_move) != 2:
            raise ValueError("Invalid input")

        if player_move[0] not in string.digits or player_move[1] not in string.digits:
            raise ValueError("You should enter numbers!")

        x, y = int(player_move[0]) - 1, int(player_move[1]) - 1
        if not (0 <= x < 3 and 0 <= y < 3):
            raise ValueError("Print Coordinates should be from 1 to 3!")

        if self.get_board_cell(x, y).role is not None:
            raise ValueError("Print This cell is occupied! Choose another one!")

        return x, y

    def switch_player(self):
        self.current_player_move = self.player1 if self.current_player_move == self.player2 else self.player2

    def player_move(self):
        point = self.get_user_move()
        self.get_board_cell(*point).role = self.current_player_move.role
        self.switch_player()

    def is_game_over(self):
        return self.check_game_state()[0]

    def get_user_move(self) -> tuple[int, int]:
        point = None
        while point is None:
            try:
                point = self.parse_player_move(input())
            except ValueError as err:
                self.show_error(str(err))
                continue
        return point

    def game(self):
        while not self.is_game_over():
            self.show_board()
            self.player_move()

        self.show_board()
        self.show_game_result()

    def get_board_cell(self, row, col):
        for board_cell in self.board.cells:
            if board_cell.row == row and board_cell.col == col:
                return board_cell
        return None

    def get_players_result(self):
        player1_won = False
        player2_won = False
        for win_solution in self.win_solutions:
            if self.check_solution(win_solution, self.player1):
                player1_won = True
            elif self.check_solution(win_solution, self.player2):
                player2_won = True
        return player1_won, player2_won

    def check_game_state(self):
        if any(cell.role is None for cell in self.board.cells):
            return False, "Game not finished"

        player1_won, player2_won = self.get_players_result()
        if player1_won and player2_won:
            return True, "Impossible"
        elif player1_won:
            return True, self.player1.role.name + " wins"
        elif player2_won:
            return True, self.player2.role.name + " wins"

        return True, "Draw"

    def show_game_result(self):
        _, msg = self.check_game_state()
        print(msg)

    def show_error(self, err_msg):
        print(err_msg)

    def show_board(self):
        print("-" * 9)

        for x in range(3):
            cell_view = " ".join([
                role.name if (role := self.get_board_cell(x, y).role) else " "
                for y in range(3)
            ])
            print(f"| {cell_view} |")

        print("-" * 9)


def main():
    TicTacToeGame().game()


if __name__ == '__main__':
    main()

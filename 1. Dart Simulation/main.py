from __future__ import annotations
from typing import TYPE_CHECKING

import csv
import random
import threading
from math import pi as PI
from time import perf_counter
from datetime import datetime

if TYPE_CHECKING:
    import _csv
    from io import TextIOWrapper
    from typing import Optional, Literal, Union


class DataFile:
    """
    A class for handling operations of the data dump.
    """

    __file_folder: str = "./dump"
    __file: TextIOWrapper
    __file_csv_writer: _csv._writer
    __data_headers: list[str] = [  # The headers of the CSV file.
        "id",
        "time",
        "dart_coordinate",
        "is_dart_hit",
    ]

    def __init__(self, file_name: Optional[str]) -> None:
        """
        The constructor of the class.

        Args:
            file_name: The name of the file.
        """
        if file_name is None:
            file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        self.file_name = f"{self.__file_folder}/{file_name}.csv"
        self.__file = open(self.file_name, "w")
        self.__file_csv_writer = csv.writer(self.__file)

        self.__initialize_csv_headers()

    def __initialize_csv_headers(self) -> None:
        """
        Initializes the headers of the CSV file.
        """
        self.__file_csv_writer.writerow(self.__data_headers)

    def write(self, data: Union[list, str]) -> None:
        """
        Writes the data to the CSV file.

        Args:
            data: The data to be written.
        """
        if isinstance(data, str):
            data = data.split(",")

        self.__file_csv_writer.writerow(data)

    def close_file(self) -> None:
        """
        Closes the file.
        """
        self.__file.close()


class DartBoard:
    """
    A class for handling operations of the dart board.
    """

    dart_board_radius: int
    dart_board_center: tuple[int, int]

    def __init__(
        self, *, dart_board_radius: int, dart_board_center: tuple[int, int] = (0, 0)
    ) -> None:
        """
        The constructor of the class.
        """
        self.dart_board_radius = dart_board_radius
        self.dart_board_center = dart_board_center

    def is_dart_hit(self, dart_coordinate: tuple[int, int]) -> bool:
        """
        Checks if the dart hits the circle.

        Args:
            dart_coordinate: The coordinate of the dart.

        Returns:
            True if the dart hits the circle, False otherwise.
        """
        pass


def throw_dart() -> tuple[int, int]:
    """
    Returns the coordinates of the dart.

    Returns:
        The coordinates of the dart.
    """
    pass


def print_results(
    *,
    total: int,
    hits: int,
    misses: int,
) -> None:
    """
    Prints the results of the simulation.

    Args:
        total: The total number of darts thrown.
        hits: The number of darts that hit the circle.
        misses: The number of darts that missed the circle.
    """
    pass


def progress_bar(no_of_completed: int, total: int, error_status: bool = False) -> None:
    """
    A progress bar that prints to the console.

    Args:
        no_of_completed: The number of completed tasks.
        total: The total number of tasks.
        error_status: The status of the error.
    """
    pass


def main():
    """
    The main function of the program.
    """
    pass


# Runs the main function.
if __name__ == "__main__":
    main()

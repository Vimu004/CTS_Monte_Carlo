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

COLOR_ORANGE = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_PURPLE = "\033[95m"
COLOR_RESET = "\033[0m"


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


def throw_dart() -> tuple[float, float]:
    """
    Returns the coordinates of the dart.

    Returns:
        The coordinates of the dart.
    """
    x: float = random.uniform(-1.0, 1.0)
    y: float = random.uniform(-1.0, 1.0)

    return (x, y)


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


def print_progress_bar(no_of_completed: int, total: int) -> None:
    """
    A progress bar that prints to the console.

    Args:
        no_of_completed: The number of completed tasks.
        total: The total number of tasks.
        error_status: The status of the error.
    """
    # Color variables
    global COLOR_GREEN, COLOR_ORANGE
    # Progress bar constants
    progress_bar_length: int = 100

    progress_color: str = COLOR_ORANGE
    progress_percentage: float = (no_of_completed * 100) / total
    progress_message: str = f"Loading {'.'* (int(progress_percentage)%4)}"
    progress_end_char: str = "\r"

    if progress_percentage == 100:
        progress_color: str = COLOR_GREEN
        progress_percentage: float = 100.0
        progress_message: str = "Done ✓"
        progress_end_char: str = "\n"

    progress_completion_bar_length: int = int(
        progress_percentage / 100 * progress_bar_length
    )

    progress_bar: str = f"{progress_color}{progress_message: <12} [{'#'*progress_completion_bar_length}{' '*(progress_bar_length-progress_completion_bar_length)}] {progress_percentage:.2f}%"

    print(progress_bar, end=progress_end_char)


def main():
    """
    The main function of the program.
    """
    pass


# Runs the main function.
if __name__ == "__main__":
    main()

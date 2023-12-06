from __future__ import annotations
from typing import TYPE_CHECKING

import csv
import random
import threading
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


class Dice:
    def __init__(self) -> None:
        """
        The constructor of the class.
        """
        pass

    @classmethod
    def roll_dice(cls) -> int:
        """
        Simulates the rolling of a dice.

        Returns:
            int: The result of the roll.
        """
        pass


def run_game(n: int) -> int:
    """
    Simulates a single game of n dice rolls

    Args:
        n (int): The number of dice rolls.

    Returns:
        int: The number of successful rolls.
    """
    pass


def print_results(no_of_successful_rolls: int, no_of_rolls: int):
    """
    Prints the results to the console.

    Args:
        no_of_successful_rolls (int): The number of successful rolls.
        no_of_rolls (int): The number of rolls.
    """
    pass


def progress_bar(no_of_completed: int, total: int, error_status: bool = False):
    """
    A progress bar that prints to the console.

    Args:
        no_of_completed (int): The number of completed tasks.
        total (int): The total number of tasks.
        error_status (bool, optional): Whether the progress bar is in error status. Defaults to False.
    """
    pass


def main():
    """
    The main function of the program.
    """
    pass


if __name__ == "__main__":
    main()

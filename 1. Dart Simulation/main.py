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

iteration_no: int = 0
total_iterations: int = 0
pi = 22/7


class IntervalThread(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


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
        "calculated_pi_value"
        "difference_of_Calculated_and_real_piValue"
    ]

    def __init__(self, file_name: Optional[str]) -> None:
        """
        The constructor of the class.

        Args:
            file_name: The name of the file.
        """
        if file_name is None:
            file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        self.file_name = file_name
        self.__file = open("C:\\Anusara\\Stat\\Monetecarlo\\CTS_Monte_Carlo\\data.csv", "w", newline='')
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

    dart_board_radius: float
    dart_board_center: tuple[int, int]
    __total_darts: int = 0
    __hit_count: int = 0

    def __init__(
        self, dart_board_radius: float, dart_board_center: tuple[int, int] = (0, 0)
    ) -> None:
        """
        The constructor of the class.
        """
        self.dart_board_radius = dart_board_radius
        self.dart_board_center = dart_board_center

    def is_dart_hit(self, dart_coordinate: tuple[float, float]) -> bool:
        """
        Checks if the dart hits the circle.

        Args:
            dart_coordinate: The coordinate of the dart.

        Returns:
            True if the dart hits the circle, False otherwise.
        """
        point = throw_dart()
        distance = (point[0] ** 2 + point[1] ** 2) ** 0.5
        self.__total_darts += 1
        if distance <= self.dart_board_radius:
            self.__hit_count += 1
            return True
        else:
            return False

    def pi_calculation(self) -> float:
        """
        Calculates the value of pi.
        """
        pi = (self.__hit_count / self.__total_darts) * 4
        
        return pi

    def print_result_summary(
        self, do_export: bool = False, csv_obj: DataFile = None
    ) -> None:
        """
        Prints the summary of the simulation.

        """

        print(f"\nTotal darts thrown: {self.__total_darts}")
        print(f"Total darts hit: {self.__hit_count}")
        print(f"Probability of hitting the dartboard: {self.__hit_count/self.__total_darts:.2f}\n")
        print(f"Calculated Pi Value equals to : {self.pi_calculation()}")
        print(f"Actual Pi Value equals to : {pi}\n")
        print(f"Error Difference equals to : {self.pi_calculation() - pi}\n ")
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

objtoDataFile = DataFile("C:\\Anusara\\Stat\\Monetecarlo\\CTS_Monte_Carlo\\data.csv")

def run_simulation(darts_total):
    """
    Does the simulation.
    """
    global iteration_no
    print_progress_bar()
    progress_thread = IntervalThread(1.0, print_progress_bar)
    progress_thread.start()

    obj = DartBoard(1.0, (0, 0) )
    for i in range(darts_total):
        iteration_no += 1
        obj.is_dart_hit(throw_dart())
        calculated_pi_value = obj.pi_calculation()
        objtoDataFile.write([iteration_no, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), throw_dart(), obj.is_dart_hit(throw_dart()),calculated_pi_value, calculated_pi_value - pi])
    progress_thread.cancel()
    print_progress_bar()

    obj.print_result_summary()
    

def print_progress_bar() -> None:
    """
    A progress bar that prints to the console.
    """
    # Color variables
    global COLOR_GREEN, COLOR_ORANGE
    global iteration_no, total_iterations
    # Progress bar constants
    progress_bar_length: int = 100

    progress_color: str = COLOR_ORANGE
    progress_percentage: float = (iteration_no * 100) / total_iterations
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

    progress_bar: str = f"{progress_color}{progress_message: <12} [{'#'*progress_completion_bar_length :<{progress_bar_length}}] {progress_percentage:.2f}%"

    print(progress_bar, end=progress_end_char)


def main():
    """
    The main function of the program.
    """
    global total_iterations
    file_path = input("Enter the path of the file you want to save: ")
    total_iterations = int(input("\nThe number of darts to throw: "))
    data_headers_for_csv = ["id", "time", "dart_coordinate", "is_dart_hit", "pi_value", "error_difference"]
    data_file = DataFile(file_path)
    data_file.write(data_headers_for_csv)
    run_simulation(total_iterations)
    data_file.close_file()


# Runs the main function.
if __name__ == "__main__":
    main()

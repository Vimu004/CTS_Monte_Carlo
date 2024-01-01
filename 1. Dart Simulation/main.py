from __future__ import annotations
from typing import TYPE_CHECKING

import csv
import random
import threading
from math import pi as PI
import numpy as np
import statistics as st
import os
from datetime import datetime
import matplotlib.pyplot as plt

if TYPE_CHECKING:
    import _csv
    from io import TextIOWrapper
    from typing import Optional, Union

COLOR_ORANGE = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

iteration_no: int = 0
total_iterations: int = 0
objtoDataFile: DataFile = None

col_data: np.array = np.array([
    [],
    [],
    [],
    []
    ])

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
        "ID",
        "Dart Coordinate(X)",
        "Dart Coordinate(Y)",
        "Is dart hit",
        "Calculated PI value",
        "Error difference",
    ]

    def __init__(self, file_name: Optional[str] = None) -> None:
        """
        The constructor of the class.

        Args:
            file_name: The name of the file.
        """
        if file_name is None or file_name == "":
            file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

        if os.path.exists(self.__file_folder) is False:
            os.mkdir(self.__file_folder)

        self.file_name = file_name
        self.__file = open(f"{self.__file_folder}/{self.file_name}.csv", "w")
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
        point = dart_coordinate
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
        calculated_pi_value = self.pi_calculation()

        print("")
        print(f"{'Dart Coordinate(X)':<25}   {'Dart Coordinate(Y)':<25}   {'Calculated PI Value':<25}   {'Error difference':<25}")
        print(f"Mode:{st.mode(col_data[0]):>20.5f}   Mode:{st.mode(col_data[1]):>20.5f}   Mode:{st.mode(col_data[2]):>20.5f}   Mode:{st.mode(col_data[3]):>20.5f}")
        print(f"Mean:{st.mean(col_data[0]):>20.5f}   Mean:{st.mean(col_data[1]):>20.5f}   Mean:{st.mean(col_data[2]):>20.5f}   Mean:{st.mean(col_data[3]):>20.5f}")
        print(f"Median:{st.median(col_data[0]):>18.5f}   Median:{st.median(col_data[1]):>18.5f}   Median:{st.median(col_data[2]):>18.5f}   Median:{st.median(col_data[3]):>18.5f}")
        print(f"Std. Deviation:{st.stdev(col_data[0]):>10.5f}   Std. Deviation:{st.stdev(col_data[1]):>10.5f}   Std. Deviation:{st.stdev(col_data[2]):>10.5f}   Std. Deviation:{st.stdev(col_data[3]):>10.5f}")

        print(f"\nTotal darts thrown: {self.__total_darts}")
        print(f"Total darts hit: {self.__hit_count}")
        print(
            f"Probability of hitting the dartboard: {self.__hit_count/self.__total_darts :.2f}\n"
        )
        print(f"Calculated Pi Value equals to : {calculated_pi_value}")
        print(f"Actual Pi Value equals to : {PI}\n")
        print(f"Error Difference equals to : {calculated_pi_value - PI}\n ")

        if do_export:
            if csv_obj is None:
                raise ValueError("The CSV object cannot be None.")

            csv_obj.write("")
            csv_obj.write(["Mode", st.mode(col_data[0]), st.mode(col_data[1]), "-", st.mode(col_data[2]), st.mode(col_data[3])])
            csv_obj.write(["Mean", st.mean(col_data[0]), st.mean(col_data[1]), "-", st.mean(col_data[2]), st.mean(col_data[3])])
            csv_obj.write(["Median", st.median(col_data[0]), st.median(col_data[1]), "-", st.median(col_data[2]), st.median(col_data[3])])
            csv_obj.write(["Standard Deviation", st.stdev(col_data[0]), st.stdev(col_data[1]), "-", st.stdev(col_data[2]), st.stdev(col_data[3])])
            csv_obj.write("")
            csv_obj.write(["Total darts thrown", self.__total_darts])
            csv_obj.write(["Total darts hit", self.__hit_count])
            csv_obj.write(
                [
                    "Probability of hitting the dartboard",
                    f"{self.__hit_count/self.__total_darts :.2f}",
                ]
            )
            csv_obj.write("")
            csv_obj.write(["Calculated Pi Value equals to", calculated_pi_value])
            csv_obj.write(["Actual Pi Value equals to", PI])
            csv_obj.write("")
            csv_obj.write(["Error Difference equals to", calculated_pi_value - PI])


def throw_dart() -> tuple[float, float]:
    """
    Returns the coordinates of the dart.

    Returns:
        The coordinates of the dart.
    """
    x: float = random.uniform(-1.0, 1.0)
    y: float = random.uniform(-1.0, 1.0)

    return (x, y)



def run_simulation(darts_total):
    """
    Does the simulation.
    """
    global iteration_no, objtoDataFile, col_data

    calculated_pi_value_list = []
    print_progress_bar()
    progress_thread = IntervalThread(1.0, print_progress_bar)
    progress_thread.start()

    obj = DartBoard(1.0, (0, 0))
    for i in range(darts_total):
        iteration_no += 1
        dart_coordinates = throw_dart()
        dart_status = obj.is_dart_hit(dart_coordinates)
        calculated_pi_value = obj.pi_calculation()
        calculated_pi_value_list.append(calculated_pi_value)

        row_data = np.array([dart_coordinates[0], dart_coordinates[1], calculated_pi_value, calculated_pi_value - PI])
        col_data = np.hstack([col_data, row_data.reshape(-1, 1)])

        objtoDataFile.write(
            [
                iteration_no,
                *dart_coordinates,
                dart_status,
                calculated_pi_value,
                calculated_pi_value - PI,
            ]
        )
    progress_thread.cancel()
    print_progress_bar()

    obj.print_result_summary(do_export=True, csv_obj=objtoDataFile)
    
    return calculated_pi_value_list

def plot(pi_values: list):
    
    X_values_for_plot = range(total_iterations)
    y_values = pi_values

    plt.plot(X_values_for_plot,y_values)
    plt.xlabel('Times (N)')
    plt.ylabel('Estimated Value of Pi')
    plt.axhline(y=22/7, color='red', linestyle='--', label='Real pi value')
    
    plt.legend()
    plt.show()



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
    global total_iterations, objtoDataFile

    file_name = input("\nEnter the name of the file you want to export to (Optional): ")
    total_iterations = int(input("The number of darts to throw: "))

    objtoDataFile = DataFile(file_name)
    plot(run_simulation(total_iterations))
    objtoDataFile.close_file()
    

# Runs the main function.
if __name__ == "__main__":
    main()

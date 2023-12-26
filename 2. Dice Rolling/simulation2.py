from __future__ import annotations
from typing import TYPE_CHECKING

import random
import csv
import os
from datetime import datetime
import threading

if TYPE_CHECKING:
    import _csv
    from io import TextIOWrapper
    from typing import Optional, Union

COLOR_ORANGE = "\033[93m"
COLOR_GREEN = "\033[92m"

iteration_no: int = 0
total_iterations: int = 0


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
    __data_headers: list[str] = []

    def __init__(
        self, file_name: Optional[str] = None, data_headers: Optional[list[str]] = None
    ) -> None:
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

        if data_headers is not None:
            self.__data_headers = data_headers
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


def simulate_dice_throws(
    num_simulations, target_sum, num_dice, csv_datafile: DataFile = None
):
    global iteration_no
    count_successful_attempts = 0

    print_progress_bar()
    progress_thread = IntervalThread(1.0, print_progress_bar)
    progress_thread.start()

    for _ in range(num_simulations):
        dice_results = [random.randint(1, 6) for _ in range(num_dice)]
        dice_sum = sum(dice_results)
        success_status = False
        iteration_no += 1

        if dice_sum == target_sum:
            count_successful_attempts += 1
            success_status = True

        csv_datafile.write(
            [
                _ + 1,
                *dice_results,
                dice_sum,
                target_sum - dice_sum,
                "Yes" if success_status else "No",
            ]
        )

    progress_thread.cancel()
    print_progress_bar()

    return count_successful_attempts


if __name__ == "__main__":
    target_sum = int(input("\nEnter the target sum(Ex:- 32): "))
    num_dice = int(input("Enter the number of dice to roll(Ex:- 10): "))
    num_simulations = int(input("Enter the number of simulations to run: "))

    total_iterations = num_simulations

    csv_file = DataFile(
        data_headers=[
            "Attempt no.",
            *[f"Dice {i}" for i in range(1, num_dice + 1)],
            "Dice sum",
            "Sum deviation",
            "Is Successful Attempt?",
        ]
    )

    no_successful_attempts = simulate_dice_throws(
        num_simulations, target_sum, num_dice, csv_file
    )
    simulated_probability = no_successful_attempts / num_simulations

    print(f"\nThe number of attempts: {no_successful_attempts} / {num_simulations}")
    print(
        f"The simulated probability of getting a sum of {target_sum} from {num_dice} dice throws is: {simulated_probability:.10f}"
    )
    print(
        f"The simulated probability of getting a sum of {target_sum} from {num_dice} dice throws as a percentage is: {simulated_probability * 100:.2f}%"
    )

    csv_file.write("")
    csv_file.write(["Target sum", target_sum])
    csv_file.write(["Number of dice", num_dice])
    csv_file.write(["Number of simulations", num_simulations])
    csv_file.write("")
    csv_file.write(["Number of successful attempts", no_successful_attempts])
    csv_file.write(["Simulated probability", simulated_probability])
    csv_file.write(["Simulated probability (%)", f"{simulated_probability * 100:.2f}%"])
    csv_file.close_file()

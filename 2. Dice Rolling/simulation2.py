import random


def simulate_dice_throws(num_simulations, target_sum, num_dice):
    count_successful_attempts = 0

    for _ in range(num_simulations):
        dice_results = [random.randint(1, 6) for _ in range(num_dice)]
        if sum(dice_results) == target_sum:
            count_successful_attempts += 1

    print("The number of attempts: ", count_successful_attempts)

    return count_successful_attempts / num_simulations


if __name__ == "__main__":
    target_sum = 32
    num_dice = 10
    num_simulations = 500

    simulated_probability = simulate_dice_throws(num_simulations, target_sum, num_dice)

    print(
        f"The simulated probability of getting a sum of {target_sum} from {num_dice} dice throws is: {simulated_probability:.10f}")
    print(
        f"The simulated probability of getting a sum of {target_sum} from {num_dice} dice throws is: {simulated_probability * 100:.2f}%")

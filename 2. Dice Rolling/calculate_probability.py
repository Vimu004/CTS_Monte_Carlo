def count_ways_to_sum(target_sum, num_dice, memo={}):
    if num_dice == 0:
        return 1 if target_sum == 0 else 0

    if (target_sum, num_dice) in memo:
        return memo[(target_sum, num_dice)]

    count = 0

    for outcome in range(1, 7):
        count += count_ways_to_sum(target_sum - outcome, num_dice - 1, memo)

    memo[(target_sum, num_dice)] = count

    return count


def calculate_probability(target_sum, num_dice):
    total_outcomes = 6 ** num_dice

    favorable_outcomes = count_ways_to_sum(target_sum, num_dice)

    print("The number of attempts that sum up to 32:", favorable_outcomes)

    probability = favorable_outcomes / total_outcomes

    return probability


if __name__ == "__main__":
    target_sum = 32
    num_dice = 10

    probability = calculate_probability(target_sum, num_dice)
    print(f"The probability of getting a sum of {target_sum} from {num_dice} dice throws is: {probability:.10f}")
    print(f"The probability of getting a sum of {target_sum} from {num_dice} dice throws is: {probability * 100:.2f}%")

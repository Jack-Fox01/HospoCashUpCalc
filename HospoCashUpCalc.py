def get_cash_input():
    denominations = {
        "£20": 20, "£10": 10, "£5": 5, "£2": 2, "£1": 1,
        "50p": 0.50, "20p": 0.20, "10p": 0.10, "5p": 0.05
    }
    cash = {}

    print("Enter the number of each denomination (decimals allowed for coins):")
    for note, value in denominations.items():
        while True:
            try:
                count = float(input(f"{note}: "))  # Accepts decimal input
                if count < 0:
                    raise ValueError("Count cannot be negative.")
                cash[note] = count
                break
            except ValueError:
                print("Invalid input. Please enter a non-negative number.")

    return cash, denominations

def calculate_total(cash, denominations):
    return round(sum(cash[note] * value for note, value in denominations.items()), 2)

def suggest_removal(cash, denominations, total):
    if total <= 100:
        print(f"\nYour total is £{total:.2f}. No need to remove anything!")
        return

    print(f"\nYour total is £{total:.2f}, which exceeds £100.")
    excess = round(total - 100, 2)
    print(f"You need to remove £{excess:.2f}.")

    # Sort denominations from largest to smallest
    sorted_denominations = sorted(denominations.items(), key=lambda x: -x[1])  
    removed = {}

    for note, value in sorted_denominations:
        if excess <= 0:
            break  # Stop if we've removed enough

        if cash[note] > 0:
            remove_amount = min(cash[note], excess // value)  # Take out whole units first
            remove_value = remove_amount * value
            excess = round(excess - remove_value, 2)
            cash[note] -= remove_amount
            removed[note] = removed.get(note, 0) + remove_amount

    # Fine-tune with smaller denominations if needed
    for note, value in reversed(sorted_denominations):  # Start from the smallest
        if excess <= 0:
            break

        if cash[note] > 0:
            remove_amount = min(cash[note], excess / value)  # Fractional removal
            remove_value = round(remove_amount * value, 2)
            excess = round(excess - remove_value, 2)
            cash[note] -= remove_amount
            removed[note] = removed.get(note, 0) + remove_amount

    print("\nSuggested removals:")
    for note, count in removed.items():
        print(f"Remove {count:.2f} x {note}")

def main():
    cash, denominations = get_cash_input()
    total = calculate_total(cash, denominations)
    suggest_removal(cash, denominations, total)

if __name__ == "__main__":
    main()
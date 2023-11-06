number_to_guess = 35
def guess_number(guess):
    if guess < number_to_guess:
        print(f"You guessed {guess} which is too low...")
    elif guess > number_to_guess:
        print(f"You guessed {guess} which is too high...")
    else:
        print(f"Congratulations! You've guessed the right number {number_to_guess}!")
from cs50 import get_string


def main():
    # Prompt the user for a credit card number
    card_number = get_string("Number: ")

    # Check if the card is valid
    if not luhn_algorithm(card_number):
        print("INVALID")
        return

    # Determine the card type
    card_type = get_card_type(card_number)
    print(card_type)


def luhn_algorithm(card_number):
    """Implement Luhn's algorithm to validate the credit card number"""
    total = 0
    reversed_digits = card_number[::-1]

    for i, digit in enumerate(reversed_digits):
        num = int(digit)
        # Multiply every second digit by 2, starting with the second-to-last
        if i % 2 == 1:
            num *= 2
            # If the result is greater than 9, subtract 9
            if num > 9:
                num -= 9
        total += num

    # The card is valid if the total modulo 10 is 0
    return total % 10 == 0


def get_card_type(card_number):
    """Determine the type of the credit card based on its number"""
    length = len(card_number)
    start_digits = int(card_number[:2])
    first_digit = int(card_number[0])

    if length == 15 and (start_digits == 34 or start_digits == 37):
        return "AMEX"
    elif length == 16 and 51 <= start_digits <= 55:
        return "MASTERCARD"
    elif (length == 13 or length == 16) and first_digit == 4:
        return "VISA"
    else:
        return "INVALID"


if __name__ == "__main__":
    main()

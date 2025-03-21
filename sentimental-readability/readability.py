from cs50 import get_string


def main():
    # Prompt the user for input text
    text = get_string("Text: ")

    # Count letters, words, and sentences
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate the Coleman-Liau index
    grade = coleman_liau_index(letters, words, sentences)

    # Print the grade level
    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")


def count_letters(text):
    """Counts the number of letters in the text."""
    return sum(1 for char in text if char.isalpha())


def count_words(text):
    """Counts the number of words in the text."""
    return len(text.split())


def count_sentences(text):
    """Counts the number of sentences in the text."""
    return sum(1 for char in text if char in ".!?")


def coleman_liau_index(letters, words, sentences):
    """Calculates the Coleman-Liau index."""
    L = (letters / words) * 100  # Average letters per 100 words
    S = (sentences / words) * 100  # Average sentences per 100 words
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


if __name__ == "__main__":
    main()

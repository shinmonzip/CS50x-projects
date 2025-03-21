import csv
import sys


def main():
    # Check for correct command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Load the database and DNA sequence files
    database = load_database(sys.argv[1])
    dna_sequence = load_dna_sequence(sys.argv[2])

    # Extract STR names
    str_names = extract_str_names(database)

    # Compute STR counts in the DNA sequence
    str_counts = compute_str_counts(dna_sequence, str_names)

    # Find a match in the database
    match_name = find_match(database, str_counts, str_names)

    # Output the result
    print(match_name)


def load_database(filename):
    """Load the DNA database from a CSV file."""
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)


def load_dna_sequence(filename):
    """Load the DNA sequence from a text file."""
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)


def extract_str_names(database):
    """Extract STR names from the database header."""
    return list(database[0].keys())[1:]  # Skip the "name" column


def compute_str_counts(dna_sequence, str_names):
    """Compute the longest match for each STR in the DNA sequence."""
    return {str_name: longest_match(dna_sequence, str_name) for str_name in str_names}


def find_match(database, str_counts, str_names):
    """Find a matching individual in the database based on STR counts."""
    for person in database:
        if all(int(person[str_name]) == str_counts[str_name] for str_name in str_names):
            return person["name"]
    return "No match"


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run


main()

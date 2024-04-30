import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print('Usage: python dna.py DATABASES_FILE SEQUENCES_FILE')
        sys.exit(1)

    # TODO: Read database file into a variable
    database = []
    try:
        with open(sys.argv[1], 'r') as file:
            reader = csv.DictReader(file)

            # convert STR value to int and append to database
            for row in reader:
                for key in row:
                    try:
                        row[key] = int(row[key])
                    except:
                        continue
                database.append(row)
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    except IOError as e:
        print("Error opening the file:", e)
        sys.exit(1)

        
    # TODO: Read DNA sequence file into a variable
    file = open(sys.argv[2], 'r')
    if file == None:
        print('Can\'t open file')
        sys.exit(1)

    sequence = file.read()
    file.close()

    # TODO: Find longest match of each STR in DNA sequence
    # init STRs to count each STR
    STRs = [{'STR':key, 'count':0} for key in database[0] if key != 'name']

    for STR in STRs:
        STR['count'] = longest_match(sequence, STR['STR'])

    # TODO: Check database for matching profiles
    is_similar = False
    person_matched = None

    # check each STR from everyones in database
    for person in database:
        for STR in STRs:
            if person[STR['STR']] == STR['count']:
                is_similar = True
            else:
                is_similar = False
                break

        if is_similar:
            person_matched = person['name']
            break

    # print the matched person's name
    if person_matched:
        print(person_matched)
    else:
        print('No match')

    sys.exit(0)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

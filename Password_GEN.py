import itertools
import random
import string
import os


def generate_password_list(name, pet_name, dob, digit_input, email, phone, ssn, extra_keywords, birthplace, fav_place, friend_name, aim_in_life, include_symbols=False, max_passwords=10000):
    # Create a base list of words from user input and extra keywords
    words = [
        name, pet_name, birthplace, fav_place, friend_name, aim_in_life
    ] + dob.split('/') + [email, phone, ssn] + extra_keywords

    # Generate additional variations (uppercase, lowercase, capitalized)
    words_variations = []
    for word in words:
        if word:
            words_variations.extend([word, word.lower(), word.upper(), word.capitalize()])
    words_variations = list(set(words_variations))  # Remove duplicates

    # Generate limited combinations of words
    combinations = []
    for i in range(2, 4):  # Generate 2-word and 3-word combinations
        combinations.extend(itertools.permutations(words_variations, i))
        if len(combinations) > max_passwords:
            combinations = combinations[:max_passwords]  # Limit to max_passwords
            break

    # Combine into passwords
    passwords = [''.join(combo) for combo in combinations]

    # Append numbers based on digit_input, limited to a reasonable range
    additional_passwords = []
    for password in passwords:
        for i in range(10 ** (digit_input - 1), 10 ** (digit_input - 1) + 100):  # Append only 100 numbers
            additional_passwords.append(f"{password}{i}")
            if len(additional_passwords) > max_passwords:
                break
        if len(additional_passwords) > max_passwords:
            break

    # Include symbols if required
    if include_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        symbol_passwords = []
        for password in passwords[:max_passwords]:  # Limit symbols for max_passwords
            symbol_passwords.append(password + random.choice(symbols))
        passwords.extend(symbol_passwords)

    # Return the final list of passwords (limited to max_passwords)
    return list(set(passwords + additional_passwords))[:max_passwords]


def save_password_list(directory, filename, password_list):
    # Use current working directory if no directory is provided
    if not directory.strip():
        directory = os.getcwd()

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the file path
    file_path = os.path.join(directory, filename)

    # Save the password list to a text file
    with open(file_path, "w") as file:
        for password in password_list:
            file.write(password + "\n")
    
    return file_path


# Print the developer's name
print("Developer: BlackCloud\n")

# Prompt the user for input
name = input("Enter your name: ")
pet_name = input("Enter your pet's name: ")
dob = input("Enter your date of birth (DD/MM/YYYY): ")
birthplace = input("Enter your birthplace: ")
fav_place = input("Enter your favorite place: ")
friend_name = input("Enter your best friend's name: ")
aim_in_life = input("Enter your aim in life: ")

# Ask for valid input for digit_input
while True:
    try:
        digit_input = int(input("Enter the number of digits to append to the password: "))
        break  # Exit the loop if the input is valid
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

email = input("Enter your email address: ")
phone = input("Enter your phone number: ")
ssn = input("Enter your social security number (SSN): ")

# Ask for symbols
include_symbols = input("Include symbols in passwords? (yes/no): ").lower() == 'yes'

# Ask for extra keywords
extra_keywords_input = input("Enter extra keywords separated by commas (leave blank if none): ")
extra_keywords = [kw.strip() for kw in extra_keywords_input.split(',') if kw.strip()]

# Ask for directory to save the file (default is the current working directory)
directory = input("Enter the directory where you want to save the password list (leave blank for default): ")

# Ask for the filename
filename = input("Enter the name of the password list file (default: password_list.txt): ").strip() or "password_list.txt"

# Generate the password list
password_list = generate_password_list(name, pet_name, dob, digit_input, email, phone, ssn, extra_keywords, birthplace, fav_place, friend_name, aim_in_life, include_symbols)

# Save the password list to a file
file_path = save_password_list(directory, filename, password_list)

print(f"\nPassword list generated and saved at: {file_path}")
print(f"Total Passwords Generated: {len(password_list)}")

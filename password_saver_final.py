import pickle
import sys

# The password list - We start with it populated for testing purposes
entries = []
# The password file name to store the data to
password_file_name = "PasswordFile.pickle"
# The encryption key for the caesar cipher
encryption_key = 16

menu_text = """
What would you like to do? Please enter number (1-6):
1. Open Password File
2. Lookup a Password
3. Add a Password
4. Save Password File
5. Print the Encrypted Password List (Testing Only)
6. Quit program
"""


def password_encrypt(plaintext, key):
    """Returns an encrypted message using a caesar cipher

    :param plaintext (string)
    :param key (int) The offset to be used for the caesar cipher
    :return (string) The encrypted message
    """
    ciphertext = ""
    for ch in plaintext:
        if ch.isalpha():
            num = ord(ch)
            num += key

            if ch.isupper():
                if num > ord("Z"):
                    num -= 26
                elif num < ord("A"):
                    num += 26
            elif ch.islower():
                if num > ord("z"):
                    num -= 26
                elif num < ord("a"):
                    num += 26
            ciphertext += chr(num)
        else:  # ch is not letter
            ciphertext += ch
    return ciphertext

def password_decrypt(ciphertext, key):
    """ Returns a decrypted message using the caesar cipher

    :param ciphertext (string)
    :param key (int) the offset to be used for the cipher
    :return:
    """
    r_key = -key
    return password_encrypt(ciphertext, r_key)


def load_password_file(file_name):
    """Loads a password file.  The file must be in the same directory as the .py file

    :param file_name (string) The file to load.  Must be a pickle file in the correct format
    """
    try:
        entries, encryption_key = pickle.load(open(file_name, "rb"))
    except FileNotFoundError:
        print("File Not Found.")


def save_password_file(file_name):
    """Saves a password file.  The file will be created if it doesn't exist.

    :param file_name (string) The file to save.
    """
    pickle.dump((entries, encryption_key), open(file_name, "wb"))


def add_entry(website, password):
    """Adds an entry with a website and password

    :param website (string) The website for the entry
    :param password (string) The unencrypted password for the entry
    """
    encrypt = password_encrypt(password, encryption_key)
    new_entry = [website, encrypt]
    entries.append(new_entry)


def lookup_password(website):
    """Lookup the password for a given website

    :param website (string) The website for the entry to lookup
    :return: Returns an unencrypted password.  Returns None if no entry is found
    """
    ciphertext = ""
    for i in range(len(entries)):
        if entries[i][0] == website.lower():
            ciphertext = entries[i][1]
    return password_decrypt(ciphertext, encryption_key)


while True:
    print(menu_text)
    choice = input()

    if choice == '1':  # Load the password list from a file
        load_password_file(password_file_name)

    if choice == '2':  # Lookup at password
        print("WEBSITE: ")
        for key_value in entries:
            print(key_value[0].title())
        website = input()
        password = lookup_password(website)
        if password:
            print('PASSWORD: ', password)
        else:
            print('Password Not Found')

    if choice == '3':  # Add a new entry
        website = input("WEBSITE: ")
        unencrypted_password = input("PASSWORD: ")
        add_entry(website, unencrypted_password)

    if choice == '4':  # Save the passwords to a file
        save_password_file(password_file_name)

    if choice == '5':  # Print out the password list
        for key_value in entries:
            print(', '.join(key_value))

    if choice == '6':  # Quit program
        sys.exit()

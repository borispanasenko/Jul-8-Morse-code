from morsedict import morse_dict


print("Enter the text: ")
while True:
    user_input = ''.join(input().upper().split())
    if user_input == "F":
        break
    try:
        for char in user_input:
            if not char.isalpha() and not char.isdigit():
                raise TypeError
    except TypeError:
        print("Only alphabetical letters and numbers.", end=' ')
    else:
        for char in user_input:
            print(f"{morse_dict[char]}", end=' ')
    print()

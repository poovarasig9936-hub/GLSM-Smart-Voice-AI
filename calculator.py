def generate_calculator_code(command):

    command = command.lower()


    # Number words conversion

    number_words = {

        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10

    }


    numbers = []


    for word in command.split():

        if word.isdigit():

            numbers.append(int(word))


        elif word in number_words:

            numbers.append(number_words[word])



    if len(numbers) < 2:

        return None



    a = numbers[0]
    b = numbers[1]



    if "add" in command or "plus" in command:

        return f"""
a = {a}
b = {b}

result = a + b

print(result)
"""



    elif "subtract" in command or "minus" in command or "sub" in command or "sab" in command:

        return f"""
a = {a}
b = {b}

result = a - b

print(result)
"""



    elif "multiply" in command or "times" in command or "multi" in command:

        return f"""
a = {a}
b = {b}

result = a * b

print(result)
"""



    elif "divide" in command or "division" in command:

        return f"""
a = {a}
b = {b}

result = a / b

print(result)
"""



    else:

        return None


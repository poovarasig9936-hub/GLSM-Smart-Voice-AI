import re


def get_input(command):

    command = command.lower()

    # Find number in command
    numbers = re.findall(r"\d+", command)

    if numbers:
        return numbers[0] + "\n"

    # Wrong program
    if "wrong" in command:
        return "AI Test\n"

    # Default
    return ""

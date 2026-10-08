from voice_input import listen
from voice_output import speak
from brain import understand_command

from code_generator import generate_code
from dsa_generator import generate_dsa

from file_manager import save_code
from code_runner import run_code


print("🤖 AI Assistant Started")

command = listen()

result = understand_command(command)

print("AI Understanding:", result)


code = None


if result.startswith("generate_"):

    dsa_words = [
        "bfs",
        "dfs",
        "stack",
        "queue",
        "binary",
        "linear",
        "bubble",
        "selection",
        "insertion"
    ]

    if any(word in command.lower() for word in dsa_words):
        code = generate_dsa(command)

    else:
        code = generate_code(command)



if code:

    print("\nGenerated Code:")
    print(code)

    filename = result.replace("generate_", "") + ".py"

    save_code(filename, code)

    run_code(filename, command)


else:

    print("Program not available")


input("\nPress Enter to close")


import subprocess
import sys

from brain import understand_command
from code_generator import generate_code
from dsa_generator import generate_dsa
from error_explainer import explain_error
from ai_tutor import explain_code



# Store last generated code
last_code = ""



def run_code(code):

    file_name = "generated_program.py"

    try:

        with open(file_name, "w") as file:
            file.write(code)


        result = subprocess.run(
            [sys.executable, file_name],
            capture_output=True,
            text=True
        )


        if result.stderr.strip():

            return (
                "❌ Error:\n"
                + result.stderr
                + "\n\n💡 Explanation:\n"
                + explain_error(result.stderr)
            )


        return (
            "🚀 Program Output:\n"
            + result.stdout
        )


    except Exception as e:

        return (
            "❌ System Error:\n"
            + str(e)
        )






def process_command(command):

    global last_code


    print("PROCESS COMMAND:", command)


    command = command.lower()




    # AI Tutor Mode

    if "explain code" in command or "explain this" in command:


        return (
            "🤖 AI Tutor:\n\n"
            + explain_code(last_code)
        )






    # Calculator Mode

    if any(word in command for word in [
        "add",
        "plus",
        "subtract",
        "minus",
        "multiply",
        "times",
        "divide"
    ]):


        from calculator import generate_calculator_code


        code = generate_calculator_code(command)


        if code is None:

            return (
                "🧮 Calculator:\n\n"
                "Numbers detect panna mudiyala."
            )


        last_code = code


        result = run_code(code)


        return (
            "🧮 Calculator:\n\n"
            "Python Code:\n"
            "----------------\n"
            + code
            + "\n----------------\n\n"
            + result
        )






    task = understand_command(command)



    if task == "unknown":

        return (
            "🤖 AI Assistant:\n\n"
            "Sorry, command understand panna mudiyala."
        )






    dsa_words = [

        "bubble",
        "selection",
        "insertion",
        "bfs",
        "dfs",
        "stack",
        "queue"

    ]





    if any(word in command for word in dsa_words):

        code = generate_dsa(command)


    else:

        code = generate_code(command)






    if code is None:


        return (
            "🤖 AI Assistant:\n\n"
            "Program generate panna mudiyala."
        )





    # Save generated code

    last_code = code





    result = run_code(code)





    return (

        "🤖 AI Assistant:\n\n"

        "✅ Code Generated Successfully\n\n"

        "Python Code:\n"

        "----------------\n"

        + code

        + "\n----------------\n\n"

        + result

    )


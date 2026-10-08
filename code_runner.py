import subprocess
import sys


def run_code(filename, user_input=""):

    print("Running:", filename)

    try:

        result = subprocess.run(
            [sys.executable, filename],
            input=user_input,
            text=True,
            capture_output=True,
            timeout=10
        )


        if result.returncode == 0:

            return (
                "Output:\n"
                + result.stdout
            )

        else:

            return (
                "Error:\n"
                + result.stderr
            )


    except subprocess.TimeoutExpired:

        return "Program took too much time"


    except Exception as e:

        return "Runner Error: " + str(e)


from flask import Flask, render_template_string, jsonify, request, send_from_directory
import os
import re
import math
import io
import contextlib

app = Flask(__name__)

ONES = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19
}

TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
}


def words_to_number(text):
    text = text.lower().replace("-", " ").strip()
    words = text.split()

    if not words:
        return None

    total = 0
    current = 0

    for word in words:

        if word in ONES:
            current += ONES[word]

        elif word in TENS:
            current += TENS[word]

        elif word == "hundred":
            if current == 0:
                current = 1
            current *= 100

        elif word == "thousand":
            if current == 0:
                current = 1
            total += current * 1000
            current = 0

        elif word == "lakh":
            if current == 0:
                current = 1
            total += current * 100000
            current = 0

        elif word == "million":
            if current == 0:
                current = 1
            total += current * 1000000
            current = 0

        elif word == "and":
            continue

        else:
            return None

    return total + current


def extract_number(text):

    match = re.search(r"-?\d+", text)

    if match:
        return int(match.group())

    number_words = (
        "zero|one|two|three|four|five|six|seven|eight|nine|"
        "ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
        "seventeen|eighteen|nineteen|twenty|thirty|forty|"
        "fifty|sixty|seventy|eighty|ninety|hundred|thousand|"
        "lakh|million|and"
    )

    matches = re.findall(
        rf"(?:{number_words})(?:[\s-]+(?:{number_words}))*",
        text.lower()
    )

    for item in matches:
        value = words_to_number(item)
        if value is not None:
            return value

    return None


def extract_two_numbers(text):

    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)

    if len(numbers) >= 2:
        return float(numbers[0]), float(numbers[1])

    text = text.lower()

    if " and " in text:

        parts = text.split(" and ", 1)

        left = parts[0]
        right = parts[1]

        remove_words = [
            "add", "addition", "plus",
            "subtract", "subtraction", "minus",
            "multiply", "multiplication", "times",
            "divide", "division", "divided",
            "modulus", "mod", "calculate"
        ]

        for word in remove_words:
            left = re.sub(rf"\b{word}\b", "", left)

        right = re.sub(r"\bplease\b", "", right)

        a = words_to_number(left.strip())
        b = words_to_number(right.strip())

        if a is not None and b is not None:
            return a, b

    if " by " in text:

        parts = text.split(" by ", 1)

        left = parts[0]
        right = parts[1]

        remove_words = [
            "divide", "division", "divided",
            "modulus", "mod", "calculate"
        ]

        for word in remove_words:
            left = re.sub(rf"\b{word}\b", "", left)

        a = words_to_number(left.strip())
        b = words_to_number(right.strip())

        if a is not None and b is not None:
            return a, b

    return None, None


def clean_number(value):

    if isinstance(value, float) and value.is_integer():
        return int(value)

    return value


def generate_program(command):

    text = command.lower().strip()

    # ADDITION
    if "add" in text or "addition" in text or "plus" in text:

        a, b = extract_two_numbers(text)

        if a is not None and b is not None:

            a = clean_number(a)
            b = clean_number(b)

            code = f'''a = {a}
b = {b}

result = a + b

print("Addition:", result)
'''

            explanation = (
                f"I generated an addition program. "
                f"We take {a} and {b}, add them, and print the answer."
            )

            return explanation, code

        return "Please give two numbers.", "# Example: add two and three"

    # SUBTRACTION
    if "subtract" in text or "subtraction" in text or "minus" in text:

        a, b = extract_two_numbers(text)

        if a is not None and b is not None:

            a = clean_number(a)
            b = clean_number(b)

            code = f'''a = {a}
b = {b}

result = a - b

print("Subtraction:", result)
'''

            explanation = (
                f"I generated a subtraction program. "
                f"We subtract {b} from {a} and print the answer."
            )

            return explanation, code

        return "Please give two numbers.", "# Example: subtract ten and three"

    # MULTIPLICATION
    if "multiply" in text or "multiplication" in text or "times" in text:

        a, b = extract_two_numbers(text)

        if a is not None and b is not None:

            a = clean_number(a)
            b = clean_number(b)

            code = f'''a = {a}
b = {b}

result = a * b

print("Multiplication:", result)
'''

            explanation = (
                f"I generated a multiplication program. "
                f"We multiply {a} by {b} and print the answer."
            )

            return explanation, code

        return "Please give two numbers.", "# Example: multiply two and five"

    # DIVISION
    if "divide" in text or "division" in text or "divided" in text:

        a, b = extract_two_numbers(text)

        if a is not None and b is not None:

            a = clean_number(a)
            b = clean_number(b)

            code = f'''a = {a}
b = {b}

if b != 0:
    result = a / b
    print("Division:", result)
else:
    print("Cannot divide by zero")
'''

            explanation = (
                f"I generated a division program. "
                f"We divide {a} by {b} and print the result."
            )

            return explanation, code

        return "Please give two numbers.", "# Example: divide one hundred by five"

    # MODULUS
    if "modulus" in text or re.search(r"\bmod\b", text):

        a, b = extract_two_numbers(text)

        if a is not None and b is not None:

            a = clean_number(a)
            b = clean_number(b)

            code = f'''a = {a}
b = {b}

if b != 0:
    result = a % b
    print("Modulus:", result)
else:
    print("Cannot calculate modulus by zero")
'''

            explanation = (
                f"I generated a modulus program. "
                f"It finds the remainder when {a} is divided by {b}."
            )

            return explanation, code

        return "Please give two numbers.", "# Example: modulus seventeen by five"

    # FACTORIAL
    if "factorial" in text:

        n = extract_number(text)

        if n is not None:

            n = int(n)

            if n < 0:
                return (
                    "Factorial is not defined for negative numbers.",
                    "# Negative factorial is not defined."
                )

            code = f'''import math

n = {n}

result = math.factorial(n)

print("Factorial of", n, "is:")
print(result)
'''

            explanation = (
                f"I generated a factorial program. "
                f"We take the number {n}, calculate its factorial "
                f"using Python, and print the answer."
            )

            return explanation, code

        return "Please give a number.", "# Example: factorial 100"

    # SQUARE
    if "square" in text:

        n = extract_number(text)

        if n is not None:

            n = int(n)

            code = f'''n = {n}

result = n ** 2

print("Square of", n, "is:", result)
'''

            explanation = (
                f"I generated a square program. "
                f"We multiply {n} by itself and print the result."
            )

            return explanation, code

        return "Please give a number.", "# Example: square 25"

    # CUBE
    if "cube" in text:

        n = extract_number(text)

        if n is not None:

            n = int(n)

            code = f'''n = {n}

result = n ** 3

print("Cube of", n, "is:", result)
'''

            explanation = (
                f"I generated a cube program. "
                f"We multiply {n} three times and print the result."
            )

            return explanation, code

        return "Please give a number.", "# Example: cube 25"

    # PRINT 1 TO N
    if "print" in text or "display" in text or "show" in text:

        range_match = re.search(
            r"(?:print|display|show).*?\b1\b\s*"
            r"(?:to|until|upto|up\s+to)\s+(.+)",
            text
        )

        if range_match:

            end_part = range_match.group(1).strip()

            end_part = re.sub(
                r"\b(numbers?|please)\b",
                "",
                end_part
            ).strip()

            digit_match = re.search(r"\d+", end_part)

            if digit_match:
                n = int(digit_match.group())
            else:
                n = words_to_number(end_part)

            if n is not None:

                n = int(n)

                code = f'''n = {n}

for i in range(1, n + 1):
    print(i)
'''

                explanation = (
                    f"I generated a program to print numbers "
                    f"from 1 to {n}. The loop starts at 1 and "
                    f"continues until {n}."
                )

                return explanation, code

        return "Please give the ending number.", "# Example: print 1 to 20"

    # EVEN
    if "even" in text:

        n = extract_number(text)

        if n is not None:

            n = int(n)

            code = f'''n = {n}

for i in range(1, n + 1):
    if i % 2 == 0:
        print(i)
'''

            explanation = (
                f"I generated a program to print even numbers "
                f"from 1 to {n}."
            )

            return explanation, code

    # ODD
    if "odd" in text:

        n = extract_number(text)

        if n is not None:

            n = int(n)

            code = f'''n = {n}

for i in range(1, n + 1):
    if i % 2 != 0:
        print(i)
'''

            explanation = (
                f"I generated a program to print odd numbers "
                f"from 1 to {n}."
            )

            return explanation, code

    # PRIME
    if "prime" in text:

        n = extract_number(text)

        if n is not None:

            n = int(n)

            code = f'''n = {n}

if n <= 1:

    print(n, "is not a prime number")

else:

    is_prime = True

    for i in range(2, int(n ** 0.5) + 1):

        if n % i == 0:
            is_prime = False
            break

    if is_prime:
        print(n, "is a prime number")
    else:
        print(n, "is not a prime number")
'''

            explanation = (
                f"I generated a prime number checking program. "
                f"It checks whether {n} is a prime number."
            )

            return explanation, code

    # FIBONACCI
    if "fibonacci" in text:

        n = extract_number(text)

        if n is not None:

            n = int(n)

            code = f'''n = {n}

a = 0
b = 1

print("Fibonacci Series:")

for i in range(n):

    print(a, end=" ")

    a, b = b, a + b
'''

            explanation = (
                f"I generated a Fibonacci program for {n} terms. "
                f"The program starts with zero and one, then "
                f"adds the previous two numbers to generate the next number."
            )

            return explanation, code

        return "Please give the number of Fibonacci terms.", "# Example: fibonacci 10"

    # BFS
    if "bfs" in text:

        code = '''from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": [],
    "F": []
}

visited = set()
queue = deque(["A"])

print("BFS Traversal:")

while queue:

    node = queue.popleft()

    if node not in visited:

        print(node, end=" ")

        visited.add(node)

        for neighbour in graph[node]:

            if neighbour not in visited:
                queue.append(neighbour)
'''

        explanation = (
            "I generated a Breadth First Search program. "
            "BFS uses a queue to visit graph nodes level by level."
        )

        return explanation, code

    # DFS
    if "dfs" in text:

        code = '''graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": [],
    "F": []
}

visited = set()


def dfs(node):

    if node in visited:
        return

    print(node, end=" ")

    visited.add(node)

    for neighbour in graph[node]:
        dfs(neighbour)


print("DFS Traversal:")

dfs("A")
'''

        explanation = (
            "I generated a Depth First Search program. "
            "DFS visits one path deeply before going to another path."
        )

        return explanation, code

    # UNKNOWN
    code = '''# Command not recognized.

# Examples:
# add two and three
# subtract 100 and 25
# multiply 20 and 5
# divide 100 by 4
# modulus 17 by 5
# square 25
# cube 10
# factorial 8
# factorial 100
# print 1 to 20
# print 1 to 1000
# fibonacci 10
# prime 97
# bfs
# dfs
'''

    return (
        "I could not understand the command. Please try another command.",
        code
    )


# ============================================================
# HTML
# ============================================================

HTML_TEMPLATE = r"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>GLSM Smart Voice AI</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    min-height: 100vh;

    background: #080808;

    color: white;

    font-family: Arial, sans-serif;

    display: flex;

    justify-content: center;

    align-items: center;

    padding: 20px;

}

.container {

    width: 800px;

    max-width: 96%;

    background: #121212;

    border: 4px solid #ff4500;

    border-radius: 15px;

    padding: 25px;

    box-shadow: 0 0 30px #ff4500;

    text-align: center;

}

h1 {

    margin-top: 0;

    color: white;

}


/* ==========================================================
   BIG CARTOON PIC
   ========================================================== */

.avatar {

    width: 300px;

    height: 300px;

    margin: 0 auto 18px auto;

    border: 4px solid #ff4500;

    border-radius: 15px;

    overflow: hidden;

    box-shadow: 0 0 25px #ff4500;

}

.avatar img {

    width: 100%;

    height: 100%;

    object-fit: cover;

}


.status {

    color: #ffcc00;

    font-weight: bold;

    margin: 15px;

}

.input-area {

    display: flex;

    gap: 10px;

    margin-bottom: 10px;

}

input {

    flex: 1;

    padding: 12px;

    background: #1e1e1e;

    color: white;

    border: 1px solid #555;

    border-radius: 6px;

    font-size: 15px;

}

button {

    border: none;

    border-radius: 6px;

    padding: 12px;

    font-weight: bold;

    cursor: pointer;

}

.send {

    background: #28a745;

    color: white;

}

.voice {

    width: 100%;

    background: #ff4500;

    color: white;

    margin-bottom: 10px;

}

.run {

    width: 100%;

    background: #007bff;

    color: white;

    margin-bottom: 10px;

    display: none;

}

.clear {

    width: 100%;

    background: #555;

    color: white;

    margin-bottom: 15px;

}

.title {

    text-align: left;

    color: #ffcc00;

    font-weight: bold;

    margin: 10px 0 6px;

}

.code {

    background: #000;

    color: #00ff66;

    padding: 15px;

    border-radius: 8px;

    text-align: left;

    font-family: Consolas, monospace;

    white-space: pre-wrap;

    max-height: 300px;

    overflow-y: auto;

}

.output {

    background: #000;

    color: #00ccff;

    padding: 15px;

    border-radius: 8px;

    text-align: left;

    font-family: Consolas, monospace;

    white-space: pre-wrap;

    min-height: 80px;

    max-height: 400px;

    overflow-y: auto;

}

</style>

</head>


<body>


<div class="container">

<h1>🤖 GLSM Smart Voice AI</h1>


<div class="avatar">

<img src="/couple.png" alt="GLSM Cartoon">

</div>


<div class="status" id="status">
AI: Ready for your command
</div>


<div class="input-area">

<input
id="userInput"
type="text"
placeholder="Example: factorial 100"
>

<button class="send" onclick="generateProgram()">
Send
</button>

</div>


<button class="voice" onclick="startVoice()">
🎤 Tap to Speak
</button>


<button
class="run"
id="runButton"
onclick="runProgram()"
>
▶ Run Program
</button>


<button class="clear" onclick="clearAll()">
Clear
</button>


<div class="title">
💻 Generated Python Program
</div>


<div class="code" id="codeOutput">
Waiting for your command...
</div>


<div class="title">
📤 Program Output
</div>


<div class="output" id="output">
Output will appear here...
</div>


</div>


<script>


function speak(text) {

    if (!("speechSynthesis" in window)) {
        return;
    }

    speechSynthesis.cancel();

    let speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    speech.rate = 0.85;

    speech.pitch = 1;

    speechSynthesis.speak(speech);
}


function speakProgram(explanation, code, output) {

    let text = explanation + " ";

    text += "The generated Python program is as follows. ";

    let lines = code.split("\n");

    for (let i = 0; i < lines.length; i++) {

        let line = lines[i].trim();

        if (line !== "") {

            text += line + ". ";

        }

    }

    if (output && output.trim() !== "") {

        text +=
            "The program output is. " +
            output;

    }

    speechSynthesis.cancel();

    let speech =
        new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    speech.rate = 0.75;

    speech.pitch = 1;

    speechSynthesis.speak(speech);
}


function generateProgram() {

    let command =
        document
        .getElementById("userInput")
        .value
        .trim();


    if (!command) {

        document.getElementById("status").innerText =
            "AI: Please enter a command.";

        speak("Please enter a command.");

        return;

    }


    document.getElementById("status").innerText =
        "AI: Generating program...";


    fetch("/generate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: command
        })

    })


    .then(response => response.json())


    .then(data => {

        document.getElementById("status").innerText =
            "AI: " + data.reply;


        document.getElementById("codeOutput").innerText =
            data.code;


        document.getElementById("output").innerText =
            "Click Run Program to see the output.";


        document.getElementById("runButton").style.display =
            "block";


        speakProgram(
            data.reply,
            data.code,
            ""
        );

    })


    .catch(error => {

        console.log(error);

        document.getElementById("status").innerText =
            "AI: Error generating program.";

    });

}


function runProgram() {

    let command =
        document
        .getElementById("userInput")
        .value
        .trim();


    if (!command) {
        return;
    }


    document.getElementById("status").innerText =
        "AI: Running program...";


    document.getElementById("output").innerText =
        "Executing...";


    fetch("/run", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: command
        })

    })


    .then(response => response.json())


    .then(data => {

        document.getElementById("status").innerText =
            "AI: " + data.reply;


        document.getElementById("output").innerText =
            data.output;


        let code =
            document.getElementById("codeOutput").innerText;


        speakProgram(
            data.reply,
            code,
            data.output
        );

    })


    .catch(error => {

        console.log(error);

        document.getElementById("status").innerText =
            "AI: Execution error.";

    });

}


function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Voice recognition is not supported. Please use Google Chrome."
        );

        return;

    }


    let recognition =
        new SpeechRecognition();


    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;


    recognition.onstart = function() {

        document.getElementById("status").innerText =
            "AI: Listening... Speak now!";

    };


    recognition.onresult = function(event) {

        let speechText =
            event.results[0][0].transcript;


        document.getElementById("userInput").value =
            speechText;


        generateProgram();

    };


    recognition.onerror = function(event) {

        document.getElementById("status").innerText =
            "AI: Voice recognition error.";

        console.log(event.error);

    };


    recognition.start();

}


function clearAll() {

    document.getElementById("userInput").value = "";

    document.getElementById("status").innerText =
        "AI: Ready for your command";

    document.getElementById("codeOutput").innerText =
        "Waiting for your command...";

    document.getElementById("output").innerText =
        "Output will appear here...";

    document.getElementById("runButton").style.display =
        "none";


    if ("speechSynthesis" in window) {

        speechSynthesis.cancel();

    }

}

</script>


</body>

</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/couple.png")
def get_image():

    folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    return send_from_directory(
        folder,
        "couple.png"
    )


@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.get_json()

        command = data.get(
            "message",
            ""
        )

        reply, code = generate_program(command)

        return jsonify({
            "reply": reply,
            "code": code
        })

    except Exception as e:

        return jsonify({
            "reply": "Error generating program.",
            "code": str(e)
        }), 500


@app.route("/run", methods=["POST"])
def run():

    try:

        data = request.get_json()

        command = data.get(
            "message",
            ""
        )

        reply, code = generate_program(command)

        output_buffer = io.StringIO()

        with contextlib.redirect_stdout(output_buffer):

            exec(
                code,
                {
                    "__builtins__": __builtins__,
                    "math": math
                }
            )

        output = output_buffer.getvalue()

        if not output:
            output = "Program executed successfully."

        return jsonify({
            "reply": "Program executed successfully.",
            "output": output
        })

    except Exception as e:

        return jsonify({
            "reply": "Program execution failed.",
            "output": "Error: " + str(e)
        })


if __name__ == "__main__":

    print("")
    print("======================================")
    print("       GLSM SMART VOICE AI")
    print("======================================")
    print("Server started successfully!")
    print("Open: http://127.0.0.1:5000")
    print("======================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
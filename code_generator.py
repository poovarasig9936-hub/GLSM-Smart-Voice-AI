import re


def generate_code(command):

    command = command.lower()


    # Hello
    if "hello" in command:

        return """
print("Hello")
"""


    # Factorial
    elif "factorial" in command or "fact" in command:

        numbers = re.findall(r'\d+', command)

        if numbers:
            n = int(numbers[0])
        else:
            n = 5


        return f"""
n = {n}

fact = 1

for i in range(1, n + 1):

    fact = fact * i


print("Factorial =", fact)
"""



    # Fibonacci
    elif "fibonacci" in command:

        numbers = re.findall(r'\d+', command)

        if numbers:
            n = int(numbers[0])
        else:
            n = 10


        return f"""
n = {n}

a = 0
b = 1


for i in range(n):

    print(a, end=" ")

    a, b = b, a + b
"""



    # Prime Number
    elif "prime" in command:


        numbers = re.findall(r'\d+', command)


        if numbers:

            n = int(numbers[0])

        else:

            n = 17



        return f"""
num = {n}


if num > 1:

    for i in range(2, num):

        if num % i == 0:

            print("Not Prime")

            break


    else:

        print("Prime")


else:

    print("Not Prime")
"""




    # Multiplication Table
    elif "table" in command:


        numbers = re.findall(r'\d+', command)


        if numbers:

            num = int(numbers[0])

        else:

            num = 5



        return f"""
num = {num}


for i in range(1,11):

    print(num, "x", i, "=", num*i)
"""




    # For Loop
    elif "for loop" in command or "loop" in command:


        return """
for i in range(1,11):

    print(i)
"""




    # While Loop
    elif "while loop" in command:


        return """
i = 1


while i <= 10:

    print(i)

    i = i + 1
"""





    # Calculator
    elif "calculator" in command:


        return """
a = 10
b = 5


print("Addition =", a+b)

print("Subtraction =", a-b)

print("Multiplication =", a*b)

print("Division =", a/b)
"""





    # Print Numbers
    elif "print" in command:


        numbers = re.findall(r'\d+', command)


        if numbers:

            limit = int(numbers[-1])

        else:

            limit = 10



        return f"""
for i in range(1,{limit+1}):

    print(i)
"""




    else:

        return None


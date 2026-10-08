def correct_code(code, error):

    error = error.lower()


    # First remove indentation problems
    if "indentationerror" in error:

        lines = code.split("\n")

        fixed_lines = []

        for line in lines:
            fixed_lines.append(line.strip())

        code = "\n".join(fixed_lines)


    # Then fix NameError
    if "nameerror" in error or "nameerror" in code.lower():

        if "print(name)" in code:

            code = code.replace(
                "print(name)",
                'name = input("Enter name:")\nprint(name)'
            )


    return code


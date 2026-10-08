def save_code(filename, code):

    file = open(filename, "w")

    file.write(code)

    file.close()

    print("File Created:", filename)

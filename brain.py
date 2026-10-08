def understand_command(command):

    command = command.lower()


    if "hello" in command:
        return "generate_hello"


    elif "print" in command:
        return "generate_print"


    elif "factorial" in command or "fact" in command:
        return "generate_factorial"


    elif "fibonacci" in command:
        return "generate_fibonacci"


    elif "prime" in command:
        return "generate_prime"


    elif "table" in command or "multiplication" in command:
        return "generate_table"


    elif any(word in command for word in [
    "calculator",
    "add",
    "plus",
    "subtract",
    "minus",
    "multiply",
    "times",
    "divide"
]):
       return "generate_calculator"


    


    elif "wrong" in command or "error" in command:
        return "generate_error_test"


    elif "bubble" in command:
        return "generate_bubble_sort"


    elif "selection" in command:
        return "generate_selection_sort"


    elif "insertion" in command:
        return "generate_insertion_sort"


    elif "bfs" in command or "breadth first" in command:
        return "generate_bfs"


    elif "dfs" in command or "depth first" in command:
        return "generate_dfs"


    elif "stack" in command:
        return "generate_stack"


    elif "queue" in command:
        return "generate_queue"


    else:
        return "unknown"


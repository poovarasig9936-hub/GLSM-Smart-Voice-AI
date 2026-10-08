def fix_error(error):

    error = error.lower()


    if "syntaxerror" in error:

        return "Check colon(:), brackets and indentation."


    elif "nameerror" in error:

        return "Variable or function name is not defined."


    elif "modulenotfounderror" in error:

        return "Required Python module is not installed."
    

    elif "indentationerror" in error:

        return "Check spaces and indentation in your Python code."


    elif "typeerror" in error:

        return "Wrong data type operation."


    elif "indexerror" in error:

        return "List index is out of range."


    elif "attributeerror" in error:

        return "Object does not have this attribute."


    else:

        return "Unknown error. Need more analysis."


def explain_error(error):

    error = str(error)

    if "SyntaxError" in error:
        return "Syntax mistake irukku. Code spelling and symbols check pannunga."

    elif "NameError" in error:
        return "Variable name wrong ah irukkalam."

    elif "TypeError" in error:
        return "Data type mismatch problem."

    elif "IndentationError" in error:
        return "Python indentation (space) check pannunga."

    else:
        return "Error identify panna mudiyala. Code check pannunga."

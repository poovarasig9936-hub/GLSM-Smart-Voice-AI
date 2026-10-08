def explain_code(code):

    code = code.lower()

    if "for" in code:
        return """
Indha code la for loop use pannirukanga.
For loop oru block of code ah repeated ah execute panna use aagum.
Range function use pannina specific number of times execute aagum.
"""

    elif "print" in code:
        return """
Print function output ah screen la display panna use aagum.
"""

    elif "if" in code:
        return """
If statement condition check panna use aagum.
Condition true na code execute aagum.
"""

    else:
        return """
Indha code pathi detailed explanation generate panna mudiyala.
"""

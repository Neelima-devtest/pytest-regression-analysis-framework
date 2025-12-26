######## This is a basic calculator app which performs addition, subtraction, multiplication and division ######## #####
############## We will be using these simple functions to write tests and then also to check code coverage #############

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

#print(add(2,3))

import re
from german_number_word_converter import convert_to_int
"""
---------------------------------------------------------------------------------------------------------------------------
Functions for mathematical operations
---------------------------------------------------------------------------------------------------------------------------
"""
def addieren(wert1: int | float, wert2: int | float) -> int | float: 
    ergebniss = wert1 + wert2
    return ergebniss

def subtraieren(wert1: int | float, wert2: int | float) -> int | float:
    ergebniss = wert1 - wert2
    return ergebniss

def multiplizieren(wert1: int | float, wert2: int | float) -> int | float:
    ergebniss = wert1 * wert2
    return ergebniss

def dividieren(wert1: int | float, wert2: int | float) -> int | float:
    ergebniss = wert1 / wert2
    return ergebniss

def exponieren(wert1: int | float, wert2: int | float) -> int | float:
    ergebniss = wert1 ** wert2
    return ergebniss
    
"""
---------------------------------------------------------------------------------------------------------------------------
Function to parse user input, call conver_to_int() to convert spelled out words into integers, determine negativity and return 
only valid integers for the mathematical functions to use
---------------------------------------------------------------------------------------------------------------------------
"""

def normalize(text: str) -> list | None:
    answer = re.split(r"(\+|-|\*|\^|hoch|/|plus|minus|mal|durch|\(|\))", text)
    answer = [current.strip() for current in answer if current.strip() != "" ]
    for i, current in enumerate(answer):
        if current.isdigit():
            answer[i] = int(current)
    
    for i, current in enumerate(answer):
        
        if current == "minus" or current == "-":
            previous = answer[i - 1] if i > 0 else None
            if previous in operators or previous is None:

                following = answer[i + 1]

                if isinstance(following, int):
                    answer[i] = -following
                else:    
                    answer[i] = (f"minus {following}")
                
                answer[i + 1] = ""

    answer = [chunk.strip() if isinstance(chunk, str) else chunk for chunk in answer if chunk !=""]
    
            
    for i, current in enumerate(answer):
        if current == "(" or current == ")":
            continue   
        if current not in operators and isinstance(current, str):
            try:
                converted = convert_to_int(current)
                answer[i] = converted
            except KeyError as e:
                print(f"{e} Please enter a valid number")
                return None
    return answer


"""
---------------------------------------------------------------------------------------------------------------------------
Here the normalized user input is routed through the PEMDAS order of operations Parantheses, Exponents, Multiplication, 
Division, Addition, Subtraction. either the answer is returned after successfully completing the equation or None is returned
in a ZeroDivisionError 
---------------------------------------------------------------------------------------------------------------------------
"""
operators = {"+": addieren,"plus":addieren, "-": subtraieren, "minus": subtraieren, "*": multiplizieren,
             "mal": multiplizieren, "/": dividieren, "durch": dividieren, "^": exponieren, "hoch": exponieren}

def resolve_pemdas(answer: list) -> int | float | list | None:
    
    pairs_list = []
    stack = []
    for i, current in enumerate(answer):
        if current == "(":
            stack.append(i)
        elif current == ")":
            open_index = stack.pop()
            close_index = i
            pairs_list.append((open_index, close_index))

    for pair in pairs_list:
        open_index, close_index = pair
        block = [item for item in answer[open_index+1 : close_index] if item != ""]
        block_result = resolve_pemdas(block)
        answer[open_index] = block_result
        for idx in range(open_index+1, close_index+1):
            answer[idx] = ""

    answer = [item for item in answer if item != ""]
    ex_list = ["^", "hoch"]
    
    while any(operator in answer for operator in ex_list):
        positions = [answer.index(operator) for operator in ex_list if operator in answer]
        index = min(positions)
        wert1 = answer[index - 1]
        symbol = answer[index]
        wert2 = answer[index + 1]

        result = operators[symbol](wert1 = wert1, wert2 = wert2)

        answer[index-1] = result

        del answer[index]
        del answer[index]

    md_list = ["*", "mal", "/", "durch"]
    while any(operator in answer for operator in md_list):
        positions = [answer.index(operator) for operator in md_list if operator in answer]  
        index = min(positions)        
        wert1 = answer[index - 1]
        symbol = answer[index]
        wert2 = answer[index + 1]
        
        try:
            result = operators[symbol](wert1 = wert1, wert2 = wert2)
        
        except ZeroDivisionError as d:
            print(f"{d} You cannot divide by zero, please enter a valid equation")
            return None
        
        answer[index-1] = result

        del answer[index]
        del answer[index]
     
    as_list = ["+", "plus", "-", "minus"]
    while any(operator in answer for operator in as_list):
        positions = [answer.index(operator) for operator in as_list if operator in answer]  
        index = min(positions)    
        wert1 = answer[index - 1]
        symbol = answer[index]
        wert2 = answer[index + 1]

        result = operators[symbol](wert1 = wert1, wert2 = wert2)

        answer[index-1] = result

        del answer[index]
        del answer[index]
    return answer[0] if len (answer) == 1 else answer

"""
---------------------------------------------------------------------------------------------------------------------------
Main function that asks for input then runs that input throught normalize(), resolve_pemdas() finaly returning the answer
---------------------------------------------------------------------------------------------------------------------------
"""

def main():
    while True:
        question = input(str("Please enter your equation:  "))
        answer = normalize(question)
        if answer is None:
            continue
        final_answer = resolve_pemdas(answer)

        if final_answer is None:
            continue
    
        print(final_answer)
        break

"""
---------------------------------------------------------------------------------------------------------------------------
Entry point user must answer if they want to perform calculations, this will continue to loop until the user answers no
---------------------------------------------------------------------------------------------------------------------------
"""

while True:
    entry = input("Are you ready to do some calculations y/n:  ")
    entry = entry.lower().strip()[:1]
    if entry == "y":
        main()
    elif entry == "n":
        print("Math is fun")
        break
    else:
        print("Please answer the question")
        continue



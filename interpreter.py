
def varmap(targetVar, state):
    if targetVar not in state:
        raise ValueError("Error: Var not found")
    return state[targetVar]

def tokenize(expression):
    tokens = []
    current_token = ""
    for char in expression:
        if char.isspace(): 
            if current_token:
                tokens.append(current_token)
                current_token = ""  
        elif char in "+-*/()": 
            if current_token:
                tokens.append(current_token)
            tokens.append(char) 
            current_token = ""
        else:
            current_token += char 

    if current_token: 
        tokens.append(current_token) 
    return tokens

def parse_primary(tokens, index, state):
    token = tokens[index]
    try:
        # Try converting to a number first
        return int(token)
    except ValueError:
        # If not a number, treat it as a variable 
        return state[token] # Access variables directly
    raise ValueError(f"Invalid token encountered: {token}") 

def parse_expression(tokens, index, state):
    """Parses an expression based on operator precedence (PEMDAS)."""
    precedence = {'*': 2, '/': 2, '+': 1, '-': 1}
    operand_stack = []  
    operator_stack = [] 

    while index < len(tokens):
        token = tokens[index]
        index += 1

        #attempted () doesn't work properly but leaving it in
        if token.isdigit():
            operand_stack.append(int(token))
        elif token == '(':
            result, index = parse_expression(tokens, index, state)
            operand_stack.append(result)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                op = operator_stack.pop()
                right = operand_stack.pop()
                left = operand_stack.pop()
                if op == '+':
                    operand_stack.append(left + right)
                elif op == '-':
                    operand_stack.append(left - right)
                elif op == '*':
                    operand_stack.append(left * right)
                elif op == '/':
                    operand_stack.append(float(left) / right)
            operator_stack.pop()
        else:
            if token in precedence:  # Check if it's a defined operator
                while operator_stack and precedence[operator_stack[-1]] >= precedence[token]:
                    op = operator_stack.pop()
                    right = operand_stack.pop()
                    left = operand_stack.pop()
                    if op == '+':
                        operand_stack.append(left + right)
                    elif op == '-':
                        operand_stack.append(left - right)
                    elif op == '*':
                        operand_stack.append(left * right)
                    elif op == '/':
                        operand_stack.append(float(left) / right)
                operator_stack.append(token)
            else:  # Handle variables
                print("Token:", token, "Value from State:", state[token]) 
                operand_stack.append(state[token])  

    while operator_stack:
        op = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()
        if op == '+':
            operand_stack.append(left + right)
        elif op == '-':
            operand_stack.append(left - right)
        elif op == '*':
            operand_stack.append(left * right)
        elif op == '/':
            operand_stack.append(float(left) / right)

    return operand_stack[0]

def evaluate_expression(tokens, state):
    return parse_expression(tokens, 0, state) 

def executeProgram(program):
    state = dict()

    for line in program.splitlines():
        if not line.strip(): 
            continue          
        if "=" in line:
            instruction = "ASSIGN" 
            equation = line
        else:
            instruction, equation = line.split(' ', 1)  

        print("Instruction:", instruction)
        print("Equation:", equation)

        if instruction == "ASSIGN":
            print("Current State before assignment:", state)  
            lhs, rhs = equation.split('=', 1)  
            lhs = lhs.strip("ASSIGN ") 
            print("LHS:", lhs)
            tokens = tokenize(rhs)
            print("Tokens:", tokens) 
            try:
                result = evaluate_expression(tokens, state) 
                print("Calculated Result:", result)
                lhs = lhs.strip()
                state[lhs] = result 
            except ValueError:
                print("Error: Invalid expression")
    
        elif instruction == "PRINT":
            try:
                print("Current State before print:", state) 
                var_name = equation.strip()
                val = state[var_name]
                print(val)
            except ValueError:
                print("Error: Variable not found")
        else:  
            print("Processing expression:", line)  
            lhs, rhs = line.split('=', 1) 
            lhs = lhs.strip() 
            print("LHS:", lhs)
            try:
                tokens = tokenize(rhs)  
                result = evaluate_expression(tokens, state)
                state[lhs] = result 
                print("Calculated Result:", result)
            except ValueError:
                print("Error: Calculation error or invalid expression") 
            print("Expression processing complete") 
            print("Current state:", state) 


sampleProgram = """
ASSIGN n = 5
ASSIGN x = n + 4 * 2
ASSIGN y = 5 / 2 - 1
ASSIGN z = 10 / 2
PRINT n
PRINT z
PRINT x
PRINT y
ASSIGN x = 5
PRINT x
"""

executeProgram(sampleProgram)

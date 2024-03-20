## Math Interpreter Project

This project implements a basic interpreter that can handle simple arithmetic expressions, variables, and assignments. 

It does **not** rely on Python's built-in functions such as eval(). Instead, the program includes its own built-in math parser!

**Key Components**

1) **Breaking Down the Code (Tokenization):** It takes a line of code and splits it up into tokens and lexemes (the terminals)

2) **Understanding the Operator Precedence:** Follows the rules of PEMDAS like giving multiplication higher priority than addition and subtraction

3) **Storing variables in the State:** Keeps track of variables and assigned values in dictionary

**Explanation of each function in code:**

* **VarMap(targetVar, state)**
   * Purpose: A helper function that takes a variable name (targetVar) and the current state of variables found in state and retrieves the value connected to that variable

* **tokenize(expression)**
   * Takes a string representing an expression like x + 4 * 2 and breaks it into a list of tokens such as {‘x’, ‘+’, 4, ‘*’, 2}
   * Essentially it iterates through each character of the expression and separates numbers based on spaces
   * It treats operators (+, -, *, /) and parentheses as individual tokens 

* **parse_primary(tokens, index, state)**
   * Handles most basic units of expression like single numbers or variables
   * Tries to convert the tokens into their respective types ie int(token)
   * If it fails, assumes token is a variable and looks it up in the state dictionary

* **parse_expression(tokens, index, state)**
   * The heart of how the program handles order of PEMDAS and interprets calculations
   * Operator precedence: creates a dictionary precedence to assign a priority level to each operator
   * Stacks 
     * Operand_stack: Stores numbers 
     * Operator_stack: Stores operators
   * Logic
      * Processes tokens one by one. If it’s a number, pushes it onto operand stack and respectively does the same for the operator
      * If the operator has higher precedence, it will calculate
      * If the incoming operator has lower or equal precedence, it pops operators from the stack and performs the operations until this condition is no longer true

* **evaluate_expression(tokens, state)**
   * Basically a bridge between tokenized expression and handling operator precedence (parse_expression)

* **executeProgram(program)**
   * Where the magic happens
   * Splits input into 2 parts, the instruction and the equation
   * Distinguishes between two types of instructions 
     * If it has Assignment(ASSIGN) as instruction: Then it takes the 2nd part of the original split, equation, and splits it again into lhs and rhs based on the ‘=’ 
        * LHS is stripped of instruction such as ASSIGN
        * Calculates the expression on the right-hand side 
        * Stores result in a variable in the program’s state
     * PRINT(PRINT): Looks up the variable to print in the state and displays its value

**Examples:**

**Example 1: Simple Example of Operator Precedence using Stack Methodology**

* Explanation of the line: `ASSIGN x = n + 4 * 2`
* Stack Status: Operand stack: [Operand: ], Operator stack: [Operator: ]
* Token “n”: Since n is a variable, we retrieve its value with the lookup function and push onto the operand stack. [Operand: 5]
* Token “+”:  + has lower precedence than the next operator (*) so it stays on the stack. [Operand: 5], [Operator: +]
* Token “4”: Since 4 is a number it’s pushed onto the stack [Operand: 5, 4]
* Token “*”: * has a higher precedence than +, so multiplication is performed. 4 * 2 = 8 and this value is pushed onto the stack. [Operand: 5, 8], [Operator: +]
* Token “2”: 2 is a number we push onto the operand stack. Since there are no more tokens the calculation is complete. 
* Since + is the only operator left, 5 and 8 are popped, we do addition, and the result 13 is pushed back onto the operand stack 
* Assignment: 13 is the last operand on the stack which is then assigned to the variable x.

**Example 2: Complex Example of Operator Precedence using Stack Methodology**

* x = n * 5 + 3 / 2 - 16
* Initialization: We start with empty operand and operator stacks.
* n (value 5): Since n is a variable with the value 5, we push '5' onto the operand stack.
* *: The multiplication operator (*) is pushed onto the operator stack.
* 5: The number '5' is pushed onto the operand stack.
* + : Because multiplication (*) has higher precedence than addition (+), it's performed first. We pop '5' and '5' from the operand stack, calculate (5 * 5 = 25), and push '25' back onto the operand stack. Now the operator stack is empty.
* 3: The number '3' is pushed onto the operand stack.
* /: The division operator (/) is pushed onto the operator stack.
* 2: The number '2' is pushed onto the operand stack.
* Division (/) has higher precedence than subtraction (-), so we pop '2' and '3' from the operand stack, calculate (3 / 2 = 1.5), and push '1.5' back onto the operand stack.
* 16: The number '16' is pushed onto the operand stack.
* Final Calculation: Now, all tokens have been processed. We pop '16' and '1.5' from the operand stack, calculate (25 + 1.5) - 16 = 9.5 and push '9.5' back onto the operand stack. This '9.5' represents the final result.
* Conclusion: With the assumption that n = 5, the result of the expression x = n * 5 + 3 / 2 -16 is 9.5.
* This is then stored in the variable x.

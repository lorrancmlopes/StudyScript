# StudyScript
"StudyScript" is a domain-specific language designed for creating study routines. It provides a simple and intuitive way to define tasks for studying, incorporating features such as variables, conditionals, and loops.

```EBNF
STUDY_ROUTINE_PROGRAM = { BLOCK };

BLOCK = "study_routine", "\n", { STATEMENT }, "end_study_routine";

STATEMENT = "λ" | VARIABLE_DECLARATION 
            | ASSIGNMENT_STATEMENT 
            | CONDITIONAL_STATEMENT 
            | LOOP_STATEMENT 
            | TASK
            | PRINT_STATEMENT;

VARIABLE_DECLARATION = "var", IDENTIFIER, "=", (NUMBER | STRING), "\n";

ASSIGNMENT_STATEMENT = IDENTIFIER, "=", (NUMBER | STRING), "\n";

CONDITIONAL_STATEMENT = "if", "(", CONDITION, ")", "{", STATEMENT, "}", "else", "{", STATEMENT, "}";

LOOP_STATEMENT = "repeat", "(", NUMBER, ")", "{", STATEMENT, "}";

TASK = "task", ">>", "(", TASK_NAME, ",", NUMBER, ",", NUMBER, ")" , "\n";

TASK_NAME = "read_book"
            | "solve_exercises"
            | "watch_lecture"
            | "practice_quiz"
            | "review_notes";

NUMBER = DIGIT, { DIGIT };
DIGIT = "0" | "1" | "..." | "9";

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" };

LETTER = "A" | "B" | "..." | "Z" | "a" | "b" | "..." | "z";

CONDITION = EXPRESSION, ("==", ">", "<"), EXPRESSION;

EXPRESSION = TERM
            | EXPRESSION, ("+" | "-" | "*" | "/"), TERM
            | "(", EXPRESSION, ")"
            | IDENTIFIER
            | NUMBER
            | STRING;

STRING = '"' ,{ CHAR } , '"';

CHAR = any_character_except_double_quote;

PRINT_STATEMENT = "print", "(", IDENTIFIER, ")", "\n";

```

## Diagram: 

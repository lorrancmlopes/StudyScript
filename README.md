# StudyScript
"StudyScript" is a domain-specific language designed to simplify the process of creating study routines. It provides a structured and intuitive way to define tasks and manage study time effectively. The main idea behind StudyScript is to streamline the organization of study activities, making it easier for learners to plan and execute their study sessions.

## Code Example
```cpp
study_routine
    var study_time = 120

    // Check if there is enough time to read a book
    if (study_time >= 60) {
        task >> (read_book, 60, study_time)
    } else {
        print("There is not enough time to read a book.")
    }

    // Check if there is enough time to solve exercises
    if (study_time >= 45) {
        task >> (solve_exercises, 45, study_time)
    } else {
        print("There is not enough time to solve exercises.")
    }

    // Loop to watch multiple lectures until time runs out
    var num_lectures = 0
    while (study_time >= 30) {
        task >> (watch_lecture, 30, study_time)
        num_lectures = num_lectures + 1
    }
    print("Watched", num_lectures, "lectures.")

    // Conditional to decide if there is time for a quiz
    if (study_time >= 20) {
        task >> (practice_quiz, 20, study_time)
    } else {
        print("There is not enough time to take a quiz.")
    }

    // Loop to review notes until time runs out
    while (study_time >= 15) {
        task >> (review_notes, 15, study_time)
    }
end_study_routine

```

```EBNF
STUDY_ROUTINE_PROGRAM = { BLOCK };

BLOCK = "study_routine", "\n", { STATEMENT }, "end_study_routine";

STATEMENT = "λ" 
            | VARIABLE_DECLARATION 
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

PRINT_STATEMENT = "print", "(", EXPRESSION, { ",", EXPRESSION }, ")", "\n";

```

## Diagram: 

![Diagram](diagram.png)
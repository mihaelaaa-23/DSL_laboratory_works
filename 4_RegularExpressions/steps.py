def steps(regex_name):
    explanation = []

    if regex_name == "regex_1":
        explanation.append("Step 1: Match the first letter - it must be 'S' or 'T'")
        explanation.append("Step 2: Match the second letter - it must be 'U' or 'V'")
        explanation.append("Step 3: Match zero or more 'W' characters (0 to 5 allowed)")
        explanation.append("Step 4: Match one or more 'Y' characters (1 to 5 allowed)")
        explanation.append("Step 5: Match exactly the digits '24' at the end")

    elif regex_name == "regex_2":
        explanation.append("Step 1: Match 'L' at the beginning")
        explanation.append("Step 2: Match one of the letters: 'M', 'I', or 'N'")
        explanation.append("Step 3: Match exactly three 'O' characters")
        explanation.append("Step 4: Match zero to five 'P' characters")
        explanation.append("Step 5: Match the character 'Q'")
        explanation.append("Step 6: Match either '2' or '3' at the end")

    elif regex_name == "regex_3":
        explanation.append("Step 1: Match zero to five 'R' characters")
        explanation.append("Step 2: Match the letter 'S'")
        explanation.append("Step 3: Match one of the letters: 'T', 'U', or 'V'")
        explanation.append("Step 4: Match the character 'W'")
        explanation.append("Step 5: Match exactly two characters from the set {'X', 'Y', 'Z'}")

    return explanation
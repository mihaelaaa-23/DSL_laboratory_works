import random


class Generator:
    def __init__(self, expr):
        self.expr = expr
        self.chars = []

    def generate_string(self):
        string = []
        i = 0

        while i < len(self.expr):
            char = self.expr[i]

            if char == "(":
                group_end = self.expr.find(")", i)
                group_content = self.expr[i + 1:group_end]
                selected = self.generate_group(group_content)
                string.append(selected)
                i = group_end

            elif char == "*":
                last = string.pop()
                string.append(last * random.randint(0, 5))

            elif char == "+":
                last = string.pop()
                string.append(last * random.randint(1, 5))

            elif char == "^":
                repeat = int(self.expr[i + 1])
                last = string.pop()
                string.append(last * repeat)
                i += 1

            elif char == "?":
                last = string.pop()
                string.append(last * random.randint(0, 1))

            elif char == "{" and i + 2 < len(self.expr) and self.expr[i + 2] == "}":
                repeat = int(self.expr[i + 1])
                last = string.pop()
                string.append(last * repeat)
                i += 2

            elif char in {"|", ")", "}"}:
                pass

            else:
                string.append(char)

            i += 1

        return ' '.join(string)

    def generate_group(self, group_expr):
        options = group_expr.split("|")
        return random.choice(options)

    def generate_n_strings(self):
        for _ in range(5):
            print(self.generate_string())

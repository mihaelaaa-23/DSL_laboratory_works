class Generator:

    def generate_regex_1(self):
        results = []
        for a in ['S', 'T']:
            for b in ['U', 'V']:
                for w_count in range(0,6):
                    for y_count in range(1,6):
                        w = "W" * w_count
                        y = "Y" * y_count
                        word = a + b + w + y + "24"
                        results.append(word)
        return results

    def generate_regex_2(self):
        results = []
        for a in ['M', 'N']:
            for p_count in range(0, 6):
                for b in ['2', '3']:
                    p = 'P' * p_count
                    word = "L" + a + "OOO" + p + "Q" + b
                    results.append(word)
        return results

    def generate_regex_3(self):
        results = []
        xyz = ['X', 'Y', 'Z']
        for r_count in range(0, 6):
            for middle in ['T', 'U', 'V']:
                for x1 in xyz:
                    for x2 in xyz:
                        r = 'R' * r_count
                        word = r + "S" + middle + "W" + x1 + x2
                        results.append(word)
        return results
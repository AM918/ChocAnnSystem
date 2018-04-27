class ProviderDirectory:

    def __init__(self):
        """Setup for the provider directory."""

        # Code : [Name, fee]
        self.codes = {
            1 :  ['Arthritis Help', 65],
            2 :  ['Breath Training', 50],
            3 :  ['Chemotherapy', 160],
            4 :  ['Death Aversion', 999],
            5 :  ['Exercising', 15],
            6 :  ['Flute Balancing', 120],
            7 :  ['Grounding', 3],
            8 :  ['Hard Exercises', 20],
            9 :  ['Interesting Socioeconomic Theory', 687],
            10 : ['Jumping Jacks', 10]
        }

    def verify(self, code):
        """Gets information for a code."""

        if code in self.codes:
            return self.codes[code]
        return None

    def write(self):
        """Writes the provider directory to a file."""
        body = ""
        for key, value in self.codes:
           body += "CODE: " + key + "\t" + \
                   "NAME: " + value[0] + "\t" + \
                   "FEE: $" + value[1] + "\n" 
        file = open("provider_directory.txt", "w")
        file.write(body)
        file.close()

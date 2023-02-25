import random
import re
import shelve


class Robot:
    def __init__(self, state):
        self.state = state
        self.words = self.state["words"]

    def prompt(self, color, who):
        return f"\x1b[{color}m{who}>\x1B[0m "

    def niall_prompt(self):
        return self.prompt(33, "Niall")

    def run(self):
        print(self.niall_prompt(),
              "Hi, I'm Niall, how may I help you?")
        while True:
            s = input(self.prompt(35, "User"))
            if s == "#brain":
                print(self.words)
                continue
            s = re.sub(r"[^\w\s']", "", s)
            self.process_input(s)
            print(self.niall_prompt(),
                  " ".join(self.generate_output()))

    def process_input(self, s):
        words = s.strip().lower().split()
        for this_word, next_word in zip([""] + words,
                                        words + [""]):
            if this_word not in self.words:
                self.words[this_word] = {}
            if next_word not in self.words[this_word]:
                self.words[this_word][next_word] = 0
            self.words[this_word][next_word] += 1
        self.state["words"] = self.words

    def generate_output(self):
        word = ""
        while True:
            next_words = self.words[word]
            next_words = sum([[word] * count
                              for word, count in next_words.items()],
                             start=[])
            word = random.choice(next_words)
            if word == "":
                break
            yield word


def main(*args):
    with shelve.open("words") as state:
        try:
            Robot(state).run()
        except EOFError:
            print()


if __name__ == "__main__":
    main()

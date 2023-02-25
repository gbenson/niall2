import shelve

class Robot:
    def __init__(self, words):
        self.words = words

    def prompt(self, color, who):
        return f"\x1b[{color}m{who}>\x1B[0m "

    def niall_prompt(self):
        return self.prompt(33, "Niall")

    def run(self):
        print(self.niall_prompt(),
              "Hi, I'm Niall, how may I help you?")
        while True:
            s = input(self.prompt(35, "User"))
            print("You typed", s)

def main(*args):
    with shelve.open("words") as state:
        try:
            Robot(state).run()
        except EOFError:
            print()

if __name__ == "__main__":
    main()

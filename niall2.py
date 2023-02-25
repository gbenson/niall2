import shelve

class Robot:
    def __init__(self, words):
        self.words = words

    def run(self):
        pass

def main(*args):
    with shelve.open("words") as state:
        Robot(state).run()

if __name__ == "__main__":
    main()

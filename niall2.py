import os
import requests


class Robot:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.rs = requests.Session()

    def prompt(self, color, who):
        return f"\x1b[{color}m{who}>\x1B[0m "

    def niall_prompt(self):
        return self.prompt(33, "Niall")

    def run(self):
        print(self.niall_prompt(),
              "Hi, I'm Niall, how may I help you?")
        while True:
            response = self.rs.post(self.endpoint, json={
                "user_input": input(self.prompt(35, "User")),
            })
            response.raise_for_status()
            print(self.niall_prompt(), response.json()["niall_output"])


def main():
    filename = os.path.join(os.path.dirname(__file__), ".endpoint")
    with open(filename) as fp:
        endpoint = fp.read().strip()
    try:
        Robot(endpoint).run()
    except EOFError:
        print()


if __name__ == "__main__":
    main()

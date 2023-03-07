import os
import requests


class Robot:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.rs = requests.Session()
        self.dry_run = False

    def prompt(self, color, who):
        return f"\x1b[{color}m{who}>\x1B[0m "

    def niall_prompt(self):
        return self.prompt(33, "Niall")

    WILLWONT = ("will", "won't")

    def toggle_dry_run(self):
        self.dry_run = not self.dry_run
        print(f"{self.niall_prompt()}I "
              f"{self.WILLWONT[self.dry_run]} "
              "update my brain with your input")

    def run(self):
        print(self.niall_prompt(),
              "Hi, I'm Niall, how may I help you?")
        while True:
            user_input = input(self.prompt(35, "User"))
            if user_input in ("#test", "#dry"):
                self.toggle_dry_run()
                continue
            request = {"user_input": user_input}
            if self.dry_run:
                request["dry_run"] = True
            response = self.rs.post(self.endpoint, json=request)
            response.raise_for_status()
            niall_output = (response.json()["niall_output"]
                            .replace("[", "\x1B[32m[")
                            .replace("]", "]\x1B[0m"))
            print(self.niall_prompt() + niall_output)


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

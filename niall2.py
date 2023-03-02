import boto3
import copy
import random
import re
import shelve

from boto3.dynamodb.conditions import Key


class Robot:
    def __init__(self, state, table):
        self.table = table
        with self.table.batch_writer() as batch:
            self._batch_upload(state, batch)

    def _batch_upload(self, state, batch):
        words = copy.deepcopy(state["words"])
        for this_word, next_words in words.items():
            for next_word, count in next_words.items():
                batch.put_item(Item={
                    "From": this_word or "_",
                    "To": next_word or "_",
                    "Weight": count,
                })
                check = state["words"][this_word].pop(next_word)
                assert check == count
            check = state["words"].pop(this_word)
            print(check)

    def prompt(self, color, who):
        return f"\x1b[{color}m{who}>\x1B[0m "

    def niall_prompt(self):
        return self.prompt(33, "Niall")

    def run(self):
        print(self.niall_prompt(),
              "Hi, I'm Niall, how may I help you?")
        while True:
            s = input(self.prompt(35, "User"))
            s = re.sub(r"[^\w\s']", "", s)
            self.process_input(s)
            print(self.niall_prompt(),
                  " ".join(self.generate_output()))

    def process_input(self, s):
        words = s.strip().lower().split()
        for this_word, next_word in zip(["_"] + words,
                                        words + ["_"]):
            self.table.update_item(
                Key={
                    "From": this_word,
                    "To": next_word,
                },
                UpdateExpression="ADD Weight :one",
                ExpressionAttributeValues={
                    ":one": 1,
                }
            )

    def generate_output(self):
        word = "_"
        while True:
            response = self.table.query(
                KeyConditionExpression=Key("From").eq(word)
            )
            next_words = sum([[item["To"]] * int(item["Weight"])
                              for item in response["Items"]],
                             start=[])
            word = random.choice(next_words)
            if word == "_":
                break
            yield word


def main():
    dyn_resource = boto3.resource("dynamodb")
    table = dyn_resource.Table("Niall2")
    table.load()

    with shelve.open("words") as state:
        try:
            Robot(state, table).run()
        except EOFError:
            print()


if __name__ == "__main__":
    main()

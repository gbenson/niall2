import boto3
import json
import random
import re

from boto3.dynamodb.conditions import Key


class Robot:
    DEFAULT_ARGS = {
        "user_input": None,
        "dry_run": False,
    }

    def __init__(self):
        self._table = None

    @property
    def table(self):
        if self._table is None:
            self._table = self._init_table()
        return self._table

    def _init_table(self):
        dyn_resource = boto3.resource("dynamodb")
        table = dyn_resource.Table("Niall2")
        table.load()
        return table

    def __call__(self, event, context):
        args = self.DEFAULT_ARGS.copy()
        args.update(json.loads(event["body"]))
        user_input = args["user_input"]
        dry_run = args["dry_run"]

        # Analyse user input.
        if user_input:
            tokens = self.tokenize(user_input)
            if tokens and not dry_run:
                self.store(tokens)

        # Generate Niall's response.
        niall_output = " ".join(self.generate())
        if dry_run:
            niall_output = "[dry] " + niall_output
        response = {"niall_output": niall_output}
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(response),
        }

    def tokenize(self, s):
        """Sanitize user input, then split into tokens.

        :param s: What the user is saying to Niall.
        :returns: A sequence of tokens (i.e. words).
        """
        s = s.strip()
        s = re.sub(r"[^\w\s']", "", s)
        s = s.lower()
        return s.split()

    def store(self, tokens):
        """Store a sequence of tokens in the database.

        :param tokens: A sequence of tokens.
        """
        tokens = list(tokens)
        for this, next in zip(["_"] + tokens, tokens + ["_"]):
            self.table.update_item(
                Key={
                    "From": this,
                    "To": next,
                },
                UpdateExpression="ADD Weight :one",
                ExpressionAttributeValues={
                    ":one": 1,
                }
            )

    def generate(self):
        """Generate a sequence of tokens.

        :returns tokens: A sequence of tokens.
        """
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


lambda_handler = Robot()


if __name__ == "__main__":
    print(lambda_handler({
        "body": json.dumps({
            "user_input": "Hello Niall",
            "dry_run": True,
        })}, None))

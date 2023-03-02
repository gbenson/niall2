import os

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


# Read the endpoint url from a file
def read_endpoint_url():
    filename = os.path.join(os.path.dirname(__file__), ".datastore")
    with open(filename) as fp:
        return fp.read().strip()


# Select your transport with a defined url endpoint
transport = RequestsHTTPTransport(read_endpoint_url())

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide GraphQL queries
get_first_words = gql("""\
  query GetFirstWords {
    queryTransition(filter: {not: {has: from}}) {
      to {
        text
      }
      count
    }
  }""")

# Execute the query on the transport
result = client.execute(get_first_words)
print(result)

get_all_words = gql("""\
query GetAllWords {
  queryTransition {
    to {
      text
    }
    count
  }
}""")
result = client.execute(get_all_words)
print(result)

get_next_words = gql("""\
  query GetNextWords {
    queryTransition {
      from {
        text: "hello"
      }
      to {
        text
      }
      count
    }
  }
""")

result = client.execute(get_next_words)
print(result)

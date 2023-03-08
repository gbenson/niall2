const theInput = document.getElementById("input");
const messages = document.getElementById("messages");

document.addEventListener("DOMContentLoaded", () => {
  theInput.addEventListener("keydown", (e) => {
    if (e.code === "Enter") {
      let userInput = theInput.value;
      theInput.value = "";
      processInput(userInput);
    }
  });
});

const apiEndpointURL = ("https://nrtt8bz8be.execute-api.us" +
                        "-east-1.amazonaws.com/prod/niall2");

async function processInput(userInput) {
  userInput = userInput.trim();
  addToChat("user", userInput);

  const niallDiv = addToChat("niall", "...");

  const response = await fetch(apiEndpointURL, {
    method: "POST",
    headers: {
      // "application/json" would be better here, but
      // then CORS preflights every single request :(
      "Content-Type": "text/plain",
    },
    body: JSON.stringify({
      user_input: userInput,
      dry_run: true,
    }),
  });
  const json = await response.json();
  console.log(json);

  niallDiv.innerText = json["niall_output"];
  niallDiv.classList.remove("waiting");
}

function addToChat(sender, message) {
  const div = document.createElement("div");
  div.classList.add("message");
  div.classList.add(`from-${sender}`);

  const div2 = document.createElement("div");
  div2.classList.add("avatar");
  div.appendChild(div2);

  const div3 = document.createElement("div");
  if (sender == "niall") {
    div3.classList.add("waiting");
  }
  div3.innerText = message;
  div.appendChild(div3);

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight - messages.clientHeight;
  return div3;
}

window.onload = function () {
    document.getElementById("chat-input").addEventListener(
        // Allow messages to be sent when pressing ENTER
        "keypress", function (event) {
            if (event.key == 'Enter') {
                var element = document.getElementById("chat-display-window");
                sendMessage();

                // // Auto scroll the chat area
                element = document.getElementById("chat-display-window");
                var xh = element.scrollHeight;
                element.scrollTop = element.scrollHeight
            }
        }
    );

    healthcheck();
}

// Constants
const URL = "http://localhost:5005/";

// Date format constant variables
const options = {
    hour: '2-digit', minute: '2-digit'
};
const dateTimeFmt = new Intl.DateTimeFormat('es-MX', options).format;

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

async function healthcheck() {
    await sleep(1000);
    createContainer("Hola! Mi nombre es Milo. &#129302;", true);
    await sleep(1000);
    axios.get(
        URL,
    ).then(function (response) {
        if (response.status == 200) {
            createContainer("Dime, ¿en qué puedo ayudarte?", true);
        } else {
            createContainer("Me gustaría ayudarte, pero no me siento bien. &#129298;"), true;
        }
    }).catch(function (error) {
        createContainer("Lo lamento, por el momento no soy capaz de atender peticiones. &#128565;", true);
    });
}

/*
sendMessage extracts the text from the input box, sends an HTTP request to the
interpreter and updates the converation section according to the response from the
server.
*/
function sendMessage() {
    // First extract the text
    var element = document.getElementById("chat-input");
    var text = element.value.trim();

    // Don't send empty input
    if (text == "") {
        return
    }

    // Add a chat container
    createContainer(text);
    element.value = "";

    // Send request to HTTP Server
    sendRequest(text);

    // Auto scroll the chat area
    // element = document.getElementById("chat-display-window");
    // var xh = element.scrollHeight;
    // // element.scrollTo(0, xh);
    // element.scrollTop = element.scrollHeight;
}

function createContainer(textInput, response = false) {
    var messagesContainer = document.getElementById("chat-messages");

    // The chat bubble
    var newMessageDiv = document.createElement("div");
    newMessageDiv.classList.add("chat-container")

    // Avatar icon
    // XXX: Leave or delete it
    // var avatarIcon = document.createElement("img");
    // avatarIcon.src = "img/avatar.png"
    // avatarIcon.className = "right"

    // Text element
    var textMessageP = document.createElement("p");
    textMessageP.innerHTML = textInput;

    // Time element
    var date = new Date();
    var timeSpan = document.createElement("span")
    timeSpan.innerHTML = dateTimeFmt(date);

    if (response) {
        newMessageDiv.classList.add("darker");
        newMessageDiv.classList.add("chat-container-left");
        timeSpan.classList.add("time-right");
    }

    newMessageDiv.appendChild(textMessageP);
    // newMessageDiv.appendChild(avatarIcon);
    newMessageDiv.appendChild(timeSpan);
    messagesContainer.appendChild(newMessageDiv);
}

function sendRequest(text) {
    // TODO: Add this later
    axios.post(
        URL + "webhooks/rest/webhook",
        { "sender": "milo", "message": text },
        {
            "Content-Type": "application/json",
            "Accept": "*/*"
        }
    ).then(function (response) {
        if (response.status == 200) {
            createContainer(response.data[0].text, true);
        } else {
            createContainer("Disculpa, ahorita no me siento bien &#129298;"), true;
        }
    }).catch(function (error) {
        createContainer("Lo lamento, por el momento no soy capaz de atender peticiones. &#128565;", true);
    });
}

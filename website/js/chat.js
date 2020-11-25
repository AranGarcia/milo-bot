window.onload = function () {
    document.getElementById("chat-input").addEventListener(
        // Allow messages to be sent when pressing ENTER
        "keypress", function (event) {
            if (event.keyCode == 13) {
                sendMessage();
            }
        }
    );
}

// Constants
const URL = "http://localhost:5005/webhooks/rest/webhook";
const Http = new XMLHttpRequest();
Http.withCredentials = true;


// Date format constant variables
const options = {
    hour: '2-digit', minute: '2-digit'
};
const dateTimeFmt = new Intl.DateTimeFormat('es-MX', options).format;

/*
sendMessage extracts the text from the input box, sends an HTTP request to the
interpreter and updates the converation section according to the response from the
server.
*/
function sendMessage() {
    // First extract the text
    element = document.getElementById("chat-input");
    text = element.value;

    // Add a chat container
    createContainer(text);
    element.value = "";

    // Auto scroll the chat area
    element = document.getElementById("chat-display-window");
    var xh = element.scrollHeight;
    element.scrollTo(0, xh);

    // Send request to HTTP Server
    sendRequest(text);

}

function createContainer(textInput) {
    var messagesContainer = document.getElementById("chat-messages");

    // The chat bubble
    var newMessageDiv = document.createElement("div");
    newMessageDiv.className = "chat-container"

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

    newMessageDiv.appendChild(textMessageP);
    // newMessageDiv.appendChild(avatarIcon);
    newMessageDiv.appendChild(timeSpan);
    messagesContainer.appendChild(newMessageDiv);
}

function sendRequest(text) {
    Http.open("POST", URL);
    Http.setRequestHeader("Content-Type", "application/json");
    Http.setRequestHeader("Accept", "*/*");
    Http.send(JSON.stringify({ "sender": "milo", "message": text }));
    Http.addEventListener("readystatechange", function () {
        if (this.readyState === 4 && this.status == 200) {
            console.log(this.responseText);
        } else {
            console.log(this);
        }
    });
}

var socket = io();

socket.on('connect', function() {
    console.log('socket connected');
});

var elementEventName = document.getElementById('event-name');
elementEventName.value = 'my event 1';

var elementMessage = document.getElementById('message');
elementMessage.value = 'my message 1';

var elementEmitButton = document.getElementById('emit-button');

var elementLogOutput = document.getElementById('log-output');
elementLogOutput.innerHTML = 'log output';


socket.onAny((event, message) => {
    let logAddition = sublogEventAndMessage('server', event, message);
    appendCurrLogWith(logAddition);
});

elementEmitButton.onclick = () => {
    let eventName = elementEventName.value;
    let message = elementMessage.value;
    let logAddition = sublogEventAndMessage('front', eventName, message);
    appendCurrLogWith(logAddition);
    let json = JSON.stringify({'event-name': eventName, 'message': message});
    socket.emit('json', json);
    socket.emit(eventName, message);
};

function sublogEventAndMessage(eventSource, eventName, jsonMessage) {
    return `${eventSource} emitted\n  event: ${eventName}\nmessage: ${JSON.stringify(jsonMessage)}`;
}

function getCurrTimeStr() {
    let date = new Date();
    return `${date.getFullYear()}.${(date.getMonth()+1).toString().padStart(2, '0')}.${date.getDate().toString().padStart(2, '0')}, ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
}

function appendCurrLogWith(logAddition) {
    elementLogOutput.innerHTML = `${getCurrTimeStr()}\n${logAddition}\n============\n${elementLogOutput.innerHTML}`;
}

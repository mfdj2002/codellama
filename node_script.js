const fs = require('fs');

// Define the named pipes
const PYTHON_TO_JS_PIPE = 'python_to_js_pipe';
const JS_TO_PYTHON_PIPE = 'js_to_python_pipe';

// Open pipes for reading and writing
const pythonToJsPipe = fs.openSync(PYTHON_TO_JS_PIPE, 'r');
const jsToPythonPipe = fs.openSync(JS_TO_PYTHON_PIPE, 'w');

// Read a message from Python
const messageFromPython = fs.readFileSync(pythonToJsPipe, 'utf-8').trim();

// Log the received message
console.log('Received message from Python:', messageFromPython);

// Process the message by appending to "Processed:"
const processedMessage = 'Processed: ' + messageFromPython;

// Log the message sent to Python
console.log('Sending message to Python:', processedMessage);

// Send the processed message back to Python
fs.writeSync(jsToPythonPipe, processedMessage);

// Close pipes
fs.closeSync(pythonToJsPipe);
fs.closeSync(jsToPythonPipe);


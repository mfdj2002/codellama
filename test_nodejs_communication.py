import subprocess
import os
import time
import platform
import win32pipe  # Import the win32pipe module from pywin32
import win32file

class TestNodeJSCommunication:
    def setUp(self):
        # Create pipes based on the operating system
        if platform.system() == 'Windows':
            self.create_named_pipe("python_to_js_pipe")
            # Note: 'js_to_python_pipe' is created by the Node.js script
        else:
            os.mkfifo("python_to_js_pipe")
            # Note: 'js_to_python_pipe' is created by the Node.js script

    def tearDown(self):
        # Remove pipes after the test
        os.remove("python_to_js_pipe")
        # Note: 'js_to_python_pipe' is removed by the Node.js script after the test

    def create_named_pipe(self, pipe_name):
        # Create named pipes on Windows using pywin32
        if platform.system() == 'Windows':
            win32pipe.CreateNamedPipe(fr'\\.\pipe\{pipe_name}', win32pipe.PIPE_ACCESS_DUPLEX,
                                      win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                                      1, 65536, 65536, 300, None)
        else:
            os.mkfifo(pipe_name)

    def test_nodejs_communication(self):
        # Start the Node.js script as a subprocess
        js_process = subprocess.Popen(['node', 'node_script.js'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            # Wait for the 'js_to_python_pipe' to be created by the Node.js script
            time.sleep(2)  # Adjust the sleep duration based on your needs

            # Open pipes for reading and writing
            with open("python_to_js_pipe", 'wb') as python_to_js_pipe, open("js_to_python_pipe", 'rb') as js_to_python_pipe:
                # User input: Get a string from the user
                message_to_js = input("Enter a message to send to Node.js: ")
                python_to_js_pipe.write(message_to_js.encode('utf-8'))
                python_to_js_pipe.flush()

                # Wait for a response from Node.js
                time.sleep(5)  # You might want to use more robust synchronization methods

                # Read the response from Node.js
                message_from_js = js_to_python_pipe.read().decode('utf-8').strip()

                # Print the message received from Node.js
                print('Received message from Node.js:', message_from_js)

                # Assert that the processed message matches the expected response
                assert message_from_js == f"Processed: {message_to_js}"


        finally:
            # Terminate the Node.js subprocess
            js_process.terminate()

if __name__ == '__main__':
    test_instance = TestNodeJSCommunication()
    test_instance.setUp()
    test_instance.test_nodejs_communication()
    test_instance.tearDown()




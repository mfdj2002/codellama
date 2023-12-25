// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const { spawn } = require('child_process');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// // This line of code will only be executed once when your extension is activated
	// console.log('Congratulations, your extension "codesummarizer" is now active!');

	// // The command has been defined in the package.json file
	// // Now provide the implementation of the command with  registerCommand
	// // The commandId parameter must match the command field in package.json
	// let disposable = vscode.commands.registerCommand('codesummarizer.helloWorld', function () {
	// 	// The code you place here will be executed every time your command is executed

	// 	// Display a message box to the user
	// 	vscode.window.showInformationMessage('Hello World from CodeSummarizer!');
	// });

	// context.subscriptions.push(disposable);
	
	let summarizer = spawn('python', ['path/to/your/script.py']);
	let disposable = vscode.window.onDidChangeTextEditorSelection(event => {
        // Check if the selection is non-empty (highlighted text)
        if (!event.selections[0].isEmpty) {
            const document = event.textEditor.document;
            const selection = event.selections[0];

            // Handle the highlighted text
            handleHighlight(document, selection);
        }
    });

    context.subscriptions.push(disposable);
}

function handleHighlight(document, selection) {
    // Logic to handle the highlighted text
}


	// let hoverProvider = vscode.languages.registerHoverProvider('*', {
    //     provideHover(document, position, token) {
    //         // Asynchronous operation wrapped in a promise
    //         const asyncOperation = new Promise((resolve, reject) => {
    //             fetchSummary(document, position, token, resolve, reject);
    //         });

    //         // Timeout promise
    //         const timeout = new Promise((resolve) => {
    //             const checkInterval = setInterval(() => {
    //                 if (token.isCancellationRequested) {
    //                     clearInterval(checkInterval);
    //                     resolve(null); // Resolve with null if cancelled
    //                 }
    //             }, 1000); // Check every 1 second for cancellation

    //             // Set a maximum time for the operation (e.g., 10 seconds)
    //             setTimeout(() => {
    //                 clearInterval(checkInterval);
    //                 resolve(null); // Resolve with null on timeout
    //             }, 10000);
    //         });

    //         // Race between async operation and timeout
    //         return Promise.race([asyncOperation, timeout]);
    //     }
    // });


    // context.subscriptions.push(hoverProvider);
// }

function fetchSummary(document, position, token, resolve, reject) {
    // Perform the actual async task
    // Example: Fetch data, perform calculations, etc.
    // Resolve the promise when the operation is complete
    // Example: resolve(new vscode.Hover("Hover Information"));
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}


//git remote add project-a /path/to/project-a
// git fetch project-a --tags
// git merge --allow-unrelated-histories project-a/master # or whichever branch you want to merge
// git remote remove project-a
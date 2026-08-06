const vscode = require('vscode');
const { LanguageClient } = require('vscode-languageclient/node');

let client;

function activate(context) {
    const serverOptions = {
        command: 'C:/Coding/Python/Two/.venv/Scripts/python.exe',
        args: ['-m', 'test2.Main.LanguageServer.Main'],
        options: {
            env: {
                ...process.env,
                PYTHONPATH: 'C:/Coding/Python/Two/Test/TheLanguage' + 
                    (process.env.PYTHONPATH ? ';' + process.env.PYTHONPATH : '')
            }
        }
    };

    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'mylang' }],
    };

    client = new LanguageClient('myLangServer', 'My Lang Server', serverOptions, clientOptions);
    
    client.start();

    

}

function deactivate() {
    if (client) return client.stop();
}

module.exports = { activate, deactivate };
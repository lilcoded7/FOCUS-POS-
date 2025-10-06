const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let djangoProcess;

function createWindow() {
  // Absolute path to your Django EXE
  const exePath = path.join(__dirname, 'dist', 'SetupBackend.exe');

  // Start Django server
  djangoProcess = spawn(exePath, [], { stdio: 'inherit' });

  // Create the Electron window
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false
    }
  });

  // Wait a few seconds for Django to start
  setTimeout(() => {
    win.loadURL('http://127.0.0.1:8765'); // match host/port from runserver.py
  }, 5000);
}

// Close Django process when Electron exits
app.on('window-all-closed', () => {
  if (djangoProcess) djangoProcess.kill();
  if (process.platform !== 'darwin') app.quit();
});

app.on('ready', createWindow);

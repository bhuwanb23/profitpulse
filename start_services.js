/**
 * Service Startup Script
 * Starts both Backend and AI/ML services for testing
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Service processes
let backendProcess = null;
let aiMlProcess = null;

// Cleanup function
function cleanup() {
  log('\n\n🛑 Shutting down services...', 'yellow');
  
  if (backendProcess) {
    log('Stopping Backend...', 'yellow');
    backendProcess.kill('SIGTERM');
  }
  
  if (aiMlProcess) {
    log('Stopping AI/ML...', 'yellow');
    aiMlProcess.kill('SIGTERM');
  }
  
  setTimeout(() => {
    log('✅ Services stopped', 'green');
    process.exit(0);
  }, 2000);
}

// Handle process termination
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('exit', cleanup);

// Start Backend
function startBackend() {
  log('\n🚀 Starting Backend Service...', 'cyan');
  
  const backendPath = path.join(__dirname, 'backend');
  const isWindows = process.platform === 'win32';
  
  // Check if node_modules exists
  if (!fs.existsSync(path.join(backendPath, 'node_modules'))) {
    log('⚠️  node_modules not found. Installing dependencies...', 'yellow');
    const installProcess = spawn(isWindows ? 'npm.cmd' : 'npm', ['install'], {
      cwd: backendPath,
      stdio: 'inherit',
      shell: true
    });
    
    installProcess.on('close', (code) => {
      if (code === 0) {
        log('✅ Dependencies installed', 'green');
        startBackendProcess();
      } else {
        log('❌ Failed to install dependencies', 'red');
        process.exit(1);
      }
    });
  } else {
    startBackendProcess();
  }
  
  function startBackendProcess() {
    backendProcess = spawn(isWindows ? 'npm.cmd' : 'npm', ['run', 'dev'], {
      cwd: backendPath,
      stdio: 'inherit',
      shell: true,
      env: {
        ...process.env,
        PORT: '3000',
        NODE_ENV: 'development'
      }
    });
    
    backendProcess.on('error', (error) => {
      log(`❌ Backend error: ${error.message}`, 'red');
    });
    
    backendProcess.on('exit', (code) => {
      if (code !== 0 && code !== null) {
        log(`❌ Backend exited with code ${code}`, 'red');
      }
    });
    
    log('✅ Backend process started (PID: ' + backendProcess.pid + ')', 'green');
  }
}

// Start AI/ML
function startAIML() {
  log('\n🚀 Starting AI/ML Service...', 'cyan');
  
  const aiMlPath = path.join(__dirname, 'ai-ml');
  const isWindows = process.platform === 'win32';
  
  // Check if venv exists
  const venvPath = path.join(aiMlPath, 'venv');
  const venvPython = isWindows 
    ? path.join(venvPath, 'Scripts', 'python.exe')
    : path.join(venvPath, 'bin', 'python');
  
  let pythonCmd = 'python';
  
  if (fs.existsSync(venvPython)) {
    pythonCmd = venvPython;
    log('✅ Using virtual environment', 'green');
  } else {
    log('⚠️  Virtual environment not found. Using system Python', 'yellow');
    log('   To create venv: cd ai-ml && python -m venv venv', 'yellow');
  }
  
  // Start AI/ML service
  aiMlProcess = spawn(pythonCmd, [
    '-m', 'uvicorn',
    'src.api.main:app',
    '--host', '0.0.0.0',
    '--port', '8000',
    '--reload'
  ], {
    cwd: aiMlPath,
    stdio: 'inherit',
    shell: true,
    env: {
      ...process.env,
      PYTHONPATH: aiMlPath,
      MODEL_SERVER_PORT: '8000',
      DEBUG: 'true'
    }
  });
  
  aiMlProcess.on('error', (error) => {
    log(`❌ AI/ML error: ${error.message}`, 'red');
    if (error.code === 'ENOENT') {
      log('   Make sure Python and uvicorn are installed', 'yellow');
      log('   Install: pip install uvicorn fastapi', 'yellow');
    }
  });
  
  aiMlProcess.on('exit', (code) => {
    if (code !== 0 && code !== null) {
      log(`❌ AI/ML exited with code ${code}`, 'red');
    }
  });
  
  log('✅ AI/ML process started (PID: ' + aiMlProcess.pid + ')', 'green');
}

// Main execution
function main() {
  log('\n' + '='.repeat(60), 'cyan');
  log('🚀 SuperHack Service Startup', 'cyan');
  log('='.repeat(60), 'cyan');
  
  // Start services
  startBackend();
  startAIML();
  
  log('\n✅ Both services are starting...', 'green');
  log('📝 Backend: http://localhost:3000', 'cyan');
  log('📝 AI/ML: http://localhost:8000', 'cyan');
  log('📝 AI/ML Docs: http://localhost:8000/docs', 'cyan');
  log('\n⚠️  Press Ctrl+C to stop all services', 'yellow');
}

// Run
main();


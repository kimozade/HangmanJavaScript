## Features
- Menu with options: play, show results, and exit
- Random word selection from a small set of programming languages
- Up to 8 incorrect attempts per round
- Input validation for single lowercase English letters
- Session scoreboard (wins/losses) until the app is closed

## Requirements
- Node.js (LTS recommended)
- npm (comes with Node.js)

## Installation
```shell script
# Install dependencies
npm install
```


If dependencies are already installed, you can skip this step.

## Running the game
From the project root:
```shell script
node "Hangman (JavaScript)/task/main.js"
```


Examples:
- macOS/Linux:
```shell script
node "Hangman (JavaScript)/task/main.js"
```

- Windows (PowerShell):
```textmate
node "Hangman (JavaScript)/task/main.js"
```


## How to play
- You’ll see a masked word as dashes (e.g., ----).
- Type a single lowercase English letter and press Enter.
- Correct letters reveal in place; incorrect guesses reduce remaining attempts.
- The round ends when you either guess the word or run out of attempts.
- Use the menu prompt to:
  - play — start a new round
  - results — show current session scoreboard
  - exit — quit the application

Notes:
- Only lowercase English letters are accepted.
- Repeated guesses are detected and won’t consume attempts.

## Project structure (high-level)
- Hangman (JavaScript)/task/main.js — main game entry point
- Hangman (JavaScript)/task/Debugger.js — optional helper for debugging locally
- package.json — project metadata and dependencies

## Troubleshooting
- Command not found: node
  - Ensure Node.js is installed and available in your PATH.
- Input behaves oddly in some terminals
  - Try running the command directly in your system terminal instead of an embedded terminal.
- Permissions or path issues on macOS/Linux
  - Wrap paths with spaces in quotes as shown above.

## Contributing
- Fork the repository
- Create a feature branch
- Submit a pull request describing your changes

## License
Specify your license here (for example, MIT).


let input = require('sync-input');

function getRandomElement(array) {
    let index = Math.floor(Math.random() * array.length);
    return array[index];
}

function isEnglishLetter(str) {
    // Проверяем каждый символ в строке
    for (let char of str) {
        if (!/^[a-z]$/.test(char)) {
            return false;
        }
    }
    return true;
}

let winning = 0;
let losing = 0;

function playGame() {
    let languages = ['python', 'java', 'swift', 'javascript'];

    let selectedLanguage = getRandomElement(languages);
    let chars = selectedLanguage.split('');
    let guessedLetters = new Array(chars.length).fill('-');
    let attempts = 8;

    //console.log(`H A N G M A N \n`);
    console.log(guessedLetters.join(''));

    while (attempts > 0 && guessedLetters.includes('-')) {
        let letter = input('Input a letter: ');

        // Проверяем длину строки (количество символов)
        if ([...letter].length !== 1 && isEnglishLetter(letter)) {
            console.log('Please, input a single letter.');
            console.log(guessedLetters.join(''));
            continue;
        }

        // Проверяем, что это английская буква
        if (!isEnglishLetter(letter) && letter.length >= 1) {
            console.log('Please, enter a lowercase letter from the English alphabet.');
            console.log(guessedLetters.join(''));
            continue;
        }

        // ИГРОВАЯ ЛОГИКА
        if (guessedLetters.includes(letter)) {
            console.log('You\'ve already guessed this letter.');
            console.log(guessedLetters.join(''));
        } else if (chars.includes(letter)) {
            for (let i = 0; i < chars.length; i++) {
                if (chars[i] === letter) {
                    guessedLetters[i] = letter;
                }
            }
            console.log(guessedLetters.join(''));
        } else {
            console.log(guessedLetters.join(''));
            console.log(`That letter doesn't appear in the word.`);
            attempts--;
        }
    }

    if (!guessedLetters.includes('-')) {
        console.log(`You guessed the word ${selectedLanguage}!`);
        console.log('You survived!');
        winning++;
    } else {
        console.log('You lost!');
        losing++;
    }
    return;
}

console.log(`H A N G M A N`);
//playGame();
while (true) {
    let menu = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')

    if (menu === 'play') {
        playGame();
        /*if (playGame === true) {
            winning++;
        } else {
            losing++;
        }*/
    } else if (menu === 'results') {
        console.log(`You won: ${winning} times.\nYou lost: ${losing} times.`);
    } else if (menu === 'exit') {
        break;
    } else {
        console.log('Invalid input. Please enter "play", "results", or "exit".');
    }
}
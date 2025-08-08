let input = require('sync-input');

function getRandomElement(array) {
    let index = Math.floor(Math.random() * array.length);
    return array[index];
}

let languages = ['python', 'java', 'swift', 'javascript'];

let selectedLanguage = getRandomElement(languages);
let chars = selectedLanguage.split('');
let guessedLetters = new Array(chars.length).fill('-');
let attempts = 8;
let englishAlphabet = /^[a-zA-Z]$/;

console.log(`H A N G M A N \n`);
console.log(guessedLetters.join(''));

while (attempts > 0 && guessedLetters.includes('-')) {
    let letter = input('Input a letter: ');

    // ОТЛАДОЧНАЯ ИНФОРМАЦИЯ
    console.log(`DEBUG: Введено: "${letter}"`);
    console.log(`DEBUG: Длина: ${letter.length}`);
    console.log(`DEBUG: Коды символов: ${letter.split('').map(c => c.charCodeAt(0))}`);

    if (letter.length !== 1) {
        console.log('Please, input a single letter.');
        console.log(guessedLetters.join(''));
        continue;
    }

    if (!englishAlphabet.test(letter)) {
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
} else {
    console.log('You lost!');
}
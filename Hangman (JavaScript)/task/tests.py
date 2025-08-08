from typing import List

from hstest import StageTest, dynamic_test, TestedProgram, WrongAnswer, CheckResult
from string import ascii_lowercase
from random import shuffle


class GameOverException(Exception):
    pass


class Config:
    SURVIVED_MESSAGE = 'You survived!'
    HANGED_MESSAGE = 'You lost!'
    MAX_TRIES = 8
    INPUT_ANNOUNCEMENT = 'Input a letter'
    INCORRECT_LETTER_MESSAGE = 'That letter doesn\'t appear in the word'
    GUESSED_THE_WORD_MESSAGE = 'You guessed the word #LANGUAGE#!'
    REOPEN_LETTER_MESSAGE = 'You\'ve already guessed this letter'
    MORE_THAN_ONE_LETTER_MESSAGE = 'Please, input a single letter'
    NON_ASCII_LETTER_MESSAGE = 'Please, enter a lowercase letter from the English alphabet'
    MENU_PROMPT = 'Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit'
    WINS_MESSAGE = 'You won: #COUNT# times.'
    LOSSES_MESSAGE = 'You lost: #COUNT# times.'

    @staticmethod
    def languages():
        return [
            'java',
            'python',
            'swift',
            'javascript',
        ]

    @classmethod
    def mask_language_map(cls):
        return {cls.make_language_mask(language): language for language in cls.languages()}

    @classmethod
    def make_language_mask(cls, word):
        return '-' * len(word)


class GameState:
    def __init__(self, program: TestedProgram, language: str, tries: int):
        self.program = program
        self.language = language
        self.tries = tries
        self.opened_letters = set()
        self.current_input = None
        self.output = None
        self.current_language_mask = self._language_mask(language)
        self.prev_language_mask = self._language_mask(language)
        self.wins = 0
        self.losses = 0

    def open_letter(self, letter: str) -> bool:
        self.current_input = letter
        self.output = self.program.execute(letter).strip()
        
        if len(letter) != 1 or not letter.islower():
            return False
            
        if letter in self.opened_letters:
            return False
            
        self.opened_letters.add(letter)
        
        if letter in self.language:
            self._update_language_mask()
            return True
            
        self.tries -= 1
        return False

    def _update_language_mask(self):
        self.prev_language_mask = self.current_language_mask
        self.current_language_mask = self._language_mask(self.language)

    def _language_mask(self, language: str) -> str:
        return ''.join(letter if letter in self.opened_letters else '-' for letter in language)

    @property
    def game_ended(self) -> bool:
        return self.tries <= 0 or self.current_language_mask == self.language

    @property
    def hanged(self) -> bool:
        return self.tries <= 0

    @property
    def survived(self) -> bool:
        return self.current_language_mask == self.language


class ValidationHelper:
    @staticmethod
    def validate_output(output: str, game_state: GameState) -> None:
        output_lower = output.lower()
        input_announcement = Config.INPUT_ANNOUNCEMENT.lower()
        
        # Do not check for "Input a letter" if the game is over
        if not game_state.game_ended:
            if not any(input_announcement in line.lower() for line in output.split('\n')):
                raise WrongAnswer("The output doesn't contain any \"Input a letter\" lines.")

        if len(game_state.current_input) > 1:
            if Config.MORE_THAN_ONE_LETTER_MESSAGE.lower() not in output_lower:
                raise WrongAnswer(f"The output doesn't contain \"{Config.MORE_THAN_ONE_LETTER_MESSAGE}\" message.")
            return

        if not game_state.current_input.islower():
            if Config.NON_ASCII_LETTER_MESSAGE.lower() not in output_lower:
                raise WrongAnswer(f"The output doesn't contain \"{Config.NON_ASCII_LETTER_MESSAGE}\" message.")
            return

        if game_state.current_input in game_state.opened_letters and \
           game_state.current_input != game_state.current_input:  # Check only for repeated input
            if Config.REOPEN_LETTER_MESSAGE.lower() not in output_lower:
                raise WrongAnswer(f"The output doesn't contain \"{Config.REOPEN_LETTER_MESSAGE}\" message.")
            return

        if game_state.current_input not in game_state.language and \
           len(game_state.current_input) == 1 and game_state.current_input.islower():
            if Config.INCORRECT_LETTER_MESSAGE.lower() not in output_lower:
                raise WrongAnswer(f"The output doesn't contain \"{Config.INCORRECT_LETTER_MESSAGE}\" message.")

    @staticmethod
    def validate_game_end(output: str, game_state: GameState) -> None:
        output_lower = output.lower()

        if game_state.survived:
            if Config.SURVIVED_MESSAGE.lower() not in output_lower:
                raise WrongAnswer(f"The output doesn't contain \"{Config.SURVIVED_MESSAGE}\" message.")
            if Config.GUESSED_THE_WORD_MESSAGE.replace('#LANGUAGE#', game_state.language).lower() not in output_lower:
                raise WrongAnswer(f"The output doesn't contain correct guessed word message.")
            game_state.wins += 1
        elif game_state.hanged:
            if Config.HANGED_MESSAGE.lower() not in output_lower:
                raise WrongAnswer(f"The output doesn't contain \"{Config.HANGED_MESSAGE}\" message.")
            game_state.losses += 1

    @staticmethod
    def validate_menu(output: str) -> None:
        if Config.MENU_PROMPT.lower() not in output.lower():
            raise WrongAnswer(f"The output doesn't contain menu prompt: \"{Config.MENU_PROMPT}\"")

    @staticmethod
    def validate_results(output: str, wins: int, losses: int) -> None:
        output_lower = output.lower()
        wins_message = Config.WINS_MESSAGE.replace('#COUNT#', str(wins)).lower()
        losses_message = Config.LOSSES_MESSAGE.replace('#COUNT#', str(losses)).lower()

        if wins_message not in output_lower:
            raise WrongAnswer(f"The output doesn't contain correct wins count message: \"{wins_message}\"")
        if losses_message not in output_lower:
            raise WrongAnswer(f"The output doesn't contain correct losses count message: \"{losses_message}\"")


class HangmanTest(StageTest):
    def __init__(self, source_name: str = ''):
        super().__init__(source_name)
        self.survived_history = {language: False for language in Config.languages()}
        self.hanged_history = {language: False for language in Config.languages()}

    @dynamic_test(order=1)
    def test_menu_and_game(self):
        pr = TestedProgram(self.source_name)
        first_block = pr.start().strip()
        helper = ValidationHelper()
        
        # Check initial menu
        helper.validate_menu(first_block)
        
        # Play and win game
        output = pr.execute("play").strip()
        language = self._parse_language(output)
        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        self._play_game(game_state, should_win=True)
        
        # Check results
        output = pr.execute("results").strip()
        helper.validate_results(output, wins=1, losses=0)
        helper.validate_menu(output)
        
        # Play and lose game
        output = pr.execute("play").strip()
        language = self._parse_language(output)
        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        self._play_game(game_state, should_win=False)
        
        # Check updated results
        output = pr.execute("results").strip()
        helper.validate_results(output, wins=1, losses=1)
        helper.validate_menu(output)
        
        # Exit game
        output = pr.execute("exit").strip()
        if not pr.is_finished():
            raise WrongAnswer("The game didn't exit after 'exit' command")

        return CheckResult.correct()

    def _parse_language(self, output: str) -> str:
        lines = output.strip().split('\n')
        
        # Find the line with dashes
        mask = None
        for line in lines:
            line = line.strip()
            if line and all(c == '-' for c in line):
                mask = line
                break
                
        if not mask:
            raise WrongAnswer("Cannot find the word mask in the output")
            
        language = Config.mask_language_map().get(mask)
        if not language:
            raise WrongAnswer(f"Unknown word mask: {mask}")
            
        return language

    def _play_game(self, game_state: GameState, should_win: bool) -> None:
        helper = ValidationHelper()
        letters = list(game_state.language if should_win else ascii_lowercase)
        shuffle(letters)
        
        test_inputs = []
        # Add invalid input data
        test_inputs.extend(['aa', 'A', '1', '*'])  # Invalid characters
        test_inputs.extend(letters)  # Correct/incorrect letters
        
        for letter in test_inputs:
            if game_state.game_ended:
                break
                
            game_state.open_letter(letter)
            helper.validate_output(game_state.output, game_state)
            
            if game_state.game_ended:
                helper.validate_game_end(game_state.output, game_state)
                helper.validate_menu(game_state.output)


if __name__ == '__main__':
    HangmanTest('hangman.hangman').run_tests()

from enum import Enum, auto
from dataclasses import dataclass
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Game state enums
class Scene(Enum):
    CROSSROAD = auto()
    LAKE = auto()
    HOUSE = auto()
    END = auto()

class Choice(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    WAIT = 'wait'
    SWIM = 'swim'
    RED = 'red'
    BLUE = 'blue'
    YELLOW = 'yellow'

class GameOver(Exception):
    """Custom exception to represent game over."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

@dataclass
class GameState:
    current_scene: Scene = Scene.CROSSROAD
    is_alive: bool = True
    won: bool = False

class InputProvider:
    """Abstract input to make testable or swappable."""
    def get_input(self, prompt: str) -> str:
        return input(prompt).strip().lower()

class GameEngine:
    def __init__(self, input_provider: InputProvider):
        self.state = GameState()
        self.input_provider = input_provider

    def run(self):
        self.show_intro()
        try:
            while self.state.is_alive and self.state.current_scene != Scene.END:
                self.route_scene()
        except GameOver as e:
            logger.info(e.message)

    def route_scene(self):
        match self.state.current_scene:
            case Scene.CROSSROAD:
                self.handle_crossroad()
            case Scene.LAKE:
                self.handle_lake()
            case Scene.HOUSE:
                self.handle_house()

    def show_intro(self):
        #TREASURE ISLAND
        # The Below ascii art is from : https://ascii.co.uk/art
        logger.info('''
        *******************************************************************************
                  |                   |                  |                     |
         _________|________________.=""_;=.______________|_____________________|_______
        |                   |  ,-"_,=""     `"=.|                  |
        |___________________|__"=._o`"-._        `"=.______________|___________________
                  |                `"=._o`"=._      _`"=._                     |
         _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
        |                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
        |___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
                  |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
         _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
        |                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
        |___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
        ____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
        /______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
        ____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
        /______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
        ____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
        /______/______/______/______/______/______/______/______/______/______/_____ /
        *******************************************************************************
        ''')        
        logger.info("Welcome to Treasure Island.")
        logger.info("Your mission is to find the treasure.")

    def handle_crossroad(self):
        choice = self.ask("You're at a crossroad. Type 'left' or 'right': ", [Choice.LEFT, Choice.RIGHT])
        if choice == Choice.LEFT:
            self.state.current_scene = Scene.LAKE
        else:
            raise GameOver("You fell into a hole. Game Over.")

    def handle_lake(self):
        choice = self.ask("You see a lake. Type 'wait' for a boat or 'swim': ", [Choice.WAIT, Choice.SWIM])
        if choice == Choice.WAIT:
            self.state.current_scene = Scene.HOUSE
        else:
            raise GameOver("You tried to swim and drowned. Game Over.")

    def handle_house(self):
        choice = self.ask("You arrive at a house with 3 doors: red, blue, yellow. Choose one: ", 
                          [Choice.RED, Choice.BLUE, Choice.YELLOW])
        if choice == Choice.RED:
            raise GameOver("Burned by fire. Game Over.")
        elif choice == Choice.BLUE:
            raise GameOver("Eaten by beasts. Game Over.")
        elif choice == Choice.YELLOW:
            self.state.won = True
            self.state.current_scene = Scene.END
            logger.info("You found the treasure! You win!")

    def ask(self, prompt: str, valid_choices: list[Choice]) -> Choice:
        while True:
            response = self.input_provider.get_input(prompt)
            for choice in valid_choices:
                if response == choice.value:
                    return choice
            logger.warning("Invalid choice. Try again.")

if __name__ == "__main__":
    engine = GameEngine(InputProvider())
    engine.run()
  


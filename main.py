from tkinter import *
import random
import os

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 69
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "yellow"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "#000000"
HIGH_SCORE_FILE = "highscore.txt"


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(oval)


class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, oval)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    save_high_score(score)
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    high_score = get_high_score()
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
                       font=('consolas', 30), text="High Score: {}".format(high_score), fill="white")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 100,
                       font=('consolas', 30), text="Press R to restart", fill="lightgreen")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 150,
                       font=('consolas', 30), text="Press Q to quit", fill="yellow")
    window.bind('<r>', restart_game)
    window.bind('<q>', quit_game)


def start_game(event=None):
    global game_started
    if not game_started:
        game_started = True
        canvas.delete("start")
        next_turn(snake, food)


def save_high_score(new_score):
    high_score = get_high_score()
    if new_score > high_score:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))


def get_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as file:
        return int(file.read())


def restart_game(event=None):
    global score, direction, game_started
    score = 0
    direction = 'down'
    game_started = False
    label.config(text="Score:{}".format(score))
    canvas.delete(ALL)
    snake.coordinates = []
    snake.squares = []
    for i in range(0, BODY_PARTS):
        snake.coordinates.append([0, 0])
    for x, y in snake.coordinates:
        oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
        snake.squares.append(oval)
    food.__init__()
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                       font=('consolas', 40), text="Press ENTER to start the game", fill="white", tag="start")
    window.bind('<Return>', start_game)


def quit_game(event=None):
    window.destroy()


window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'
game_started = False

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                   font=('consolas', 40), text="Press ENTER to start the game", fill="white", tag="start")

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', start_game)

snake = Snake()
food = Food()

window.mainloop()

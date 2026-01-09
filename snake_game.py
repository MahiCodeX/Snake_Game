import tkinter as tk
import random

# ---------- SETTINGS ----------
WIDTH = 400
HEIGHT = 400
BOX = 20

LEVEL_SPEED = {
    1: 300,
    2: 260,
    3: 220,
    4: 180
}

LEVEL_COLOR = {
    1: "green",
    2: "blue",
    3: "yellow",
    4: "orange"
}

LEVEL_SCORE_LIMIT = {
    1: 5,
    2: 10,
    3: 15
}

# ---------- WINDOW ----------
root = tk.Tk()
root.title("Snake Game")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

restart_btn = tk.Button(root, text="Restart Game", bg="orange")
restart_btn.pack(pady=5)

# ---------- GAME VARIABLES ----------
snake = []
direction = "Right"
food = (0, 0)
score = 0
level = 1
game_running = True
waiting_for_click = False
badge_text = ""

# ---------- FUNCTIONS ----------
def draw():
    canvas.delete("all")

    canvas.create_text(10, 10,
        text=f"Score: {score}   Level: {level}",
        fill="white", anchor="nw", font=("Arial", 12))

    for x, y in snake:
        canvas.create_rectangle(
            x, y, x+BOX, y+BOX,
            fill=LEVEL_COLOR[level]
        )

    fx, fy = food
    canvas.create_oval(fx, fy, fx+BOX, fy+BOX, fill="red")

    if waiting_for_click:
        canvas.create_text(
            WIDTH//2, HEIGHT//2,
            text=badge_text,
            fill="gold",
            font=("Arial", 18, "bold")
        )
        canvas.create_text(
            WIDTH//2, HEIGHT//2 + 30,
            text="Click anywhere to continue",
            fill="white",
            font=("Arial", 12)
        )


def change_direction(new_dir):
    global direction
    if new_dir == "Left" and direction != "Right":
        direction = new_dir
    elif new_dir == "Right" and direction != "Left":
        direction = new_dir
    elif new_dir == "Up" and direction != "Down":
        direction = new_dir
    elif new_dir == "Down" and direction != "Up":
        direction = new_dir


def wrap_position(x, y):
    if x < 0:
        x = WIDTH - BOX
    elif x >= WIDTH:
        x = 0
    if y < 0:
        y = HEIGHT - BOX
    elif y >= HEIGHT:
        y = 0
    return x, y


def move_snake():
    global food, score, game_running, waiting_for_click, badge_text, level

    if not game_running or waiting_for_click:
        return

    x, y = snake[0]

    if direction == "Left":
        x -= BOX
    elif direction == "Right":
        x += BOX
    elif direction == "Up":
        y -= BOX
    elif direction == "Down":
        y += BOX

    # WALL LOGIC
    if level == 1:
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_over()
            return
    else:
        x, y = wrap_position(x, y)

    new_head = (x, y)

    if new_head in snake:
        game_over()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 5
        food = (
            random.randrange(0, WIDTH, BOX),
            random.randrange(0, HEIGHT, BOX)
        )
        check_level_complete()
    else:
        snake.pop()

    draw()
    root.after(LEVEL_SPEED[level], move_snake)


def check_level_complete():
    global level, waiting_for_click, badge_text

    if level in LEVEL_SCORE_LIMIT and score == LEVEL_SCORE_LIMIT[level]:
        badge_text = f"TCM completed level {level}"
        waiting_for_click = True
        draw()
    elif level == 4 and score == 20:
        badge_text = "🏆 TCM WON THE GAME 🏆"
        waiting_for_click = True
        draw()


def continue_game(event):
    global level, waiting_for_click

    if waiting_for_click:
        waiting_for_click = False
        if level < 4:
            level += 1
        draw()
        move_snake()


def game_over():
    global game_running
    canvas.create_text(
        WIDTH//2, HEIGHT//2,
        text="GAME OVER",
        fill="red",
        font=("Arial", 24)
    )
    game_running = False


def init_game():
    global snake, direction, food, score, level
    global game_running, waiting_for_click

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "Right"
    food = (
        random.randrange(0, WIDTH, BOX),
        random.randrange(0, HEIGHT, BOX)
    )
    score = 0
    level = 1
    game_running = True
    waiting_for_click = False
    draw()
    move_snake()


def restart_game():
    init_game()


# ---------- BINDINGS ----------
restart_btn.config(command=restart_game)

root.bind("<Left>", lambda e: change_direction("Left"))
root.bind("<Right>", lambda e: change_direction("Right"))
root.bind("<Up>", lambda e: change_direction("Up"))
root.bind("<Down>", lambda e: change_direction("Down"))
canvas.bind("<Button-1>", continue_game)

# ---------- START ----------
init_game()
root.mainloop()
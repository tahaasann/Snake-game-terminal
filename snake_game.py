import curses
import random

# Constants for direction keys
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

# Symbols for the snake and food
SNAKE_BODY = 'O'
FOOD = '#'

def draw_borders(win):
    screen_height, screen_width = win.getmaxyx()
    for y in range(1, screen_height - 1):
        win.addch(y, 0, '|')
        win.addch(y, screen_width - 2, '|')
    for x in range(1, screen_width - 1):
        win.addch(0, x, '-')
        win.addch(screen_height - 2, x, '-')

def display_info(win, score, level, remaining_food):
    win.addstr(0, 2, f'Score: {score} | Level: {level} | Remaining Food: {remaining_food}')
    win.refresh()

# Initialize terminal screen
screen = curses.initscr()
curses.curs_set(0)
screen_height, screen_width = screen.getmaxyx()
win = curses.newwin(screen_height, screen_width, 0, 0)
win.keypad(1)
win.timeout(100)

# Draw borders
draw_borders(win)

# Initial snake position and length
snake_x = screen_width // 4
snake_y = screen_height // 2
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Create 100 food items initially
food_count = 100
foods = []
while len(foods) < food_count:
    nf = [
        random.randint(1, screen_height - 3),
        random.randint(1, screen_width - 3)
    ]
    if nf not in snake and nf not in foods:
        foods.append(nf)
        win.addch(nf[0], nf[1], FOOD)

# Initial direction
key = curses.KEY_RIGHT
direction = RIGHT

# Score and level info
score = 0
level = 1

# Display info on screen
display_info(win, score, level, len(foods))

# Start the game
while True:
    next_key = win.getch()
    if next_key == -1:
        key = key
    else:
        key = next_key

    # Update direction
    if key == curses.KEY_UP and direction != DOWN:
        direction = UP
    elif key == curses.KEY_DOWN and direction != UP:
        direction = DOWN
    elif key == curses.KEY_LEFT and direction != RIGHT:
        direction = LEFT
    elif key == curses.KEY_RIGHT and direction != LEFT:
        direction = RIGHT

    # Calculate new head position
    new_head = [snake[0][0], snake[0][1]]
    if direction == UP:
        new_head[0] -= 1
    elif direction == DOWN:
        new_head[0] += 1
    elif direction == LEFT:
        new_head[1] -= 1
    elif direction == RIGHT:
        new_head[1] += 1

    # Allow snake to pass through walls
    if new_head[0] == 0:
        new_head[0] = screen_height - 3
    elif new_head[0] == screen_height - 2:
        new_head[0] = 1
    if new_head[1] == 0:
        new_head[1] = screen_width - 3
    elif new_head[1] == screen_width - 2:
        new_head[1] = 1

    # Self-collision check
    if new_head in snake:
        curses.endwin()
        quit()

    # Add new head to the snake
    snake.insert(0, new_head)

    # Food consumption check
    if new_head in foods:
        foods.remove(new_head)
        score += 10

        # Update score and level check
        if len(foods) == 0:
            level += 1
            win.timeout(150 - (level - 1) * 10)
            win.addstr(0, screen_width // 2 - 10, f'Congratulations! You reached Level {level}')
            win.refresh()
            curses.napms(2000)  # Wait for 2 seconds
            draw_borders(win)
            # Create new 100 food items
            while len(foods) < food_count:
                nf = [
                    random.randint(1, screen_height - 3),
                    random.randint(1, screen_width - 3)
                ]
                if nf not in snake and nf not in foods:
                    foods.append(nf)
                    win.addch(nf[0], nf[1], FOOD)

    else:
        tail = snake.pop()
        win.addch(tail[0], tail[1], ' ')

    # Update info on screen
    display_info(win, score, level, len(foods))

    # Draw snake
    win.addch(snake[0][0], snake[0][1], SNAKE_BODY)

# End the game
curses.endwin()

import turtle
import random
import time
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vaiga1234",
    database="snake_game"
)
cursor = db.cursor()

# Function to save high score to the database
def save_high_score(score):
    query = "UPDATE high_score SET SCORE=%s"%(score,)
    cursor.execute(query)
    db.commit()

# Function to get the current high score from the database
def get_high_score():
    cursor.execute("SELECT MAX(score) FROM high_score")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0


# Create turtle screen
screen = turtle.Screen()
screen.title('SNAKE GAME')
screen.setup(width=700, height=700)
screen.tracer(0)
turtle.bgcolor('black')

# Create border for the game
turtle.speed(5)
turtle.pensize(4)
turtle.penup()
turtle.goto(-310, 250)
turtle.pendown()
turtle.color('turquoise')
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.right(90)
turtle.forward(600)
turtle.right(90)
turtle.forward(500)
turtle.penup()
turtle.hideturtle()

# Game variables
score = 0
delay = 0.1
high_score = get_high_score()

# Snake
snake = turtle.Turtle()
snake.speed(0)
snake.shape('square')
snake.color("turquoise")
snake.penup()
snake.goto(0, 0)
snake.direction = 'stop'

# Food
fruit = turtle.Turtle()
fruit.speed(0)
fruit.shape('circle')
fruit.color('red')
fruit.penup()
fruit.goto(30, 30)

old_fruit = []

# Scoring
scoring = turtle.Turtle()
scoring.speed(0)
scoring.color("white")
scoring.penup()
scoring.hideturtle()
scoring.goto(0, 300)
scoring.write("Score :", align="center", font=("Courier", 24, "bold"))

# Define how to move the snake
def snake_go_up():
    if snake.direction != "down":
        snake.direction = "up"

def snake_go_down():
    if snake.direction != "up":
        snake.direction = "down"

def snake_go_left():
    if snake.direction != "right":
        snake.direction = "left"

def snake_go_right():
    if snake.direction != "left":
        snake.direction = "right"

def snake_move():
    if snake.direction == "up":
        y = snake.ycor()
        snake.sety(y + 20)

    if snake.direction == "down":
        y = snake.ycor()
        snake.sety(y - 20)

    if snake.direction == "left":
        x = snake.xcor()
        snake.setx(x - 20)

    if snake.direction == "right":
        x = snake.xcor()
        snake.setx(x + 20)

# Keyboard bindings
screen.listen()
screen.onkeypress(snake_go_up, "Up")
screen.onkeypress(snake_go_down, "Down")
screen.onkeypress(snake_go_left, "Left")
screen.onkeypress(snake_go_right, "Right")

# Game over function
def game_over():
    global score, high_score

    # Save high score if current score is higher
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    screen.clear()
    screen.bgcolor('black')
    scoring.goto(0, 0)
    scoring.write("    GAME OVER \n Your Score is {}\n High Score is {}".format(score, high_score), align="center", font=("Courier", 30, "bold"))

# Main game loop
game=True
while game:
    screen.update()

    # Snake and fruit collisions
    if snake.distance(fruit) < 20:
        x = random.randint(-290, 270)
        y = random.randint(-240, 240)
        fruit.goto(x, y)
        scoring.clear()
        score += 1
        scoring.write("Score:{}".format(score), align="center", font=("Courier", 24, "bold"))
        delay -= 0.001

        # Create new segment for the snake
        new_fruit = turtle.Turtle()
        new_fruit.speed(0)
        new_fruit.shape('square')
        new_fruit.color('turquoise')
        new_fruit.penup()
        old_fruit.append(new_fruit)

    # Add segments to snake
    for index in range(len(old_fruit) - 1, 0, -1):
        a = old_fruit[index - 1].xcor()
        b = old_fruit[index - 1].ycor()
        old_fruit[index].goto(a, b)

    if len(old_fruit) > 0:
        a = snake.xcor()
        b = snake.ycor()
        old_fruit[0].goto(a, b)

    snake_move()

    # Snake and border collision
    if snake.xcor() > 280 or snake.xcor() < -300 or snake.ycor() > 240 or snake.ycor() < -240:
        time.sleep(1)
        game_over()
        game=False
        break

    # Snake collision
    for food in old_fruit:
        if food.distance(snake) < 20:
            time.sleep(1)
            game_over()
            game=False
            break

    time.sleep(delay)

db.close()
turtle.Terminator()


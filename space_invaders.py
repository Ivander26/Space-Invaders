import time
from turtle import Turtle, Screen
from typing import List
import tkinter as tk

class Bullet(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.goto(x, y)
        self.shapesize(stretch_len=0.2, stretch_wid=0.2)
        self.y_move = 15
        self.state = "ready"

    def fire(self):
        if self.state == "ready":
            self.state = "fire"
            self.showturtle()

    def move(self):
        if self.state == "fire":
            y_new = self.ycor() + self.y_move
            self.sety(y_new)

        if self.ycor() > 380:
            self.destroy()

    def destroy(self):
        self.hideturtle()
        self.state = "ready"
        self.goto(0, -400)  
        bullets.remove(self)


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.left(90)
        self.color("white")
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.goto(0, -300)
        self.shoot_delay = 0.4
        self.last_shot_time = time.time()

    def go_right(self):
        new_x = self.xcor() + 20
        if new_x < 230:
            self.goto(new_x, self.ycor())

    def go_left(self):
        new_x = self.xcor() - 20
        if new_x > -230:
            self.goto(new_x, self.ycor())

    def shoot_bullet(self):
        current_time = time.time()
        if current_time - self.last_shot_time > self.shoot_delay:
            bullet = Bullet(self.xcor(), self.ycor() + 10)
            bullet.fire()
            bullets.append(bullet)
            self.last_shot_time = current_time


class Enemy(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.goto(x, y)
        self.direction = 1

    def move(self):
        new_x = self.xcor() + 5 * self.direction
        self.goto(new_x, self.ycor())
        if abs(new_x) > 230:
            self.shift_down()

    def shift_down(self):
        self.direction *= -1
        self.goto(self.xcor(), self.ycor() - 20)

    def destroy(self):
        self.hideturtle()
        enemies_list.remove(self)
        del self


def check_collision(obj1, obj2):
    return obj1.distance(obj2) < 20


def game_over():
    player.hideturtle()
    for enemy in enemies_list:
        enemy.hideturtle()
    pen.clear()
    pen.goto(0, 0)
    pen.color("white")
    pen.write("GAME OVER", align="center", font=("Courier", 24, "normal"))


def level_up():
    global level
    level += 1
    pen.clear()
    pen.goto(0, 360)
    pen.write(f"Level: {level}", align="center", font=("Courier", 24, "normal"))


def update_score():
    global score
    score += 10
    pen.clear()
    pen.goto(0, 320)
    pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))


def shooting():
    player.shoot_bullet()


def setup_screen(width=600, height=400) -> None:
    """Set up the screen, adjusting to fit the laptop screen."""
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    aspect_ratio = width / height
    if screen_width / screen_height > aspect_ratio:
        screen_width = int(screen_height * aspect_ratio)
    else:
        screen_height = int(screen_width / aspect_ratio)

    screen.setup(width=screen_width, height=screen_height)
    screen.bgcolor("black")
    screen.title("Space Invaders")
    screen.tracer(0)

screen = Screen()
setup_screen()

player = Player()
bullets = []
score = 0
level = 1

pen = Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()

enemies_list = []
for y in range(270, 150, -50):
    for x in range(-220, 240, 40):
        enemy = Enemy(x, y)
        enemies_list.append(enemy)

screen.listen()
screen.onkey(player.go_right, "d")
screen.onkey(player.go_left, "a")
screen.onkey(shooting, "space")

game_is_on = True
while game_is_on:
    time.sleep(0.05)
    screen.update()

    for enemy in enemies_list:
        enemy.move()

        if check_collision(player, enemy):
            game_over()
            game_is_on = False
            break

        for bullet in bullets[:]:
            if check_collision(bullet, enemy):
                bullet.destroy()
                enemy.destroy()
                update_score()

    if not enemies_list:
        level_up()
        for y in range(270, 150, -50):
            for x in range(-220, 240, 40):
                enemy = Enemy(x, y)
                enemies_list.append(enemy)

    for bullet in bullets:
        bullet.move()

screen.mainloop()

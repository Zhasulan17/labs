import pygame
from pygame.math import Vector2
import datetime
import random
import psycopg2 
import pygame_menu

pygame.init()

# Establish database connection
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Nurdaulet05"
)
cur = conn.cursor()

# Create the tables if they don't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    current_level INTEGER DEFAULT 1
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS user_scores (
    score_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    score INTEGER,
    game_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()


# Creating the Snake class
class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.eated = False
        self.isDead = False

    def drawingSnake(self):
        for block in self.body:
            body_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 128, 0), body_rect)
        snake_head = pygame.Rect(self.body[0].x * cell_size, self.body[0].y * cell_size, cell_size, cell_size)
        headTexture = pygame.image.load('snakehead.png')
        headTexture = pygame.transform.scale(headTexture, (40, 40))
        screen.blit(headTexture, snake_head)

    def snakeMoving(self):
        if self.eated:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + direction)
            self.body = body_copy[:]
            self.eated = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + direction)
            self.body = body_copy[:]


# Creating the Fruit class
class Fruit:
    def __init__(self):
        self.randomize()
    
    def drawingFruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        self.food = pygame.image.load(f'food{self.randomFood}.png').convert_alpha()
        self.food = pygame.transform.scale(self.food, (35, 35))
        screen.blit(self.food, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 2)
        self.y = random.randint(0, cell_number - 2)
        self.pos = Vector2(self.x, self.y)
        self.randomFood = random.randint(1, 3)


# Creating the Game class for overall game control
class Game:
    def __init__(self, initial_level=1):
        self.snake = Snake()
        self.fruit = Fruit()
        self.level = initial_level  # user’s level from database (or default)
        self.score = 0

    def update(self):
        self.snake.snakeMoving()
        self.checkCollision()

    def drawElements(self):
        self.snake.drawingSnake()
        self.fruit.drawingFruit()
        self.scoreDrawing()

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.eated = True
            if self.fruit.randomFood == 1:
                self.score += 1
            elif self.fruit.randomFood == 2:
                self.score += 2
            elif self.fruit.randomFood == 3:
                self.score += 3
            self.fruit.randomize()
            self.levelAdding()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
        for block in wall_coordinates:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def gameOver(self):
        if self.snake.body[0].x >= (cell_number - 1) or self.snake.body[0].x <= 0:
            return True
        if self.snake.body[0].y >= (cell_number - 1) or self.snake.body[0].y <= 0:
            return True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                return True
        for block in wall_coordinates:
            if block == self.snake.body[0]:
                return True
        return False

    def levelAdding(self):
        global snake_speed
        # Increase level every 3 points if appropriate
        if (self.score // 3) > (self.level - 1):
            self.level += 1
            snake_speed = max(50, snake_speed - 10)  # prevent snake_speed from becoming too low
            pygame.time.set_timer(SCREEN_UPDATE, snake_speed)

    def scoreDrawing(self):
        score_text = "Score: " + str(self.score)
        score_surface = font.render(score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect(center=(cell_size * cell_number - 150, 40))
        screen.blit(score_surface, score_rect)

        level_text = "Level: " + str(self.level)
        level_surface = font.render(level_text, True, (56, 74, 12))
        level_rect = level_surface.get_rect(center=(cell_size * cell_number - 150, 70))
        screen.blit(level_surface, level_rect)

    def spawingWalls(self):
        # Example wall spawning based on level; add or modify as needed
        if self.level >= 3:
            wall_coordinates.extend([Vector2(9, 8), Vector2(9, 9), Vector2(9, 10), Vector2(9, 11)])
            for wall in wall1:
                wall_rect = pygame.Rect(wall.x * cell_size, wall.y * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
        if self.level >= 4:
            for i in range(20):
                wall_rect = pygame.Rect(0, i * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(0, i))
        if self.level >= 5:
            for i in range(20):
                wall_rect = pygame.Rect((cell_number - 1) * cell_size, i * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(cell_number - 1, i))
        # More wall configurations for higher levels...

    def pauseState(self):
        global isPause
        if not isPause:
            screen.blit(pause, (0, 0, 800, 800))
            pygame.time.set_timer(SCREEN_UPDATE, 0)
            isPause = True
        else:
            pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
            isPause = False


# Global variables and initializations
clock = pygame.time.Clock()
cell_size = 40
cell_number = 20
direction = Vector2(1, 0)
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
done = False

font = pygame.font.Font('font.ttf', 25)
nowSeconds = int(datetime.datetime.now().strftime("%S"))
snake_speed = 150

# Predefined wall coordinates and textures
wall1 = [Vector2(9, 8), Vector2(9, 9), Vector2(9, 10), Vector2(9, 11)]
wall_texture = pygame.image.load('cobble4040.png')
wall_coordinates = []
pause = pygame.image.load('pause.png')
isPause = False

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, snake_speed)

# Global variable to store the database user id after login
db_user_id = None
def reset_user_progress(name_box):
    global user_name
    user_name = name_box.get_value().strip()
    cur.execute("UPDATE users SET current_level = 1 WHERE username = %s", (user_name,))
    conn.commit()
    print(f"User '{user_name}' level has been reset to 1.")
# Checks for the user in the users table.
def name_checker(NAMEBOX):
    global db_user_id, current_level, user_name
    user_name = NAMEBOX.get_value().strip()
    
    # Search for the user in the database
    cur.execute("SELECT user_id, current_level FROM users WHERE username = %s;", (user_name,))
    row = cur.fetchone()
    
    if row:
        db_user_id = row[0]
        current_level = row[1]
        print(f"User '{user_name}' already exists with current level: {current_level}. Continuing game from this level.")
        start_the_game(current_level)
    else:
        # Insert new user record
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id;", (user_name,))
        db_user_id = cur.fetchone()[0]
        conn.commit()
        current_level = 1
        print(f"Welcome, new user '{user_name}'! Starting at level {current_level}.")
        start_the_game(current_level)


def save_state(game):
    # Save the game state and update user's level
    # Insert into user_scores, then update the current level in users
    cur.execute("INSERT INTO user_scores (user_id, score) VALUES (%s, %s);", (db_user_id, game.score))
    cur.execute("UPDATE users SET current_level = %s WHERE user_id = %s;", (game.level, db_user_id))
    conn.commit()
    print(f"Game state saved for {user_name}: Score {game.score} at Level {game.level}.")


def start_the_game(initial_level):
    global done, direction, nowSeconds
    game = Game(initial_level)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == SCREEN_UPDATE and not isPause:
                game.update()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.pauseState()
                elif event.key == pygame.K_RIGHT:
                    if direction.x != -1:
                        direction = Vector2(1, 0)
                elif event.key == pygame.K_LEFT:
                    if direction.x != 1:
                        direction = Vector2(-1, 0)
                elif event.key == pygame.K_UP:
                    if direction.y != 1:
                        direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN:
                    if direction.y != -1:
                        direction = Vector2(0, 1)
                # Press "I" as a shortcut to save state and exit
                elif event.key == pygame.K_i:
                    save_state(game)
                    done = True

        if game.gameOver():
            save_state(game)
            done = True

        # Reposition fruit if needed every 3 seconds
        now = int(datetime.datetime.now().strftime("%S"))
        if abs(now - nowSeconds) > 3:
            game.fruit.randomize()
            nowSeconds = now
        
        screen.fill((175, 215, 70))
        wall_coordinates.clear()  # Clear previous frame wall coordinates before redrawing based on level
        game.spawingWalls()
        game.drawElements()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Set up the main menu for username input
menu = pygame_menu.Menu('Welcome', 800, 800, theme=pygame_menu.themes.THEME_BLUE)
name_box = menu.add.text_input('Name :', default='username')
menu.add.button('Play', name_checker, name_box)
menu.add.button('Reset Progress', lambda: reset_user_progress(name_box))
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)

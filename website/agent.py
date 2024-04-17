import torch
import random
import numpy as np
import sys
from collections import deque
from flask_login import current_user
from .game import SnakeGameAI, Direction, Point, BLOCK_SIZE
from .model import Linear_QNet, QTrainer
from .dbmodels import AI
from . import db
import time
from .events import socketio
from flask_socketio import emit
from flask_login import current_user
from flask import request

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3) # model is initialized here
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon: # defining logic for exploration
            move = random.randint(0, 2)
            final_move[move] = 1
        else:                                       # defining logic for exploitation
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train(eat_apple, stay_alive, die):

    start_time = time.time()

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    score = 0
    agent = Agent()
    game = SnakeGameAI(eat_apple, stay_alive, die)
    while agent.n_games <= 100:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move, agent.n_games, total_score, record, score)
        state_new = agent.get_state(game)
        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            total_score += score

    mean_score = total_score / agent.n_games
    return agent.n_games, record, mean_score

def log_to_db(high_score, avg_score, eat, alive, die, user_id):
    ai = AI(high_score=int(high_score), avg_score=int(avg_score), eat=int(eat), alive=int(alive), die=int(die), user_id=user_id)
    db.session.add(ai)
    db.session.commit()

# def send_high_scores():
#     data = {}
#     data["ais"] = []
#     for ai in current_user.ais:
#         data["ais"].append({"highscore": ai.high_score, "eat": ai.eat, "alive": ai.alive, "die": ai.die})
#     socketio.emit("highscore_data", {"data": data}, to=request.sid)
#     print(data)

def start(eat, alive, die):

    num_games, high_score, avg_score = train(int(eat), int(alive), int(die))
    log_to_db(high_score, avg_score, eat, alive, die, current_user.id)

if __name__ == '__main__':
    start()

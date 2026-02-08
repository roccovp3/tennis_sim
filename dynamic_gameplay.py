import random
import numpy as np
from point import Point

def play_point_rand(match, p):
    point = None
    if random.random() < p:
        point = Point(match.player_one)
    else:
        point = Point(match.player_two)
    
    return point

def play_point(match):
    player_serving, player_not_serving = match.get_server_and_receiver()

    # Serve
    if random.random() < 1 - player_serving.serve_skill:
        return Point(player_not_serving)

    ball_position = np.random.choice(
        len(player_serving.serve_placement),
        p=player_serving.serve_placement
    )

    # Return attempt
    if ball_position <= 4:
        return_hit_prob = player_not_serving.return_skill * player_not_serving.backhand_skill
        shot_hit = "backhand"
    else:
        return_hit_prob = player_not_serving.return_skill * player_not_serving.forehand_skill
        shot_hit = "forehand"

    if random.random() < 1 - return_hit_prob:
        return Point(player_serving)

    # Ball sent back by receiver
    if shot_hit == "backhand":
        ball_position = np.random.choice(
            len(player_not_serving.backhand_placement),
            p=player_not_serving.backhand_placement
        )
    else:
        ball_position = np.random.choice(
            len(player_not_serving.forehand_placement),
            p=player_not_serving.forehand_placement
        )

    # Rally
    player_serving_is_hitting = True
    while True:
        hitter = player_serving if player_serving_is_hitting else player_not_serving
        receiver = player_not_serving if player_serving_is_hitting else player_serving

        if ball_position <= 4:
            miss = random.random() < 1 - hitter.backhand_skill
            ball_position = np.random.choice(len(hitter.backhand_placement), p=hitter.backhand_placement)
        else:
            miss = random.random() < 1 - hitter.forehand_skill
            ball_position = np.random.choice(len(hitter.forehand_placement), p=hitter.forehand_placement)

        if miss:
            return Point(receiver)

        player_serving_is_hitting = not player_serving_is_hitting
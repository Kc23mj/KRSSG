#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

class GameModerator:
    def __init__(self):
        self.player_a_hitpoints = {'Fire': 300, 'Water': 400, 'Earth': 500}
        self.player_b_hitpoints = {'Rock': 300, 'Thunder': 400, 'Wind': 500}

        self.stat_pub = rospy.Publisher('game_status', String, queue_size=10)

        rospy.init_node('game_moderator', anonymous=True)
        rospy.Subscriber('player_a_moves', String, self.process_player_a_moves)
        rospy.Subscriber('player_b_moves', String, self.process_player_b_moves)

        self.start_game()

    def process_player_a_moves(self, data):
        moves = data.data.split(',')
        i = 0
        for move in moves:
            action, target = move.split()
            if action == '1': 
                print(f"{self.list_monsters_a[i]} attacked {target}")
                self.player_b_hitpoints[target] -= int(0.2 * self.player_a_hitpoints[action])
            elif action == '2':  
                print(f"{self.list_monsters_a[i]} attacked all")
                for monster in self.player_b_hitpoints:
                    self.player_b_hitpoints[monster] -= int(0.1 * self.player_a_hitpoints[action])
            i = i + 1

    def process_player_b_moves(self, data):
        moves = data.data.split(',')
        for move in moves:
            action, target = move.split()
            if action == '1': 
                self.player_a_hitpoints[target] -= int(0.2 * self.player_b_hitpoints[action])
            elif action == '2':  
                for monster in self.player_a_hitpoints:
                    self.player_a_hitpoints[monster] -= int(0.1 * self.player_b_hitpoints[action])

        self.check_winner()

    def check_winner(self):
        if all(hitpoints <= 0 for hitpoints in self.player_a_hitpoints.values()):
            print("Player B wins!")
            rospy.signal_shutdown("Game Over")
        elif all(hitpoints <= 0 for hitpoints in self.player_b_hitpoints.values()):
            print("Player A wins!")
            rospy.signal_shutdown("Game Over")

    def start_game(self):
        while not rospy.is_shutdown():
            
            self.data = f"{round}${','.join(self.player_a_hitpoints.keys())}${','.join(self.player_b_hitpoints.keys())}"
            self.stat_pub.publish(self.data)
            rospy.spin()

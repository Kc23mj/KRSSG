#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

class PlayerA:
    def __init__(self):
        self.player_a_hitpoints = {}
        self.player_b_hitpoints = {}

        rospy.init_node('game_status_playerA', anonymous=True)
        rospy.Subscriber('game_status', String, self.data_from_server)
        self.moves_A_pub = rospy.Publisher('player_a_moves', String, queue_size=10)

    def data_from_server(self, data):
        members = data.data.split('$')#data : "2$300,200,300$220,200,100"
        self.round = members[0]
        self.hitpoints_a = members[1].data.split(',')#'300, 200, 330' string
        self.hitpoints_b = members[2].data.split(',')

        self.monsters_a = ['Fire', 'Water', 'Earth']
        self.monsters_b = ['Rock', 'Thunder', 'Wind']

        #forms dic where keys are elements from monster list and values are from hitpoints list
        self.player_a_hitpoints = {monster: int(hitpoint) for monster, hitpoint in zip(self.monsters_a, self.hitpoints_a)}
        self.player_b_hitpoints = {monster: int(hitpoint) for monster, hitpoint in zip(self.monsters_b, self.hitpoints_b)}
        
        self.print_game_status()

    def print_game_status(self):
        print("Current Status:")
        for monster, hitpoint in self.player_a_hitpoints.items():
            print(f"{monster}: {hitpoint}")
        print("\n")    
        for monster, hitpoint in self.player_b_hitpoints.items():
            print(f"{monster}: {hitpoint}")

    def take_moves_input(self):
        print(f"Round {self.round}")
        moves = []
        for monster in ['Fire', 'Water', 'Earth']:
            move = input(f"{monster}'s turn: ")
            # if move == '1':
            #     target = input(f"{monster}")
            #     moves.append(f"{move} {target}")
            # elif move == '2':
            moves.append(move)
        self.publish_moves(','.join(moves))

    def publish_moves(self, moves):
        self.moves_A_pub.publish(moves)

    def start_game(self):
        while not rospy.is_shutdown():
            self.take_moves_input()

if __name__ == '__main__':
    player_a = PlayerA()
    player_a.start_game()
    rospy.spin()

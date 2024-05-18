#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

round = 1
player_a_hitpoints = {'Fire': 300, 'Water': 400, 'Earth': 500}
player_b_hitpoints = {'Rock': 300, 'Thunder': 400, 'Wind': 500}

class GameModerator:
    def __init__(self):
        global player_a_hitpoints
        global player_b_hitpoints
        self.list_monsters_a = list(player_a_hitpoints.keys)
        self.list_monsters_b = list(player_b_hitpoints.keys)

        # self.current_player = 'A'  # Start with Player A

        self.stat_pub = rospy.Publisher('game_status', String,  queue_size=10)

        #here, anonymous = True
        # will generate diff unique node names perhaps game_moderator1234 game_moderator2345 etc 
        rospy.init_node('game_moderator', anonymous=True)
        self.start_game()

        #to publish game status to both players after each round contains:
        # roundno$player_a_hp$player_b_hitpoints
        rospy.Subscriber('player_a_moves', String, self.process_player_a_moves)
        rospy.Subscriber('player_b_moves', String, self.process_player_b_moves)
        self.check_winner()

    def process_player_a_moves(self, data):#string "1 rock,2 ,1 thunder"
        moves = data.data.split(',') #list ['1 rock','2 ','1 thunder']
        i = 0
        for move in moves:
            action, target = move.split()
            if action == '1':  # Attack One
                print(f"{self.list_monsters_a[i]} attacked {target}")
                player_b_hitpoints[target] -= int(0.2 * player_a_hitpoints[action])
            elif action == '2':  # Attack All
                print(f"{self.list_monsters_a[i]} attacked all")
                for monster in self.player_b_hitpoints:
                    player_b_hitpoints[monster] -= int(0.1 * player_a_hitpoints[action])
            i = i + 1
        # self.print_attacks('A', moves)
        

    def process_player_b_moves(self, data):
        moves = data.data.split(',')
        for move in moves:
            action, target = move.split()
            if action == '1':  # Attack One
                player_a_hitpoints[target] -= int(0.2 * player_b_hitpoints[action])
            elif action == '2':  # Attack All
                for monster in self.player_a_hitpoints:
                    player_a_hitpoints[monster] -= int(0.1 * player_b_hitpoints[action])

        # self.print_attacks('B', moves)
        

    # def print_attacks(self, player, moves):
    #     print(f"Player {player}'s attacks:") #Round likhna padega
    #     for move in moves:
    #         action, target = move.split()
    #         print(f"Attack: {action}, Target: {target}")

    def check_winner(self):
        if all(hitpoints <= 0 for hitpoints in player_a_hitpoints.values()):
            print("Player B wins!")
            rospy.signal_shutdown("Game Over")
        elif all(hitpoints <= 0 for hitpoints in player_b_hitpoints.values()):
            print("Player A wins!")
            rospy.signal_shutdown("Game Over")

    def start_game(self):
            # publish round player a and b hp to both the player but how to publish it after 
            # each and every round 
            self.data = f"{round}${','.join(player_a_hitpoints)}${','.join(player_b_hitpoints)}"               
            self.stat_pub.publish(self.data)
            # if self.current_player == 'A':

            #     rospy.loginfo("Fire's turn")
            #     rospy.loginfo("Water's turn")
            #     rospy.loginfo("Earth's turn")
            # else:
            #     rospy.loginfo("Rock's turn")
            #     rospy.loginfo("Thunder's turn")
            #     rospy.loginfo("Wind's turn")
            rospy.sleep(1)


    # def call_constructor(cls):
    #     return cls()

if __name__ == '__main__':

    while not rospy.is_shutdown():
        # GameModerator.call_constructor()
        moderator = GameModerator()

    #  #constructor __init__ got executed when this object is initiated
    # moderator.start_game()
    # rospy.spin()

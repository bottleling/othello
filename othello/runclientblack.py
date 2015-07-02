import client, randomplayer
import supermanplayer
#replace randomplayer.RandomPlayer with your player
#make sure to specify the color of the player to be 'B'
blackPlayer = randomplayer.RandomPlayer('B')
#blackPlayer = supermanplayer.SupermanPlayer('B')
blackClient = client.Client(blackPlayer)
blackClient.run()

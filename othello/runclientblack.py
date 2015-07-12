import client, randomplayer, bitplayer2
import supermanplayer
#replace randomplayer.RandomPlayer with your player
#make sure to specify the color of the player to be 'B'
#blackPlayer = randomplayer.RandomPlayer('B')
#blackPlayer = supermanplayer.SupermanPlayer('B')
blackPlayer = bitplayer2.BitPlayer2('B')
blackClient = client.Client(blackPlayer)
blackClient.run()

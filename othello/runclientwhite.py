import client, randomplayer, supermanplayer

#replace randomPlayer.RandomPlayer with your player
#make sure to specify the color of the player to be 'W'
#whitePlayer = randomplayer.RandomPlayer('W')
whitePlayer = supermanplayer.SupermanPlayer('W')
whiteClient = client.Client(whitePlayer)
whiteClient.run()

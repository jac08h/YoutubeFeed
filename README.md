# Description
Find new videos on your favourite Youtube channels since last time you checked.
You have to obtain your own Youtube API key to use this program.

# How to Use
1. Clone/download repository
2. In "channels.txt" write YT channels you want to "subscribe" to.
3. In "youtube_feed.py" write your Youtube API key on 7th line(apiKey="YOUR_KEY")
3. Run youtube_feed.py

## Example output
    Last checked: 13:07  31.12.2016
    
    **************************************** 
    Computerphile
    ****************************************
       Dijkstra's Algorithm - Computerphile
       17:22  04.01.2017 ; 10 minutes, 43 seconds
       https://www.youtube.com/watch?v=GazC3A4OQTE
       Dijkstra's Algorithm finds the shortest path between two points. Dr Mike Pound explains how it works.
   
    ****************************************   
    Daniel Shiffman
    ****************************************
       No videos found in this time period :(

        
        
        Press enter to exit. 

### Misc


The channel names are not always exactly what you see. You can get channel name by navigating to channel's page.

E.G.: Say you want to add channel "Smarter Every Day" to your feed. Go to channel's page on youtube and copy the part in URL after "/user/". In this example URL would be "https://www.youtube.com/user/destinws2" so you add "destinws2" to your "channels.txt" file.


Is also available to add channels which have ID in URL. In "channels.txt" add:

[CHANNEL_NAME][SPACE][###][SPACE][CHANNEL_ID] where [CHANNEL_ID] is the number you see on channel's page.

E.G. : When you go to channel Daniel Shiffman, you can see directly it's id in URL. So you add to "channels.txt":
    
    Daniel Shiffman ### UCvjgXvBlbQiydffZU7m1_aw
    

To use this program, you have to obtain Youtube API key. If you are not sure how to do that, follow this link: https://www.slickremix.com/docs/get-api-key-for-youtube/

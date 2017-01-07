# Description
Find new videos on your favourite Youtube channels since last time you checked.
You have to obtain your own Youtube API key to get videos and you will need to get your own client secret file to add those videos to your Watch Later playlist

# How to Use
##Using the Source
1. Clone/download repository  
2. Setup the utility as shown below  
3. Run gui_main.py  

##Using the windows compiled executable
1. Download the release  
2. Setup the utility as shown below  
3. Run YoutubeFeed.exe  

##Setup the utility
1. Follow the "Create your project and select API services" instructions on the [Obtaining authorization credentials](https://developers.google.com/youtube/registering_an_application)  
2. Copy the API Key string to the "API Key" entry in the settings.json file
3. Download the OAuth 2.0 client IDs to your YoutubeFeed folder and add the client_secret file name to the "Client Secret File" entry in the settings.json file

# Shortcuts and Actions
1. Check Channel Feed [Ctrl + 1] - Recheck the channels specified in the "subscription_manager.xml" file for new videos published since the Last Checked Date  
2. Update Date [Ctrl + 2] - Update the Last Checked Date to the current date  
3. Add to Watch Later [Ctrl + 3] - Add the videos shown in the utility to your Watch Later playlist. Progress is shown in the progress bar next to the button. After it's finished, the Last Checked date is updated to the current date.  

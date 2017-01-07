from my_youtube_api import Channel, Video
from os.path import getmtime
from datetime import datetime, timedelta

FILENAME = "channels.txt"


def process_file(filename, get_date_update_timestamp=True):
    """
    returns tuple(
        datetime object,
        dictionary - channel:id
        )

    """
    channels = {}
    with open(filename, "r") as f:
        lines = f.readlines()

        for line in lines:
            try:  # explicit channel Id
                channel_name, channel_id = line.strip().split(" ### ")
                channels[channel_name] = channel_id
            except ValueError:
                channel_name = line.strip()
                channels[channel_name] = 0

    date = None
    if get_date_update_timestamp:
        last_modification = getmtime(filename)
        date = datetime.fromtimestamp(last_modification)
        with open(filename, "w") as f:
            for line in lines:
                f.write(line)  # rewrite lines to change last modification date

    return date, channels


def getNewVideos(last_x_days=None):
    if last_x_days:
        date, channels = process_file(FILENAME, get_date_update_timestamp=False)
        date = datetime.today() - timedelta(days=last_x_days)
    else:
        date, channels = process_file(FILENAME, get_date_update_timestamp=True)

    print("Getting videos since: {}".format(date.strftime("%H:%M  %d.%m.%Y")))
    for channelName, chId in sorted(channels.items()):  # alphabetical order
        # create Channel objects for every channel, assign an ID unless explicitly specified in file
        if chId == 0:
            chan = Channel(channelName)
            chan.setChannelId()
        else:
            chan = Channel(channelName, channel_id=chId)

        print("\n" + "*" * 40 + " \n{}\n".format(channelName) + "*" * 40)
        videos = chan.getVideosSince(date)
        for videoId in videos:
            vid = Video(videoId)
            data = vid.getData()
            try:
                print("   {}\n   {} ; {}\n   {}\n   {}\n\n".format(data["title"], data["date"], data["duration"],
                                                                   data["url"], data["description"].split("\n")[0]))
            except UnicodeError:  # unicode error - running in Command Line (fixed in Python 3.6)
                print("   {}\n   {}\n   {}\n    \n    -Unable to display more informtaion\n\n".format(data["date"],
                                                                                                      data["duration"],
                                                                                                      data["url"]))
        if len(videos) == 0:
            print("   No videos found in this time period :(\n")

    input("\nPress enter to exit. ")


if __name__ == "__main__":
    getNewVideos()

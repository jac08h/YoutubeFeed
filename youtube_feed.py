from youtube_api import *
from os.path import getmtime

FILENAME = "channels.txt"


def process_file(filename):
    """
    returns tuple(
        datetime object,
        dictionary - channel:id
        )

    """
    channels = {}
    last_modification = getmtime(FILENAME)
    date = datetime.fromtimestamp(last_modification)
    with open(FILENAME, "r") as f:
        # 2016 12 17   19 29
        # tuple to create datetime object
        lines = f.readlines()

        for line in lines:
            try:  # explicit channel Id
                channelName, channelId = line.strip().split(" ### ")
                channels[channelName] = channelId
            except:
                channelName = line.strip()
                channels[channelName] = 0

    with open(FILENAME, "w") as f:
        for line in lines:
            f.write(line)

    return date, channels


def main():
    if apiKey is None:
        raise ValueError("Youtube API key missing.")

    date, channels = process_file(FILENAME)
    print("Last checked: {}".format(date.strftime("%H:%M  %d.%m.%Y")))
    for channelName, chId in sorted(channels.items()):  # alphabetical order
        # create Channel objects for every channel, assign an ID unless explicitly specified in file
        if chId == 0:
            chan = Channel(channelName)
            chan.setChannelId()
        else:
            chan = Channel(channelName, channelId=chId)

        print("\n" + "*" * 40 + " \n{}\n".format(channelName) + "*" * 40)
        videos = chan.getVideosSince(date)
        for videoId in videos:
            vid = Video(videoId)
            data = vid.getData()
            try:
                print(
                "   {}\n   {} ; {}\n   {}\n   {}\n\n".format(data["title"], data["date"], data["duration"], data["url"],
                                                             data["description"].split("\n")[0]))
            except:  # unicode error (not running in IDLE)
                print("   {}\n   {}\n   {}\n    \n    -Unable to display more informtaion\n\n".format(data["date"],
                                                                                                      data["duration"],
                                                                                                      data["url"]))
        if len(videos) == 0:
            print("   No videos found in this time period :(\n")

    i = input("\nPress enter to exit. ")


if __name__ == "__main__":
    main()

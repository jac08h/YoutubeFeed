from youtube_api import Channel, Video, data
from datetime import datetime, timedelta
import os


def get_data():
    """
    returns tuple(
        datetime object,
        dictionary - channel:id
        )

    """
    try:
        mtime = os.path.getmtime(__file__)  # last running time of program

    except OSError:
        mtime = 0

    channels = data["channels"]
    last_modified_date = datetime.fromtimestamp(mtime)

    return last_modified_date, channels


def getNewVideos(last_x_days=None):
    """
    ast_x_days: get videos from last X days
    """
    if last_x_days:
        _, channels_list = get_data()
        date = datetime.today() - timedelta(days=last_x_days)
    else:
        date, channels_list = get_data()

    print("Getting videos since {}".format(date.strftime("%H:%M  %d.%m.%Y")))
    for channel_dict in channels_list:

        # create Channel objects for every channel, assign an ID unless explicitly specified in file
        name, alias, chId = channel_dict["name"], channel_dict["alias"], channel_dict["id"]
        chan = Channel(name, alias, chId)
        if len(chId) == 0:
            chan.setChannelId()

        print("\n" + "*" * 40 + " \n{}\n".format(name) + "*" * 40)
        videos = chan.getVideosSince(date)
        for videoId in videos:
            vid = Video(videoId)
            video_data = vid.getData()
            try:
                print("   {}\n   {} ; {}\n   {}\n   {}\n\n".format(video_data["title"], video_data["date"],
                                                                   video_data["duration"],
                                                                   video_data["url"],
                                                                   video_data["description"].split("\n")[0]))
            except UnicodeError:  # unicode error - running in Command Line (fixed in Python 3.6)
                print(
                    "   {}\n   {}\n   {}\n    \n    -Unable to display more informtaion\n\n".format(video_data["date"],
                                                                                                    video_data[
                                                                                                        "duration"],
                                                                                                    video_data["url"]))
        if len(videos) == 0:
            print("   No videos found in this time period :(\n")

    input("\nPress enter to exit. ")


if __name__ == "__main__":
    getNewVideos()

import sys
from datetime import datetime, timedelta

import settings_api
from youtube_api import Channel, Video


def get_data(update_date=True):
    """
    returns tuple(
        datetime object,
        dictionary - channel:id
        )

    """
    data = settings_api.get_all()
    if len(data["last_date"]) == 0:  # first time
        last_date = datetime.now()
    else:
        last_date = datetime.strptime(data["last_date"], "%Y-%m-%d %H:%M:%S.%f")

    channels = data["channels"]

    if update_date:
        settings_api.update_date(data, datetime.now())

    return last_date, channels


def getNewVideos(last_x_days=None):
    """
    last_x_days: get videos from last X days (int)
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

        print("\n" + "*" * 40 + " \n{}\n".format(chan.getAliasOrName()) + "*" * 40)
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
    try:
        getNewVideos(int(sys.argv[1]))
    except IndexError:
        getNewVideos()
    except ValueError:
        raise ValueError("Invalid number.")

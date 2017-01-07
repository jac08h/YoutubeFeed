from settings_api import Settings
import youtube_api as ya

import datetime as dt

from xml.etree import ElementTree
from urllib.parse import urlparse


def process_file(subscription_feed):
    """
    returns tuple(
        datetime object,
        dictionary - channel:id
        )

    """
    channels = {}
    with open(subscription_feed, mode='r', encoding="utf8") as readfile:
        root = ElementTree.parse(readfile).getroot()
        for child in root[0][0]:
            channels[child.attrib['title']] = urlparse(child.attrib['xmlUrl']).query[11:]

    return channels


def main():
    if not ya.apiKey or ya.apiKey.isspace():
        raise ValueError("Youtube API key missing.")

    settings = Settings()
    date = dt.datetime.strptime(settings.get_last_checked(), '%Y-%m-%d')
    print("Last checked: {}".format(date.strftime("%H:%M  %d.%m.%Y")))

    channels = process_file("subscription_manager.xml")
    for channelName, chId in sorted(channels.items()):  # alphabetical order
        # create Channel objects for every channel, assign an ID unless explicitly specified in file
        if chId == 0:
            chan = ya.Channel(channelName)
            chan.set_channel_id()
        else:
            chan = ya.Channel(channelName, channel_id=chId)

        print("\n" + "*" * 40 + " \n{}\n".format(channelName) + "*" * 40)
        videos = chan.get_videos_since(date)
        for videoId in videos:
            vid = ya.Video(videoId)
            data = vid.get_data()
            try:
                print("   {}\n   {} ; {}\n   {}\n   {}\n\n".format(data["title"], data["date"], data["duration"],
                                                                   data["url"], data["description"].split("\n")[0]))
            except:  # unicode error (not running in IDLE)
                print("   {}\n   {}\n   {}\n    \n    -Unable to display more informtaion\n\n".format(data["date"],
                                                                                                      data["duration"],
                                                                                                      data["url"]))
        if len(videos) == 0:
            print("   No videos found in this time period :(\n")
    settings.update_last_run(str(dt.date.today()))
    i = input("\nPress enter to exit. ")

if __name__ == "__main__":
    main()

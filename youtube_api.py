from settings_api import Settings

import urllib.request
import json
import re
from datetime import datetime, timedelta

settings = Settings()
apiKey = settings.get_api_key()
# https://www.slickremix.com/docs/get-api-key-for-youtube/

youtubeApiUrl = "https://www.googleapis.com/youtube/v3"
youtubeChannelsApiUrl = youtubeApiUrl + "/channels?key={0}&".format(apiKey)
youtubeSearchApiUrl = youtubeApiUrl + "/search?key={0}&".format(apiKey)
youtubeVideoApi = youtubeApiUrl + "/videos?key={0}&".format(apiKey)

requestParametersChannelId = youtubeChannelsApiUrl + 'forUsername={0}&part=id'
requestChannelVideosInfo = youtubeSearchApiUrl + 'channelId={0}&' \
                                                 'part=id&' \
                                                 'order=date&' \
                                                 'type=video&' \
                                                 'publishedBefore={1}&' \
                                                 'publishedAfter={2}&' \
                                                 'pageToken={3}&' \
                                                 'maxResults=50'
requestVideoInfo = youtubeVideoApi + "part=snippet&id={0}"
requestVideoTime = youtubeVideoApi + "part=contentDetails&id={0}"


class Channel:
    def __init__(self, channel_name, channel_alias=None, channel_id=None):

        self.channelName = channel_name
        self.channelAlias = channel_alias
        self.channelId = channel_id

    def __str__(self):
        return "Channel name:  {}\nChannel Alias:  {}\nChannelId:  {}".format(self.channelName,
                                                                              self.channelAlias,
                                                                              self.channelId)

    def __repr__(self):
        return "Channel name:  {}\nChannel Alias:  {}\nChannelId:  {}".format(self.channelName,
                                                                              self.channelAlias,
                                                                              self.channelId)

    def set_channel_id(self):
        try:
            url = requestParametersChannelId.format(self.channelName)
            resp = urllib.request.urlopen(url).read().decode("utf8")

            json_resp = json.loads(resp)
            self.channelId = json_resp["items"][0]["id"]
        except KeyError:
            print("ERROR setting ID for channel: {}".format(self.channelName))
            self.channelId = "error"

    def _get_videos_between(self, from_date, to_date):
        """
        dates= datetime.datetime objects

        :param from_date: Earliest date
        :param to_date: Latest date
        :return:
        """
        # format dates
        from_date = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        to_date = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        next_page_token = ""
        found_all = False

        ret_val = []

        while not found_all:
            try:
                url = requestChannelVideosInfo.format(self.channelId, to_date, from_date, next_page_token)
                resp = urllib.request.urlopen(url).read().decode("utf8")

                json_resp = json.loads(resp)
                returned_videos = json_resp["items"]

                for video in returned_videos:
                    ret_val.append(video["id"]["videoId"])

                try:
                    next_page_token = json_resp["nextPageToken"]

                except KeyError:  # no nextPageToken
                    found_all = True

            except IndexError:  # error; no videos found. don't print anything
                found_all = True

        return ret_val

    def get_previous_days_video(self, previous_days):
        current_date = datetime.now()
        previous_date = datetime.now() - timedelta(days=previous_days)

        return self._get_videos_between(previous_date, current_date)

    def get_videos_since(self, since_date):
        """
        sinceDate = datetime.datetime object
        """

        current_date = datetime.now()
        return self._get_videos_between(since_date, current_date)

    def get_all_videos(self):
        first_youtube_video = datetime(year=2005, month=4, day=22)  # first youtube video -1
        current_date = datetime.now()

        return self._get_videos_between(first_youtube_video, current_date)


class Video:
    def __init__(self, video_id):
        self.videoId = video_id

    def get_data(self, parse_duration=True, parse_date=True):
        try:
            results = {}
            url = requestVideoInfo.format(self.videoId)
            resp = urllib.request.urlopen(url).read().decode("utf8")

            json_resp = json.loads(resp)
            snippet = json_resp["items"][0]["snippet"]
            results["title"] = snippet["title"]
            results["date"] = snippet["publishedAt"]
            results["description"] = snippet["description"]
            results["url"] = "https://www.youtube.com/watch?v={}".format(self.videoId)

            # need to create different request for duration
            url = requestVideoTime.format(self.videoId)
            resp = urllib.request.urlopen(url).read().decode("utf8")
            json_resp = json.loads(resp)
            duration = json_resp["items"][0]["contentDetails"]["duration"]

            if parse_duration:
                # parses iso 8601 duration manually
                digits = re.findall(r"\d+", duration)
                times = ["seconds", "minutes", "hours"]
                res = []

                for digit, time in zip(digits[::-1], times):
                    res.append("{} {},".format(digit, time))

                res.reverse()  # start with biggest unit
                parsed_duration = " ".join(res)[:-1]  # omit last colon
                results["duration"] = parsed_duration
            else:
                results["duration"] = duration

            if parse_date:
                # 2016-12-17T14:54:05.000Z --> 14:54  12.12.2016
                digits = re.findall(r"\d+", results["date"])
                parsed_date = "{hours}:{minutes}  {day}.{month}.{year}".format(
                    hours=digits[3], minutes=digits[4], day=digits[2], month=digits[1], year=digits[0]
                )

                results["date"] = parsed_date

            # we don't need else here since un-parsed date is already in results dict
            return results

        except IndexError:
            print("ERROR: Finding video data for video {}".format(self.videoId))
            return None

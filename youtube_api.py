import urllib.request
from urllib.error import HTTPError
import json
import re
from datetime import datetime

FILENAME = "my_settings.json"

with open(FILENAME) as data_file:
    data = json.load(data_file)
apiKey = data["api_key"]

youtubeApiUrl = "https://www.googleapis.com/youtube/v3"
youtubeChannelsApiUrl = youtubeApiUrl + "/channels?key={0}&".format(apiKey)
youtubeSearchApiUrl = youtubeApiUrl + "/search?key={0}&".format(apiKey)
youtubeVideoApi = youtubeApiUrl + "/videos?key={0}&".format(apiKey)

requestParametersChannelId = youtubeChannelsApiUrl + 'forUsername={0}&part=id'
requestChannelVideosInfo = youtubeSearchApiUrl + 'channelId={0}&part=id&order=date&type=video&publishedBefore={1}&publishedAfter={2}&pageToken={3}&maxResults=50'
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

    def setChannelId(self):
        try:
            url = requestParametersChannelId.format(self.channelName)
            resp = urllib.request.urlopen(url).read().decode("utf8")

            jsonResp = json.loads(resp)
            self.channelId = jsonResp["items"][0]["id"]
        except KeyError:
            print("ERROR setting ID for channel: {}".format(self.channelName))
            self.channelId = "error"

    def _getVideosBetween(self, since_date, to_date):
        """
        dates= datetime.datetime objects
        """
        # format dates
        since_date = since_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        to_date = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        nextPToken = ""
        foundAll = False

        retVal = []

        while not foundAll:
            try:
                req = requestChannelVideosInfo.format(self.channelId, to_date, since_date, nextPToken)
                with urllib.request.urlopen(req) as response:
                    html = response.read()

                jsonResp = json.loads(html)
                returnedVideos = jsonResp["items"]

                for video in returnedVideos:
                    retVal.append(video["id"]["videoId"])

                try:
                    nextPToken = jsonResp["nextPageToken"]

                except KeyError:  # no nextPageToken
                    foundAll = True

            except HTTPError:
                print("Bad request.")

            except IndexError:  # error; no videos found. dont print anything
                foundAll = True

        return retVal

    def getVideosSince(self, since_date):
        """
        sinceDate = datetime.datetime object
        """

        todayDate = datetime.now()
        return self._getVideosBetween(since_date, todayDate)

    def getAllVideos(self):
        firstDate = datetime(year=2005, month=4, day=22)  # first youtube video -1
        todayDate = datetime.now()

        return self._getVideosBetween(firstDate, todayDate)


class Video:
    def __init__(self, video_id):
        self.videoId = video_id

    def getData(self, parse_duration=True, parse_date=True):
        try:
            results = {}
            url = requestVideoInfo.format(self.videoId)
            resp = urllib.request.urlopen(url).read().decode("utf8")

            jsonResp = json.loads(resp)
            snippet = jsonResp["items"][0]["snippet"]
            results["title"] = snippet["title"]
            results["date"] = snippet["publishedAt"]
            results["description"] = snippet["description"]
            results["url"] = "https://www.youtube.com/watch?v={}".format(self.videoId)

            # need to create different request for duration
            url = requestVideoTime.format(self.videoId)
            resp = urllib.request.urlopen(url).read().decode("utf8")
            jsonResp = json.loads(resp)
            duration = jsonResp["items"][0]["contentDetails"]["duration"]

            if parse_duration:
                # parses iso 8601 duration manually
                digits = re.findall(r"\d+", duration)
                times = ["seconds", "minutes", "hours"]
                res = []

                for digit, time in zip(digits[::-1], times):
                    res.append("{} {},".format(digit, time))

                res.reverse()  # start with biggest unit
                parsedDuration = " ".join(res)[:-1]  # omit last colon
                results["duration"] = parsedDuration
            else:
                results["duration"] = duration

            if parse_date:
                # 2016-12-17T14:54:05.000Z --> 14:54  12.12.2016
                digits = re.findall(r"\d+", results["date"])
                parsedDate = "{hours}:{minutes}  {day}.{month}.{year}".format(
                    hours=digits[3], minutes=digits[4], day=digits[2], month=digits[1], year=digits[0]
                )

                results["date"] = parsedDate

            # no need for else as unparsed date is already in results dict
            return results

        except IndexError:
            print("ERROR: Finding video data for video {}".format(self.videoId))
            return None

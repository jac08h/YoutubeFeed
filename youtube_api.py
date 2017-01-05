import urllib.request
import json
import re
from datetime import datetime, timedelta

apiKey = None # Write your Youtube API key here
# https://www.slickremix.com/docs/get-api-key-for-youtube/


youtubeApiUrl = "https://www.googleapis.com/youtube/v3"
youtubeChannelsApiUrl = youtubeApiUrl + "/channels?key={0}&".format(apiKey)
youtubeSearchApiUrl = youtubeApiUrl + "/search?key={0}&".format(apiKey)
youtubeVideoApi = youtubeApiUrl + "/videos?key={0}&".format(apiKey)

requestParametersChannelId = youtubeChannelsApiUrl + 'forUsername={0}&part=id'
requestChannelVideosInfo = youtubeSearchApiUrl + 'channelId={0}&part=id&order=date&type=video&publishedBefore={1}&publishedAfter={2}&pageToken={3}&maxResults=50'
requestVideoInfo = youtubeVideoApi + "part=snippet&id={0}"
requestVideoTime = youtubeVideoApi + "part=contentDetails&id={0}"


class Channel:
    def __init__(self, channelName, channelAlias=None, channelId=None):

        self.channelName = channelName
        self.channelAlias = channelAlias
        self.channelId = channelId

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

    def _getVideosBetween(self, sinceDate, toDate):
        """
        dates= datetime.datetime objects
        """
        # format dates
        sinceDate = sinceDate.strftime("%Y-%m-%dT%H:%M:%SZ")
        toDate = toDate.strftime("%Y-%m-%dT%H:%M:%SZ")

        nextPToken = ""
        foundAll = False

        retVal = []

        while not foundAll:
            try:
                url = requestChannelVideosInfo.format(self.channelId, toDate, sinceDate, nextPToken)
                resp = urllib.request.urlopen(url).read().decode("utf8")

                jsonResp = json.loads(resp)
                returnedVideos = jsonResp["items"]

                for video in returnedVideos:
                    retVal.append(video["id"]["videoId"])

                try:
                    nextPToken = jsonResp["nextPageToken"]

                except KeyError:  # no nextPageToken
                    foundAll = True

            except IndexError:  # error; no videos found. dont print anything
                foundAll = True

        return retVal

    def getLastXDaysVideos(self, last_x_days):
        todayDate = datetime.now()
        previousDate = datetime.now() - timedelta(days=last_x_days)

        return self._getVideosBetween(previousDate, todayDate)

    def getVideosSince(self, sinceDate):
        """
        sinceDate = datetime.datetime object
        """

        todayDate = datetime.now()
        return self._getVideosBetween(sinceDate, todayDate)

    def getAllVideos(self):
        firstDate = datetime(year=2005, month=4, day=22)  # first youtube video -1
        todayDate = datetime.now()

        return self._getVideosBetween(firstDate, todayDate)


class Video:
    def __init__(self, videoId):
        self.videoId = videoId

    def getData(self, parseDuration=True, parseDate=True):
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

            if parseDuration:
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

            if parseDate:
                # 2016-12-17T14:54:05.000Z --> 14:54  12.12.2016
                digits = re.findall(r"\d+", results["date"])
                parsedDate = "{hours}:{minutes}  {day}.{month}.{year}".format(
                    hours=digits[3], minutes=digits[4], day=digits[2], month=digits[1], year=digits[0]
                )

                results["date"] = parsedDate

            # we don't need else here since unparsed date is already in results dict
            return results


        except IndexError:
            print("ERROR: Finding video data for video {}".format(self.videoId))
            return None

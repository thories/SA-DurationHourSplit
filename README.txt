# Splunk Addon - SA-DurationHourSplit
Splunk app which provides command to split duration into assigned hours. Example:

* Starttime: 12:30:00
* Duration: 120 minutes

Add multivalue field to search with the following values:
* 12:00:00_1800
* 13:00:00_3600
* 14:00:00_1800

Using the mvexpand in combination with the rex command enables you to visualize the  duration over time using the timechart command instead of having the duration only assigned to the hour of the event starting time.

Parameters:
field_starttime (mandatory) = name of field which contains start time. Start time value(s) needs to be an epoch timestamp (integer)
field_duration (mandatory) = name of field which containt duration. Duration value(s) needs to be in seconds (integer)
result (optional) = name of result column (default=Timestamp_Duration)

Example:

```| stats count | eval test=1479999508 | eval duration=1200 | durationbyhour field_starttime=test field_duration=duration | mvexpand Timestamp_Duration | rex field=Timestamp_Duration "(?<_time>[^_]+)_(?<seconds>.+$)" | eval _time=strptime(_time,"%Y-%m-%d %H:%M:%S") | timechart span=1h sum(seconds)```

---

![alt tag](https://raw.githubusercontent.com/thories/SA-DurationHourSplit/master/static/2016-11-25_23-03-40.png)

Support: https://github.com/thories/SA-DurationHourSplit/issues/new

Credits:

* Splunk SDK: https://github.com/splunk/splunk-sdk-python
* Icon: adventure_airport_city_clock_time_town_world_icon by Olya Philipenko - https://www.iconfinder.com/hk12215


# Splunk Addon - SA-DurationHourSplit
Splunk app which provides command to split duration into assigend hours. Example:

* Starttime: 12:30:00
* Duration: 120 minutes

Add multivalue field to search with the following values:
* 12:00:00_30
* 13:00:00_60
* 14:00:00_30

Using the mvexpand in combination with the rex command enables you to visualize the  duration over time using the timechart command instead of having the duration only assigend to the hour of the event starting time. Example:

```| stats count | eval test=1479999508 | eval duration=1200 | durationbyhour field_starttime=test field_duration=duration | mvexpand Duration_Hour  | rex field=Duration_Hour "(?<_time>[^_]+)_(?<seconds>.+$)" | eval _time=strptime(_time,"%Y-%m-%d %H:%M:%S") | timechart span=1h sum(seconds)```

---

![alt tag](https://raw.githubusercontent.com/thories/SA-DurationHourSplit/master/2016-11-25_23-03-40.png)

Integrated / Used libs:

Splunk SDK: https://github.com/splunk/splunk-sdk-python

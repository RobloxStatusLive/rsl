# <img style="float: right;" src="https://doy2mn9upadnk.cloudfront.net/uploads/default/original/4X/d/8/a/d8a9a1964099afb7c1778761eef6f915c68c3f19.png"> Official Roblox Status Live v2
### The smarter alternative to the [Roblox Status Page](https://status.roblox.com).
#### Created with 🧡 by [iiPython](https://iipython.cf) and [Crcoli737](https://devforum.roblox.com/u/crcoli737)
###### Logo created by [GamersInternational](https://devforum.roblox.com/u/gamersinternational)
***
## Overview
### How it works.
Roblox Status Live uses the [Roblox API](https://devforum.roblox.com/t/collected-list-of-apis/557091) endpoints [status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) and [ping times](https://www.techtarget.com/searchnetworking/definition/ping) to determine if Roblox is working correctly. We also use other determining factors, such as [Roblox's Official Status page](https://status.roblox.com) to determine if there is an active incident at Roblox.
### Why is it important?
If you are not an active Roblox player or developer, the use of Roblox Status Live may not be very important to you. However if you are a developer, knowing the status of Roblox and it's APIs can help you determine player count, projected revenue, and the lost revenue due to the inability for players to purchase [gamepasses](https://education.roblox.com/en-us/resources/game-passes) or [developer products](https://developer.roblox.com/en-us/articles/Developer-Products-In-Game-Purchases).
### Why is Roblox Status Live better other automated down detectors?
Well, the answer to this question is more complicated than one may think. For example, [Status+](https://status-plus.github.io/StatusPlus/) is a great down detector for Roblox, but it has its downfalls. Status+'s website may seem better than our's however that's just because it uses a template, specifically the [Upptime template](https://github.com/upptime/upptime). 

You may be thinking, just because a website uses a template doesn't make it bad, and you would be correct. However, using a template to make your website often comes with [downsides](https://www.techwalla.com/articles/what-is-the-disadvantage-of-using-a-template), such as the website being impersonal to Roblox specifically. 

Another downside to Status+ is that they have hard limits on their downtime detector, just because an API had a threshold violation doesn't always mean that the API is down, this often causes many false positives. 

At Roblox Status Live, we are evolving very quickly and plan on using an [Artificial Intelligence and Machine Learning engine](https://azure.microsoft.com/en-us/overview/artificial-intelligence-ai-vs-machine-learning/#introduction) to help determine if Roblox is having an outage, what the outage consists of, and an estimated ETA for a resolution. 

## Roblox Status Live API
### Summary
The Roblox Status Live API is an easy way for other developers to integrate the Roblox Status Live data into their own third-party applications.

### Status API Contents

Link: https://robloxstatus.live/api/status

Now let's take a look at what kind of information the Status API contains. 

#### Services Container

```json
"services": [ # The services container contains a list of all the Roblox APIs.
    {
      "code": 200, # The code element shows the HTTP response code of the specified API.
      "guess": [ # The guess table shows the predicted status of the specified API.
        "up", 
        "No problems detected"
      ], 
      "id": "twostepverification", # The id element is simply for identification purposes.
      "name": "2FA", # The name element is also for identification purposes.
      "ping": 65.07, # The ping element shows the round-trip ping time (in milliseconds) for the specified API.
      "url": "https://twostepverification.roblox.com/" # The URL element shows the URL to the specified API.
    }, 
```

#### Status Container
```json
"status": [ # The status container simply shows the overall status of Roblox based on the status of the APIs.
    "online", # Status of Roblox
    "green" # A color representing the status of Roblox.
  ]
```

### Historical API Contents

Link: https://robloxstatus.live/api/historical

#### Documentation Coming Soon!

#### More API Documentation coming soon!

## Important Information

### Roblox Status Live Links:
- [Roblox Website](https://roblox.com/)
- [Roblox Status Live Website](https://robloxstatus.live/)
- [Roblox Status Live Source Code](https://github.com/ii-Python/rsl)
- [Roblox Status Live Devforum Thread](https://devforum.roblox.com/t/roblox-status-live-the-better-automatic-roblox-down-detector/1567879)
- [Roblox Status Live Status API](https://robloxstatus.live/api/status)
- [Roblox Status Live Historical API](https://robloxstatus.live/api/historical)

## Change Log

#### Roblox Status Live v2 Coming **Very** Soon!

### v1.2 Minor Update
- Added Historical Roblox Downtime.
- Added a new Historical API.
- Added more API details once clicked upon.

### v1.1 Minor Update
- Added more Roblox APIs to the API List.
- Rewrote the Roblox Status Live API.
- Rewrote the backend of Roblox Status Live in preperation for Roblox Status Live v2.
- We have a new logo in preperation for RSL v2.

### v1.0 Initial Release
- Initial Release of Roblox Status Live.

### Copyright Notices: 
#### Copyright 2022 [iiPython](https://iipython.cf)
#### Copyright 2020-2022 [Crcoli737](https://devforum.roblox.com/u/crcoli737)
#### Roblox Status Live Logo is Intellectual Property of [GamersInternational](https://devforum.roblox.com/u/gamersinternational)

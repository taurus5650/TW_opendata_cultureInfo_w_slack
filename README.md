# tw_culture_opendata_w_slack

### Intro
- May through to slack bot knowing Taiwan concert / event's information.
- Open dataset from Ministry of Culture (https://opendata.culture.tw/frontsite/openData/detail?datasetId=274)
![final_result.png](result_readme%2Ffinal_result.png)

### Setup
1. Create virtual env and active venv
```commandline
python - m venv venv
source venv / bin / activate
```

2. Install library
```commandline
pip install - r requirement
```

3. Setup ur slack bot
- a. Create slack bot (Ref. [Create Slack Bot Using Python Tutorial With Examples](https: // www.pragnakalp.com / create - slack - bot - using - python - tutorial - with -examples /))
- b. Copy manifest.yml an paste to app menifest setting
![slack_manifest.png](result_readme % 2Fslack_manifest.png)
- c. Create an slack channel and add ur slack bot

4. In venv, export the token
- a. Copy the SLACK_BOT_TOKEN and SLACK_APP_TOKEN from slack api
![SLACK_BOT_TOKEN.png](result_readme % 2FSLACK_BOT_TOKEN.png)
![SLACK_APP_TOKEN.png](result_readme % 2FSLACK_APP_TOKEN.png)
- b. Command in venv
```commandline
export SLACK_BOT_TOKEN = xoxb - xxxxx
export SLACK_APP_TOKEN = xapp - xxxxx
```

5. Started the code
```commandline
python3 app.py
```

6. User able input "concert" / "event" / "exhibition" to get information
- [Screen Recording 2023 - 08 - 13 at 9.02.52 PM.mov](result_readme % 2FScreen % 20Recording % 202023 - 08 - 13 % 20at % 209.02.52 % 20PM.mov)

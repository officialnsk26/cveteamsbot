# cveteamsbot
CVE Teams Bot
_____________   _______________            _______   ___________________.______________
\_   ___ \   \ /   /\_   _____/            \      \  \_____  \__    ___/|   \_   _____/
/    \  \/\   Y   /  |    __)_    ______   /   |   \  /   |   \|    |   |   ||    __) 
\     \____\     /   |        \  /_____/  /    |    \/    |    \    |   |   ||     \ 
 \______  / \___/   /_______  /           \____|__  /\_______  /____|   |___|\___  /
        \/                  \/                    \/         \/                  \/1.0

Customized bot specifically for MS Teams CVE Bot Notifications, leveraged from the BotPEASS framework.

Use this bot to monitor new CVEs from defined vendors and send notification alert to MS Teams.

Example with Microsoft Teams

![image](https://github.com/officialnsk26/cveteamsbot/assets/84531371/f05c7110-de6a-463e-9db0-501db6ca0da1)

Configure one for yourself
Configuring your own BotPEASS that notifies you about the new CVEs containing specific keywords is very easy!

Fork this repo
Modify the file config/cve-notif.yaml and set your own vendors
MSTEAMS_WEBHOOK_URL:(Optional) Set the Microsoft Teams webhook to send messages to your Microsoft Teams channel
Check .github/wordflows/cve-notif.yaml and configure the cron (once every 8 hours by default)

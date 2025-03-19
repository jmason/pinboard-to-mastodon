# pinboard-to-mastodon

Gateway pinboard.in posts to Mastodon -- as used on https://mstdn.social/@jmason_links .

## How To Use

Create a new Mastodon bot account (be sure to use a bot-friendly Mastodon instance).
Tick the "automated" box so people will know it's a bot.

Go to Settings -> Development (https://mstdn.social/settings/applications on my instance).
Hit the "New Application" button.  Select the "read" and "write" scopes and hit save,
then copy the access token from "Your access token" at the top of the page.

Copy "envs.sample" to "envs" and fill in the necessary values.

Fill in the appropriate RSS feed address for your Pinboard account; changing the "u:jm"
part to match your username should be all that is needed.

Once this is done, run ". envs; ./gateway.py" as often as necessary; it'll maintain a sqlite
database to track which URLs have been previously posted.


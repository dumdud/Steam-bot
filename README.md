<h1 align= center > Steam chat helper</h1>
<b align= center >A simple chat bot made in python with some helpful features for Steam gaming.</b>

## Table of contents
 - [💻Installing and running the bot.](#install)
 - [🎮Get wiki articles for the games you're playing.](#wiki)
 - [⏰Set up reminders that can be repeated daily or just once](#reminder)

## 💻Installing and running the bot. <a name = "install"></a>

Python 3.11+ and pip are required.

 1. Download or clone the repository.
 2. Install dependencies with the following console command:
 `python pip install -r requirements.txt` 
 3. Start the bot using "run_bot.bat" or "run_bot - console.bat".
 4. Enter the steam credentials of the steam account you wish to use for the bot.
<span style="color:red">NOTE: THE CREDENTIALS ARE STORED IN PLAIN TEXT INSIDE A JSON FILE.</span>

Optionally you can create an "admins.txt" file with the [SteamIDs](http://www.steam64.com/) you want to give admin rights to. Doing so gives you the ability to use the `!name` and `!disconnect` commands.

`!name` allows you to change the bot's name.
`!disconnect` logs off and shuts down the program.


 
## 🎮Get wiki articles for the games you're playing.<a name = "wiki"></a>

With the `!wiki` command you can quickly search Fandom wikis, either the base wiki URL or an specific article

Usage
: Type `!wiki` in chat to get a link for the game you're currently playing on steam

: `!wiki` and a search parameter to get an specific article 

: You can also look for a game if you're not currently playing anything

## ⏰Set up reminders that can be repeated daily or just once. <a name = "reminder"></a>

Set custom messages as reminders using `!alarm` or `!timer`.

**Usage**
: Use` !alarm` followed by your custom message, and a 24hour formatted time stamp to set up a daily reminder.
: **Example**: `!alarm touch grass 18:00`

: `!timer` works the same way for one time use
: Use `!list` to get a list of all your reminders.
: Using `!delete` will wipe all reminders


# Trans Resource Bot 🏳️‍⚧️

A Discord bot that provides trans-related resources, user data handling, and automated meme responses. This bot is designed to help create a supportive and interactive community experience.

## Features 

* 📌 Trans Resources: Shares helpful information for transgender individuals.
* 🔄 Database Support: Stores and retrieves user pronoun data.
* 🖼 Meme Generator: Responds with memes based on user input.
* 🔗 API Integration: Connects to pronoun.page (and respective language versions) APIs for additional functionality.

## Technologies Used
* Python 3.11+
* Discord API (`discord.py`)
* SQLite3 (DB Browser)
* Asynchronous I/O HTTP Library (`aiohttp`)
* Logging Library (for debugging purposes)

## To Install
### 1. Clone the repository
 ```
 git clone https://github.com/kate-the-gr8-tra/trans_resource_bot.git
 cd trans_resource_bot
 ```
### 2. Install dependencies
 ```
 pip install -r requirements.txt
 ```
### 3. Setting Up Your Own Bot Token & Guild ID
Before running the bot, you must create a Discord bot token and provide your guild (server) ID.

 **Step 1: Create a Discord Bot Token**
1. Go to the **[Discord Developer Portal](https://discord.com/developers/applications)**.
2. Click "New Application" and give your bot a name.
3. Navigate to the "Bot" tab and click "Add Bot".
4. Click "Reset Token" to generate a new token.
5. Copy the token (WARNING: Do NOT share this token!).
 
 **Step 2: Get Your Server (Guild) ID**
1. In Discord, go to User Settings > Advanced.
2. Ensure Developer Mode is enabled
3. Right-click your Discord server name (in the left panel) and select Copy ID.
4. Save this ID for the next step.
  
  **Step 3: Create an info.txt file**
  
  Inside the project directory, create a new file called info.txt and paste the following information:
  ```
  your-guild-id-here
  your-bot-token-here
  ```

  Example: 
  ```
  123456789012345678
  mfa.WE1rdsTR1ngofL3tt3r5AnDnUmB3rs
  ```
  ⚠ **Important**:
  * Make sure `info.txt` is in the same folder as bot.py.
  * DO NOT share `info.txt` publicly or upload it to GitHub

### 4. Invite your Bot to a Discord Server
  
  Before running the bot, you need to invite it to a server:
  1. Go to the OAuth2 > URL Generator tab in the Developer Portal.
  2. Under Scopes, check ✅ "bot".
  3. Under Bot Permissions, select:
     * ✅ Send Messages
     * ✅ Send Message
     * ✅ Read Messages
     * ✅ Embed Links
     * ✅ Attach Files
     * ✅ Manage Roles

  4. Copy the generated URL and open it in a browser.
  5. Select your test server and click **"Authorize"**.

### 5. Run the Bot

Once everything is set up, start the bot using:

```
python bot.py
```

## Commands & Usage
| Command | Description |
|---------|------------|
| `/edit_info` | Edit your pronouns and info |
| `/explain_neopronouns` | Sends an embed containing a brief summary of what neopronouns are and when they're used|
| `/haircut` | Sends a link that allows users to find trans-friendly hair places :3 |
| `/help_me` | Sends links to sites and resources for LGBTQ+ friendly mental health |
| `/pronouns` | Sends links to sites where you can explore pronouns |
| `/help_me` | Sends links to sites and resources for LGBTQ+ friendly mental health |
| `/read_books` | Sends a resource for trans literature |
| `/register` | Register your pronouns and info |
| `/send_info` | Sends user information and crafts an example sentence using the user's name and pronoun information|

## 📅 To-Do List

* Add a `help` command to list bot's functionalities and how to use them
* Perform stress tests

## Contributing 
Want to help improve this bot? Feel free to submit a pull request or open an issue for feature requests and bug fixes!

## Liscence

This project is open-source under the MIT License.

## Contact me:

**Bluesky:** [@katie-k8-kat.bsky.social](https://bsky.app/profile/katie-k8-kat.bsky.social)

**Website Page:** https://kitty-kat-k8.neocities.org/



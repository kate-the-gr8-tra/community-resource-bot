# Community Resource Bot

This Community Resource Bot is a Discord bot that provides users with access to curated resources and simple self-service commands. It demonstrates the use of:

## Features 

* Slash commands (`/register`, `/edit_info`, `/send_info`, `/resources`, etc.)
* A local SQLite database for user data
* Integration with the pronouns.page API

## Technologies Used
* Python 3.11+
* Discord API (`discord.py`)
* SQLite3 (DB Browser)
* Asynchronous I/O HTTP Library (`aiohttp`)
* Logging Library (for debugging purposes)

## To Install
### 1. Clone the repository
 ```
 git clone https://github.com/kate-the-gr8-tra/community-resource-bot.git
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
| `/delete_info` | Remove your data from the database. |
| `/edit_info` | Update a specific field (e.g., pronouns). |
| `/help` | Displays list of commands. |
| `/ping` | Quick responsiveness test. |
| `/register` | Create or update your profile. |
| `/resources` | View curated resource links. |
| `/send_info` | View your current stored information. |

## To-Do List

* Implement test modules
* Update `/register` to be idempotent

## Contributing 
Want to help improve this bot? Feel free to submit a pull request or open an issue for feature requests and bug fixes!

## Liscence

This project is open-source under the MIT License. This project also uses the Pronouns.page API
under the Opinionated Queer License v1.1 (https://en.pronouns.page/license). The API and its responses are not covered by this project’s MIT license.

## Contact me:

**Linkedin:** https://www.linkedin.com/in/katherine-tuttle-33b4a32b6/ 
 
**Email** tuttlekatie2@gmail.com




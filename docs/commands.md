# Commands

> NanoBot's prefix is 2 exclamation marks. (`!!`)

[Permissions Reference](./permissions.md)

| Command Name | Description                                | Usage                              | Category   | Permissions  |
| ------------ | ------------------------------------------ | ---------------------------------- | ---------- | ------------ |
| help         | Shows the help message.                    | !!help                             | General    | NanoBot User  |
| hello        | Shows an introduction message.             | !!hello                            | General    | NanoBot User  |
| invite       | Shows a link to invite NanoBot.            | !!invite                           | General    | NanoBot User  |
| info         | Shows bot info.                            | !!info                             | General    | NanoBot User  |
| user         | Shows info about the requested user.       | !!user [user]                      | General    | NanoBot User  |
| guild        | Shows guild info.                          | !!guild                            | General    | NanoBot User  |
| guilds       | Shows average guild info.                  | !!guilds                           | General    | NanoBot User  |
| ping         | Shows Discord gateway response time.       | !!ping [times]                     | General    | NanoBot User  |
| dog          | Shows a random dog.                        | !!dog                              | General    | NanoBot User  |
| cat          | Shows a random cat.                        | !!cat                              | General    | NanoBot User  |
| status       | Shows statuspage.io info.                  | !!status <help/[page]>             | General    | NanoBot User  |
| prune\*      | Bulk-deletes up to 100 messages.           | !!prune <amount>                   | Moderation | NanoBot Mod   |
| kick\*       | Kicks a user for a specified reason.       | !!kick <user> [reason]             | Moderation | NanoBot Mod   |
| ban\*        | Bans a user for a specified reason.        | !!ban <user> [reason]              | Moderation | NanoBot Mod   |
| cmd          | Custom commands interface.                 | !!cmd <help/add/edit/del>          | Admin      | NanoBot Admin |
| join         | Joins the specified voice channel.         | !!join [channel]                   | Music      | NanoBot User  |
| summon\*\*   | Joins your voice channel.                  | !!summon                           | Music      | NanoBot User  |
| play         | Searches⁺ for and plays the entered query. | !!play <query/url⁺>                | Music      | NanoBot User  |
| yt           | Searches YouTube for the entered query.    | !!yt <query/url>                   | Music      | NanoBot User  |
| queue        | Shows songs in queue.                      | !!queue                            | Music      | NanoBot User  |
| volume       | Changes player volume.                     | !!volume <amount>                  | Music      | NanoBot User  |
| pause        | Pauses the current song.                   | !!pause                            | Music      | NanoBot User  |
| resume       | Resumes the current song.                  | !!resume                           | Music      | NanoBot User  |
| stop         | Stops the player and leaves the channel.   | !!stop                             | Music      | NanoBot User  |
| skip         | Skips the current song.                    | !!skip                             | Music      | NanoBot User  |
| playing      | Shows the currently playing song.          | !!playing                          | Music      | NanoBot User  |
| overwatch    | Overwatch commands.                        | !!ow <help/profile/hero/map/event> | Overwatch  | NanoBot User  |

See the `!!help` command for more info.

> NOTE: [] means that arguments are not required, but <> means that they are. Also, do not use [] and <> when using the bot.

\* NanoBot requires special permissions to perform this command.

\*\* Obsolete.

⁺ View the list of supported sites here: [https://rg3.github.io/youtube-dl/supportedsites.html](https://rg3.github.io/youtube-dl/supportedsites.html)

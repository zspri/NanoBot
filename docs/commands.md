# Commands

> NanoBot's prefix is 2 exclamation marks. (`!!`)

[Permissions Reference](./permissions.md)

| Command Name | Description                                | Usage               | Category   | Permissions  |
| ------------ | ------------------------------------------ | ------------------- | ---------- | ------------ |
| help         | Shows the help message.                    | !!help              | General    | NanoBot User |
| hello        | Shows an introduction message.             | !!hello             | General    | NanoBot User |
| info         | Shows bot info.                            | !!info              | General    | NanoBot User |
| user         | Shows info about the requested user.       | !!user <user>       | General    | NanoBot User |
| guild        | Shows guild info.                          | !!guild             | General    | NanoBot User |
| ping         | Shows Discord gateway response time.       | !!ping [times]      | General    | NanoBot User |
| dog          | Shows a random dog.                        | !!dog               | General    | NanoBot User |
| cat          | Shows a random cat.                        | !!cat               | General    | NanoBot User |
| status       | Shows statuspage.io info.                  | !!status <page>     | General    | NanoBot User |
| prune\*      | Bulk-deletes up to 100 messages.           | !!prune <amount>    | Moderation | NanoBot Mod  |
| prune2\*     | Individually deletes up to 100 messages.   | !!prune2 <amount>   | Moderation | NanoBot Mod  |
| join         | Joins the specified voice channel.         | !!join <channel>    | Music      | NanoBot User |
| summon\*\*   | Joins your voice channel.                  | !!summon            | Music      | NanoBot User |
| play         | Searches⁺ for and plays the entered query. | !!play <query|url⁺> | Music      | NanoBot User |
| yt           | Searches YouTube for the entered query.    | !!yt <query|url>    | Music      | NanoBot User |
| queue        | Shows songs in queue.                      | !!queue             | Music      | NanoBot User |
| volume       | Changes player volume.                     | !!volume <amount>   | Music      | NanoBot User |
| pause        | Pauses the current song.                   | !!pause             | Music      | NanoBot User |
| resume       | Resumes the current song.                  | !!resume            | Music      | NanoBot User |
| stop         | Stops the player and leaves the channel.   | !!stop              | Music      | NanoBot User |
| skip         | Skips the current song.                    | !!skip              | Music      | NanoBot User |
| playing      | Shows the currently playing song.          | !!playing           | Music      | NanoBot User |

> NOTE: [] means that arguments are not required, but <> means that they are.

\* NanoBot requires special permissions to perform this command.
\*\* Obsolete.
⁺ View the list of supported sites here: https://rg3.github.io/youtube-dl/supportedsites.html

# Ruxy

Ruxy's official Discord bot.

## Features

* Slash commands
* User information commands
* Repository shortcuts for the Rux ecosystem
* Owner management commands
* Fast local command syncing

## Commands

### Utility

| Command | Description       |
| ------- | ----------------- |
| `/ping` | Check bot latency |
| `/poll` | Make a poll (max of 10 options) |

### User

| Command   | Description                            |
| --------- | -------------------------------------- |
| `/whoami` | Display information about yourself     |
| `/whois`  | Display information about another user |

### Repositories

| Command | Description                   |
| ------- | ----------------------------- |
| `/repo` | Get links to Rux repositories |

### Moderation

| Command       | Description                           |
| ------------- | ------------------------------------- |
| `/blacklist`  | Blacklists a user from using the bot  |
| `/unblacklist`| Unblacklists a user                   |
| `/mute`       | mutes a user                          |
| `/unmute`     | unmutes a user                        |

### Owner

| Command     | Description                |
| ----------- | -------------------------- |
| `/shutdown` | Shut down the bot          |
| `/restart`  | Restart the bot            |

### Fun

| Command         | Description                               |
| --------------- | ----------------------------------------- |
| `/self-timeout` | Timeout the member itself specified time  |
| `/joke`         | Sends a random joke                       |
| `/rps`          | Play **rock, paper, scissors** with computer | 


### Examples

| Command           | Description                                             |
| ----------------- | ------------------------------------------------------- |
| `/example`        | Show a random Rux example or a specific example by name |
| `/example-list`   | List all available examples                             |
| `/example-reload` | Reload all examples from disk                           |
| `/example-stats`  | Display example statistics                              |

#### Example Directory

Examples are loaded from:

```text
Examples/
├── hello.rux
├── variable_decl.rux
└── ...
```

Each `.rux` file becomes an example that can be viewed through the bot.

## License

Licensed under the MIT License.

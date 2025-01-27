# PyLink 1.3.0 (2018-05-08)
The 1.3 update focuses on backporting some commonly requested and useful features from the WIP 2.0 branch. This release includes all changes from 1.3-beta1, plus the following:

- Errors due to missing permissions now log to warning. [issue#593](https://github.com/GLolol/PyLink/issues/593)
- Documentation updates to advanced-relay-config.md and the FAQ

# PyLink 1.3-beta1 (2018-04-07)
The 1.3 update focuses on backporting some commonly requested and useful features from the WIP 2.0 branch. This beta release includes all changes from 1.2.1, plus the following:

#### New features
- **Backported the launcher from 2.0-alpha2**:
    - Added support for daemonization via the `--daemon/-d` option. [issue#187](https://github.com/GLolol/PyLink/issues/187)
    - Added support for shutdown/restart/rehash via the command line. [issue#244](https://github.com/GLolol/PyLink/issues/244)
    - The launcher now detects and removes stale PID files when `psutil` (an optional dependency) is installed, making restarting from crashes a more streamlined process. [issue#512](https://github.com/GLolol/PyLink/issues/512)
    - PID file checking is now enabled by default, with the `--check-pid/-c` option retained as a no-op option for compatibility with PyLink <= 1.2
    - Following 2.0 changes, sending SIGUSR1 to the PyLink daemon now triggers a rehash (along with SIGHUP).
- Service bot idents, hosts, and realnames can now be configured globally and on a per-network basis. [issue#281](https://github.com/GLolol/PyLink/issues/281)
- Relay server suffix is now configurable by network (`servers::<netname>::relay_server_suffix` option). [issue#462](https://github.com/GLolol/PyLink/issues/462)
- Login blocks can now be restricted to specific networks, opered users, and hostmasks. [issue#502](https://github.com/GLolol/PyLink/issues/502)
- Relay now supports relaying more channel modes, including inspircd blockhighlight +V and exemptchanops +X (the whitelist was synced with 2.0-alpha3)

#### Bug fixes
- automode: fix errors when managing channels with multiple #'s in its name
- protocols/p10: fix the `use_hashed_cloaks` option not working correctly (it mistakenly read the value of `use_account_cloaks` instead)
- relay_clientbot: fix `@#channel` messages being relayed to channels other than the target
- Fixed sporadic disconnect issues on `BlockingIOError`, `ssl.SSLWantReadError`, and `ssl.SSLWantWriteError`
- protocols/unreal: fix the wrong hook name being sent when receiving legacy (Unreal 3.2) user introductions
- global: ignore empty `global:` configuration blocks

#### Misc changes
- Config loading now uses `yaml.safe_load()` instead of `yaml.load()` so that arbitrary code cannot be executed. [issue#589](https://github.com/GLolol/PyLink/issues/589)
- Significantly revised example-conf for wording and consistency.
- protocols/unreal: bumped protocol version to 4017 (no changes needed)

# PyLink 1.2.1
The "Dancer" release. Changes from 1.2.0:

#### Bug fixes
- unreal: fix TypeError when relaying prefix modes via `mode()`
- Fix wrong database and PID filenames if the config file name includes a period (".")
- automode: don't send empty mode lines if no users match the ACL
- networks: check in "remote" that the remote network is actually connected
- Fix commonly reported crashes on `logging:` config syntax errors ([49136d5](https://github.com/GLolol/PyLink/commit/49136d5abd609fd5e3ba2ec2e42a0443118e62ab))
- Backported fixes from 2.0-dev:
    - p10: fix wrong hook name for user introduction
    - clientbot: warn when an outgoing message is blocked (e.g. due to bans) (#497)
    - ts6: fix setting real host of users to 'None' if it wasn't given

#### Misc changes
- Removed incorrect descriptions regarding P10 `extended_accounts`. Both X3 and atheme support extended accounts, and this needs to match your IRCd settings regardless.
- Updated definitions in `channel/user-modes.csv`.

#### Internal improvements
- Backported improvements from 2.0-dev:
    - Fix support for Hybrid 8.x trunk
    - Minor logging cleanup for relay and `Irc.matchHost()`.
    - Fix cmode `+p` mapping on TS6 networks.

# PyLink 1.2.0
The "Dragons" release. Changes since 1.2.0-rc1:

#### Feature changes
- Make relay nick tagging configurable per-network; backported from 2.0-dev (#494)

#### Bug fixes

- Fix extraneous removal of PID files even when `-n/--no-check-pid` was set or if the PID file already existed on launch (PyLink would quit and delete the old PID file in these cases)
- servprotect: bump default threshold up to 10 hits/10 seconds, as the old limit was too prone to false positives
- Fix extraneous queue threads not being stopped when a network disconnects (0d5afd2)
- Fix relay errors on disconnect due to race conditions in network handling (a0a295f)

#### Misc changes
- Updated example config and FAQ.

For a summary of major changes since 1.1.x, see the changelog for 1.2.0-rc1.

# PyLink 1.2.0-rc1

The "Droplet" release. Changes since 1.2-beta1:

#### Bug fixes
- relay: fix channel claim disabling (i.e. "`CLAIM #channel -`" was broken since 1.2-alpha1)
- IRCS2SProtocol: fix `UnboundLocalError` in "message coming from wrong way" error
- ts6: fix parsing of the `INVITE` command's `ts` argument
- automode: fix formatting and examples in `setacc` help text
- p10: fix rejoin-on-kick relaying by also acknowledging kicks sent from PyLink to its clients with a PART

### Major changes since 1.1.x
- Added support for snircd, ircu, and other (generic) P10 variants. The target IRCd can be chosen using the new server-specific `p10_ircd` option; see the example config for details (#330).
- **The `nefarious` protocol module was renamed to `p10`**, as it is no longer Nefarious-specific. You should update your configuration to use the new name!
- **Certain configuration options were renamed / deprecated:**
    - The `bot:` configuration block was renamed to `pylink:`, with the old name now deprecated.
    - `logging:stdout` is now `logging:console` (the previous name was a misnomer since text actually went to `stderr`).
    - The `bot:prefix` option is deprecated: you should instead define the `prefixes` setting in a separate config block for each service you wish to customize (e.g. set `automode:prefix` and `games:prefix`)
- **Using new-style accounts exclusively (i.e. specifying things under `login:accounts`) now requires a `permissions:` block for PyLink to start** (#413).
- New `stats` (uptime info) and `global` (global announcement) plugins.
- Plugins and protocol modules can now be loaded from any directory, using the new `plugin_dirs` and `protocol_dirs` options. (#350)
    - The `pylink-contribdl` utility was dropped as it is now it obsolete.
- Relay message formatting became more flexible, and messages from servers (e.g. spurious invite announcements) can now be dropped: look for the `relay_weird_senders` and `accept_weird_senders` options.
- Relay now forbids linking to channels where the home network is down, which previously caused errors due to unreliable target TS (#419). This, along with the regular TS check, can be overridden with a new `link --force` option.
- The `remote` command now routes replies back to the caller network, and supports service bots that aren't the main PyLink bot via a `--service` option.
- Service bot spawning can now be disabled via the global `spawn_services` and per-service `spawn_service` options; doing so will merge the relevant commands into the main PyLink bot.
- Added a `pylink::show_unknown_commands` option to optionally disable "unknown command" errors. This option can also be overridden per-server and per-service (#441).
- Added a `pylink::prefer_private_replies` option to default to private command replies (#409).
- Relay can now announce to leaf channels when the home network disconnects; see the `relay::disconnect_announcement` option (#421).

For a full list of changes since 1.1.x, consult the changelogs for the 1.2.x beta and alpha releases below.

# PyLink 1.2-beta1
The "Dynamo" release. This release includes all fixes from 1.1.2, plus the following:

#### Feature changes
- Added configurable encoding support via the `encoding` option in server config blocks ([#467](https://github.com/GLolol/PyLink/pull/467)).
- **Certain configuration options were renamed / deprecated:**
    - The `bot:` configuration block was renamed to `pylink:`, with the old name now deprecated.
    - `logging:stdout` is now `logging:console` (the previous name was a misnomer since text actually went to `stderr`).
    - The `bot:prefix` option is deprecated: you should instead define the `prefixes` setting in a separate config block for each service you wish to customize (e.g. set `automode:prefix` and `games:prefix`)
- Added new `$and` and `$network` exttargets - see the new [exttargets documentation page](https://github.com/GLolol/PyLink/blob/1.2-beta1/docs/exttargets.md) for how to use them.
- Hostmasks can now be negated in ban matching: e.g. `!*!*@localhost` now works. Previously, this negation was limited to exttargets only.
- `relay_clientbot` no longer colours network names by default. It is still possible to restore the old behaviour by defining [custom clientbot styles](https://github.com/GLolol/PyLink/blob/1.2-beta1/docs/advanced-relay-config.md#custom-clientbot-styles).
- `relay_clientbot` no longer uses dark blue as a random colour choice, as it is difficult to read on clients with dark backgrounds.

#### Bug fixes
- Fix service respawn on KILL not working at all - this was likely broken for a while but never noticed...
- Fix kick-on-rejoin not working on P10 IRCds when `joinmodes` is set. (a.k.a. acknowledge incoming KICKs with a PART per [the P10 specification](https://github.com/evilnet/nefarious2/blob/ed12d64/doc/p10.txt#L611-L618))
- servprotect: only track kills and saves to PyLink clients, not all kills on a network!
- Fix `~#channel` prefix messages not working over relay on RFC1459-casemapping networks ([#464](https://github.com/GLolol/PyLink/issues/464)).
- Show errors when trying to use `showchan` on a secret channel in the same way as actually non-existent channels. Previously this error response forced replies as a private notice, potentially leaking the existence of secret/private channels.
- example-conf: fix reversed description for the password encryption setting.

#### Internal changes
- Portions of the IRC/relay stack were refactored to prevent various hangs on shutdown.
- Performance improvements for outgoing message queuing: the queue system now blocks when no messages are in the queue instead of polling it multiple times a minute.
- Logging fixes: startup warnings (e.g. from config deprecations) now log to files as well as the console.

# PyLink 1.2-alpha1
The "Darkness" release. This release includes all fixes from 1.1.2, plus the following summary of changes:

#### Feature changes
- **Added support for snircd, ircu, and other (generic) P10 variants.** The target IRCd can be chosen using the new server-specific `p10_ircd` option; see the example config for details (#330).
- **The `nefarious` protocol module was renamed to `p10` - you should update your configuration to use the new name!**
- Plugins and protocol modules can now be loaded from any directory, making pylink-contrib 20% more useful! Look for the `plugin_dirs` and `protocol_dirs` options in the example config. (#350)
    - The `pylink-contribdl` utility was dropped as this makes it obsolete.
- Relay now forbids linking to channels where the home network is down, which previously caused errors due to unreliable target TS (#419). This, along with the regular TS check, can be overridden with a new `link --force` option.
- SASL timeout for clientbot is now configurable, with the default raised to 15 seconds
- **New-style accounts (i.e. anything under `login:accounts`) now require a `permissions:` block for PyLink to start** (#413).
- New `stats` (uptime info) and `global` (global announcement) plugins
- Improvements to the `remote` command of the `networks` plugin:
    - Plugin replies are now routed back to the sender's network.
    - Added an optional `--service` option to call commands for service bots other than the main PyLink service.
- `servprotect` KILL/SAVE limits and expiry time are now configurable (#417)
- Added the `pylink::show_unknown_commands` option to optionally disable "unknown command" errors. This option can also be overridden per-server and per-service (#441).
- Added the `pylink::prefer_private_replies` option to default to private command replies (#409)
- Relay message formatting became more flexible, and messages from user-less senders can now be dropped (fa30d3c c03f2d7)
- Added global and per-service `spawn_service(s)` options to optionally disable service bot spawning
- The `bots` plugin now allows specifying channel prefixes (e.g. `@+`) in `join`
- exec: Added `iexec`, `ieval`, `peval`, `pieval`: `i`\* commands run code in an isolated, persistent local scope, while `p`\* commands evaluate expressions while pretty-printing the output
- Relay: implement optional network disconnect announcements (see the `relay::disconnect_announcement` option; #421)

#### Bug fixes
- Service bots no longer throw errors when attempting to call empty commands via fantasy.
- Protocol modules now send PONG immediately instead of queuing it, which should prevent ping timeouts at times of very high activity.

#### Internal improvements
- Protocols now verify that incoming messages originate from the right direction (#405)
- `Irc.matchHost` now supports matching CIDR ranges (#411)
- Added an `utils.IRCParser` class based off `argparse`, for flexible argument parsing (#6).
- Rewrote outgoing message queues to use `queue.Queue` (#430), and support a limit to the amount of queued lines (#442)
   - Also, added a `clearqueue` command to force clear the queue on a network.
- PyLink protocol capabilities were introduced, reducing the amount of protocol name hardcoding in plugins (#337)
- Service bots no longer create stubs on Clientbot networks, and instead route replies through the main bot (#403)
- The default throttle time was halved from 0.01s to 0.005s.
- ServiceBot is now more flexible in help formatting, fixing indented lines and consecutive newlines not showing on IRC.
- Configuration validation no longer uses skippable asserts (#414)
- inspircd: better support for OPERTYPE on InspIRCd 3.x
- Clientbot now tracks channel modes and channel TS on join.
- Clientbot now generates PUIDs/PSIDs with the nick or server name as prefix, and checks to make sure incoming senders don't clash with one.
- commands: `showchan` now shows TS on connections without the `has-ts` protocol capability as well, even though this value may be unreliable

#### Misc changes
- The `bot:` config block is renamed to `pylink:`. Existing configurations will still work, as the `bot` and `pylink` blocks are always merged together (#343).
- Added better documentation for generic options available to all service bots (`nick`, `ident`, `prefix` for fantasy, etc.)
- `Irc.botdata`, `Irc.conf`, `Irc.checkAuthenticated()` have been deprecated: use `conf.conf['pylink']`, `conf.conf`, and the permissions API respectively instead!

# PyLink 1.1.2

The "Calamari" release.

#### Bug fixes
- Multiple fixes for the `unreal` protocol module when using UnrealIRCd 3.2 links:
    - fccec3a Fix crashes on processing SJOIN when a user behind a 3.2 server has a nick starting with a symbol
    - 8465edd Fix kicks to Unreal 3.2 users (PUIDs) not updating the internal state - this would've caused odd prefix mode desyncs if a user was kicked and rejoined.
    - df4acbf Fix prefix modes not being set on Unreal 3.2 users (affects Automode, etc.)
- Backported SASL fixes from 1.2-dev:
    - b14ea4f Send CAP LS before NICK/USER so that we consistently get a SASL response before connect - this fixes SASL on networks like freenode, where connections can often complete before a SASL response from services is ever received.
    - 84448e9 22ceb3f The above commit rewrites SASL to depend on a timely response from the server, so a configurable timeout for SASL/CAP is also introduced. (#424)

#### Feature changes
- 22ceb3f Added the `sasl_timeout` option for Clientbot networks (this defaults to 15 seconds if not set).

#### Internal improvements
- Backported stability improvements from 1.2-dev:
    - d70ca9f Rewrite connection error handling to include `RuntimeError` and `SystemExit` (#438)

# PyLink 1.1.1

The "Crush" release. Changes from 1.1.0:

#### Bug fixes
- The `pylink-mkpasswd` program is actually installed now when using `pip` (PyPI) or `setup.py`.
- Backported protocol module fixes from 1.2-dev:
    - unreal: fix crashes when receiving `SJOIN` with only a prefix and no UID
    - inspircd: work around extraneous letters sent in `FJOIN` timestamps (Anope 1.8.x bug)
    - nefarious: fix a typo causing crashes on user mode changes
- Relay: in `claim`, show a less ambiguous error when a relay channel doesn't exist on the caller's network.
- corecommands: removed extraneous `irc.checkAuthenticated()` call

#### Feature changes
- `pylink-mkpasswd` now supports interactive password input via getpass, which is more secure than passing passwords raw on the command line.

#### Misc changes
- More prominent migration notes regarding permissions and new accounts system.

# PyLink 1.1.0

The "Calico" release. This is mostly a cleanup and documentation update from 1.1-beta2, with the following additional change:
- Made passlib an optional dependency (password hashing will be disabled if passlib isn't installed), simplifying the upgrade process.

For a full list of changes since 1.0.x, see the release notes for the 1.1 alpha & beta series. Summary of major changes since 1.0.x:

- :closed_lock_with_key: **Redone authentication configuration**, now supporting **multiple accounts**, hashed passwords, and fine-tuned permissions.
   - Old configurations using `login:user` and `login:password` will still work, but are now deprecated. Consider migrating to the new `login:` block in the example config.
   - This also adds a new optional dependency of passlib (https://passlib.readthedocs.io/en/stable/), which is required for the password hashing portion.
- Protocol modules now wrap long messages (SJOIN and MODE) to prevent cutoff shenanigans from happening.
   - This fixes a particularly nasty bug that can corrupt the TS on UnrealIRCd channels if a MODE command sets more than 12 modes at once (#393).
- Added utilities to download contrib modules (`pylink-contribdl`) and hash passwords for the new accounts configuration (`pylink-mkpasswd`).
- Most plugins were ported to the permissions API.
- Clientbot now supports mode syncing, SASL (with optional reauth), and IRCv3 multi-prefix.
- Services bots now support setting modes on themselves on join: see "joinmodes" in the example conf
- Changehost gained a few new features, including optional (per network) vHost enforcement.
- Added a `bindhost` option in server blocks, for multi-homed hosts.
- PID file checking was implemented - Run PyLink with the `--check-pid` argument in order to turn it on.
- The `ts6` protocol module now supports `KICK` without arguments and legacy `UID` introduction (for older servers / services).
- Relay: added a `purge` command to remove all relays involving a network.
- Added support for ircd-ratbox (`ratbox` protocol module).
- Changing the console log level via REHASH now works.
- New `servermaps` plugin, displaying network `/map`'s from the PyLink server's perspective.

# PyLink 1.1-beta2

The "Conscience" release. Changes from 1.1-beta1:

#### Bug fixes

- Protocol modules now wrap longer messages (SJOIN and MODE) to prevent cutoff shenanigans from happening.
    - This fixes a particularly nasty bug that can corrupt the TS on UnrealIRCd channels if a MODE command sets more than 12 modes at once (#393).
- Pong handling is a lot less strict now (it just makes sure the sender is the uplink). In other words, fix issues on UnrealIRCd where PONGs get ignored if the argument doesn't match the server name exactly (e.g. different case).
- Clientbot protocol fixes:
    - Fix SASL PLAIN auth on Python 3.4 (TypeError with bytes formatting with `%b`).
    - Don't repeat KICK hooks if the source is internal: this prevents KICK events from being relayed twice to Clientbot links, when the kicked user is also a Clientbot user.
    - Clientbot now explicitly sends `/names` after join, to guarantee a response.
    - Fix message recognition treating nick prefixes without `ident@host` as servers (this polluted the state)
    - Fix prefix mode changes for unknown/missing users in `/who` causing KeyError crashes
- ts6: fix setting mode `-k *` not working due to wrongly ordered logic (1.1-dev regression)
- ts6: fix handling of KICK without a reason argument
- Automode: remove some repeated "Error:" text in error messages
- `IrcChannel` no longer assumes `+nt` on new channels, as this is not necessarily correct

#### Feature changes
- Changing the console log level via REHASH is now supported.
- Added a bind host option for multi-homed hosts.

#### Internal improvements
- updateTS now ignores any broken TS values lower than 750000, instead of propagating them (e.g. over relay) and making the problem worse.
- The UnrealIRCd protocol module was updated to actually use extended SJOIN (SJ3). This should make bursts/startup more efficient, as modes, users, and bans are now sent together.

# PyLink 1.1-beta1

The "Crunchy" release. This release includes all bug fixes from PyLink 1.0.4, along with the following:

### Changes from 1.1-alpha1

#### Feature changes
- Most plugins were ported to use the permissions API, meaning multiple accounts are actually useful now!
    - Having a **PyLink login** with *new* style accounts **no longer implies access to everything** on the PyLink daemon. See the updated example conf regarding the new `permissions:` block.
    - **Logins implying admin access** is limited to **old accounts ONLY** (i.e. logins defined via login:user/password)
    - The `commands` plugin now has permissions checks for `echo`, `showuser`, `showchan`, and `status`. The latter three are granted to all users (`*!*@*`) by default, while `echo` is restricted.
- Clientbot now supports IRCv3 SASL (with optional reauth!) and multi-prefix. See the example conf for details on the former (the latter is enabled automatically when available).
- PID file checking is now **disabled** by default for better migration from 1.0.x. Run PyLink with `--check-pid` in order to turn it on.
- commands: add a new `logout` command (#370)
- The `list` command now supports optionally filtering commands by plugin.

#### Bug fixes
- The permission to use servermaps is now `servermaps.map` instead of `servermap.map`.
- networks: fix the `remote` command to work with permissions (i.e. override the correct account name)
- relay: add missing permissions check on the `linked` command

#### Internal fixes / improvements
- relay: rewrite host normalization to whitelist instead of blacklist characters. This should improve compatibility with IRCds as previously untested characters are introduced.
- relay_clientbot: faster colour hashing using built-in `hash()` instead of md5
- opercmds: removed the source argument from `kick` and `kill`; it's confusing and isn't very useful

#### Misc. changes
- Documentation updates: add a permissions reference, document advanced relay config, etc.

# PyLink 1.0.4
Tagged as **1.0.4** by [GLolol](https://github.com/GLolol)

The "Bonfire" release.

#### Bug fixes
- protocols: implement basic nick collision detection in UID handlers. This fixes users potentially going missing on UnrealIRCd networks, if the remote IRCd introduces a user of the same nick *after* PyLink does. Thanks to kevin for reporting!
- relay: strip underscores (`_`) from hosts on ts6 and ratbox, fixing possible invalid user@host errors
- Backported fixes from 1.1.x / devel:
    - Demote "unknown user" warnings in mode handling to DEBUG, suppressing warnings when old services like Anope 1.8 set modes on users as they quit.
    - Fix `irc.matchHost()` confusing the `realhost` boolean to be the same as `ip`.
    - changehost: add missing permissions check to `applyhosts`; it now requires the `changehost.applyhost` permission.

#### Misc changes
- networks: update help for `disconnect` to reflect how it now always disables autoconnect.

# PyLink 1.1-alpha1

The "Candescent" release.

### Changes from 1.0.3

#### Feature changes
- **Clientbot now supports optional mode syncing** :tada: See the example conf for how to configure it (look for "modesync").
- PID file checking has been implemented and is turned on by default. :warning: **When upgrading from 1.0.x, remove `pylink.pid` before starting!**
- Revamped login configuration system, which now supports **multiple accounts and hashed passwords**
    - :warning: `login:user` and `login:password` are now deprecated and may be removed in a future release. Consider migrating to the new `login:` block in the example config.
    - Hashing new passwords can be done using the `mkpasswd` command via IRC, or the new command line utility `pylink-mkpasswd`.
- Services bots now support setting modes on themselves on join: see "joinmodes" in the example conf
- Added a contrib module downloader (`pylink-contribdl`)
- Relay now uses the PyLink permission system. The following permissions are now available:
	- Granted to opers by default:
		- `relay.create`
		- `relay.destroy`
		- `relay.claim`
		- `relay.link`
		- `relay.delink`
		- `relay.linkacl.view`
		- `relay.linkacl`
	- Granted to all users by default:
		- `relay.linked`
	- And the following which is not explicitly granted:
		- `relay.savedb`
- Relay: added a `purge` command to remove all relays involving a network
- Automode now supports remote channel manipulation in the form `netname#channel` (#352)
- protocols/ts6 now supports legacy UID introduction, for older servers / services
- Changehost gained a few new features (look for "changehost:" in the example conf):
    - Optional (per network) vHost enforcement: now you can create spoofs like freenode without using their IRCd!
    - Enforcement exceptions for the feature above
    - Options to enable/disable matching users by IP and real host
- New protocol support for `ircd-ratbox`, based off `ts6`
- New servermaps plugin, displaying network `/map`'s from the PyLink server's perspective. Relay links can be expanded as well to make this more detailed!
- Oper status tracking is now a network-specific option, for better security. Look for "track_oper_statuses" in the example config.
- The PyLink launcher now sets the terminal title on launch (Windows & POSIX)
- relay: implement a complementary `showchan` command, showing a list of relay links

#### Bug fixes
- Relay is potentially less crashy when PyLink is split off while it tries to introduce users (#354).
- The `bots` plugin now allows JOIN/NICK/PART on all service bots
- Relay: skip channel TS check for Clientbot (some users had this as a sporadic issue)
- Irc: explicitly kill connect loop threads after an Irc object has been removed. This fixes various freezing issues caused by ghosted connections after a network splits (#351).
- Relay: don't error when removing a channel from a network that isn't connected. (AttributeError on `removeChannel()` if `irc.pseudoclient` isn't set)

#### Internal fixes / improvements
- Server ID and service client name (if applicable) are now stored inside `IrcUser` objects, removing the need for some expensive reverse lookups
- Relay and Automode now use a centralized DataStore (backwards compatible) in `structures` for their database implementation
- Docstring rewrapping is now supported for neater, wrappable docstrings! (#307)
- `Irc.error()` was added for easier error replies; it is a simple wrapper around `Irc.reply()`
- Relay now uses locks in DB read/writes, for thread safety
- Most camel case functions in Relay were renamed to lowercase with underscores (PEP 8)

#### Misc. changes
- exec: Drop `raw` text logging to DEBUG to prevent information leakage (e.g. passwords on Clientbot)
- Removed `update.sh` (my convenience script for locally building + running PyLink)

# [PyLink 1.0.3](https://github.com/GLolol/PyLink/releases/tag/1.0.3)
Tagged as **1.0.3** by [GLolol](https://github.com/GLolol) on 2016-11-20T04:51:11Z

The "Buoyant" release.

### Changes from 1.0.2

#### Bug fixes
- Fixed invalid database names such as "automode-/tmp/test.db" from being generated when PyLink is started with an absolute path to its config.
- Backported fixes from 1.1-dev:
    - relay: skip channel TS checks for Clientbot, preventing possible "channel too old" errors on link.

#### Feature changes
- Backported features from 1.1-dev:
    - Relay: allow configuring custom relay server suffixes

#### Misc. changes
- Various spelling/grammar fixes in the example config.

# [PyLink 1.0.2](https://github.com/GLolol/PyLink/releases/tag/1.0.2)
Tagged as **1.0.2** by [GLolol](https://github.com/GLolol) on 2016-10-15T05:52:37Z

The "Baluga" release.

### Changes from 1.0.1

#### Bug fixes
- Clientbot: Fixed nick collisions between virtual clients and real users (#327)
- Fix typo in example conf that caused `log::filerotation` to become an empty, `None`-valued block. This in turn caused the `log` module to crash.

#### Feature changes
- Clientbot now uses a more specific realname fallback ("PyLink Relay Mirror Client") instead of potentially misleading text such as "PyLink Service Client". In the future, this text may be made configurable.

#### Internal fixes / improvements
 - setup.py: reworded warnings if `git describe --tags` fails / fallback version is used. Also, the internal VCS version for non-Git builds is now `-nogit` instead of `-dirty`.

# [PyLink 1.0.1](https://github.com/GLolol/PyLink/releases/tag/1.0.1)
Tagged as **1.0.1** by [GLolol](https://github.com/GLolol) on 2016-10-06T02:13:42Z

The "Beam" release.

### Changes from 1.0.0

#### Bug fixes

- **Fix PyLink being uninstallable via PyPI due to missing VERSION and README.md**
- ts6: don't crash when CHGHOST target is a nick instead of UID
- relay: clobber colour codes in hosts
- bots: allow JOIN/NICK/QUIT on ServiceBot clients

# [PyLink 1.0.0](https://github.com/GLolol/PyLink/releases/tag/1.0.0)
Tagged as **1.0.0** by [GLolol](https://github.com/GLolol) on 2016-09-17T05:25:51Z

The "Benevolence" release.

### Changes from 1.0-beta1

#### Bug fixes
- Clientbot now relays text sent from service bots.
- Fixed KeyErrors in Clientbot when receiving WHO replies for clients we don't know -- these are now ignored.
- Relay now skips mode type definitions when doing reverse mode lookup. This fixes channel mode `+l` mever being relayed UnrealIRCd, because `+l` happened to be the only supported type C mode.
- protocols/nefarious: fix UnboundLocalError when no modes are given on user introduction
- fantasy: don't error when bots are removed while processing a message (e.g. on shutdown)

#### Feature changes
- Automode now limits `listacc` to opers instead of all users (with default permissions settings).

#### Internal fixes / improvements
- Fixed incomplete hook payload keys from 1.0-beta1 (`oldchan`/`chandata` -> `channeldata`)
- services_support: hack away nick clashes between service clients & real users from Clientbot networks
- clientbot: downgrade bad updateClient() calls to warning

#### Misc. changes
- Documentation updates: Automode+permissions guide, README refresh, others.
- Example configuration changes:
  - Automode's bot nick now defaults to "Automode" instead of "ModeBot" for consistency.
  - Added a debug log example <sup><sup><sup>because nobody knew how to turn it on</sup></sup></sup>
  - Fix inverted option description for Relay's `show_netsplits` option.

# [PyLink 1.0-beta1](https://github.com/GLolol/PyLink/releases/tag/1.0-beta1)
Tagged as **1.0-beta1** by [GLolol](https://github.com/GLolol) on 2016-09-03T07:49:12Z

The "Badgers" release. Note: This is an **beta** build and may not be completely stable!

### Changes from 0.10-alpha1

#### Bug fixes
- Fixes for the Clientbot protocol module:
    - Fix `nick()` referring to the wrong variables (and thus not working at all)
    - Fix crashes caused by forced nick changes on connect
    - Clientbot now only sends `CHGHOST/CHGIDENT/CHGNAME` hooks the field has actually changed
- Automode now joins the Modebot client on `setacc`, if not already present

#### Feature changes
- Irc: implement basic message queueing (1 message sent per X seconds, where X defaults to 0.01 for servers) .
    - This appears to also workaround sporadic SSL errors causing disconnects (https://github.com/GLolol/PyLink/issues/246)
- relay: CLAIM is now more resistant to things like `/OJOIN` abuse<sup><sup><sup>Seriously people, show some respect for your linked networks ;)</sup></sup></sup>.
- core: New permissions system, used exclusively by Automode at this time. See `example-permissions.yml` in the Git tree for configuration options.
- relay_clientbot now optionally supports PMs with users linked via Clientbot. This can be enabled via the `relay::allow_clientbot_pms` option, and provides the following behaviour:
    - Private messages and notices *TO* Clientbot users are forwarded from the Relay bot as NOTICE.
    - Private messages can be sent *FROM* Clientbot users using the `rpm` command in `relay_clientbot`
- The PyLink launcher now shows the full VCS version in `pylink -v`
- Revert "relay_clientbot: always lowercase network name (stylistic choice)"

#### Internal fixes / improvements
- protocols/unreal: use umode `+xt` instead of blind `/SETHOST` when spawning users
- protocols/clientbot: handle numerics 463 (ERR_NOPERMFORHOST), 464 (ERR_PASSWDMISMATCH), and 465 (ERR_YOUREBANNEDCREEP) as fatal errors
- protocols: various fields in hook payloads are renamed for consistency:
    - The `chandata` field in SQUIT payloads is renamed to `channeldata`
    - The `oldchan` field in MODE payloads is renamed to `channeldata`
- `Irc.msg()` should no longer send empty text strings (which are technically illegal) in things like help strings.
- Irc: make sending of loopback hooks in `msg()` optional
- relay_clientbot: switch to `irc.msg()` for relayed text

#### Misc. changes
- Various to documentation update and installation instruction improvements.

# [PyLink 0.10-alpha1](https://github.com/GLolol/PyLink/releases/tag/0.10-alpha1)
Tagged as **0.10-alpha1** by [GLolol](https://github.com/GLolol) on 2016-08-22T00:04:34Z

The "Balloons" release. Note: This is an **alpha** build and may not be completely stable! This version includes all fixes from PyLink 0.9.2, with the following additions:

### Changes from 0.9.2

#### Bug fixes
- Improved syncing between Automode and Relay on JOINs. In other words: fixed Automode sometimes setting modes on join before all of a target's relay clones have joined corresponding relay channels on remote networks.
- protocols/inspircd now tracks required modules for vHost updating (CHGHOST/IDENT/NAME), instead of potentially sending unknown commands to the IRCd and causing a netsplit.
- changehost now explicitly forbids `$host` from being used in expansion fields, preventing vHosts from potentially being set in a loop whenever `applyhosts` is called.
- `eval` now formats empty strings correctly, instead of having no visible reply. In other words, it now wraps all output with `repr()`.
- relay: fix reversed prefix mode order in bursts (e.g. `+@~UID` instead of `~@+UID`). Fortunately, this is minor detail; no noticeable adverse effects to IRCd linking was ever experienced.

#### Feature changes

- **WIP** Clientbot protocol module: allows PyLink to connect as a bot to servers, for purposes such as relay.
    - Some features such as flood protection, services account tracking, and IRCv3 support are still missing.
    - **For Clientbot relay support, remember to also load the `relay_clientbot` plugin!**
- Added the ability to rotate logs at certain sizes, keeping X backups for reference.
- REHASH now updates file logging settings.
- Relay now allows configuring a list of nick globs to always tag nicks (`forcetag_nicks:` block in `relay:`)
- networks: new `reloadproto` command, allowing in-place reloading of protocol modules without restart.
- Ctrl-C / KeyboardInterrupt now cleanly shuts down PyLink (in most cases).
- SSL cert file and key file are now optional.
- changehost: show more friendly errors when an expansion field is unavailable
- protocols/inspircd: add support for SAKICK, ALLTIME.
- protocols/ unreal: add support for TSCTL ALLTIME.
- Added support for `/time` requests.

#### Internal fixes / improvements
- Shutdown now cleanly quits the PyLink service bot instead of simply splitting off.
- PyLink now shows a better error if a protocol module chosen is missing.
- Config key validation is now protocol-specific.
- The `IrcUser.identified` attribute was renamed to `IrcUser.account`.
- exec: make `pylinkirc` and `importlib` accessible for easier debugging.
- SQUIT hooks get a few more arguments, such as `nicks` (affected nicks) and `serverdata` (old IrcServer object).
- Retrieving the hostname used by the current PyLink instance is now a shared function: `irc.hostname()`
- Better handling of empty lines in command help - these are now sent as a single space instead of passing invalid text like `:<UID> NOTICE <UID> :` to the IRCd (no text in the text parameter).
- protocols/ts6: handle incoming ETB (extended topic burst) and EOPMOD (partial support; op moderated +z messages are converted to forms like `@#channel`).
- protocols/unreal: explicitly declare support for ESVID, or account name arguments in service stamps. Realistically this doesn't seem to affect S2S traffic, but it is the correct thing to do.

#### Misc. changes
- `FakeIRC` and `FakeProto` are removed (unused and not updated for 0.10 internal APIs)

# [PyLink 0.9.2](https://github.com/GLolol/PyLink/releases/tag/0.9.2)
Tagged as **0.9.2** by [GLolol](https://github.com/GLolol) on 2016-08-21T23:59:23Z

The "Acorn" release.

### Changes from 0.9.1

#### Bug fixes

- Relay now treats `{}` as valid characters in nicks.
- Fixed services login tracking for older Anope services + UnrealIRCd. Previously, PyLink would incorrectly store login timestamps as the account name, instead of the user's nick.
- Relay now normalizes `/` to `.` in hostnames on IRCd-Hybrid.
- Cloaked hosts for UnrealIRCd 3.2 users are now applied instead of the real host being visible.

# [PyLink 0.9.1](https://github.com/GLolol/PyLink/releases/tag/0.9.1)
Tagged as **0.9.1** by [GLolol](https://github.com/GLolol) on 2016-08-07T03:05:01Z

### *Important*, backwards incompatible changes for those upgrading from 0.8.x!
- The configuration file is now **pylink.yml** by default, instead of **config.yml**.
- PyLink now requires installing itself as a module, instead of simply running from source. Do this via `python3 setup.py install --user`.
- The `use_experimental_whois` option for InspIRCd servers and the `spawn_servers` option in Relay have been removed, as they are now implied.

### Changes from 0.9.0

#### Bug fixes

- Fixed various bugs in channel TS handling (this should reduce mode desyncs with relay).
- protocols/unreal: fixed services account support for older services (e.g. Anope < 2.0) that don't explicitly use account names for logins (#296).
- Mode changes are no longer sorted alphabetically when relayed: sorting now only applies for displaying a list of modes, such as in WHOIS.
- Invalid autojoin channels are now ignored, instead of passing potentially invalid data to the IRCd.

#### Feature changes

- `setup.py` now explicitly forbids installing on Python 2 (#297).
- The `nefarious` protocol module now forwards MODE and KICK through servers if the sender isn't opped, preventing many mode bounces, kick failures, and HACK server notices.

#### Internal fixes / improvements

- protocols/hybrid,ts6,unreal: Casemapping-specific lowercasing is now consistently used for channel names
- Relay now catches errors on network removal and ignores them.
- Channels names are now case normalized when receiving `@#channel` messages.

#### Misc. changes
- Minor example configuration updates, including a mention of passwordless UnrealIRCd links by setting recvpass and sendpass to `*`.

# [PyLink 0.9.0](https://github.com/GLolol/PyLink/releases/tag/0.9.0)
Tagged as **0.9.0** by [GLolol](https://github.com/GLolol) on 2016-07-25T05:49:55Z

### *Important*, backwards incompatible changes for those upgrading from 0.8.x!
- The configuration file is now **pylink.yml** by default, instead of **config.yml**.
- PyLink now requires installing itself as a module, instead of simply running from source. Do this via `python3 setup.py install --user`.
- The `use_experimental_whois` option for InspIRCd servers and the `spawn_servers` option in Relay have been removed, as they are now implied.

----

### Changes from 0.9-beta1

##### Added / changed / removed features
- PyLink is now slightly more descriptive if you try to start it with missing dependencies or a missing conf file.
- The PyLink API reference is now at https://pylink.github.io/ instead of in `docs/technical`.
- The `exec` and `eval` commands now have access to the `pylinkirc` and `importlib` imports by default.
- `jupe` from the `opercmds` plugin now requires the admin login instead of just oper.
- opercmds: `kick` now treat channels case insensitively.
- Documentation update: there are now guides to Automode and PyLink's Services API.

##### Bug fixes
- Fixed the `reload` command (again).
- Fixed compatibility with ircmatch 1.2: PyLink previously used features that were only available in the unreleased Git version.
- The `identify` command now responds with NOTICE instead of PM, behaving like any other command. Thanks to @Techman- for pointing this out.
- The `identify` command must be called in private again.
- Relay now shows secret channels in `linked` to those inside the channel, regardless of whether they're opered.
- `$channel:#channel:prefixmode` exttarget matching no longer raises errors if the target isn't in the specified channel.

##### Internal improvements
- Redone version handling so `__init__.py` isn't committed anymore.
- `update.sh` now passes arguments to the `pylink` launcher.

# [PyLink 0.9-beta1](https://github.com/GLolol/PyLink/releases/tag/0.9-beta1)
Tagged as **0.9-beta1** by [GLolol](https://github.com/GLolol) on 2016-07-14T02:11:07Z

### *Important*, backwards incompatible changes for those upgrading from 0.8.x
 - The configuration file is now **pylink.yml** by default, instead of **config.yml**.
 - PyLink now requires installing itself as a module, instead of simply running from source. Do this via `python3 setup.py install --user`.

----

### Changes from 0.9-alpha1

##### Added / changed / removed features
- The `use_experimental_whois` option for InspIRCd servers is removed, and is now implied.
- New config option `bot: whois_show_extensions_to_bots`, which optionally disables extended WHOIS replies for users marked as a bot (+B).
    - This increases security when relay is enabled, for bots that look for services logins in WHOIS.
- Automode has new `clearacc` and `syncacc` commands, for clearing and syncing access lists respectively.
- Relay now allows nick tagging to be turned off by default, via the option `relay: tag_nicks` (#116)
    - This is experimental, and nick tagging is still enabled by default.
    - Any attempts to KILL or SVSNICK a relay client are treated to force tag a nick, so things like `/ns release`, `/ns ghost`, and `/ns regain` should work with network services.
- Automode now only sends one MODE command per sync, to prevent changes from flooding channels.
- Relay separators can now be configured globally (`relay: separator` option), with server-specific overriding that value if given.

##### Bug fixes
- corecommands: fix `unload` failing to remove hooks and commands (0.9.x regression).
- protocols/nefarious: only send EOB_ACK to the direct uplink, preventing stray "acknowledged end of net.burst" messages from showing up. Thanks to Speakz on Evilnet IRC for reporting.
- protocols/unreal: fix server name of the uplink server not being saved (#268)
- Channel prefixes are now sorted in WHOIS output (i.e. no more wrong `@~#channel`), and only the highest prefix shown
- Fixed issues in internal channel mode tracking (c1cd6f4 58d71b0)
- WHOIS requests to the PyLink server for clients that aren't PyLink bots now work (syntax: `/raw whois pylink.server somenick`). "No such nick" errors are also sent when the target is missing, instead of raising warnings.
    - These WHOIS responses were previously sent from the wrong source (the server that the client was on, instead of the PyLink server), causing them to be ignored if they were going the wrong way.
- Automode now treat channels case insensitively in `delacc`.
- `ascii` and `rfc1459` case mappings now treat Unicode case sensitively, in the same way an IRCd would.

##### Internal improvements
- Removed inaccurate references to signon time in WHOIS and elsewhere.
- Changes to user timestamps are now tracked on NICK and SAVE commands
- Relay now creates relay clones with the current time as nick TS, instead of the origin user's TS.
    - This has the effect of purposely losing nick collisions against local users, so that it's easier to reclaim nicks.

# [PyLink 0.9-alpha1](https://github.com/GLolol/PyLink/releases/tag/0.9-alpha1)
Tagged as **0.9-alpha1** by [GLolol](https://github.com/GLolol) on 2016-07-09T07:27:47Z

### Summary of changes from 0.8.x

##### Backwards incompatible changes
 - Configuration file is now **pylink.yml** by default, instead of **config.yml**.
 - PyLink now requires installing itself as a module, instead of simply running from source. Do this via `python3 setup.py install --user`.

##### Added / changed / removed features
- New **`ctcp`** plugin, handling CTCP VERSION and PING ~~(and perhaps an easter egg?!)~~
- New **`automode`** plugin, implementing basic channel ACL by assigning prefix modes like `+o` to hostmasks and exttargets.
- New exttarget support: see https://github.com/GLolol/PyLink/blob/0.9-alpha1/coremods/exttargets.py#L15 for a list of supported ones.
- Relay can now handle messages sent by users not in a target channel (e.g. for channels marked `-n`)
- Relay subserver spawning is now always on - the `spawn_servers` option is removed
- Relay can now optionally show netsplits from remote networks, using a `show_netsplits` option in the `relay:` block
- The `channels` configuration option in `server:` blocks is now optional, and defaults to no channels if not specified
- The `maxnicklen` configuration option is also now optional, with a default value of 30 characters.
- `--version`, `--no-pid`, and `--help` are now implemented by PyLink's command line script
- Test cases were dropped - they were broken and poorly maintained.
- CPUlimit wrapper scripts were removed.
- Service bots now allow plugins to define service descriptions and mark commands as featured when adding them.
- Command replies for services bots are now consolidated into core. In general, FANTASY commands now reply in channel as PRIVMSG, while all commands sent in PM reply as private notices.
- protocols/inspircd: new `use_experimental_whois` server option, which forces PyLink to handle WHOIS requests locally. This allows relay WHOIS extensions like account name and origin server name (`whois_show_*` options) to actually work on InspIRCd networks.
- PyLink can now optionally protect its services clients by setting servprotect modes (InspIRCd umode `+k`, `+S` elsewhere). The option for this is `protect_services` in the `bot:` block.
- The `networks` now deletes IRC objects when `disconnect` is used. To reconnect all disconnected networks, use the `rehash` command.
- Relay now hides disconnected leaf networks from LINKED output.

##### Bug fixes
- Services bots will now ignore unhandled CTCP requests, instead of responding with "Unknown command"
- The `sid` field for TS6 servers now accepts unquoted numeric SIDs (integers) by normalize the SID to a string
- protocols/nefarious: fix wrong variable in "/join 0" handling causing crashes
- The PyLink bot now rejoins relay channels when it is killed
- protocols/ts6: fix wrong args in TB handling

##### Internal improvements
- `coreplugin.py` is split into `coremods/`, with many different submodules for easier maintenance.
- Rewritten channel TS handling to be more concise and reusable
- protocols/unreal: warn about mode bounces instead of fighting with the uplink
- protocols/ts6, protocols/nefarious: use protocol-specific ban bursting instead of sending a regular MODE
- `Irc.parseModes()` now handles strings given as the mode list properly, instead of only accepting a list of modestring arguments
- `SQUIT` handlers now return an `uplink` field with the SID of the server that the target was split from
- protocols/ts6: send 12 users (SJOIN) and 10 modes (TMODE) per line, instead of 10 and 9 respectively
- Relay is now slightly more careful when normalizing nicks: they can't have invalid characters, start with a hyphen (-), etc.
- Modes are now sorted when joined. You'll now see things like `+Hiow` instead of `+wHoi`
- protocols/inspircd: services clients with mode +k now have the "Network Service" oper type, in WHOIS replies and elsewhere
- SQUIT and KILL handling are moved into a protocols/ircs2s.py module, as the handling is basically the same on both TS6 and P10.
- protocols/nefarious,ts6,unreal: KILL handling (inbound & outbound) now supports kill paths and formats kill reasons properly
- protocols: encapsulated (ENCAP) commands are now implicitly expanded, so protocol modules no longer need to bother with IF statement chains in a `handle_encap()`

# [PyLink 0.8-alpha4](https://github.com/GLolol/PyLink/releases/tag/0.8-alpha4)
Tagged as **0.8-alpha4** by [GLolol](https://github.com/GLolol) on 2016-06-30T18:56:42Z

Major changes in this snapshot release:

- **SECURITY**: Forbid SSLv2 and SSLv3 in SSL socket creation (0fbf9e1)
- Configurable nicks for services (per-net and global, #220, #229)
- Resolve server hostnames when connecting (#158).
- protocols/ts6: fix incorrect WHOIS syntax causing connection abort (6060a88)
- protocols/nefarious: fix bad `/join 0` handling causing connection abort (b1e138d)
- relay: forbid linking two channels on the same network (e47738c)
- protocols: various fixes for mode definitions, including missing `+i` handling on ts6 and unreal (26df48c, 3e19e9c)
- Consistent defaults to ping frequency and timeout (now 90 and 180 seconds respectively)
- Example conf: fix various typos (0edb516, cd4bf55) and be more clear about link blocks only being examples
- Various freezes and crash bugs fixed (dd08c01, 1ad8b2e, 504a9be, 5f2da1c)

Full diff: https://github.com/GLolol/PyLink/compare/0.8-alpha3...0.8-alpha4

# [PyLink 0.8-alpha3](https://github.com/GLolol/PyLink/releases/tag/0.8-alpha3)
Tagged as **0.8-alpha3** by [GLolol](https://github.com/GLolol) on 2016-06-01T02:58:49Z

- relay: support relaying a few more channel modes (flood, joinflood, freetarget, noforwards, and noinvite)
- Introduce a new (WIP) API to create simple service bots (#216).
- The main PyLink client now spawns itself with hideoper whenever available, to avoid filling up `/lusers` and `/stats P/p`. (#194)
- The `fantasy` plugin now supports per-bot prefixes; see example conf for details.
- Purge c_ and u_ prefixes from PyLink's internal named modes definitions (#217).
- Various documentation updates.
- New `games` plugin, currently implementing eightball, dice, and fml.
- Various fixes to the Nefarious protocol module (89ed92b46a4376abf69698b76955fec010a230b4...c82cc9d822ad46f441de3f2f820d5203b6e70516, #209, #210).

# [PyLink 0.8-alpha2](https://github.com/GLolol/PyLink/releases/tag/0.8-alpha2)
Tagged as **0.8-alpha2** by [GLolol](https://github.com/GLolol) on 2016-05-08T04:40:17Z

- protocols/nefarious: fix incorrect decoding of IPv6 addresses (0e0d96e)
- protocols/(hybrid|nefarious): add missing BURST/SJOIN->JOIN hook mappings, fixing problems with relay missing users after a netjoin
- protocols/unreal: fix JOIN handling storing channels with the wrong case (b78b9113239bf115b476810c00e06f3a62118df5)
- protocols/inspircd: fix wrong username being sent when formatting KILL text
- commands: Fix `loglevel` command being ineffective (#208)
- relay: Fix various race conditions, especially when multiple networks happen to lose connection simultaneously
- API changes: many commands from `utils` were split into either `Irc()` or a new `structures` module (#199)

[Full diff](https://github.com/GLolol/PyLink/compare/0.8-alpha1...0.8-alpha2)

# [PyLink 0.8-alpha1](https://github.com/GLolol/PyLink/releases/tag/0.8-alpha1)
Tagged as **0.8-alpha1** by [GLolol](https://github.com/GLolol) on 2016-04-23T03:14:21Z

- New protocol support: IRCd-Hybrid 8.x and Nefarious IRCu
- Track user IPs of UnrealIRCd 3.2 users (#196)
- SIGHUP now rehashes PyLink on supported platforms (#179)
- Improved mode support for Charybdis (#203)
- Fix disconnect logic during ping timeouts

[Full diff](https://github.com/GLolol/PyLink/compare/0.7.2-dev...0.8-alpha1)

# [PyLink 0.7.2-dev](https://github.com/GLolol/PyLink/releases/tag/0.7.2-dev)
Tagged as **0.7.2-dev** by [GLolol](https://github.com/GLolol) on 2016-04-19T14:03:50Z

Bug fix release:

- Support mixed Unreal 3.2/4.0 networks (#193)
- More complete APIs for checking channel access (#168)
- New **`servprotect`** plugin for KILL/SAVE flood protection. This was split out of relay due to expiringdict not being installable via pip.
- Documentation update (protocol module variables, mention new WHOIS, VERSION hooks)
- Minor fixes for Windows support. (#183)
- SIGTERM should now shut down the daemon cleanly. (#179)

----
- 8ee64d5ec1bf9c87f16ba3a1210c2210bf50cd5f readme: mention why expiringdict is broken in pip3
- 528dfdba2abc95701fe037bb9d3fa41a7f9476c0 pmodule-spec: mention cmodes, umodes, prefixmodes variables
- cb3187c5e95e78517671d53b32915d869f4fc9e9 ts6_common: do reverse nick lookup for KICK targets
- 55afa1bff626e0dfea607149e285e0303bd3d01a unreal: log instances of PUID manging to debug
- 75984c3c4c788ba13894c1f37eb37436cbbe2d21 ts6_common: add abstraction to convert UIDs->outgoing nicks
- 9f20f8f76719a47e6ce8d0e1868dbeb056fd049e unreal: update SJOIN matching regex
- 4157cb5671691b848a19c2f084e2d49fd6212381 ts6_common: use a better variable name for _getSid()
- e687bb0a78fce6fd6446c5a0655e1ec037120b26 unreal: remove outfilter hack, this doesn't handle text including PUIDs properly
- 0136ff2c3a74561535259a9453687ce367465272 example conf: mention using spaces to indent
- 86781d37ba773525bb96eedaf45f33af420f0a38 README: fix typo
- 9fde35fd774e199648873b73cfca7e186b40eeca relay: handle server name conflicts more correctly
- c01b4497415691b140af747fb6187b4d41337d1d relay: treat network names case-sensitively
- 02ec50826bd0af2e60a5fd024a68a2579c6ce2b2 unreal: fix super() syntax in SQUIT handling
- 16779aa5ce067bfc4f9ddbf377e5238da105ea2b classes: remove lower() call when storing netname
- 6acfbb41253bfe8c9093636612b3c48b8f25eb09 unreal: case-desensitize legacy server names when handling user introductions from them
- 62da384caeb62f892286b9c1f269865e5b5dcbc3 README: unreal 3.2 mixed networks are supported now, sorta
- 5d0f450c73ea2fbac2f136b7805825c51900a024 Merge branches 'master' and 'devel' into devel+unreal32
- 956167538a4a7366ba23ca81624f798c0297bc64 unreal: add warnings & more descriptive errors regarding mixed_link
- f3ceefe87fe30aaae29d2e904fa44c6fd7a6e6aa unreal: initialize legacy users on the right server
- efd13d20ee4d801c0f69bee59d7335ca9e632069 example-conf: add sample unreal block, documenting mixed_link
- 44b102ffce03b746ad172c266f00eece15c92f1a networks: allow all opers to run 'autoconnect'
- 13e97177e2641595709a2940eb038b9fac2bdb3a docs: Add a PyLink oper guide
- c4273e68a4226ea2d9ee8f355ced734f6e57c88a unreal: fix for Python 3.4 support
- 4f088942273b612a8979c6874d16ed34e3930825 unreal: typofix
- 10be9623180ae1ed2dcbe4cffb598b79b4e2e39f unreal: actually return the hook data for NICK & KILL
- 44dc856ffaa4af4ee7918d7e6129e210b7842ca2 unreal: use an awful outFilter hack to convert PUIDs->nicks when sending outgoing commands
- 74ee1ded4dbf48fb123533a5277a35185eca2fa4 unreal: Start work on some really hacky Unreal 3.2 compat code (#193)
- 3e7255e4b2e052c76cd94784ad04b4e3cbf96604 classes: remove ts6-specific hack in Protocol.removeClient
- 514072804c7ba7a647e925c3e2cf0f1a95c2f8c8 README: mention the implications of #193
- fd32bbf45f91ea25fffd7397453afe0f6c49c7b8 unreal: fix typo in last commit
- efcc30c9838e8863b0a750973bc22e050bcd997d unreal: don't confuse legacy SERVER introductions from our uplink with protocol negotiation
- fab404f8d6312e83b317c41821ce9efb255beca9 Merge branches 'master' and 'wip/relay-fixes' into devel
- 3a8b0aa123c32c55ea4cb599fe56c613c74c2d64 relay: catch OSError too when loading DB
- 1bcadbe12b1df4b9d92954025697892c98b100b3 Use more flexible shebangs (/usr/bin/env python3)
- 9e33081bc9544d59316833c7d1a75fce517c087e relay: fix typo in comment
- d21344342d7c69a2f7ca578692d27c8907219920 relay: experimental fix for #183
- 8b7a9f6b459576641296271f7e4ce6ba0a2d9339 Merge pull request #189 from DanielOaks/devel+ignore-env
- d287a22aecd9aed707068bea12c61437df4a9aa2 gitignore: Ignore env folder for virtualenvs
- 58519011b8fa23b06c36632fa154bead56588a25 coreplugin: modularize shutdown routines, handle SIGTERM->shutdown
- b100f30cfe537fc3e0cbc1f2773cf32fbe98306a fantasy: break if IRC object isn't ready
- cf363432f0aa9d8152cfbe2bbbdb6f644bcef960 pylink: use abspath() to get the source directory
- 662d1ce03f8bb4b1110dab413cb13422737eeb9f inspircd: warn that inspircd 2.2 support is experimental
- 4a0ee6f54c6f2952abfb634c84369e506623c2c5 relay: be more thread-safe via dict.copy()
- 305db9f7540bea1f671007a2b1eea7cdd6c9fd87 utils: also don't crash in applyModes for bad mode targets
- e70dfb081196a2091d06476adc71bc8c4457f91f Merge branch 'master' into devel
- 08c3b99dfb17d6f7b284664366291010eed9e455 relay: fix ambiguous logging in KICK blocking
- 4125ff33b1803ab12e475fa508b3d1e1578f38b4 pylink: prettier "Loaded plugins" log message on start
- d5d3c2422bf2c623ffc3ccdf36110ed6a174dd6a inspircd: define minimum & target protocol versions instead of hardcoding them
- 70b9bde2c4cafb9f2ac9d2cf4ea96b341893c032 unreal: fix a little typo
- ad517f80da2ea23fb65cc9b0114b2fe0205b67d4 unreal: bump protocol version to 4000
- 19ac5b59a51988573eeab6ff77ded38ef4e93d04 protocols: drop underscores from pre-defined opertypes
- c71d2bfcb95d69aa1c54e46e1b388a7704e541c9 coreplugin: sync opertype changes in handle_operup
- 9278e56dd82e043b61d1acbe55bd68c6c82e3d97 coreplugin: normalize WHOIS output format
- 44083ccd5e94e3814b0bfff6f272567bef28bc5e core: Store opertype info in all IrcUser objects
- bdbc1020f2742bb004025bfd51966069f8841e5e Merge branch 'master' into devel
- fbd8659a7d6e2b08b7baa45bbdd95dbff67724b4 classes: spawn PyLink clients with a custom opertype
- a91fa46549e7601cb339fd9fc02e5ed47fbd1797 Regenerate pydoc documentation
- c8a35147765f04fb98e8629f6b475cf9a198feb4 hooks-reference: add VERSION and WHOIS
- f618b96b347b1a5c11cb11b9089ffb7f87874265 inspircd: add VERSION handling
- 00552a41a739ecccd2a25ffbb4314f81b142fcab Move detailed version string generation to utils
- 23056e97e3952561a83f466712cbc2a7c3df056a protocols & coreplugin: add handlers for VERSION requests
- 45c2abdae79ad14342a4cfb615c7b658d0aaa9ac Irc: run initVars() on connect too
- aedb05608e6ed02503bd077d7b7d2974936da734 relay: actually, just kill handle_spawnmain
- b2b04c8e7501c2abc9e83317d9da4047b76ef5d9 classes: really ignore errors when shutting down sockets
- ce3d3cf697278d571ccda4f043a3300405336e7e relay: check to make sure network is ready before handling spawnmain
- 0bb54d88e05431549cba39b0e172a70980ee727d New servprotect plugin (anti-KILL/SAVE flood)
- 9fe3373906a2e79fd860b9ffcbcfcccbafb40fa8 relay: get rid of kill/save protection
- 75ec95b8d358fc5a9ec936dae386bddc4fde0210 Merge branch 'master' into devel
- 03b53aee59f81ba3a271e84e6f260c9a6b4ea95c Merge branch 'staging' into devel
- e1830786452220484e7ed16d42053d5b288c77e1 protocols: Remove "secret" testing channel name
- 6962f3b73e8b18501bf91f4af6abfa64a55c9d8a ts6: unset has_eob correctly on reconnects
- c176c90bb6d3ac87bbda8953e68ac3998fd138ab coreplugin: use IrcChannel.getPrefixModes in whois replies
- f5f0df52ce0aaac3df5a21f117fe9f6bca71d801 classes: raise KeyError, not return KeyError...
- c86a02e044c47651ee6a942a51cd4572e7d92884 relay: use IrcChannel.getPrefixModes
- e948db5c7bf051ea780bfc36bc47495787b702ee classes: support looking at older versions of prefix modes mappings
- d84cfbcda169b2c1a428f5609463a4606ea07105 utils: simplify prefix modes handling in applyModes
- e8b00185854444faa12e0316b09bfe75731a9b60 classes: Implement IrcChannel.is(Voice|Halfop|Op)Plus (#168)
- ed333a6d1b03ecf57c6ea0917ccd54c1680f3ed4 classes: implement IrcChannel.isOp, isVoice, getPrefixmodes, etc
- 8135f3a735cf1bd15e3805eed7b29c4694ba1ab2 core: Depluralize prefixmodes mappings (#168)
- 1d4350c4fd00e7f8012781992ab73a1b73f396d2 classes: provide IrcChannel objects with their own name using KeyedDefaultdict
- 544d6e10418165415c8ffe2b5fbe59fcffd65b0f utils: add KeyedDefaultdict

# [PyLink 0.7.1-dev](https://github.com/GLolol/PyLink/releases/tag/0.7.1-dev)
Tagged as **0.7.1-dev** by [GLolol](https://github.com/GLolol) on 2016-03-31T01:42:41Z

Bugfix release. Lingering errata which you may still encounter: #183.

- 0fd093644cf14c9b689ce8d606722989df3477de utils: don't crash when mode target is invalid
- 1930739aad815efcadcdb50ccbcddd44bdcd4aef Revert "Irc: don't call initVars() on IRC object initialization"
- 2b16f25b612e2d3a0ba145cf314e5167b24c0767 classes.Irc: clear state on disconnect, not on connect
- a4395ed9893509334b868a9ba20f2da96923448c log: respect child loggers' levels if they are lower than the main one's
- 46922ce879e7505d09d2008960740d4a7e1082f7 relay: remove dead networks' servers from the servers index unconditionally
- f2a21148e7bb9ddd4f17767aaffe6fc408e66942 Irc: run initVars() on connect too
- 9cd1635f68dafee47f147de43b258014d14da6e2 unreal: fix wrong variable name in handle_umode2
- 2169a9be28331c6207865d50912cd671ff3c34a2 utils: actually abort when mode target is invalid

# [PyLink 0.7.0-dev](https://github.com/GLolol/PyLink/releases/tag/0.7.0-dev)
Tagged as **0.7.0-dev** by [GLolol](https://github.com/GLolol) on 2016-03-21T19:09:12Z

### Changes from 0.6.1-dev:

- d12e70d5e5c1981cf3eeb3c55e716bcb09b4af16 ts6: unset has_eob correctly on reconnects
- 5b2c9c593b467eb6fcd35f6fad3ff4f62925e4fe Add .mailmap
- abce18a5baf5d11d7e9f26b4339d1e64134eff52 log: split multi-line channel logs into multiple PRIVMSGs
- a8303d01102ba234ab667fad0df01cfb80e2c31b commands: sort channel list in 'showuser' output
- 0dd8b80a21d89998234c839663671ab662b8d6f9 docs/t: use rawgit links to serve HTML
- 506ae011a4a13531a66272573441f6f6bf5471f6 Update autogenerated docs (adding a script to do this now)
- d8e5202e5b684acc2571f0578319c48456a2345e world: use a better module description
- 2adb67d38e49e166658d9e996fb4869bc7a69a86 runtests: remove .py extension, only run tests when ran as a script
- da7bd649d2c19a544381a4002b55d8b352757414 conf: fix testconf missing the logging: section
- 557efc369f4e1bde965042513112b08bf2940c33 docs/t: mark hooks-reference as finished in README
- 9d0fcb5395f88b8aeda284c71ab4f30bbf97296c docs: finish off hooks-reference (#113)
- 15b35f1853b1d0826a409a4b5cc2216005a3554c ts6: support charybdis +T mode (closes #173)
- 359bfcd9dae38e5e6e487f9c773144ee26af06a5 bots: map 'msg' command to 'say' too
- b6889fb0978b563709356cb708290bf123e55b3b irc: fix spacing in certificate fingerprint logging
- 7f5bc52152bc082f7beb689233d062b7714ff571 relay: fix errors in KILL handling when target isn't in any relay channels
- 3527960d18b2366084ca0c7ad99c16a907e4f0fd coreplugin: tell plugins to exit cleanly before closing connections
- 9b0db81068e2c07867bd8100cb9007a198770cb5 changehost: modularize, add a command to apply cloaks now, match IPs too
- 14388d932fb774fa714b6e2d65f5cd3e2d51c3cf utils.getHostmask: add option to return IP address
- 5fed4629a612ba0e01616e61c70e03f3ce93c511 networks: remove networks with autoconnect off in 'disconnect'
- 8ac5436152cc70d187eb380e99f5bd46097bf39c relay: allow admins to destroy channels hosted on other networks
- 4df027cac43a44318504f83767eeba0573963d66 coreplugin: ignore services' attempts to send accountname before user introduction
- 1ce2725f1e19d9140f478acd5631f837dd4ba8ed bots: update help for 'msg' command (reflect changes made for #161)
- 54dc51aed4753691530b2ff056dac20ff2ac7c72 bots: make source client names optional (Closes #161)
- 34ca9730470c0479ee8d647317c2bf399d349472 relay: cleanup, consistently include the function in log.debug calls
- a740163cbef345f4487c2c5ead89e8e76cc6a6e1 relay: implement DB exporting using threading.Timer, similar to classes.Irc.schedulePing
- d5312018505893401eab59856fde756ed5916737 Merge branch 'master' into devel
- ae8f369f2e1a321c93b1d3537af804d3eee18160 relay: only show networks that are actually connected in LINKED
- de1a9a7995cc3110dbf2d289ca2c01d230a2ebc8 relay: various cleanup
- eec8e0dca4cd598e078e715f3b0784d0f6431933 log: attempt to remedy #164 (more testing needed)
- 40d76c8bb6b25a6a7fa49001ca921827e3d13081 coreplugin: demote successful oper-up messages to debug
- df23b797803f33d79d05cc8b66d72fa1bc214715 commands: reformat 'showuser' output, and show services login info (#25)
- decdf141fd7328c2ee133e8b1ecd6ccf946a6c16 unreal: don't use updateClient to update hostname of clients internally
- 2ebdb4bad65ae66cc33ea2fcb7cef445dfa8a395 unreal: support services account tracking (#25), fix handle_SVSMODE applying modes on the wrong target
- cabdb11f86cbe42165f36c3d4743eeef5a8cb7e9 inspircd: implement services account tracking (#25)
- 0fff91edfd3e10c4106039bc3b89101d6780c95f ts6: implement services account tracking (#25)
- cf15bed58dfd91ebb2ff2aa31ae19706f3f8abe5 classes: add services_account field in IrcUser (#25), default 'identified' attribute to empty string instead of None
- 584f95211383a3363be39c39a0409f65d1793de0 conf: check to make sure logging block exists in config
- 5877031203ceee2e60dc3d204691ddcb31393761 Merge branch 'master' into devel
- 21167e8fb3db21bf07bac890e2787a4fc535ffb1 example conf: use 1 "#" without trailing space for commented-out options
- 0d4655c381a1096920e16ce443ca688a7223755c core: support multiple channel loggers with DIFFERENT log levels & fix example conf (#83)
- 669e889e6fbc9a8405f4c8a751ccebe2c1990faa Support configurable SSL fingerprint hash types (Closes #157)
- 08fd50d3d8cbed4885791ec97f7c64f025664e08 Logging improvements, including support for custom file targets (#83)
- de84a5b4376da3e9636bad6463d7b79af0faa0c2 log: default level should be INFO, not DEBUG
- cf1de08457753bdfd13d340f2cfcb3e02998dd67 commands: support rehashing channel loggers
- 2503bd3ee5e512a5f6bfbd5ffe64edabcb64c278 commands: In rehash, use irc.disconnect() to disconnect networks removed from conf
- 14efb27fe8179cc199dab182e567c1ce4567ccdc Initial experimental support for logging to channels (#83)
- 4b939ea641284aa9bbb796adc58d273f080e59ee ts6: rewrite end-of-burst code (EOB is literally just a PING in ts6)
- 5a68dc1bc5f880d1117ca81e729f90fb5e1fce38 Irc: don't call initVars() on IRC object initialization

# [PyLink 0.6.1-dev](https://github.com/GLolol/PyLink/releases/tag/0.6.1-dev)
Tagged as **0.6.1-dev** by [GLolol](https://github.com/GLolol) on 2016-03-02T05:15:22Z

* Bug fix release.
    - unreal: fix handing of users connecting via IPv4 3c3ae10
    - ts6: fix incorrect recording of null IPs as 0 instead of 0.0.0.0 fdad7c9
    - inspircd, ts6: don't crash when receiving an unrecognized UID 341c208
    - inspircd: format kill reasons like `Killed (sourcenick (reason))` properly.

# [PyLink 0.6.0-dev](https://github.com/GLolol/PyLink/releases/tag/0.6.0-dev)
Tagged as **0.6.0-dev** by [GLolol](https://github.com/GLolol) on 2016-01-23T18:24:10Z

Notable changes in this release:

- New "opercmds" plugin:
    - This merges some functionality from the bots plugin, but also adds new commands such as `jupe`, `kill`, `topic`, and `checkban`.
- New "changehost" plugin - Automated configurable vHost setting on connect.
- Some core changes will **break** protocol modules and plugins written for older PyLink versions:
    - Some functions have been renamed:
        - `utils.nickToUid(irc, nick)` -> `irc.nickToUid(nick)`
        - `utils.isInternalClient(irc, uid)` -> `irc.isInternalClient(uid)`
        - `utils.isInternalServer(irc, uid)` -> `irc.isInternalServer(uid)`
        - `utils.clientToServer(irc, uid)` -> `utils.getServer(uid)`
        - `utils.getProtoModule(...)` -> `utils.getProtocolModule(...)`
    - Protocol specification is rewritten, with "Client" and "Server" dropped from the suffix of most outgoing commands: see acdd7dbb782765f581...2fd0a8ae741a663d.
- exec plugin: add `inject` and `raw` commands (4e7396b).
- exec plugin: support newline (and other) escapes in `exec` (375dbe8).
- protocols: allow changing remote users' hosts in updateClient (741fed9).
- Speed up and clean up shutdown sequence, fixing hangs due to sockets not shutting down cleanly (#152).
- protocols/unreal: Support cloaking with user mode `+x` (#136).
- Various bug fixes - see https://github.com/GLolol/PyLink/compare/0.5-dev...0.6.0-dev for a full diff.

# [PyLink 0.5-dev](https://github.com/GLolol/PyLink/releases/tag/0.5-dev)
Tagged as **0.5-dev** by [GLolol](https://github.com/GLolol) on 2015-12-06T17:54:02Z

The "We're getting somewhere..." release.

### Changes
- *Bug fixes, all the bug fixes*.

#### Core
- Support IPv6 connections in config.
- The offending hook data is now logged whenever a hook function errors, for more convenient debugging.
- Add sanity checks for autoconnect - delay has to be at least 1 second now, to prevent connect floods that go on without any delay in between!
- Add `irc.reply()` to send command replies to callers in the right context (channel or PM).
- More base commands are in `coreplugin` instead of `commands.py` now, making the latter reloadable without restart.
- Don't crash when REHASH loads a config file that's invalid.
- utils: Replace imp (deprecated) with importlib.

#### Plugins
- commands: Add a command to set log level (#124).
- commands: Update `irc.botdata` (`bot:` data in config) in REHASH.
- fantasy: Support nick prefixes (e.g. `PyLink: help`), along with a configurable prefix.

#### Protocols
- protocols/TS6: Fix SQUIT handling and introduction of SID-less servers (i.e. atheme's `/os JUPE`) (#119)
- protocols/unreal: **Add (experimental) support for UnrealIRCd 4.0.x!**
- plugins: More complete INFO logging: plugin loading/unloading, unknown commands called, successful operups

Full diff:https://github.com/GLolol/PyLink/compare/0.4.6-dev...0.5-dev

# [PyLink 0.4.6-dev](https://github.com/GLolol/PyLink/releases/tag/0.4.6-dev)
Tagged as **0.4.6-dev** by [GLolol](https://github.com/GLolol) on 2015-10-01T23:44:20Z

Bugfix release:

- f20e6775770b7a118a697c8ae08364d850cdf116 relay: fix PMs across the relay (7d919e6 regression)
- 55d9eb240f037a3378a92ab7661b31011398f565 classes.Irc: prettier __repr__

# [PyLink 0.4.5-dev](https://github.com/GLolol/PyLink/releases/tag/0.4.5-dev)
Tagged as **0.4.5-dev** by [GLolol](https://github.com/GLolol) on 2015-09-30T04:14:22Z

The "fancy stuff!" release.

New features including in-place config reloading (rehashing) (#89), FANTASY support (#111), and plugin (re/un)loading without a restart.

Full diff since 0.4.0-dev: https://github.com/GLolol/PyLink/compare/0.4.0-dev...0.4.5-dev

# [PyLink 0.3.50-dev](https://github.com/GLolol/PyLink/releases/tag/0.3.50-dev)
Tagged as **0.3.50-dev** by [GLolol](https://github.com/GLolol) on 2015-09-19T18:28:24Z

Many updates to core, preparing for an (eventual) 0.4.x release. Commits:

- 63189e9 relay: look at the right prefix mode list when rejoining from KILL
- cb83db4 relay: don't allow creating a channel that's already part of a relay
- 8faf86a relay: rejoin killed users to the RIGHT channels
- 2e0a5e5 utils.parseModes: fix IndexError on empty query
- 1f95774 inspircd: add proper fallback value for OPERTYPE?
- d6cb9d4 Merge commit '320de2079a78202e99c7b6aeb53c28c13f43ba47'
- 320de20 relay: add INVITE support (Closes #94)
- 60dc3fe relay: use "Channel delinked." part message when delinking channels
- 9a47ff8 Merge branch 'master' into devel
- ace0ddf relay: use JOIN instead of SJOIN for non-burst joins
- c2ee9ef Merge branch 'master' into devel
- 19fa31d relay: fix incorrect logging in getSupportedUmodes()
- 2f760c8 relay: Don't send empty user mode changes
- 4f40fae relay: in logs, be a bit more specific why we're blocking KILLs and KICKs
- 0b590d6 relay/protocols: use utils.toLower() for channel names, respecting IRCd casemappings
- 4525b81 relay.handle_kill: prevent yet another RuntimeError
- 26e102f Show oper types on WHOIS
- 8d19057 relay: set umode +H (hideoper) on all remote opered clients
- 5480ae1 classes: Remove "opertype" IrcUser() argument
- 531ebbb Merge branch 'master' into devel
- f9b4457 Decorate relay clients, etc. with custom OPERTYPEs
- 4a964b1 Merge branch 'master' into devel
- 1062e47 classes.IrcChannel: default modes to +nt on join
- d270a18 Remove unused imports
- 94f83eb relay.showuser: show home network/nick, and relay nicks regardless of oper status
- 5503477 commands: distinguish commands with multiple binds in 'list'
- 8976322 Replace admin.showuser with prettier whois-style cmds in 'commands' and 'relay'
- e1e31f6 Allow multiple plugins to bind to one command name!
- afd6d8c Refactor conf loading; skip the file-loading parts entirely for tests (#56)
- cda54c7 main: Fix b71e508.
- a58bee7 Modularize tests using common classes, add our custom test runner (#56)
- 549a1d1 classes: IrcServer.users is now a set()
- adb9ef1 classes: fixes for the test API
- 973aba6 Move utils' global variables to world.py
- b71e508 classes.Irc no longer needs a conf argument; tweak tests again
- ad5fc97 Many fixes to test API, utils.reverseModes stub
- ab4cb4d Merge branch 'master' into devel
- 2fe9b62 Consistently capitalize errors and other messages
- bc7765b Let's use consistent "Unknown command" errors, right?
- d059bd4 Move 'exec' command into its separate plugin
- 3d621b0 Move checkAuthenticated() to utils, and give it and isOper() toggles for allowing oper/PyLink logins
- 090fa85 Move Irc() from main.py to classes.py

# [PyLink 0.3.1-dev](https://github.com/GLolol/PyLink/releases/tag/0.3.1-dev)
Tagged as **0.3.1-dev** by [GLolol](https://github.com/GLolol) on 2015-09-03T06:56:48Z

Bugfix release + LINKACL support for relay. [Commits since 0.3.0-dev](https://github.com/GLolol/PyLink/compare/0.3.0-dev...0.3.1-dev):

- 043fccf4470bfbc8041056f5dbb694be079a45a5 Fix previous commit (Closes #100)
- 708d94916477f53ddc79a90c4ff321f636c01348 relay: join remote users before sending ours
- 8d44830d5c5b12abd6764038d7e9983998acdfc6 relay.handle_kill: prevent yet another RuntimeError
- 6d6606900e2df60eb8055da0e4452a560c7510b5 relay: coerse "/" to "|" in nicks if "/" isn't present in the separator
- c8e7b72065b2686c9691b276989ee948023ffe4d protocols: lowercase channel names in PRIVMSG handling
- 37eecd7d69cec794186024bf715a8ba55902d0e8 pr/inspircd: use OPERTYPE to oper up clients correctly, and handle the metadata accordingly 9f0f4cb1246c95335f42a24f7c5016175e6fba66 relay: burst the right set of modes
- 7620cd7433d9dc53dda1bdb06f6a9c673757f1f6 pr/inspircd: fix compatibility with channel mode +q (~)
- 3523f8f7663e618829dccfbec6eccfaf0ec87cc5 LINKACL support
- 51389b96e26224aab262b7b090032d0b745e9590 relay: LINKACL command (Closes #88)

# [PyLink 0.2.5-dev](https://github.com/GLolol/PyLink/releases/tag/0.2.5-dev)
Tagged as **0.2.5-dev** by [GLolol](https://github.com/GLolol) on 2015-08-16T05:39:34Z

See the diff for this development build: https://github.com/GLolol/PyLink/compare/0.2.3-dev...0.2.5-dev

# [PyLink 0.2.3-dev](https://github.com/GLolol/PyLink/releases/tag/0.2.3-dev)
Tagged as **0.2.3-dev** by [GLolol](https://github.com/GLolol) on 2015-07-26T06:11:20Z

The "prevent PyLink from wrecking my server's CPU" release.

Mostly bug fixes here, with a couple of scripts added (`start-cpulimit.sh` and `kill.sh`) added to assist running PyLink under the protection of [CPUlimit](https://github.com/opsengine/cpulimit). :)

#### New features

- relay: Block most duplicate modes from being relayed (#71)
- main: write a PID file to `pylink.pid` (f85fbd934bb2001122079da9e37e2fd1f9041a18)
- ts6: support `+AOS` charybdis extension modes, warning if the IRCd doesn't support them (146ab5e)

#### Fixes
- relay: quit users who aren't on any shared channels after KICK (71a3464)
- Use RFC1459 for case mapping on InspIRCd (01220b3)
- relay: Fix handling of local `SAVE` (e4da670) and `KILL` (a4da9b5) commands
- relay: fix nick collision loop on `SAVE` + when both tagged (i.e. _42XAAAAAA) and untagged (42XAAAAAA) versions of a UID nick exist (e354ada)
- relay: Fix command arguments of `DELINK` on home networks (c07cfb1)
- relay: `SJOIN` users once, and only once (#71, b681a67)
- main.Irc: catch `OSError` (bad file descriptor) errors and disconnect
- ts6: add QS as a required capability (69e16e5)
- ts6: fix `JOIN` handling and `parse_as` key handling in hooks (ddefd38)
- relay: only wait for `irc.connected` once per network (4d7d7ce)

Full diff: https://github.com/GLolol/PyLink/compare/0.2.2-dev...0.2.3-dev

# [PyLink 0.2.2-dev](https://github.com/GLolol/PyLink/releases/tag/0.2.2-dev)
Tagged as **0.2.2-dev** by [GLolol](https://github.com/GLolol) on 2015-07-24T18:09:44Z

The "please don't break again :( " release.

- Added `WHOIS` handling support for TS6 IRCds.
- ts6: fix handling of `SID`, `CHGHOST`, and `SQUIT` commands.
- Support noctcp (mode `+C`) on charybdis, and wallops (`+w`) in relay.
- Raised fallback ping frequency to 30

...And of course, lots and lots of bug fixes; I won't bother to list them all.

Full diff: https://github.com/GLolol/PyLink/compare/0.2.0-dev...0.2.2-dev

# [PyLink 0.2.0-dev](https://github.com/GLolol/PyLink/releases/tag/0.2.0-dev)
Tagged as **0.2.0-dev** by [GLolol](https://github.com/GLolol) on 2015-07-23T04:44:17Z

Many changes in this development release, including:

- **New `ts6` protocol module, for charybdis 3.x.**
- relay: add nick collision handling via `SAVE` (#61).
- relay: trivial tasks like `TOPIC`, `MODE`, `KICK` and `PART` no longer spawn new clients for their senders, and are routed through the pseudoserver when applicable instead (e76d31d c0f8259).
- Irc: be safer against `UnicodeDecodeError` caused by `socket.recv()` cutoff, by decoding each individual line instead (06d17d5).
- relay: make the `nick/net` separator a per-network config option. (ad34f6c).
- relay: Use a whitelist when it comes to relaying modes (#54), and strip out bans that don't match `nick!user@host` syntax (#55).
- relay: Handle user mode changes (#64).
- Support different case mappings for nicknames (RFC1459 vs ASCII) (#75).
- inspircd: remove `RSQUIT` command handler (3494d4f).

And of course, many, many bug fixes! (relay should now work properly with more than 2 networks, for example...)

Full diff: https://github.com/GLolol/PyLink/compare/0.1.6-dev...0.2.0-dev

# [PyLink 0.1.6-dev](https://github.com/GLolol/PyLink/releases/tag/0.1.6-dev)
Tagged as **0.1.6-dev** by [GLolol](https://github.com/GLolol) on 2015-07-20T06:09:40Z

### Bug fixes and improvements from 0.1.5-dev

- Irc.send: catch `AttributeError` when `self.socket` doesn't exist; i.e. when initial connection fails (b627513)
- Log output to `log/pylink.log`, along with console (#52, 61804b1 fbc2fbf)
- main/coreplugin: use `log.exception()` instead of `traceback.print_exc()`, so logs aren't only printed to screen (536366d)
- relay: don't relay messages sent to the PyLink client (688675d)
- relay: add a `save` command, and make rescheduling optional in `exportDB()` (c00da49)
- utils: add `getHostmask()` (1b09a00)
- various: Log command usage, `exec` usage, successful logins, and access denied errors in `admin.py`'s commands (57e9bf6)

Full diff: https://github.com/GLolol/PyLink/compare/0.1.5-dev...0.1.6-dev

# [PyLink 0.1.5-dev](https://github.com/GLolol/PyLink/releases/tag/0.1.5-dev)
Tagged as **0.1.5-dev** by [GLolol](https://github.com/GLolol) on 2015-07-18T20:01:39Z

### New features

- Hooks for `CHGHOST`, `CHGIDENT`, and `CHGNAME` (f9d8215 35f1c88)
- IrcUser: Implement user channel tracking via an `IrcUser.channels` attribute (d97fce8)
- Send PING to our uplink periodically, and quit if we don't get a response (#42, #57)
    - New server `pingfreq` option is introduced to set the time between PINGs.
- relay: Only spawn clients if they share a channel, and quit them when they leave all shared channels (cf32461)
- Support autoreconnecting to networks! A new `autoconnect` server setting is added to set autoconnect delay.
- New `PYLINK_DISCONNECT` hook to keep track of network disconnections (3f6f78b)
- relay: add a `LINKED` command (#65, bbcd70b)
- commands: add a `HELP` command (#8, 6508cb3 4553eda)

### Bug fixes
- relay: don't spawn tagged clones for the internal PyLink client (40fd9e3)
- relay: don't send empty `MODE` commands if there are no supported modes left after filtering (2a586a6)
- protocol/inspircd: don't raise KeyError when removing channel from user fails (73c625a)
- relay: only join PyLink to channels & set topics if there's actually a relay on the network (49943a7)
- relay: fix the wrong modes being propagated to the wrong channels on `LINK` (#53, ccf7596)
- relay: fix "RuntimeError: dictionary changed size during iteration" in `handle_part` (d30890c)
- relay: Only allow messaging users in common channels / channels that you're in (#62, 024ac16)

### Misc. changes
- Move client/server spawning, hook calling, command handling, and KILL/KICK detection outside the protocol module (0aa2f98 fdea348)
- Fix fakeirc and tests for relay (#56, a51cfcb)

### Removed features
- commands: remove `debug` command; it's useless now that `exec`, `showchan`, and `showuser` exist (50665ec)
- admin: `tell` command has been removed. Rationale: limited usefulness; doesn't wrap long messages properly. (4553eda)

You can view the full diff here: https://github.com/GLolol/PyLink/compare/0.1.0-dev...0.1.5-dev

# [PyLink 0.1.0-dev](https://github.com/GLolol/PyLink/releases/tag/0.1.0-dev)
Tagged as **0.1.0-dev** by [GLolol](https://github.com/GLolol) on 2015-07-16T06:27:12Z

PyLink's first pre-alpha development snapshot.

Working protocol modules:
- InspIRCd 2.0.x - `inspircd`

Working plugins:
- `admin`
- `hooks`
- `commands`
- `relay`


# Starting meme-server
git clone

`cd` to meme-server

`./start.sh`


Make sure you're in a tmux session to ensure that it remains running upon disconnecting from SSH

## Tmux stuffs
`tmux new -s <session name>` - Starts a new session with the given name

`tmux attach -t <session name>` - Attaches to the session with the given name, if any

`tmux ls` - Lists all active tmux sessions

`tmux kill-session -t <session name>` - Kills the session with the given name, if any


**Shortcuts**

`Ctrl^b+d` to detach from an active session, if attached.

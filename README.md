# Ursina TCP Deathmatch

A small multiplayer first-person deathmatch game built with [Ursina](https://www.ursinaengine.org/) and Python TCP sockets. One player runs the server and other players connect as clients over a local network or a reachable public address.

![Enter Game](https://github.com/user-attachments/assets/5b8176bb-78be-4212-8782-6b41f9232a22)
![Shoot and Run](https://github.com/user-attachments/assets/e44349bd-d11a-4ce0-812f-747f95e70794)
![Respawn](https://github.com/user-attachments/assets/c6f43550-f8c6-4251-86ad-35b5c2d468d1)

## Features

- First-person movement, jumping, shooting, health, death, and respawning
- Up to 10 concurrent players
- Player names represented by selectable colors
- TCP networking for player movement, health, bullets, and respawn events
- Fullscreen Ursina game window with a Tkinter connection screen

## Requirements

- Python 3.10 or newer
- A display and audio-capable environment for the client
- Windows, Linux, or macOS

Install the dependencies from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Linux or macOS, activate the environment with:

```bash
source .venv/bin/activate
```

## Start a Game

### 1. Start the server

From the repository root:

```bash
python server/main.py
```

The server listens on port `8888` on all interfaces (`0.0.0.0`) and automatically detects and displays your Tailscale IPv4 address (if Tailscale is running) alongside your local LAN address. Keep this terminal open while playing.

### 2. Start a client

In a second terminal, from the repository root:

```bash
python client/main.py
```

When the connection screen appears, enter a player name, the server address, and port `8888`.
- **Over Tailscale:** Use the server machine's Tailscale IPv4 address (e.g. `100.x.y.z`), which is auto-detected and prefilled in the connection dropdown.
- **On the same computer:** Use `127.0.0.1` or the Tailscale IP.
- **On the same local Wi-Fi / LAN:** Use the server computer's local IPv4 address.

Every player runs their own copy of the client and connects to the same server. The server allows a maximum of 10 players.

## Controls

| Action | Control |
| --- | --- |
| Move | `W` `A` `S` `D` |
| Jump | `Space` |
| Aim | Mouse |
| Shoot | Left mouse button |
| Respawn after death | `R`, `Space`, `Enter`, or the respawn button |
| Exit | `Esc` |

## Network Setup

For LAN play, allow Python through the server computer's firewall and make sure all computers are on the same network. The default port is `8888` for both the client and server.

For internet play, forward TCP port `8888` to the server computer or use a TCP tunneling service. Players must connect to the resulting public address. Do not expose the server to the internet without considering firewall rules and access control; this project does not include authentication or encrypted transport.

## Project Layout

```text
client/
	main.py       Client entry point and game loop
	network.py    TCP client and message serialization
	player.py     Local player, health, death, and respawn behavior
	enemy.py      Remote player representation
	bullet.py     Projectile behavior
	floor.py      Arena floor
	map.py        Arena geometry
	assets/       Textures and audio
server/
	main.py       TCP game server
requirements.txt
```

## Troubleshooting

- **Connection refused:** Start the server first and confirm the address and port are correct.
- **Timeout:** Check the firewall, port forwarding, and whether the server is reachable from the client machine.
- **Invalid address:** Enter an IPv4 address or hostname that resolves on the client machine.
- **Missing asset or GUI errors:** Run the client from the repository root with `python client/main.py`, and use a desktop session rather than a headless terminal.
- **Port already in use:** Stop the process using port `8888`, or change `PORT` in both `server/main.py` and `client/main.py` to the same available port.

## License

See [LICENSE](LICENSE).

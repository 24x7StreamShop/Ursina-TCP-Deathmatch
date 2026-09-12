import socket
import json



class Network:
    """
    A client class to abstract away socket functions and make communication with server less of a headache.

    Args:
        server_addr (str): IPv4 address of the server
        server_port (int): Port at which server is running
        username (str): Username of this client's player
    """

    def __init__(self, server_addr: str, server_port: int, username: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = server_addr
        self.port = server_port
        self.username = username
        self.recv_size = 2048
        self.id = 0

    def settimeout(self, value):
        self.client.settimeout(value)

    def connect(self):
        """
        Connect to the server and get a unique identifier
        """

        self.client.connect((self.addr, self.port))
        self.id = self.client.recv(self.recv_size).decode("utf8")
        self.client.send(self.username.encode("utf8"))

    def receive_info(self):
        msg = None
        try:
            msg = self.client.recv(self.recv_size)
        except socket.error as e:
            print(e)
            return None

        if not msg:
            return None

        try:
            msg_decoded = msg.decode("utf8")
            left_bracket_index = msg_decoded.index("{")
            right_bracket_index = msg_decoded.index("}") + 1
            msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]
            msg_json = json.loads(msg_decoded)
            return msg_json
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
            return None

    def send_player(self, player):
        pos = (player.world_x, player.world_y, player.world_z)
        player_info = {
            "object": "player",
            "id": self.id,
            "position": pos,
            "rotation": player.rotation_y,
            "health": player.health,
            "joined": False,
            "left": False
        }
        player_info_encoded = json.dumps(player_info).encode("utf8")

        try:
            self.client.send(player_info_encoded)
        except socket.error as e:
            print(e)

    def send_bullet(self, bullet):
        bullet_info = {
            "object": "bullet",
            "position": (bullet.world_x, bullet.world_y, bullet.world_z),
            "damage": bullet.damage,
            "direction": bullet.direction,
            "x_direction": bullet.x_direction
        }

        bullet_info_encoded = json.dumps(bullet_info).encode("utf8")

        try:
            self.client.send(bullet_info_encoded)
        except socket.error as e:
            print(e)

    def send_health(self, player):
        health_info = {
            "object": "health_update",
            "id": player.id,
            "health": player.health
        }

        health_info_encoded = json.dumps(health_info).encode("utf8")

        try:
            self.client.send(health_info_encoded)
        except socket.error as e:
            print(e)

    def send_respawn(self, position=(0, 1, 0), health=100):
        if hasattr(position, "x"):
            pos = (position.x, position.y, position.z)
        else:
            pos = (position[0], position[1], position[2])

        respawn_info = {
            "object": "respawn",
            "id": self.id,
            "position": pos,
            "health": health
        }

        respawn_info_encoded = json.dumps(respawn_info).encode("utf8")

        try:
            self.client.send(respawn_info_encoded)
        except socket.error as e:
            print(e)


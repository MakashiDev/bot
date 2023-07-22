import json

class Agent:
    def __init__(self, filename="config.json"):
        """
        Agent is a class that handles all the data for the bot.
        It is used to store and retrieve data from the config.json file.
        
        Parameters
        ----------
        filename : str
        """
        self.filename = filename

    def get_server_by_guild_id(self, guild_id):
        with open(self.filename, "r") as f:
            server = json.load(f)
            servers = server["servers"]
            for s in servers:
                if s["guildId"] == guild_id:
                    return s
        return None

    def get_from_json(self, server_id, index, group=None):
        server = self.get_server_by_guild_id(server_id)
        if server:
            if group is None:
                return server.get(index)
            else:
                if group == "town":
                    for town in server.get("towns", []):
                        if town["name"].lower() == index.lower():
                            return town
                elif group == "roles":
                    return server.get("roles", {}).get(index)
                elif group == "channels":
                    return server.get("channels", {}).get(index)
        return None

    def set_to_json(self, server_id, index, value, group=None):
        server = self.get_server_by_guild_id(server_id)
        if server:
            if group is None:
                server[index] = value
            else:
                if group == "town":
                    for town in server.get("towns", []):
                        if town["name"].lower() == index.lower():
                            town.update(value)
                elif group == "roles":
                    server["roles"][index] = value
                elif group == "channels":
                    server["channels"][index] = value

        with open(self.filename, "w") as f:
            json.dump(server, f)

    def add_server_to_json(self, welcome_channel, announcement_channel , general_channel,ticket_channel,  ticket_log_channel, ticket_category, ticket_master_role, guild_id, members, guild_name):
        server = self.get_server_by_guild_id(guild_id)
        if server:
            return "Already Set Up"

        with open(self.filename, "r") as f:
            data = json.load(f)
            servers = data.get("servers", [])
            servers.append({
                "guildId": guild_id,
                "guildName": guild_name,
                "members": members,
                "channels": {
                    "welcomeChannelId": welcome_channel,
                    "ticketChannelId": ticket_channel,
                    "ticketLogChannelId": ticket_log_channel,
                    "ticketCategory": ticket_category,
                    "announcementChannelId": announcement_channel,
                    "generalChannelId": general_channel,
                    "ticketMsg": 0,
                },
                "roles": {
                    "ticketMaster": ticket_master_role,
                },
                "towns": [],
                "ticketCount": 0,
            })
        with open(self.filename, "w") as f:
            json.dump(data, f)
        return "Server Added"

    def add_town_to_json(self, town_name, town_leader_role, guild_id, town_role=None, town_channel=None):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                return "Town Already Exists"

        towns.append({
            "name": town_name,
            "leader": town_leader_role,
            "role": town_role,
            "channel": town_channel,
            "members": [],
        })

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Town Added"

    def remove_town_from_json(self, town_name, guild_id):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                towns.remove(town)
                with open(self.filename, "w") as f:
                    json.dump(server, f)
                return "Town Removed"
        return "Town does not exist"

    def update_town_in_json(self, town_name, town_leader_role, guild_id, town_role=None, town_channel=None):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                town["leader"] = town_leader_role
                town["role"] = town_role
                town["channel"] = town_channel

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Town Updated"

    def add_town_role_to_json(self, town_name, town_role, guild_id):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                town_roles = town.get("roles", [])
                if town_role not in town_roles:
                    town_roles.append(town_role)

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Town Role Added"

    def remove_town_role_from_json(self, town_name, town_role, guild_id):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                town_roles = town.get("roles", [])
                if town_role in town_roles:
                    town_roles.remove(town_role)

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Town Role Removed"

    def add_town_channel_to_json(self, town_name, town_channel, guild_id):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                town_channels = town.get("channels", [])
                if town_channel not in town_channels:
                    town_channels.append(town_channel)

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Town Channel Added"

    def remove_town_channel_from_json(self, town_name, town_channel, guild_id):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                town_channels = town.get("channels", [])
                if town_channel in town_channels:
                    town_channels.remove(town_channel)

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Town Channel Removed"
    def add_member_to_town(self, town_name, member, guild_id):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                members = town.get("members", [])
                if member.id not in members:
                    json_member = {
                        "id": member.id,
                        "name": member.name,
                        "discriminator": member.discriminator,
                        "nick": member.nick,
                    }
                    members.append(json_member)

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Member Added"
    def remove_member_from_town(self, town_name, member, guild_id):
        server = self.get_server_by_guild_id(guild_id)
        if not server:
            return "Server Not Found"

        towns = server.get("towns", [])
        for town in towns:
            if town["name"].lower() == town_name.lower():
                members = town.get("members", [])
                if member.id in members:
                    members.remove(member.id)

        with open(self.filename, "w") as f:
            json.dump(server, f)
        return "Member Removed"


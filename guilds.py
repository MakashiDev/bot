import json

class Guilds:
    def __init__(self, filename="config.json"):
        """
        Agent is a class that handles all the data for the bot.
        It is used to store and retrieve data from the config.json file.
        
        Parameters
        ----------
        filename : str
        """
        self.filename = filename
        self.data = None
        self.guild = None
        self.init()


    def init(self):
        """
        Initializes the agent by loading the config.json file.
        """
        with open(self.filename, "r") as f:
            self.data = json.load(f)

    def get_guild(self, guildIndex):
        """
        Initializes the guild by loading the config.json file.
        
        Parameters
        ----------
        guildIndex : int
            The index of the guild in the config.json file.

        Returns
        -------
        Guild
            The guild object.
        """


        return Guild(guildIndex, self.data)
        
    
    def update_data(self, data):
        """
        Parameters
        ----------
        data : dict
            The data to update the config.json file with.
        """
        self.data = data
        with open(self.filename, "w") as f:
            json.dump(data, f)
    
    def get_data(self):
        """
        Returns
        -------
        dict
            The data of the agent.
        """
        return self.data
    def get_guilds(self):
        """
        Returns
        -------
        dict
            The guilds
        """
        return self.data

    def new(self, guildId, guildName, members, channels, roles, towns):
        """
        Parameters
        ----------
        guildId : int
            The id of the guild.
        guildName : str
            The name of the guild.
        members : int
            The members of the guild.
        channels : object
            The channels of the guild.
        roles : object
            The roles of the guild.
        """
        data = self.get_data()
        data.append({
            "guildId": guildId,
            "guildName": guildName,
            "members": members,
            "channels": channels,
            "roles": roles 
        })
        self.update_data(data)
        

    def get_guild_index(self, id):
        """
        Parameters
        ----------
        id : int
            The id of the guild.
        
        Returns
        -------
        int
            The index of the guild in the config.json file.
        """
        for i in range(len(self.data)):
            if self.data[i]["guildId"] == id:
                return i
        return None
    
    

class Guild:
    def __init__(self, guildIndex, data):
        """
        Guild is a class that handles all the data for a specific guild.
        It is used to store and retrieve data from the config.json file.
        
        Parameters
        ----------
        guildIndex : int
            The index of the guild in the config.json file.
        data : dict
            The data to update the config.json file with.
        """
        self.guildIndex = guildIndex
        self.guild = None
        self.data = data
        
        self.init()
    
    
    def init(self):
        """
        Initializes the guild by loading the config.json file.
        """
        self.guild = self.data[str(self.guildIndex)]
    
    
    def update_data(self, data):
        """
        Parameters
        ----------
        data : dict
            The data to update the config.json file with.
        """
        self.data[str(self.guildIndex)] = data
        with open("config.json", "w") as f:
            json.dump(data, f)
    
    
    def get_data(self):
        """
        Returns
        -------
        dict
            The data of the guild.
        """
        return self.guild
    
    def add_new_town(self, name, ownerID, role, channel):
        """
        Parameters
        ----------
        name : str
            The name of the town.
        ownerID : int
            The id of the owner of the town.
        members : list
            The members of the town.
        """
        data = self.get_data()
        data["towns"].append({
            "name": name,
            "ownerID": ownerID,
            "members": [],
            "role": role,
            "channel": channel
        })
        self.update_data(data)
    
    def update_town(self, town_name, role, channel):
        """
        Parameters
        ----------
        town_name : str
            The name of the town to update.
        role : int
            The id of the role to update.
        channel : int
            The id of the channel to update.
        """
        data = self.get_data()
        for i in range(len(data["towns"])):
            if data["towns"][i]["name"] == town_name:
                data["towns"][i]["role"] = role
                data["towns"][i]["channel"] = channel
                break
        self.update_data(data)

    def remove_town(self, town_name):
        """
        Parameters
        ----------
        town_name : str
            The name of the town to remove.

        Removes a town from the guild.
        """
        data = self.get_data()
        for i in range(len(data["towns"])):
            if data["towns"][i]["name"] == town_name:
                data["towns"].pop(i)
                break
        self.update_data(data)

    def add_new_member(self, townName, username, id):
        """
        Parameters
        ----------
        townIndex : int
            The index of the town in the towns list.
        memberID : int
            The id of the member to add.
        """
        data = self.get_data()
        for i in range(len(data["towns"])):
            if data["towns"][i]["name"] == townName:
                data["towns"][i]["members"].append({
                    "username": username,
                    "id": id
                })
                break
        self.update_data(data)

    def remove_member(self, townIndex, memberID):
        """
        Parameters
        ----------
        townIndex : int
            The index of the town in the towns list.
        memberID : int
            The id of the member to remove.
        """
        data = self.get_data()
        data["towns"][townIndex]["members"].remove(memberID)
        self.update_data(data)

    def get_role(self, role_name):
        """
        Parameters
        ----------
        role_name : str
            The name of the role to get.
        
        Returns
        -------
        int
            The id of the role.
        """
       
        return self.guild["roles"][role_name]
    
    def get_channel(self, channel_name):
        """
        Parameters
        ----------
        channel_name : str
            The name of the channel to get.
        
        Returns
        -------
        int
            The id of the channel.
        """
        return self.guild["channels"][channel_name]

    def get_ticket_count(self):
        """
        Returns
        -------
        int
            The number of tickets in the guild.
        """
        return len(self.guild["ticketCount"])
    
    def set_ticket_count(self, count):
        """
        Parameters
        ----------
        count : int
            The number of tickets in the guild.
        """
        data = self.get_data()
        data["ticketCount"] = count
        self.update_data(data)

    def get_towns(self):
        """
        Returns
        -------
        list
            The towns in the guild.
        """
        return self.guild["towns"]
    


    

    
    
    
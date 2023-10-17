import discord  # py-cord
import logging
import json
from guilds import Guilds
import os

guilds = Guilds()

# Set up logging
logging.basicConfig(level=logging.INFO)


token = ""
try:
    with open("token.txt", "r") as f:
        token = f.read()
except FileNotFoundError:
    raise FileNotFoundError(
        "token.txt not found. Please create a file called token.txt and put your bot token in it.")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.guilds = True

bot = discord.Bot(intents=intents)



@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the Kingdom of Doveria"))
    await setUpJoinTickets()
    # log with yellow text
    logging.info("Bot is ready")

# when bot joins a server
@bot.event
async def on_guild_join(guild):
    owner = guild.owner
     # embed explaing how to set up the bot,  and thank them for adding the bot
    embed = discord.Embed(title="Thank you for adding me to your server", description="Thank you for adding me to your server", color=0x00a6ff)
    embed.add_field(name="How to set up the bot", value="To set up the bot use the command `/setup <welcome_channel> <announcement_channel> <general_channel> <ticket_channel> <ticket_log_channel> <ticket_category> <ticket_master_role>`", inline=False)
    # explain that to add town role and town channel you must pay for premium
    embed.add_field(name="Premium", value="To get premium go to https://www.patreon.com/kingdomofdoveria", inline=False)
    # say that yuo need premium to add town role and town channel
    embed.add_field(name="Premium Commands", value="To add a town role use the command `/addtownrole <town_name> <town_role>`", inline=False)
    embed.add_field(name="Premium Commands", value="To add a town channel use the command `/addtownchannel <town_name> <town_channel>`", inline=False)
    # explain that Homeland is a bot to help you manage your Stonework RP servers, and make it easy to manage your citizens, and the towns there in 
    embed.add_field(name="What is Homeland", value="Homeland is a bot to help you manage your Stonework RP servers, and make it easy to manage your citizens, and the towns there in", inline=False)
    # explain that Homeland is a bot to help you manage your Stonework RP servers, and make it easy to manage your citizens, and the towns there in
    embed.add_field(name="Ticket System", value="Homeland has a ticket system to make it easy for users to get support, or join the server.", inline=False)
    embed.add_field(name="Joining Process", value="Homeland makes it really easy to add new users to your servers, with easy commands.", inline=False)
    embed.add_field(name="Premium Commands", value="To add a town role use the command `/addtownrole <town_name> <town_role>`", inline=False)
    embed.add_field(name="Premium Commands", value="To add a town channel use the command `/addtownchannel <town_name> <town_channel>`", inline=False)
    try:
        channels = guild.channels
        for channel in channels:
            if channel.type == discord.ChannelType.text:
                # check if name contains general
                if "general" in channel.name.lower():
                    general = channel
                
        #send
        await general.send(owner.mention)
        await general.send(embed=embed)
    except:
        #dm the owner
        dm = await owner.create_dm()
        await dm.send(owner.mention)
        await dm.send(embed=embed)
    # log with yellow text
    logging.info(f"Bot joined {guild.name}")
    
        
                        


@bot.event
async def on_command(ctx):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")


async def createTicket(ticketType, interaction):

    guildIndex = guilds.get_guild_index(interaction.guild.id)
    guild = guilds.get_guild(guildIndex)

    supportRole = interaction.guild.get_role(guild.get_role("ticket"))
    ticketLogChannel = interaction.guild.get_channel(guild.get_channel("ticketLogs"))
    catergory = interaction.guild.get_channel(guild.get_channel("ticketCat"))
    ticketCount = guild.get_ticket_count() + 1

    guild.set_ticket_count(ticketCount)

    

    # Create the ticket channel
    ticketChannel = await interaction.guild.create_text_channel(ticketType + "-" + str(ticketCount), topic="Ticket created by " + interaction.user.display_name, category=catergory)
    # Give the user access to the channel
    await ticketChannel.set_permissions(interaction.user, read_messages=True, send_messages=True, attach_files=True, embed_links=True, add_reactions=True,)
    # Give the support role access to the channel
    await ticketChannel.set_permissions(supportRole, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True)
    # Remove the everyone role from the channel
    await ticketChannel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False, view_channel=False)
    # give the bot access to the channel
    await ticketChannel.set_permissions(bot.user, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True, manage_channels=True)
    # Now send a embed welcoming the user to the channel
    
    await interaction.response.send_message("Ticket is created" + ticketChannel.mention, ephemeral=True, delete_after=15)

    embed = discord.Embed(title="Welcome to your " + ticketType + " ticket",
                          description="Please follow the format below for explaining your issue.", color=0x00a6ff)
    if ticketType == "Support" or ticketType == "Other":
        embed.add_field(name="Format",
                        value="IGN", inline=False)
        embed.add_field(name="",
                        value="Issue", inline=False)
        embed.add_field(
            name="", value="Any screenshots or related information", inline=False)

    elif ticketType == "Joining":
        embed.add_field(name="Format",
                        value="", inline=False)
        embed.add_field(name="IGN",
                        value="", inline=False)
        embed.add_field(name="Timezone",
                        value="", inline=False)
        embed.add_field(name="Why do you want to join",
                        value="", inline=False)
        embed.add_field(name="How will you contribute to the nation",
                        value="", inline=False)
        embed.add_field(name="How active are you", value="", inline=False)
        embed.add_field(name="Do you know anyone in the nation",
                        value="", inline=False)
        embed.add_field(name="Play style", value="", inline=False)
        embed.add_field(name="Previous experience",
                        value="", inline=False)
        embed.add_field(name="What town would you want to join?",
                        value="", inline=False)

    embed.set_footer(
        text="You can upload screenshots or any other related information.")

    await ticketChannel.send(supportRole.mention)
    await ticketChannel.send("A support representative will be with you shortly. Please be patient.")

    logging.info(
        f"Ticket created: {ticketChannel.name} | User: {interaction.user.name}#{interaction.user.discriminator}")

    class MyView(discord.ui.View):
        @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.red, emoji="🔒")
        def __init__(self):
            super().__init__(timeout=None)
        async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
            # Log the ticket
            await ticketLogChannel.send(f"The ticket `{ticketChannel.name}` has been closed by {interaction.user.mention}")
            
            html_content = await generate_discord_log_html(ticketChannel)

            # Write the HTML content to a file
            with open('log.html', 'w') as f:
                f.write(html_content)

            #Send the file to Discord within an Embed
            embed = discord.Embed(title=f"{ticketChannel.name} Logs",  color=0x00FF00)
            embed.add_field(name="How to view" , value="Simply download the file and open it. It will open in your broswer to view.", inline=False)
            embed.footer(text="Limit 200 messages")
            await ticketLogChannel.respond(file=discord.File('log.html'), embed=embed)

            # Delete the file from the bot
            os.remove('log.html')
            # delete the channel
            await ticketChannel.delete()

    
    await ticketChannel.send(f"interaction.user.mention", embed=embed, view=MyView())
    await ticketLogChannel.send(f" The ticket `{ticketChannel.name}` has been created by {interaction.user.mention}")

    logging.info(
        f"Ticket closed: {ticketChannel.name} | User: {interaction.user.name}#{interaction.user.discriminator}")

    # Send a log message

async def setUpJoinTickets():
    # Varbibles 

    # Embed explaing how to create a ticket
    embed = discord.Embed(title="How to join the country",
                          description="You can join the country by clicking the button below", color=0x00a6ff)
    embed.add_field(name=":trophy: Joining",
                    value="Click the button below to create a joining ticket", inline=False)

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label='Join', style=discord.ButtonStyle.grey, emoji="🏆")
        async def joining(self, button: discord.ui.Button, interaction: discord.Interaction):
            await createTicket("Joining", interaction)



    # Setup all servers tickets
    servers = guilds.get_guilds()

    # Loop through all servers
    for server in servers:
        # Get the server
        guild = bot.get_guild(server["guildId"])
        # Get the ticket channel
        print(server["channels"]["ticket"])
        ticketChannel = guild.get_channel(server["channels"]["ticket"])  
        try:
            message = await ticketChannel.fetch_message(server["ticketMsg"])
            await message.edit(embed=embed, view=MyView())
        except:
            message = await ticketChannel.send(embed=embed, view=MyView())
            await message.pin()
            await ticketChannel.last_message.delete()
            server["ticketMsg"] = message.id
            guilds.update_guild(server["guildId"], server)

    # Send a log message
    logging.info("Ticket setup complete")

async def setUpTownTickets():
    # Varbibles 

    # Embed explaing how to apply to make a new town
    embed = discord.Embed(title="How to apply to make a new town",
                            description="You can apply to make a new town by clicking the button below", color=0x00a6ff)
    embed.add_field(name=":trophy: Town",
                    value="Click the button below to create a town application ticket", inline=False)
    
    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        @discord.ui.button(label='Town', style=discord.ButtonStyle.grey, emoji="🏰")
        async def town(self, button: discord.ui.Button, interaction: discord.Interaction):
            await createTicket("Town", interaction)
            


    # Setup all servers tickets
    servers = guilds.get_guilds()

    # Loop through all servers
    for server in servers:
        # Get the server
        guild = bot.get_guild(server["guildId"])
        # Get the ticket channel
        print(server["channels"]["ticket"])
        ticketChannel = guild.get_channel(server["channels"]["ticket"])  
        try:
            message = await ticketChannel.fetch_message(server["ticketMsg"])
            await message.edit(embed=embed, view=MyView())
        except:
            message = await ticketChannel.send(embed=embed, view=MyView())
            await message.pin()
            await ticketChannel.last_message.delete()
            server["ticketMsg"] = message.id
            guilds.update_guild(server["guildId"], server)

    # Send a log message
    logging.info("Ticket setup complete")



@bot.event
async def on_member_join(member):

    displayName = member.display_name
    mention = member.mention
    server = member.guild
    guild = guilds.get_guild(guilds.get_guild_index(server.id))
    welcomechannel = server.get_channel(guild.get_channel("welcome"))
    announcementchannel = server.get_channel(guild.get_channel("announcements"))
    generalchannel = server.get_channel(guild.get_channel("general"))
    ticketchannel = server.get_channel(guild.get_channel("ticket"))
    

    embed = discord.Embed(title="Welcome " + displayName + f"to {server.name}'s Discord Server",
                          description=f"{server.name}'s Discord Server", color=0x00a6ff)
    embed.add_field(name=f"<#{ticketchannel.id}>",
                    value="Go there to join or for support", inline=False)
    embed.add_field(name=f"<#{announcementchannel.id}>",
                    value="Where we will announce stuff.", inline=False)
    embed.add_field(name=f"<#{generalchannel.id}>",
                    value="Here you can chat with everyone", inline=True)
    await welcomechannel.send(mention)
    await welcomechannel.send(embed=embed)
    logging.info(f"User joined: {member.name}#{member.discriminator}")


@bot.command(description="This command pings the bot")
async def ping(ctx):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    await ctx.respond("pong")
    logging.info("pong used by " + ctx.author.display_name)


@bot.command()
@discord.default_permissions(
    administrator=True
)

async def welcome(ctx, member: discord.Member):
    on_member_join(member)
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    await on_member_join(member)
    await ctx.respond("Welcome message sent to " + member.mention, ephemeral=True)


@bot.command(description="This command allows Admins to process users joining the kingdom", aliases=["process"], pass_context=True, brief="process a user for joining a town", usage="process", )
@discord.default_permissions(
    administrator=True
)
async def process(ctx, member: discord.Member):
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    towns = guild.get_towns()
    options = []


    for town in towns:
        options.append(discord.SelectOption(
            label=town["name"], description=town["name"], emoji="🏰"))
        

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.select(placeholder="Admin please select the users town", options=options)
        async def select(self, select: discord.ui.Select, interaction: discord.Interaction):
            # check if user is admin
            if interaction.user.guild_permissions.administrator == False:
                await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
                return
            # get the leaders
            leaders = []
            for town in towns:
                leaders.append(town["leader"])
            

            self.value = select.values[0]
            # check if the user is a leader
            if interaction.user.id in leaders:
                await interaction.response.send_message("You are a leader", ephemeral=True)
                return
            else:
                for town in towns:
                    if town["name"] == self.value:
                        leader = bot.get_user(town["leader"])
                        dm = await leader.create_dm()
                        joinRequest = discord.Embed(title="Join Request", description="Join Request", color=0x00a6ff)
                        joinRequest.add_field(name="User", value=member.mention, inline=False)
                        joinRequest.add_field(name="Town", value=town["name"], inline=False)
                        # explain how to use /accept and /deny
                        joinRequest.add_field(name="How to accept", value="To accept this user use the command `/accept <user>`", inline=False)
                        joinRequest.add_field(name="How to deny", value="To deny this user use the command `/deny <user> <reason>`", inline=False)
                        await dm.send(embed=joinRequest)
                        channel = ctx.channel
                        channel.set_permissions(leader, read_messages=True, send_messages=True, view_channel=True)
                        await channel.send(leader.mention)
                        embed = discord.Embed(title="Join Request", description="Join Request", color=0x00a6ff)
                        embed.add_field(name="User", value=member.mention, inline=False)
                        embed.add_field(name="Town", value=town["name"], inline=False)
                        await channel.send(embed=embed)
                        await interaction.response.send_message("Join request sent to " + leader.mention, ephemeral=True)
                        return
    # send message to the channel but only the user who used the command can see it
    await ctx.respond("Ticket Staff select town user would like to join", view=MyView())


@bot.command(description="This command allows Admins to accept users joining the kingdom", aliases=["accept"], pass_context=True, brief="accept a user for joining a town", usage="accept", )
@discord.default_permissions(
    manage_messages=True
)
async def accept(ctx, member: discord.Member):
    leaders = []
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    towns = guild.get_towns()
    for town in towns:
        leaders.append(town["leader"])
    if ctx.author.id in leaders:
        for town in towns:
            if town["leader"] == ctx.author.id:
                role = guild.get_role(town["role"])
                if role != None:
                    await member.add_roles(role)
                guild.add_new_member(town["name"], member.name, member.id)
                embed = discord.Embed(title="Join Request Accepted", description="Join Request Accepted", color=0x00a6ff)
                embed.add_field(name="User", value=member.mention, inline=False)
                embed.add_field(name="Town", value=town["name"], inline=False)
                embed.add_field(name="Accepted by", value=ctx.author.mention, inline=False)
                await ctx.respond(embed=embed)
                return
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    


                    
                    
        
   


@bot.command(description="This command allows Admins to deny users joining a town", aliases=["deny"], pass_context=True, brief="deny a user for joining a town", usage="deny", )
@discord.default_permissions(
    manage_messages=True
)
async def deny(ctx, member: discord.Member, reason=None):
    leaders = []
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    towns = guild.get_towns()
    for town in towns:
        leaders.append(town["leader"])
    if ctx.author.id in leaders:
        for town in towns:
            if town["leader"] == ctx.author.id:
                embed = discord.Embed(title="Join Request Denied", description="Join Request Denied", color=0x00a6ff)
                embed.add_field(name="User", value=member.mention, inline=False)
                embed.add_field(name="Town", value=town["name"], inline=False)
                embed.add_field(name="Denied by", value=ctx.author.mention, inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)
                await ctx.respond(embed=embed)
                return
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    


@bot.command(desctiption="This command purges messages", aliases=["clear"], pass_context=True, brief="Purges messages", usage="purge", )
@discord.default_permissions(administrator=True)
async def purge(ctx, amount=5):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    amount = int(amount)
    await ctx.channel.purge(limit=amount)
    await ctx.respond("Messages purged", delete_after=5)


# send ticket message
@bot.command(description="This command sets up the ticket system", aliases=["setup"], pass_context=True, brief="Sets up the ticket system", usage="setup")
@discord.default_permissions(administrator=True)
async def ticket(ctx):
    if str(ctx.author.id) == "577985634359050251":
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        await setUpJoinTickets()
    else:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        
        await ctx.respond("Only the bot owner can do that", ephemeral=True)
        return
    
# add a ban command
@bot.command(description="This command bans a user", aliases=["ban"], pass_context=True, brief="Bans a user", usage="ban")
@discord.default_permissions(administrator=True)

async def ban(ctx, member: discord.Member, reason=None):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Banned User: {member.name}#{member.discriminator}, Reason: {reason}")
        await member.ban(reason=reason)
        if reason.lower() == "treason":
            embed = discord.Embed(title="Treason", description="User kicked for treason", color=0x00a6ff)
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Reason", value="This person has been found guilty of Treason", inline=False)
            embed.add_field(name="Banned By", value=ctx.author.mention, inline=False)
            await ctx.respond(embed=embed)
            return
        # fancy embed saying who was banned, reason, and who banned them
        embed = discord.Embed(title="Ban", description="User banned", color=0xff0000)
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Banned by", value=ctx.author.mention, inline=False)
        # set image to the banned users avatar
        embed.set_image(url="https://cdn.discordapp.com/attachments/1091499067428831243/1158169369277382667/7FCA4A69-D4D8-4862-AB3F-685CC7BDB766.jpg?ex=651b44c7&is=6519f347&hm=c9202e9492f08ec39281ff619ee2c793c7ca6b6ece3ee59f68b30f555699ff8a&")
        await ctx.respond(embed=embed)
        
        
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
#kick command with mad fancy embed
@bot.command(description="This command kicks a user", aliases=["kick"], pass_context=True, brief="Kicks a user", usage="kick")
@discord.default_permissions(administrator=True)

async def kick(ctx, member: discord.Member, reason=None):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Kicked User: {member.name}#{member.discriminator}, Reason: {reason}")
        await member.kick(reason=reason)
        # check if reason is Treason and if it is do a fnacy embed saying they were kicked for treason
        if reason == "Treason":
            embed = discord.Embed(title="Treason", description="User kicked for treason", color=0x00a6ff)
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Reason", value="This person has been found guilty of Treason", inline=False)
            embed.add_field(name="Kicked By", value=ctx.author.mention, inline=False)
            await ctx.respond(embed=embed)
            return
        # fancy embed saying who was kicked, reason, and who kicked them
        embed = discord.Embed(title="Kick", description="User kicked", color=0x00a6ff)
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Kicked by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
# report bot issues

@bot.command(description="This command reports a bug", aliases=["reportBug"], pass_context=True, brief="Reports a bug", usage="reportBug")
async def reportbug(ctx, command: str, bug: str):
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))

    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    if str(ctx.guild.id) != "1091499066887770213":
        await ctx.respond("This command can only be used in the Kingdom of Doveria server", ephemeral=True)
        return
    # fancy embed saying who reported the bug and what the bug is
    embed = discord.Embed(title="Bug Report", description=f"{ctx.author.mention} reported a bug", color=0xff2600)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
    embed.add_field(name=command, value=bug, inline=True)
    await ctx.respond("Bug reported", delete_after=5,)
    bugsChannelId = ctx.guild.get_channel(guild.get_channel("bugs"))
    await bugsChannelId.send(embed=embed)



@bot.command(description="This command sets up the bot for the server", aliases=["setup"], pass_context=True, brief="Sets up the bot for the server", usage="setup")
@discord.default_permissions(administrator=True)
async def setup(ctx, welcomechannel: discord.TextChannel, announcementchannel: discord.TextChannel, generalchannel : discord.TextChannel,  ticketchannel: discord.TextChannel, ticketlogchannel: discord.TextChannel, ticketcategory: discord.CategoryChannel, ticketmasterrole: discord.Role):
    if ctx.author.guild_permissions.administrator:
        logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # Add server to json
        """  jsonStuff = agent.add_server_to_json(
            welcomechannel.id, announcementchannel.id, generalchannel.id, ticketchannel.id, ticketlogchannel.id, ticketcategory.id, ticketmasterrole.id,
            ctx.guild.id, ctx.guild.member_count, ctx.guild.name
        ) """
        channels= {
            "welcome": welcomechannel.id,
            "announcements": announcementchannel.id,
            "general": generalchannel.id,
            "ticket": ticketchannel.id,
            "ticketLogs": ticketlogchannel.id,
            "ticketCat": ticketcategory.id
        }
        roles = {
            "ticket": ticketmasterrole.id
        }
        guilds.new(ctx.guild.id, ctx.guild.name, ctx.guild.member_count , channels, roles)
        jsonStuff = "Server Added"

        if jsonStuff == "Server Added":
            # fancy embed saying server was added
            embed = discord.Embed(title="Server Added", description="Server Added", color=0x00a6ff)
            embed.add_field(name="Welcome Channel", value=f"<#{welcomechannel.id}>", inline=False)
            embed.add_field(name="Announcement Channel", value=f"<#{announcementchannel.id}>", inline=False)
            embed.add_field(name="General Channel", value=f"<#{generalchannel.id}>", inline=False)
            embed.add_field(name="Ticket Channel", value=f"<#{ticketchannel.id}>", inline=False)
            embed.add_field(name="Ticket Log Channel", value=f"<#{ticketlogchannel.id}>", inline=False)
            embed.add_field(name="Ticket Category", value=f"<#{ticketcategory.id}>", inline=False)
            embed.add_field(name="Ticket Master Role", value=f"{ticketmasterrole.mention}", inline=False)
            # talk about how to add towns
            embed.add_field(name="How to add towns", value="To add a town use the command `/addtown <town_name> <town_leader> <town_role> <town_channel>`", inline=False)
            # explain that to add town role and town channel you must pay for premium
            embed.add_field(name="Premium", value="To get premium go to https://www.patreon.com/kingdomofdoveria", inline=False)
            # say that yuo need premium to add town role and town channel
            embed.add_field(name="Premium Commands", value="To add a town role use the command `/addtownrole <town_name> <town_role>`", inline=False)
            embed.add_field(name="Premium Commands", value="To add a town channel use the command `/addtownchannel <town_name> <town_channel>`", inline=False)
            embed.add_field(name="Added by", value=ctx.author.mention, inline=False)
            await ctx.respond(embed=embed)
            embed = discord.Embed(title="How to create a ticket",
                          description="To create a ticket click the button based on your ticket needs", color=0x00a6ff)
            embed.add_field(name=":white_check_mark: Support",
                            value="Click the button below to create a support ticket", inline=False)
            embed.add_field(name=":trophy: Joining",
                            value="Click the button below to create a joining ticket", inline=False)
            embed.add_field(name=":man_shrugging: Other",
                            value="Click the button below to create a other ticket", inline=False)

            class MyView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                @discord.ui.button(label='Support', style=discord.ButtonStyle.grey, emoji="✅")
                async def support(self, button: discord.ui.Button, interaction: discord.Interaction):
                    await createTicket("Support", interaction)

                @discord.ui.button(label='Joining', style=discord.ButtonStyle.grey, emoji="🏆")
                async def joining(self, button: discord.ui.Button, interaction: discord.Interaction):
                    await createTicket("Joining", interaction)

                @discord.ui.button(label='Other', style=discord.ButtonStyle.grey, emoji="🤷‍♂️")
                async def other(self, button: discord.ui.Button, interaction: discord.Interaction):
                    await createTicket("Other", interaction)
            ticketMsg = await ticketchannel.send(embed=embed, view=MyView())
            guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
            guild.set_ticket_msg(ticketMsg.id)
            guild.set_ticket_count(0)

            await ticketMsg.pin()
            await ticketchannel.last_message.delete()


        else:
            await ctx.respond(jsonStuff)
            
# Town commands

@bot.command(description="Adds a town to the server", brief="Adds a town", usage="addtown <town_name> <town_leader>")
@discord.default_permissions(administrator=True)
async def addtown(ctx, town_name, town_leader: discord.Member, town_role: discord.Role = None, town_channel: discord.TextChannel = None):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    """ response = agent.add_town_to_json(town_name, town_leader.id, ctx.guild.id, town_role.id if town_role else None, town_channel.id if town_channel else None) """
    guild.add_new_town(town_name, town_leader.id, town_role.id if town_role else None, town_channel.id if town_channel else None)
    response = "Town Added"
    if response == "Town Added":
        # fancy embed saying town was added
        embed = discord.Embed(title="Town Added", description="Town Added", color=0x00a6ff)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Leader Role", value=town_leader.mention, inline=False)
        embed.add_field(name="Role", value=town_role.mention if town_role else "None", inline=False)
        embed.add_field(name="Channel", value=f"<#{town_channel.id}>" if town_channel else "None", inline=False)
        embed.add_field(name="Added by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)

@bot.command(description="Removes a town from the server", brief="Removes a town", usage="removetown <town_name>")
@discord.default_permissions(administrator=True)
async def removetown(ctx, town_name):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    guild.remove_town(town_name)
    response = "Town Removed"
    if response == "Town Removed":
        # fancy embed saying town was removed
        embed = discord.Embed(title="Town Removed", description="Town Removed", color=0x00a6ff)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Removed by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)


@bot.command(description="Updates a town in the server", brief="Updates a town", usage="updatetown <town_name> <town_leader> <town_role> <town_channel>")
@discord.default_permissions(administrator=True)
async def updatetown(ctx, town_name, town_leader: discord.Member, town_role: discord.Role = None, town_channel: discord.TextChannel = None):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    response = "Town Updated"
    if response == "Town Updated":
        # fancy embed saying town was updated
        embed = discord.Embed(title="Town Updated", description="Town Updated", color=0x00a6ff)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Leader Role", value=town_leader.mention, inline=False)
        embed.add_field(name="Role", value=town_role.mention if town_role else "None", inline=False)
        embed.add_field(name="Channel", value=f"<#{town_channel.id}>" if town_channel else "None", inline=False)
        embed.add_field(name="Updated by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)



# add users to towns
@bot.command(description="Adds a user to a town", brief="Adds a user to a town", usage="addusertotown <user> <town_name>")
@discord.default_permissions(administrator=True)
async def addusertotown(ctx, member: discord.Member, town_name):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    guild.add_new_member(town_name, member.name, member.id)
    response = "Member Added"
    if response == "Member Added":
        # fancy embed saying member was added
        embed = discord.Embed(title="Member Added", description="Member Added", color=0x00a6ff)
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Added by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)


# remove users from towns
@bot.command(description="Removes a user from a town", brief="Removes a user from a town", usage="removeuserfromtown <user> <town_name>")
@discord.default_permissions(administrator=True)
async def removeuserfromtown(ctx, member: discord.Member, town_name):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    guild.remove_member(town_name, member.id)
    response = "Member Removed"
    if response == "Member Removed":
        # fancy embed saying member was removed
        embed = discord.Embed(title="Member Removed", description="Member Removed", color=0x00a6ff)
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Removed by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)


async def generate_discord_log_html(channel: discord.TextChannel):
    # Get all messages from the channel
    
@bot.command(description="Adds a role to a town", brief="Adds a role to a town", usage="addtownrole <town_name> <town_role>")
@discord.default_permissions(administrator=True)
async def addtownrole(ctx, town_name, town_role: discord.Role):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    guild.add_role_to_town(town_name, town_role.id)
    response = "Role Added"
    if response == "Role Added":
        # fancy embed saying role was added
        embed = discord.Embed(title="Role Added", description="Role Added", color=0x00a6ff)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Role", value=town_role.mention, inline=False)
        embed.add_field(name="Added by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)

@bot.command(description="Removes a role from a town", brief="Removes a role from a town", usage="removetownrole <town_name> <town_role>")
@discord.default_permissions(administrator=True)
async def removetownrole(ctx, town_name, town_role: discord.Role):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    guild.remove_role_from_town(town_name, town_role.id)
    response = "Role Removed"
    if response == "Role Removed":
        # fancy embed saying role was removed
        embed = discord.Embed(title="Role Removed", description="Role Removed", color=0x00a6ff)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Role", value=town_role.mention, inline=False)
        embed.add_field(name="Removed by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)


@bot.command(description="Adds a channel to a town", brief="Adds a channel to a town", usage="addtownchannel <town_name> <town_channel>")
@discord.default_permissions(administrator=True)
async def addtownchannel(ctx, town_name, town_channel: discord.TextChannel):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    guild.add_channel_to_town(town_name, town_channel.id)
    response = "Channel Added"
    if response == "Channel Added":
        # fancy embed saying channel was added
        embed = discord.Embed(title="Channel Added", description="Channel Added", color=0x00a6ff)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Channel", value=f"<#{town_channel.id}>", inline=False)
        embed.add_field(name="Added by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)
    
@bot.command(description="Removes a channel from a town", brief="Removes a channel from a town", usage="removetownchannel <town_name> <town_channel>")
@discord.default_permissions(administrator=True)
async def removetownchannel(ctx, town_name, town_channel: discord.TextChannel):
    logging.info(f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    guild.remove_channel_from_town(town_name, town_channel.id)
    response = "Channel Removed"
    if response == "Channel Removed":
        # fancy embed saying channel was removed
        embed = discord.Embed(title="Channel Removed", description="Channel Removed", color=0x00a6ff)
        embed.add_field(name="Town", value=town_name, inline=False)
        embed.add_field(name="Channel", value=f"<#{town_channel.id}>", inline=False)
        embed.add_field(name="Removed by", value=ctx.author.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(response)

@bot.command(description="Allows a citizen to self assign a town", brief="Allows a citizen to self assign a town", usage="selfassign <town_name>")
async def selfassign(ctx, town_name):
    # check if the user has the role with the id 1120816529794146387
    citizen = ctx.guild.get_role(1120816529794146387)
    if citizen not in ctx.author.roles:
        await ctx.respond("You must be a citizen to use this command", ephemeral=True)
        return


    guild = guilds.get_guild(guilds.get_guild_index(ctx.guild.id))
    towns = guild.get_towns()
    for town in towns:
        if town["name"] == town_name:
            role = guild.get_role(town["role"])
            if role != None:
                await ctx.author.add_roles(role)
                guild.add_new_member(town["name"], ctx.author.name, ctx.author.id)
                embed = discord.Embed(title="Town Self Assigned", description="Town Self Assigned", color=0x00a6ff)
                embed.add_field(name="User", value=ctx.author.mention, inline=False)
                embed.add_field(name="Town", value=town["name"], inline=False)
                await ctx.respond(embed=embed)
                return
            else:
                await ctx.respond("This town does not have a role", ephemeral=True)
                return
    await ctx.respond("This town does not exist", ephemeral=True)
    return

    # Start building the HTML content
    html_content = '<!DOCTYPE html><html lang="en"> <head> <title>'+ channel.name +' <meta charset="UTF-8" /> <meta name="viewport" content="width=device-width, initial-scale=1.0" /> <style> body { font-family: Arial, sans-serif; background-color: #36393f; color: #fff; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; } .dm-container { background-color: #2f3136; border-radius: 5px; padding: 20px; height: 100%; width: 100%; } .message { margin: 10px 0; display: flex; } .user-avatar { width: 40px; height: 40px; border-radius: 50%; background-color: #7289da; } .message-content { background-color: #40444b; border-radius: 10px; padding: 10px; margin-left: 10px; flex-grow: 1; } .username { font-weight: bold; color: #7289da; margin-right: 5px; } .timestamp { font-size: 12px; color: #999; } .message-text { margin-top: 5px; } </style> </head> <body> <div class="dm-container">'

    async for message in channel.history(limit=200):
        # For each message, format it as a Discord-like chat bubble
        username = message.author.display_name
        content = message.content
        time = message.created_at.strftime("%H:%M")+" UTC"
        avatarURL = message.author.display_avatar.url


        # Format the message as a chat bubble
        message_html = f'<div class="message"> <div class="user-avatar"><img src="{avatarURL}" class="user-avatar" alt="User Avatar" /></div> <div class="message-content"> <span class="username">{username}</span> <span class="timestamp">{time}</span> <div class="message-text"> {content} </div> </div> </div> '

        # Append the message HTML to the overall content
        html_content += message_html

    # Close the HTML body and document
    html_content += '</div> </body> </html>'

    return html_content

        

# Run the bot
bot.run(token)

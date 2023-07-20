import discord  # py-cord
import logging
import json

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


def getFromJson(serverID, index, group=None):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == serverID:
                if group == None:
                    return i[index]
                else:
                    if group == "town":
                        for x in i["towns"]:
                            if x["name"] == index:
                                return x
                    elif group == "roles":
                        return i["roles"][index]
                    elif group == "channels":
                        return i["channels"][index]

        
    
def setToJson(serverID, index, value, group=None):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == serverID:
                if group == None:
                    i[index] = value
                else:
                    if group == "town":
                        for x in i["towns"]:
                            if x["name"] == index:
                                x = value
                    elif group == "roles":
                        i["roles"][index] = value
                    elif group == "channels":
                        i["channels"][index] = value
    with open("server.json", "w") as f:
        json.dump(server, f)    


@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the Kingdom of Doveria"))
    await setUpTickets()
    # log with yellow text
    logging.info("Bot is ready")


@bot.event
async def on_command(ctx):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")


async def createTicket(ticketType, interaction):

    supportRole = interaction.guild.get_role(getFromJson(interaction.guild.id, "ticketMaster", "roles"))
    ticketLogChannel = interaction.guild.get_channel(getFromJson(interaction.guild.id, "ticketLogChannelId", "channels"))
    catergory = interaction.guild.get_channel(getFromJson(interaction.guild.id, "ticketCategory", "channels"))
    ticketCount = getFromJson(interaction.guild.id, "ticketCount") + 1
    setToJson(interaction.guild.id, "ticketCount", ticketCount)
    

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
        embed.add_field(name="How will you contribute to the kingdom",
                        value="", inline=False)
        embed.add_field(name="How active are you", value="", inline=False)
        embed.add_field(name="Do you know anyone in the kingdom",
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
        async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
            # Log the ticket
            await ticketLogChannel.send(f"The ticket `{ticketChannel.name}` has been closed by {interaction.user.mention}")
            # delete the channel
            await ticketChannel.delete()

    
    await ticketChannel.send(embed=embed, view=MyView())
    await ticketLogChannel.send(f" The ticket `{ticketChannel.name}` has been created by {interaction.user.mention}")

    logging.info(
        f"Ticket closed: {ticketChannel.name} | User: {interaction.user.name}#{interaction.user.discriminator}")

    # Send a log message


async def setUpTickets():
    # Varbibles 

    # Embed explaing how to create a ticket
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


    # Setup all servers tickets
    servers = []
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]

    for server in servers:
        ticketChannel = bot.get_channel(server["channels"]["ticketChannelId"])
        guild = bot.get_guild(server["guildId"])
        
        ticketMessage = await ticketChannel.fetch_message(server["channels"]["ticketMsg"])

        # Send the message
        try:
            await ticketMessage.edit(embed=embed, view=MyView())
        except:
            #purge the channel
            await ticketChannel.purge(limit=100)

            new_message = await ticketChannel.send(embed=embed, view=MyView())
            setToJson(guild.id, "ticketMsg", new_message.id, "channels")
            
            

    # Send a log message
    logging.info("Ticket setup complete")


@bot.event
async def on_member_join(member):
    displayName = member.display_name
    mention = member.mention
    welcomeChannel = bot.get_channel(1122027613070831687)

    embed = discord.Embed(title="Welcome " + displayName + " to the Kingdom of Doveria's Discord Server",
                          description="Kingdom of Doveria's Discord Server", color=0x00a6ff)
    embed.add_field(name="<#1125123275832434778>",
                    value="Go there to join or for support", inline=False)
    embed.add_field(name="<#1121744511840813219>",
                    value="Where we will announce stuff.", inline=False)
    embed.add_field(name="<#1091499067428831243>",
                    value="Here you can chat with everyone", inline=True)
    await welcomeChannel.send(mention)
    await welcomeChannel.send(embed=embed)
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


@bot.command(description="This command allows Admins to process users joining the kingdom", aliases=["process"], pass_context=True, brief="process a user for joining a town", usage="process", )
@discord.default_permissions(
    administrator=True
)
async def process(ctx, member: discord.Member):
    channel = bot.get_channel(ctx.channel.id)
    if ctx.author.guild_permissions.administrator == False:
        ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    # make dropdown menu for the following towns, Carrothia, Doveria, and Skycliff
    options = [
        discord.SelectOption(
            label="Carrothia", description="Carrothia", emoji="🏰"),
        discord.SelectOption(
            label="Doveria", description="Doveria", emoji="🏰"),
        discord.SelectOption(
            label="Skycliff", description="Skycliff", emoji="🏰"),
    ]

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.select(placeholder="Admin please select the users town", options=options)
        async def select(self, select: discord.ui.Select, interaction: discord.Interaction):
            # check if user is admin
            if interaction.user.guild_permissions.administrator == False:
                await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
                return
            carrothianLeader = bot.get_user(carrothianLeaderID)
            doveriaLeader = bot.get_user(doverianLeaderID)
            SkycliffLeader = bot.get_user(SkycliffLeaderID)

            self.value = select.values[0]
            if self.value == "Carrothia":
                await carrothianLeader.send(member.mention + " is waiting to be processed to join Carrthia")
                channel = interaction.channel.id
                channel = bot.get_channel(channel)
                # give carrothian leader perms to the channel
                await channel.set_permissions(carrothianLeader, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True)
                await carrothianLeader.send("Please type /accept " + member.mention + " in <#" + str(channel) + ">")
                await carrothianLeader.send("Please type /deny " + member.mention + " in <#" + str(channel) + ">")
                await channel.send(carrothianLeader.mention)
                channel.send(member.mention)
                embed = discord.Embed(title="Welcome " + member.display_name + " to the Kingdom of Doveria",
                                      description="Town: Carrothia", color=0x00a6ff)
                embed.add_field(name="Please wait for a leader to process you",
                                value="You will be notified when you are processed", inline=False)
                await channel.send(embed=embed)
                # delete the message
                await interaction.message.delete()
            elif self.value == "Doveria":
                await doveriaLeader.send(member.mention + " is waiting to be processed to join Doveria")
                channel = interaction.channel.id
                channel = bot.get_channel(channel)
                # give doverian leader perms to the channel
                await channel.set_permissions(doveriaLeader, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True)

                await doveriaLeader.send("Please type /accept " + member.mention + " in <#" + str(channel) + ">")
                await doveriaLeader.send("Please type /deny " + member.mention + " in <#" + str(channel) + ">")
                await channel.send(doveriaLeader.mention)
                await channel.send(member.mention)
                embed = discord.Embed(title="Welcome " + member.display_name + " to the Kingdom of Doveria",
                                      description="Town: Doveria", color=0x00a6ff)
                embed.add_field(name="Please wait for a leader to process you",
                                value="You will be notified when you are processed", inline=False)
                await channel.send(embed=embed)
                # delete the message
                await interaction.message.delete()
            elif self.value == "Skycliff":
                await SkycliffLeader.send(member.mention + " is waiting to be processed to join Skycliff")
                channel = interaction.channel.id
                channel = bot.get_channel(channel)
                # give Skycliff leader perms to the channel
                await channel.set_permissions(SkycliffLeader, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True)
                await SkycliffLeader.send("Please type /accept " + member.mention + " in <#" + str(channel) + ">")
                await SkycliffLeader.send("Please type /deny " + member.mention + " in <#" + str(channel) + ">")
                await channel.send(SkycliffLeader.mention)
                await channel.send(member.mention)
                embed = discord.Embed(title="Welcome " + member.display_name + " to the Kingdom of Doveria",
                                      description="Town: Easmit", color=0x00a6ff)
                embed.add_field(name="Please wait for a leader to process you",
                                value="You will be notified when you are processed", inline=False)
                await channel.send(embed=embed)
                # delete the message
                await interaction.message.delete()
            else:
                await interaction.response.send_message("Please select a town", ephemeral=True)
                return

    # send message to the channel but only the user who used the command can see it
    await ctx.respond("Admin Please select the town for processing.", view=MyView())


@bot.command(description="This command allows Admins to accept users joining the kingdom", aliases=["accept"], pass_context=True, brief="accept a user for joining a town", usage="accept", )
@discord.default_permissions(
    manage_messages=True
)
async def accept(ctx, member: discord.Member):
    # check if user is carrothian leader
    carrothianLeader = bot.get_user(carrothianLeaderID)
    doveriaLeader = bot.get_user(doverianLeaderID)
    SkycliffLeader = bot.get_user(SkycliffLeaderID)
    if ctx.author == carrothianLeader:
        channel = bot.get_channel(ctx.channel.id)
        # give the user the role
        role = discord.utils.get(ctx.guild.roles, name="Citizen of Carrothia")
        await member.add_roles(role)
        role = discord.utils.get(ctx.guild.roles, name="Citizen")
        await member.add_roles(role)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been accepted into Carrothia")
        # send message to the channel
        await channel.send(member.mention + " has been accepted into Carrothia")
    # check if user is doverian leader
    elif ctx.author == doveriaLeader:
        channel = bot.get_channel(ctx.channel.id)
        # give the user the role
        role = discord.utils.get(ctx.guild.roles, name="Citizen of Doveria")
        await member.add_roles(role)
        role = discord.utils.get(ctx.guild.roles, name="Citizen")
        await member.add_roles(role)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been accepted into Doveria")
        # send message to the channel
        await channel.send(member.mention + " has been accepted into Doveria")
    # check if user is Skycliff leader
    elif ctx.author == SkycliffLeader:
        channel = bot.get_channel(ctx.channel.id)
        # give the user the role
        role = discord.utils.get(ctx.guild.roles, name="Citizen of Skycliff")
        await member.add_roles(role)
        role = discord.utils.get(ctx.guild.roles, name="Citizen")
        await member.add_roles(role)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been accepted into Skycliff")
        # send message to the channel
        await channel.send(member.mention + " has been accepted into Skycliff")
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return


@bot.command(description="This command allows Admins to deny users joining a town", aliases=["deny"], pass_context=True, brief="deny a user for joining a town", usage="deny", )
@discord.default_permissions(
    manage_messages=True
)
async def deny(ctx, member: discord.Member, reason=None):
    carrothianLeader = bot.get_user(carrothianLeaderID)
    doveriaLeader = bot.get_user(doverianLeaderID)
    SkycliffLeader = bot.get_user(SkycliffLeaderID)

    # check if user is carrothian leader
    if ctx.author == carrothianLeader:
        channel = bot.get_channel(ctx.channel.id)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been denied into Carrothia")
        # send message to the channel
        await channel.send(member.mention + " has been denied into Carrothia for " + reason)
        await channel.send("Please try joining a different town")
    # check if user is doverian leader
    elif ctx.author == doveriaLeader:
        channel = bot.get_channel(ctx.channel.id)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been denied into Doveria")
        # send message to the channel
        await channel.send(member.mention + " has been denied into Doveria for " + reason)
        await channel.send("Please try joining a different town")
    # check if user is Skycliff leader
    elif ctx.author == SkycliffLeader:
        channel = bot.get_channel(ctx.channel.id)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been denied into Skycliff")
        # send message to the channel
        await channel.send(member.mention + " has been denied into Skycliff for " + reason)
        await channel.send("Please try joining a different town")
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
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        await setUpTickets()
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
# add a ban command
@bot.command(description="This command bans a user", aliases=["ban"], pass_context=True, brief="Bans a user", usage="ban")
@discord.default_permissions(administrator=True)

async def ban(ctx, member: discord.Member, reason=None):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Banned User: {member.name}#{member.discriminator}, Reason: {reason}")
        await member.ban(reason=reason)
        if reason == "Treason":
            embed = discord.Embed(title="Treason", description="User kicked for treason", color=0x00a6ff)
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Reason", value="This person has been found guilty of Treason", inline=False)
            embed.add_field(name="Banned By", value=ctx.author.mention, inline=False)
            await ctx.respond(embed=embed)
            return
        # fancy embed saying who was banned, reason, and who banned them
        embed = discord.Embed(title="Ban", description="User banned", color=0x00a6ff)
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Banned by", value=ctx.author.mention, inline=False)
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
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    # fancy embed saying who reported the bug and what the bug is
    embed = discord.Embed(title="Bug Report", description=f"{ctx.author.mention} reported a bug", color=0xff2600)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
    embed.add_field(name=command, value=bug, inline=True)
    await ctx.respond("Bug reported", delete_after=5,)
    bugsChannelId = bot.get_guild(guildId).get_channel(getFromJson("bugsChannelId"))
    await bugsChannelId.send(embed=embed)



def addServerToJson(welcomeChannel, ticketChannel, ticketLogChannel, ticketCategory, ticketMasterRole, guildId, members, guildName):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                return "Already Set Up"
        servers.append({
            "guildId": guildId,
            "guildName": guildName,
            "members": members,
            "channels": {
                "welcomeChannelId": welcomeChannel,
                "ticketChannelId": ticketChannel,
                "ticketLogChannelId": ticketLogChannel,
                "ticketCategory": ticketCategory,
            },
            "roles": {
                "ticketMaster": ticketMasterRole,
            }
        })
    with open("server.json", "w") as f:
        json.dump(server, f)
    return "Server Added"

#set up bot for server
@bot.command(description="This command sets up the bot for the server", aliases=["setup"], pass_context=True, brief="Sets up the bot for the server", usage="setup")
@discord.default_permissions(administrator=True)
async def setup(ctx, welcomeChannel : discord.channel, ticketChannel : discord.channel, ticketLogChannel : discord.channel, ticketCategory : discord.channel, ticketMasterRole : discord.role):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # add server to json
        jsonStuff = addServerToJson(welcomeChannel.id, ticketChannel.id, ticketLogChannel.id, ticketCategory.id, ticketMasterRole.id, ctx.guild.id, ctx.guild.member_count, ctx.guild.name)
        if jsonStuff == "Already Set Up":
            await ctx.respond("Server is already set up", ephemeral=True)
            return
        #fancy embed saying the bot is set up, and explaining how to add towns
        embed = discord.Embed(title="Bot Setup", description="The bot has been set up", color=0x00a6ff)
        embed.add_field(name="Adding Towns", value="To add towns to the bot use the command /addTown <town name> <town leader role>", inline=False)
        embed.add_field(name="Example", value="/addTown Carrothia @Carrothian Leader", inline=False)
        embed.add_field(name="Removing Towns", value="To remove towns from the bot use the command /removeTown <town name>", inline=False)
        embed.add_field(name="Example", value="/removeTown Carrothia", inline=False)
        # below is premium features make feild to tell users
        embed.add_field(name="Premium Features", value="To get premium features please donate to the bot or send nitro to <@577985634359050251>", inline=False)
        embed.add_field(name="Adding Town Roles", value="To add town roles to the bot use the command /addTownRole <town name> <town role>", inline=False)
        embed.add_field(name="Example", value="/addTownRole Carrothia @Carrothian", inline=False)
        embed.add_field(name="Removing Town Roles", value="To remove town roles from the bot use the command /removeTownRole <town name> <town role>", inline=False)
        embed.add_field(name="Example", value="/removeTownRole Carrothia @Carrothian", inline=False)
        embed.add_field(name="Adding Town Channels", value="To add town channels to the bot use the command /addTownChannel <town name> <town channel>", inline=False)
        embed.add_field(name="Example", value="/addTownChannel Carrothia #carrothia", inline=False)
        embed.add_field(name="Removing Town Channels", value="To remove town channels from the bot use the command /removeTownChannel <town name> <town channel>", inline=False)
        embed.add_field(name="Example", value="/removeTownChannel Carrothia #carrothia", inline=False)

        await ctx.respond(embed=embed)

    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
def addTownToJson(townName, townLeaderRole, guildId, townRole=None, townChannel=None):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        return "Town already exists"
                towns.append({
                    "name": townName,
                    "leader": townLeaderRole,
                    "role": townRole,
                    "channel": townChannel
                })
    with open("server.json", "w") as f:
        json.dump(server, f)
    return "Town Added"

# add town to bot
@bot.command(description="This command adds a town to nation", aliases=["addTown"], pass_context=True, brief="Adds a town to the bot", usage="addTown")
@discord.default_permissions(administrator=True)
async def addtown(ctx, townName, townLeaderRole : discord.role):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # add town to json
        jsonStuff = addTownToJson(townName, townLeaderRole.id, ctx.guild.id)
        if jsonStuff == "Town already exists":
            await ctx.respond("Town already exists", ephemeral=True)
            return
        # fancy embed saying the town was added
        embed = discord.Embed(title="Town Added", description="Town has been added", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Leader Role", value=townLeaderRole.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
# remove town from json
def removeTownFromJson(townName, guildId):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        towns.remove(i)
                        return "Town Removed"
    return "Town does not exist"

    
@bot.command(description="This command removes a town from nation", aliases=["removeTown"], pass_context=True, brief="Removes a town from the bot", usage="removeTown")
@discord.default_permissions(administrator=True)
async def removetown(ctx, townName):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # remove town from json
        jsonStuff = removeTownFromJson(townName, ctx.guild.id)
        if jsonStuff == "Town does not exist":
            await ctx.respond("Town does not exist", ephemeral=True)
            return
        # fancy embed saying the town was removed
        embed = discord.Embed(title="Town Removed", description="Town has been removed", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
#update town in json
def updateTownInJson(townName, townLeaderRole, guildId, townRole=None, townChannel=None):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        i["leader"] = townLeaderRole
                        i["role"] = townRole
                        i["channel"] = townChannel
    with open("server.json", "w") as f:
        json.dump(server, f)
    return "Town Updated"

# update town in bot
@bot.command(description="This command updates a town in nation", aliases=["updateTown"], pass_context=True, brief="Updates a town in the bot", usage="updateTown")
@discord.default_permissions(administrator=True)
async def updatetown(ctx, townName, townLeaderRole : discord.role):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # update town in json
        jsonStuff = updateTownInJson(townName, townLeaderRole.id, ctx.guild.id)
        if jsonStuff == "Town does not exist":
            await ctx.respond("Town does not exist", ephemeral=True)
            return
        # fancy embed saying the town was updated
        embed = discord.Embed(title="Town Updated", description="Town has been updated", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Leader Role", value=townLeaderRole.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    

# add town role to json
def addTownRoleToJson(townName, townRole, guildId):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        townRoles = i["townRoles"]
                        for i in townRoles:
                            if i["townRole"] == townRole:
                                return "Town Role already exists"
                        townRoles.append({
                            "townRole": townRole
                        })
    with open("server.json", "w") as f:
        json.dump(server, f)
    return "Town Role Added"

# add town role to bot
@bot.command(description="This command adds a town role to a town", aliases=["addTownRole"], pass_context=True, brief="Adds a town role to the bot", usage="addTownRole")
@discord.default_permissions(administrator=True)
async def addtownrole(ctx, townName, townRole : discord.role):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # add town role to json
        jsonStuff = addTownRoleToJson(townName, townRole.id, ctx.guild.id)
        if jsonStuff == "Town Role already exists":
            await ctx.respond("Town Role already exists", ephemeral=True)
            return
        # fancy embed saying the town role was added
        embed = discord.Embed(title="Town Role Added", description="Town Role has been added", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Role", value=townRole.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return

# remove town role from json
def removeTownRoleFromJson(townName, townRole, guildId):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        townRoles = i["townRoles"]
                        for i in townRoles:
                            if i["townRole"] == townRole:
                                townRoles.remove(i)
                                return "Town Role Removed"
    return "Town Role does not exist"

# remove town role from bot
@bot.command(description="This command removes a town role from a town", aliases=["removeTownRole"], pass_context=True, brief="Removes a town role from the bot", usage="removeTownRole")
@discord.default_permissions(administrator=True)
async def removetownrole(ctx, townName, townRole : discord.role):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # remove town role from json
        jsonStuff = removeTownRoleFromJson(townName, townRole.id, ctx.guild.id)
        if jsonStuff == "Town Role does not exist":
            await ctx.respond("Town Role does not exist", ephemeral=True)
            return
        # fancy embed saying the town role was removed
        embed = discord.Embed(title="Town Role Removed", description="Town Role has been removed", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Role", value=townRole.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
# update town role in json
def updateTownRoleInJson(townName, townRole, guildId):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        townRoles = i["townRoles"]
                        for i in townRoles:
                            if i["townRole"] == townRole:
                                i["townRole"] = townRole
    with open("server.json", "w") as f:
        json.dump(server, f)
    return "Town Role Updated"

# update town role in bot
@bot.command(description="This command updates a town role in a town", aliases=["updateTownRole"], pass_context=True, brief="Updates a town role in the bot", usage="updateTownRole")
@discord.default_permissions(administrator=True)
async def updatetownrole(ctx, townName, townRole : discord.role):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        # update town role in json
        jsonStuff = updateTownRoleInJson(townName, townRole.id, ctx.guild.id)
        if jsonStuff == "Town Role does not exist":
            await ctx.respond("Town Role does not exist", ephemeral=True)
            return
        # fancy embed saying the town role was updated
        embed = discord.Embed(title="Town Role Updated", description="Town Role has been updated", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Role", value=townRole.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
# all town channel stuff

# add town channel to json
def addTownChannelToJson(townName, townChannel, guildId):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        townChannels = i["townChannels"]
                        for i in townChannels:
                            if i["townChannel"] == townChannel:
                                return "Town Channel already exists"
                        townChannels.append({
                            "townChannel": townChannel
                        })
    with open("server.json", "w") as f:
        json.dump(server, f)
    return "Town Channel Added"

# add town channel to bot
@bot.command(description="This command adds a town channel to a town", aliases=["addTownChannel"], pass_context=True, brief="Adds a town channel to the bot", usage="addTownChannel")
@discord.default_permissions(administrator=True)
async def addtownchannel(ctx, townName, townChannel : discord.channel):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        
        # add town channel to json
        jsonStuff = addTownChannelToJson(townName, townChannel.id, ctx.guild.id)
        if jsonStuff == "Town Channel already exists":
            await ctx.respond("Town Channel already exists", ephemeral=True)
            return
        # fancy embed saying the town channel was added
        embed = discord.Embed(title="Town Channel Added", description="Town Channel has been added", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Channel", value=townChannel.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
# remove town channel from json
def removeTownChannelFromJson(townName, townChannel, guildId):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        townChannels = i["townChannels"]
                        for i in townChannels:
                            if i["townChannel"] == townChannel:
                                townChannels.remove(i)
                                return "Town Channel Removed"
    return "Town Channel does not exist"

# remove town channel from bot
@bot.command(description="This command removes a town channel from a town", aliases=["removeTownChannel"], pass_context=True, brief="Removes a town channel from the bot", usage="removeTownChannel")
@discord.default_permissions(administrator=True)
async def removetownchannel(ctx, townName, townChannel : discord.channel):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")

        # remove town channel from json
        jsonStuff = removeTownChannelFromJson(townName, townChannel.id, ctx.guild.id)
        if jsonStuff == "Town Channel does not exist":
            await ctx.respond("Town Channel does not exist", ephemeral=True)
            return
        # fancy embed saying the town channel was removed
        embed = discord.Embed(title="Town Channel Removed", description="Town Channel has been removed", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Channel", value=townChannel.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    
# update town channel in json
def updateTownChannelInJson(townName, townChannel, guildId):
    with open("server.json", "r") as f:
        server = json.load(f)
        servers = server["servers"]
        for i in servers:
            if i["guildId"] == guildId:
                towns = i["towns"]
                for i in towns:
                    if i["townName"] == townName:
                        townChannels = i["townChannels"]
                        for i in townChannels:
                            if i["townChannel"] == townChannel:
                                i["townChannel"] = townChannel
    with open("server.json", "w") as f:
        json.dump(server, f)
    return "Town Channel Updated"

# update town channel in bot
@bot.command(description="This command updates a town channel in a town", aliases=["updateTownChannel"], pass_context=True, brief="Updates a town channel in the bot", usage="updateTownChannel")
@discord.default_permissions(administrator=True)
async def updatetownchannel(ctx, townName, townChannel : discord.channel):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")

        # update town channel in json
        jsonStuff = updateTownChannelInJson(townName, townChannel.id, ctx.guild.id)
        if jsonStuff == "Town Channel does not exist":
            await ctx.respond("Town Channel does not exist", ephemeral=True)
            return
        # fancy embed saying the town channel was updated
        embed = discord.Embed(title="Town Channel Updated", description="Town Channel has been updated", color=0x00a6ff)
        embed.add_field(name="Town Name", value=townName, inline=False)
        embed.add_field(name="Town Channel", value=townChannel.mention, inline=False)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    




# Run the bot
bot.run(token)

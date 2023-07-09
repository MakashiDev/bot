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


with open("server.json", "r") as f:
    server = json.load(f)
    global guildId, ticketChannelId, ticketLogChannelId, ticketCategory, ticketMsg, carrothianLeaderID, doverianLeaderID, eastmitLeaderID, supportRoleId, carrothianRoleID, doverianRoleID, eastmitRoleID, ticketCount
    guildId = server["guildId"]
    ticketChannelId = server["ticketChannelId"]
    ticketLogChannelId = server["ticketLogChannelId"]
    ticketCategory = server["ticketCategory"]
    ticketMsg = server["ticketMsg"]
    carrothianLeaderID = server["leaders"]["carrothianLeaderID"]
    doverianLeaderID = server["leaders"]["doverianLeaderID"]
    eastmitLeaderID = server["leaders"]["eastmitLeaderID"]
    supportRoleId = server["roles"]["supportRoleId"]
    carrothianRoleID = server["roles"]["carrothianRoleID"]
    doverianRoleID = server["roles"]["doverianRoleID"]
    eastmitRoleID = server["roles"]["eastmitRoleID"]
    ticketCount = server["ticketCount"]


# logging.basicConfig(level=logging.INFO)


@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the Kingdom of Doveria"))
    logging.info("Bot is ready")
    await setUpTickets()


@bot.event
async def on_member_join(member):
    logging.info(f"User joined: {member.name}#{member.discriminator}")


@bot.event
async def on_command(ctx):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")


async def createTicket(ticketType, interaction):

    supportRole = interaction.guild.get_role(supportRoleId)
    ticketLogChannel = interaction.guild.get_channel(ticketLogChannelId)
    catergory = interaction.guild.get_channel(ticketCategory)
    localticketCount = ticketCount + 1
    with open("server.json", "w") as f:
        server["ticketCount"] = localticketCount
        json.dump(server, f)

    # Create the ticket channel
    ticketChannel = await interaction.guild.create_text_channel(ticketType + "-" + str(localticketCount), topic="Ticket created by " + interaction.user.display_name, category=catergory)
    # Give the user access to the channel
    await ticketChannel.set_permissions(interaction.user, read_messages=True, send_messages=True, attach_files=True, embed_links=True, add_reactions=True,)
    # Give the support role access to the channel
    await ticketChannel.set_permissions(supportRole, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True)
    # Remove the everyone role from the channel
    await ticketChannel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False, view_channel=False)
    # give the bot access to the channel
    await ticketChannel.set_permissions(bot.user, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True, manage_channels=True)
    # Now send a embed welcoming the user to the channel

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

    await interaction.response.send_message("Ticket is created" + ticketChannel.mention, ephemeral=True)
    await ticketChannel.send(embed=embed, view=MyView())
    await ticketLogChannel.send(f" The ticket `{ticketChannel.name}` has been created by {interaction.user.mention}")

    logging.info(
        f"Ticket closed: {ticketChannel.name} | User: {interaction.user.name}#{interaction.user.discriminator}")

    # Send a log message


async def setUpTickets():
    # get the channel named tickets in the server
    server = bot.get_guild(guildId)
    ticketChannel = server.get_channel(ticketChannelId)
    ticketMessage = None
    try:
        ticketMessage = await ticketChannel.fetch_message(ticketMsg)
    except:
        print("Ticket message not found")

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
        @discord.ui.button(label='Support', style=discord.ButtonStyle.grey, emoji="✅")
        async def support(self, button: discord.ui.Button, interaction: discord.Interaction):
            await createTicket("Support", interaction)

        @discord.ui.button(label='Joining', style=discord.ButtonStyle.grey, emoji="🏆")
        async def joining(self, button: discord.ui.Button, interaction: discord.Interaction):
            await createTicket("Joining", interaction)

        @discord.ui.button(label='Other', style=discord.ButtonStyle.grey, emoji="🤷‍♂️")
        async def other(self, button: discord.ui.Button, interaction: discord.Interaction):
            await createTicket("Other", interaction)
    # Send the message
    try:
        await ticketMessage.edit(embed=embed, view=MyView())
    except:
        await ticketChannel.send(embed=embed, view=MyView())
        with open('server.json', 'r+') as f:
            data = json.load(f)
            data['ticketMsg'] = ticketMessage.id
            json.dump(data, f)

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
    logging.info(displayName + " joined the server")


@bot.command(description="This command pings the bot")
async def ping(ctx):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    await ctx.send("pong")
    logging.info("pong used by " + ctx.author.display_name)


@bot.command()
async def welcome(ctx, member: discord.Member):
    on_member_join(member)
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")


@bot.command(description="This command allows Admins to process users joining the kingdom", aliases=["process"], pass_context=True, brief="process a user for joining a town", usage="process", )
async def process(ctx, member: discord.Member):
    channel = bot.get_channel(ctx.channel.id)
    if ctx.author.guild_permissions.administrator == False:
        ctx.send("You do not have permission to use this command", ephemeral=True)
        return
    # make dropdown menu for the following towns, Carrothia, Doveria, and Eastmit
    options = [
        discord.SelectOption(
            label="Carrothia", description="Carrothia", emoji="🏰"),
        discord.SelectOption(
            label="Doveria", description="Doveria", emoji="🏰"),
        discord.SelectOption(
            label="Eastmit", description="Eastmit", emoji="🏰"),
    ]

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @discord.ui.select(placeholder="Admin please select the users town", options=options)
        async def select(self, select: discord.ui.Select, interaction: discord.Interaction):
            # check if user is admin
            if interaction.user.guild_permissions.administrator == False:
                await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)
                return
            carrothianLeader = bot.get_user(carrothianLeaderID)
            doveriaLeader = bot.get_user(doverianLeaderID)
            eastmitLeader = bot.get_user(eastmitLeaderID)

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
                await channel.send(member.mention)
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
            elif self.value == "Eastmit":
                await eastmitLeader.send(member.mention + " is waiting to be processed to join Eastmit")
                channel = interaction.channel.id
                channel = bot.get_channel(channel)
                # give eastmit leader perms to the channel
                await channel.set_permissions(eastmitLeader, read_messages=True, send_messages=True, manage_messages=True, view_channel=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, add_reactions=True)
                await eastmitLeader.send("Please type /accept " + member.mention + " in <#" + str(channel) + ">")
                await eastmitLeader.send("Please type /deny " + member.mention + " in <#" + str(channel) + ">")
                await channel.send(eastmitLeader.mention)
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
    await ctx.send("Admin Please select the town for processing.", view=MyView())


@bot.command(description="This command allows Admins to accept users joining the kingdom", aliases=["accept"], pass_context=True, brief="accept a user for joining a town", usage="accept", )
async def accept(ctx, member: discord.Member):
    # check if user is carrothian leader
    carrothianLeader = bot.get_user(carrothianLeaderID)
    doveriaLeader = bot.get_user(doverianLeaderID)
    eastmitLeader = bot.get_user(eastmitLeaderID)
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
    # check if user is eastmit leader
    elif ctx.author == eastmitLeader:
        channel = bot.get_channel(ctx.channel.id)
        # give the user the role
        role = discord.utils.get(ctx.guild.roles, name="Citizen of Eastmit")
        await member.add_roles(role)
        role = discord.utils.get(ctx.guild.roles, name="Citizen")
        await member.add_roles(role)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been accepted into Eastmit")
        # send message to the channel
        await channel.send(member.mention + " has been accepted into Eastmit")
    else:
        await ctx.send("You do not have permission to use this command", ephemeral=True)
        return


@bot.command(description="This command allows Admins to deny users joining a town", aliases=["deny"], pass_context=True, brief="deny a user for joining a town", usage="deny", )
async def deny(ctx, member: discord.Member, reason=None):
    carrothianLeader = bot.get_user(carrothianLeaderID)
    doveriaLeader = bot.get_user(doverianLeaderID)
    eastmitLeader = bot.get_user(eastmitLeaderID)

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
    # check if user is eastmit leader
    elif ctx.author == eastmitLeader:
        channel = bot.get_channel(ctx.channel.id)
        # remove the user from the channel
        await channel.set_permissions(member, read_messages=False, send_messages=False, view_channel=False)
        # send message to the user
        await member.send("You have been denied into Eastmit")
        # send message to the channel
        await channel.send(member.mention + " has been denied into Eastmit for " + reason)
        await channel.send("Please try joining a different town")
    else:
        await ctx.send("You do not have permission to use this command", ephemeral=True)
        return


@bot.command(desctiption="This command purges messages", aliases=["clear"], pass_context=True, brief="Purges messages", usage="purge", )
async def purge(ctx, amount=5):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    amount = int(amount)
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages purged", delete_after=5)


# send ticket message
@bot.command(description="This command sets up the ticket system", aliases=["setup"], pass_context=True, brief="Sets up the ticket system", usage="setup")
async def ticket(ctx):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        await setUpTickets()
    else:
        await ctx.send("You do not have permission to use this command", ephemeral=True)
        return


@bot.command(description="Kicks user due to treson", aliases=["kickTreasoon"], pass_context=True, brief="Kicks user due to treson", usage="kickTreason")
async def kickTreason(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        logging.info(
            f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
        reason = "Treason"

        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked for Treason against the Kingdom of Doveria")
        await member.send(f"You have been kicked from the Kingdom of Doveria for Treason")
    else:
        await ctx.send("You do not have permission to use this command", ephemeral=True)
        return

# Run the bot
bot.run(token)

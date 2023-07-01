import discord  # py-cord


token = ""
with open("token.txt", "r") as f:
    token = f.read()


intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.guilds = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready")
    await setUpTickets()


async def createTicket(ticketType, interaction):
    supportRole = interaction.guild.get_role(1122050028186370068)
    ticketLogChannel = bot.get_channel(1122047542654414888)
    ticketCategory = bot.get_channel(1122053063604195338)
    with open("ticketCount.txt", "r") as f:
        ticketCount = int(f.read())
    ticketCount += 1
    with open("ticketCount.txt", "w") as f:
        f.write(str(ticketCount))

    # Create the ticket channel
    ticketChannel = await interaction.guild.create_text_channel(ticketType + "-" + str(ticketCount), topic="Ticket created by " + interaction.user.display_name, category=ticketCategory)
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
                          description="Please follow the format below for explaing your issue.", color=0x00a6ff)
    if ticketType == "Support":
        embed.add_field(name="Format",
                        value="IGN", inline=False)
        embed.add_field(name="",
                        value="Issue", inline=False)
        embed.add_field(
            name="", value="Any screenshots or related infomation", inline=False)
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
        embed.add_field(name="How did you find out about us",
                        value="", inline=False)

    elif ticketType == "Other":
        embed.add_field(name="Format",
                        value="IGN", inline=False)
        embed.add_field(name="",
                        value="How can we help you", inline=False)

    embed.add_field(name="Our Team will be with you shortly",
                    value="Please be patient", inline=False)

    embed.set_footer(text="Ticket created by " + interaction.user.display_name)

    class MyView(discord.ui.View):
        @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.red, emoji="🔒")
        async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
            # Log the ticket
            await ticketLogChannel.send("Ticket " + ticketChannel.name + " was closed by " + interaction.user.display_name)
            # delete the channel
            await ticketChannel.delete()

    await interaction.response.send_message("Ticket is created" + ticketChannel.mention, ephemeral=True)
    await ticketChannel.send(supportRole.mention)
    await ticketChannel.send(embed=embed, view=MyView())
    await ticketLogChannel.send("Ticket " + ticketChannel.name + " was created by " + interaction.user.display_name)


async def setUpTickets():
    ticketChannel = bot.get_channel(1122028695712956447)
    ticketMessage = await ticketChannel.fetch_message(1122049720253173760)
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
    await ticketMessage.edit(embed=embed, view=MyView())


@bot.event
async def on_member_join(member):
    displayName = member.display_name
    mention = member.mention
    welcomeChannel = bot.get_channel(1122027613070831687)
    embed = discord.Embed(title="Welcome " + displayName + " to the Kingdom of Doveria's Discord Server",
                          description="Kingdom of Doveria's Discord Server", color=0x00a6ff)
    embed.add_field(name="<#1122028695712956447>",
                    value="Go there to join or for support", inline=False)
    embed.add_field(name="<#1121744511840813219>",
                    value="Where we will announce stuff.", inline=False)
    embed.add_field(name="<#1091499067428831243>",
                    value="Here you can chat with everyone", inline=True)
    await welcomeChannel.send(mention)
    await welcomeChannel.send(embed=embed)

    # this decorator makes a slash command


@bot.command(description="This command pings the bot")
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def welcome(ctx, member: discord.Member):

    # check if the user has the admin role
    if ctx.author.guild_permissions.administrator == False:
        ctx.send("You do not have permission to use this command", ephemeral=True)
        return

    mention = member.mention
    member = member.display_name
    welcomeChannel = bot.get_channel(1122027613070831687)
    embed = discord.Embed(title="Welcome " + member + " to the Kingdom of Doveria's Discord Server",
                          description="Kingdom of Doveria's Discord Server", color=0x00a6ff)
    embed.add_field(name="<#1122028695712956447>",
                    value="Go there to join or for support", inline=False)
    embed.add_field(name="<#1121744511840813219>",
                    value="Where we will announce stuff.", inline=False)
    embed.add_field(name="<#1091499067428831243>",
                    value="Here you can chat with everyone", inline=True)
    await welcomeChannel.send(embed=embed)
    await welcomeChannel.send(mention)


@bot.command(desctiption="This command purges messages", aliases=["clear"], pass_context=True, brief="Purges messages", usage="purge", )
async def purge(ctx, amount=5):
    if ctx.author.guild_permissions.administrator == False:
        await ctx.send("You do not have permission to use this command", delete_after=5)
        return
    amount = int(amount)
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages purged", delete_after=5)

print("Bot is running")
print(token)
bot.run(token)

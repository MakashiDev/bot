import discord
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

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
                          description="Please follow the format below for explaining your issue.", color=0x00a6ff)
    if ticketType == "Support":
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
        embed.add_field(name="Age", value="", inline=False)
        embed.add_field(name="Level",
                        value="", inline=False)
        embed.add_field(name="Play style", value="", inline=False)
        embed.add_field(name="Previous experience",
                        value="", inline=False)
        embed.add_field(name="", value="", inline=False)

    embed.set_footer(
        text="You can upload screenshots or any other related information using the paperclip icon below.")

    await ticketChannel.send(embed=embed)
    await ticketChannel.send("A support representative will be with you shortly. Please be patient.")

    logging.info(
        f"Ticket created: {ticketChannel.name} | User: {interaction.user.name}#{interaction.user.discriminator}")


class MyView(discord.ui.View):
    @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.red, emoji="🔒")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        ticketChannel = interaction.channel
        ticketLogChannel = bot.get_channel(1122047542654414888)

        logging.info(
            f"Ticket closed: {ticketChannel.name} | User: {interaction.user.name}#{interaction.user.discriminator}")

        # Delete the ticket channel
        await ticketChannel.delete()
        # Send a log message
        await ticketLogChannel.send(f"The ticket `{ticketChannel.name}` has been closed by {interaction.user.mention}")


async def setUpTickets():
    ticketChannel = bot.get_channel(1125123275832434778)
    ticketMessage = await ticketChannel.fetch_message(1122049720253173760)
    ticketLogChannel = bot.get_channel(1122047542654414888)
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
        await ticketMessage.delete()
        await ticketChannel.send(embed=embed, view=MyView())

    # Send a log message
    logging.info("Ticket setup complete")


@bot.command(description="This command pings the bot")
async def ping(ctx):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    await ctx.send("pong")


@bot.command()
async def welcome(ctx, member: discord.Member):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    welcomeEmbed = discord.Embed(title="Welcome to the server!",
                                 description=f"Welcome {member.mention}! Please read the rules in the <#754137468990330242> channel and assign yourself a role in <#754137752942639944>.", color=0x00a6ff)
    await ctx.send(embed=welcomeEmbed)


@bot.command(description="This command purges messages", aliases=["clear"], pass_context=True, brief="Purges messages", usage="purge")
async def purge(ctx, amount=5):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    amount = int(amount)
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages purged", delete_after=5)


# send ticket message
@bot.command(description="This command sets up the ticket system", aliases=["setup"], pass_context=True, brief="Sets up the ticket system", usage="setup")
async def ticket(ctx):
    logging.info(
        f"User: {ctx.author.name}#{ctx.author.discriminator} | Command: {ctx.command.name}")
    await setUpTickets()

# Run the bot
logging.info("Bot is running")
logging.info(token)
bot.run(token)

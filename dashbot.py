import discord
from discord import app_commands
from discord.ext import commands
import logging
import os

# ----- LOGGING -----
logging.basicConfig(level=logging.INFO)

# ----- CHANNEL IDS -----
DOORDASH_CHANNEL_ID = 1455458487676043324
UBEREATS_CHANNEL_ID = 1455458658174636033

# ----- INTENTS -----
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----- BOT READY -----
@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="DashBot | /vouch for DoorDash & Uber Eats"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")
    print("🚀 DashBot is online!")

# ----- VOUCH COMMAND -----
@bot.tree.command(
    name="vouch",
    description="Submit a rating, comment, and REQUIRED image"
)
@app_commands.describe(
    rating="Rate your experience",
    comment="Your review",
    image="Upload your order image (REQUIRED)"
)
@app_commands.choices(rating=[
    app_commands.Choice(name="⭐ 1", value=1),
    app_commands.Choice(name="⭐⭐ 2", value=2),
    app_commands.Choice(name="⭐⭐⭐ 3", value=3),
    app_commands.Choice(name="⭐⭐⭐⭐ 4", value=4),
    app_commands.Choice(name="⭐⭐⭐⭐⭐ 5", value=5),
])
async def vouch(
    interaction: discord.Interaction,
    rating: int,
    comment: str,
    image: discord.Attachment
):
    # ----- FORCE IMAGE -----
    if not image:
        await interaction.response.send_message(
            "⚠️ You must upload an image of your order.",
            ephemeral=True
        )
        return

    channel = interaction.channel

    # ----- CHANNEL CHECK -----
    if channel.id == DOORDASH_CHANNEL_ID:
        service = "DoorDash"
    elif channel.id == UBEREATS_CHANNEL_ID:
        service = "Uber Eats"
    else:
        await interaction.response.send_message(
            "❌ This command only works in DoorDash or Uber Eats channels.",
            ephemeral=True
        )
        return

    stars = "⭐" * rating

    # ----- CONFIRMATION TO USER -----
    await interaction.response.send_message(
        "✅ Your vouch has been submitted!",
        ephemeral=True
    )

    # ----- EMBED POST -----
    embed = discord.Embed(
        title=f"{service} Order Complete ✅",
        description=(
            f"👤 **User:** {interaction.user.mention}\n"
            f"⭐ **Rating:** {stars}\n"
            f"💬 **Comment:** {comment}"
        ),
        color=0x00FF00
    )
    embed.set_image(url=image.url)
    embed.set_footer(text="DealDash • Verified Order")

    await channel.send(embed=embed)

# ----- RUN BOT (RAILWAY SAFE) -----
bot.run(os.getenv("TOKEN"))

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import urllib.parse

load_dotenv()


my_secret = os.getenv('DISCORD_TOKEN')

#intent = discord.Intents.default()
#intent.members = True
#intent.message_content = True

#client = discord.Client(intents = intent)
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@bot.event
async def on_ready():
  print("We have logged in as {0.user}".format(bot))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"hey {interaction.user.mention}!")

@bot.tree.command(name="invite")
async def getInvite(interaction: discord.Interaction):
  GUILD_ID = os.getenv("SERVER_ID")
  server = bot.get_guild(int(GUILD_ID))

  if server is None:
    await interaction.response.send_message("Error: Server not found.")
    return
  
  invites = []
  for i in range(3):
    invite_msg = await server.text_channels[0].create_invite(max_uses=1)
    invites.append(invite_msg)
  for invite in invites:
    print(invite)

  await interaction.response.send_message(f"{invite_msg.url}")


async def invite_msgs():
  GUILD_ID = os.getenv("SERVER_ID")
  server = bot.get_guild(int(GUILD_ID))

  if server is None:
    return "Error"
  
  invite_msg = await server.text_channels[0].create_invite(max_uses=1)
  return f"this is invite_msg"

@bot.tree.command(name="notice")
async def notice(interaction: discord.Interaction):
  def pages():
    url = "http://beu-bih.ac.in/BEUP/Default.aspx"
    data = requests.get(url)

    return data.text

  page = pages()
  soup = BeautifulSoup(page, "html.parser")

  notices = soup.find_all('div', style='border-bottom:1px dashed #2621C2;')
  

  embed = discord.Embed(
    colour=discord.Colour.dark_grey(),
    description='BEU recent notices',
    title='Notice'
  )

  embed.set_author(name="BEU", url="http://beu-bih.ac.in/BEUP/Default.aspx")
  for notice in notices:
    notice_link = notice.find('a')

    embed.add_field(name=notice_link.text, value=f"[Click](http://beu-bih.ac.in/BEUP/{urllib.parse.quote_plus(notice_link['href'])})", inline=False)

  await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
  bot.run(my_secret)
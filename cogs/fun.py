import sys
sys.path.append('./utility')
import discord, random, tools
from discord.ext import commands

def get_random_color():
    return random.choice([0x4287f5, 0xf54242, 0xf5f242])

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='meme', aliases=['get_meme', 'r/meme'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def get_meme(self, ctx):
        meme = await tools.get_meme()

        embed = discord.Embed(color=get_random_color())
        embed.set_author(name=meme['title'], icon_url="https://media.discordapp.net/attachments/791551341516423168/818890921688170527/OtTAJXEZ_400x400.png")
        embed.set_image(url=meme['img_url'])
        embed.set_footer(text=f"Posted by: {meme['author']}, 👍 {meme['up_votes']} | 💬 {meme['comments']}",
                        icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))
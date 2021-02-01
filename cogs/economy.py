import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import random
import sqlite3

def get_random_color():
    return random.choice([0x4287f5, 0xf54242, 0xf5f242])

def open_account(user: discord.Member):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    if result:
        return
    if not result:
        sql = "INSERT INTO main(member_id, wallet, bank) VALUES(?,?,?)"
        val = (user.id, 500, 0)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

def add_bal(user: discord.Member, amount: int):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET wallet = ? WHERE member_id = ?"
    val = (result[1] + amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

def remove_bal(user: discord.Member, amount: int):
    db = sqlite3.connect('data/bank.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT * from main WHERE member_id = {user.id}")
    result = cursor.fetchone()

    sql = f"UPDATE main SET wallet = ? WHERE member_id = ?"
    val = (result[1] - amount, user.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close() 

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="bal", aliases=['balance'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def balance(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        open_account(member)

        db = sqlite3.connect('data/bank.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE member_id = {member.id}")
        result = cursor.fetchone()

        embed = discord.Embed(color=get_random_color(), timestamp=ctx.message.created_at)
        embed.set_author(name=f"{member.name}'s Balance", icon_url=member.avatar_url)
        embed.add_field(name="Wallet", value=f"{result[1]} <:OP_Coin:805019550445600798>")
        embed.add_field(name="Bank", value=f"{result[2]} <:OP_Coin:805019550445600798>")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(name="beg")
    async def beg(self, ctx):
        possibility = random.randint(1, 5)
        if possibility == 3:
            return await ctx.send(
                "You begged for coins but recieved a 🩴 instead"
            )

        amount = random.randrange(60, 200)

        outcomes = [
            f"You got **{amount}** <:OP_Coin:805019550445600798>",
            f"Batman gave you **{amount}** <:OP_Coin:805019550445600798>",
            f"You begged your mom for **{amount}** <:OP_Coin:805019550445600798>"
        ]

        add_bal(ctx.author, amount)
        await ctx.send(random.choice(outcomes))

    @commands.command(name="dep", aliases=['deposit'])
    @commands.cooldown(1, 3, BucketType.user)
    async def dep(self, ctx, amount):
        db = sqlite3.connect('data/bank.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * from main WHERE member_id = {ctx.author.id}")
        result = cursor.fetchone()

        if result[1] == 0:
            return await ctx.send(
                "You have 0 coins in your wallet :|"
            )
        done = False
        if amount == "all" or amount == "max":
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (result[2] + result[1], ctx.author.id)
            await ctx.send(f"Successfully deposited **{result[1]}** <:OP_Coin:805019550445600798>")
            remove_bal(ctx.author, result[1])  
            done = True
        if not done:
            try:
                amount = int(amount)
            except ValueError:
                return await ctx.send(
                    "Only `integers | max | all` will be excepted as the amount"
                )

            if result[1] < amount:
                return await ctx.send(
                    f"You cannot deposit more than **{result[1]}** <:OP_Coin:805019550445600798>"
                )
            
            sql = "UPDATE main SET bank = ? WHERE member_id = ?"
            val = (result[2] + amount, ctx.author.id)
            await ctx.send(
                f"Successfully deposited **{amount}** <:OP_Coin:805019550445600798>"
            )
            remove_bal(ctx.author, amount)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
            
    
def setup(client):
    client.add_cog(Economy(client))
#Remember source pointbot/bin/activate
#Remember to download discord.py with pip
import os
import discord
import re
import random
import datetime
from discord import app_commands

intents=discord.Intents.default()
intents.message_content=True
memory=[]

class warhammermatch:
	player1=""
	player2=""
	score1=""
	score2=""
	faction1=""
	faction2=""
	wtc1=""
	wtc2=""
	time=""
	match_id=""
	winner="none"
	wtc_diff=0
	def __init__(self, submitter,player1, player2, score1, score2):
		self.match_id=random.randint(1000000,9999999)
		self.submitter=submitter
		self.player1=player1
		self.player2=player2
		self.score1=score1
		self.score2=score2
		self.score1=int(score1)
		self.score2=int(score2)
		self.wtc_diff= min(10,int((abs(self.score1-self.score2)-1)/5)) 
		
		if self.score1==self.score2:
			self.winner="noone, noone wins in war, everyone loses"
		elif self.score1>self.score2:
			self.winner=player1
		else:
			self.winner=player2
		if self.winner == player1:
			self.wtc1= 10+self.wtc_diff
			self.wtc2= 10-self.wtc_diff
		else:
			self.wtc1= 10-self.wtc_diff
			self.wtc2= 10+self.wtc_diff
	def set_factions(self,faction1,faction2):
		self.faction1=faction1
		self.faction2=faction2

	def get_data(self):
		return(self.match_id,self.submitter,self.player1,self.player2,self.score1,self.score2,self.faction1,self.faction2)

	def save_data(self):
		with open("pointbot/memory","a") as permanent_memory:
			permanent_memory.write(str(self.match_id)+","+str(self.submitter)+","+str(self.player1)+","+str(self.score1)+","+str(self.wtc1)+","+str(self.player2)+","+str(self.score2)+","+str(self.wtc2)+","+str(datetime.datetime.now())+"\n")

	def get_winner(self):
		return(self.winner)

	def get_match_id(self):
		return(self.match_id)

class my_client(discord.Client):
	def __init__(self, *, intents:discord.Intents):
		super().__init__(intents=intents)
		self.tree=app_commands.CommandTree(self)
		
	async def setup_hook(self):
		guild_id=622767259466727474
		ks=discord.Object(id=guild_id)
		self.tree.copy_global_to(guild=ks)
		await self.tree.sync(guild=ks)


	def register_match(self,poster,player1,score1,player2,score2):
		if score1 not in range(0,101):
			error = "Player 1 score out of bounds\n"
		if score2 not in range(0,101):
			error += "Player 2 score out of bounds\n"
		
		new_match = warhammermatch(poster,player1, player2, score1, score2)
		print(new_match.get_data())
		new_match.save_data()
		return("And the winner is: "+new_match.get_winner() + "\n" + "your match id is: "+str(new_match.get_match_id()))
			
	def delete_match(self,match_id,user):
		#Open memory file
		#Find correct line
		#Purge that line. Or just add something that marks it as deleted 
		#When i say "delete" i mean "Mark with a #"
		with open("pointbot/memory","r") as permanent_memory_read:
			lines=permanent_memory_read.readlines()
			change_marker=False
			try:
				#Eww
				with open("pointbot/memory","w") as permanent_memory_write:
					for line in lines:
						if re.match(str(match_id)+","+str(user)+".*",line):
							permanent_memory_write.write("#"+line)
							change_marker=True
						else:
							permanent_memory_write.write(line)
				if change_marker is True:
					return("Match deleted")
				else: 
					return("It did not work")
			except Exception as e:
				print(str(e))
				return("It did not work, exception")


	def full_list_matches(self,user,*args):
		#flow control
		avg=False
		limit=False
		for arg in args:
			if arg=="avg":
				avg=True
			elif arg=="limit":
				limit=True
		if limit:
			matchlist=[["player1","score","wtc","player2","score","wtc"]]
		else:
			matchlist=[["id","user","player1","score","wtc","player2","score","wtc","date"]]
		matches_found=False
		
		try: 
			with open("pointbot/memory","r") as permanent_memory_read:
				lines=permanent_memory_read.readlines()
				if len(lines)>0:
					for line in lines:
						if "," in line:
							if "#" not in line and (user==line.split(",")[2] or user==line.split(",")[5]):
								if limit:
									matchlist.append(line.split(",")[2:-1])
								else:
									matchlist.append(line[:-1].split(","))
								matches_found=True
						else:
							print("the file might be wierd?")
				else:
					return("No matches registered")
			if matches_found:
				post = ""
				for x in matchlist: 
					post+="\n"
					for y in x:
						if len(y)> 11:
							y=y[:10]
						post+=y.ljust(11," ")

				if avg:
					return(matchlist[1:])
						
				return("```"+post+"```")
				print(matchlist)
			
			else:
				return("No matches registered")
		except Exception as e:
			print(e)

	def avg(self,user):
		wtc_total=[]
		normal_total=[]
		match_list=self.full_list_matches(user,"avg")
		extra_info=""	
		for match in match_list:
			if match[2]==user:
				print(match[3], match[4])
				normal_total.append(int(match[3]))
				wtc_total.append(int(match[4]))
			elif match[5]==user:
				print(match[6],match[7])
				normal_total.append(int(match[6]))
				wtc_total.append(int(match[7]))
		normal_sum=sum(normal_total)/len(match_list)
		wtc_sum=sum(wtc_total)/len(match_list)
		normal_best=sum(sorted(normal_total)[-5:])/len(normal_total[-5:])	
		wtc_best=sum(sorted(wtc_total)[-5:])/len(wtc_total[-5:])
		embed = discord.Embed(title=f"Scoresheet for {user}")
		embed.add_field(name="average score:",value=normal_sum,inline=True)
		embed.add_field(name="average wtc score:",value=wtc_sum,inline=True)
		embed.add_field(name="",value="",inline=False)
		embed.add_field(name="average of top 5:",value=normal_best,inline=True)
		embed.add_field(name="average of top 5 wtc:", value=wtc_best,inline=True)
		if len(normal_total)<5:
			embed.add_field(name="",value="",inline=False)
			embed.add_field(name="extra info:",value="You havn't played 5 matches, so your top 5 is really the same as your normal average")

		return(embed)



################################################OLD
	
	#When we get a message, do stuff
	async def on_message(self, message):
		#Never, ever answer yourself
		if message.author == self.user:
			return

with open("../disckey") as dt_file:
	dt = "".join(dt_file.readlines())
#	print("".join(dt)) 
intents.message_content=True
client = my_client(intents=intents) 

async def on_ready():
	print(client.guilds)
	print(client.tree.get_commands())
	print("Lets go!")

@client.tree.command(name="help",description="prints helpful tips")
async def test(interaction: discord.Interaction):
	await interaction.response.send_message(f"""
hello {interaction.user.mention}
I am a bot that keeps track of warhammer matches
Arguments are described inside Crocoparenthesis with a hint and a data type separated by a colon
Common commands are: 

/register_match 
Register a match
Syntax: /register_match <player1:mention_user> <score:int> <player2:mention_user> <score:int>
Tip: user third_party_register_match if you want to register a match agains a person outside of this discord server

/third_party_register_match
Syntax: /register_match <player1:mention_user> <score:int> <player2:str> <score:int>
Tip: Dont use this if you play against someone that is present in this discord server

/delete
Delete a match
Syntax: /delete <matchid:int>
Tip: See match ids with /full_list
Tip: You can only delete matches you have registered yourself
Tip: This command is not truly destructive

/full_list
List all matches of a player verbosely 
Syntax: /full_list <player:mention_user>

/list
List all matches of a player
Syntax: /list <player:mention_user>

/avg
Show the scoresheet for a player
Syntax /avg <player:mention_user>
""")

@client.tree.command(name="register_match",description="Register a match, use mentions for players")
async def register(interaction: discord.Interaction, player1: discord.Member, score1: int, player2:discord.Member, score2:int):
	submitter = str(interaction.user) 
	post=client.register_match(interaction.user,player1.name,score1,player2.name,score2)
	
	await interaction.response.send_message(post)

@client.tree.command(name="third_party_register_match",description="Register a match, use mention for memberplayer and string for third party")
async def register(interaction: discord.Interaction, player1: discord.Member, score1: int, player2:str, score2:int):
	submitter = str(interaction.user) 
	post=client.register_match(interaction.user,player1.name,score1,"ext_"+player2,score2)
	
	await interaction.response.send_message(post)

@client.tree.command(description="Deletes a match based on id")
async def delete(interaction: discord.Interaction,match_id:int):
	post=client.delete_match(match_id,interaction.user)

	await interaction.response.send_message(post)

@client.tree.command(description="Mention the user whose matches you want to see")
async def full_list(interaction: discord.Interaction, user:discord.Member):
	print(user)
	post=client.full_list_matches(user.name)

	await interaction.response.send_message(post)

@client.tree.command(description="Mention the user whose matches you want to see")
async def list(interaction: discord.Interaction, user:discord.Member):
	print(user)
	post=client.full_list_matches(user.name,"limit")

	await interaction.response.send_message(post)

@client.tree.command(description="Calculates your average registered scorescore")
async def avg(interaction: discord.Interaction, user:discord.Member):
	post = client.avg(user.name)	
	await interaction.response.send_message(embed=post)



client.run(dt)

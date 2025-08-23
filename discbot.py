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



	def list_matches(self,user):
		matchlist=[["id","user","player1","score","wtc","player2","score","wtc"]]
		matches_found=False

		try: 
			with open("pointbot/memory","r") as permanent_memory_read:
				lines=permanent_memory_read.readlines()
				for line in lines:
					print(line.split(","))
					if "#" not in line and (user==line.split(",")[2] or user==line.split(",")[5]):
						matchlist.append(line[:-1].split(","))
						matches_found=True
			if matches_found:
				post = ""
				for x in matchlist: 
					post+="\n"
					for y in x:
						if len(y)> 11:
							y=y[:10]
						post+=y.ljust(11," ")

				return("```"+post+"```")
				print(matchlist)
			else:
				return("No matches registered")
		except Exception as e:
			print(e)




################################################OLD
	
	#When we get a message, do stuff
	async def on_message(self, message):
		#Never, ever answer yourself
		if message.author == self.user:
			return
		#To be removed, current instances latest 10 registered matches
		elif message.content == 'tell me a story':
			thingstosend=memory[-10:]
			post = ''.join(str(item)+"\n" for item in thingstosend)
			await message.channel.send(post)
		#Help message.
		elif message.content == "!help" or message.content == "Hur fan funkar det här?":
			await message.channel.send("Pointbot är en dum bot, den har några funktioner. Främst så registerar den poäng och normaliserar dem enligt WTC-stil på en skala från 0 till 20 baserat på poängdiff.\n\n\n man kan använda \'!Register ditt_namn poäng motståndar_namn poäng\' för att registrera en match.\n Exempel:\n!Register: Clownen 15 Bananen 23\nEller ännu bättre:\n !Register me 15 @mention 30 - Regga med din egen och någon annans användare för att få ännu bättre spårbarhet i matcher \n\n !list - Lista dina egna matcher \n\n !list @mention - lista någon annans matcher\n\n!delete [int] - ta bort en match du har lagt till\n\n!avg - se ditt snittpoäng\n!avg @mention - se en annan persons snittpoäng\n\n\n")
		
#		elif re.match(r"^!newreg:* [^\s]+ \d+ [^\s+ \d+]",message.content):
#			mess=re.match(r"!newreg:* ([^\s]+) (\d+) ([^\s]+) (\d+)",message.content)
#			score1=int(mess[2])
#			score2=int(mess[4])
#			if len(message.mentions) == 2:
#				player1=str(message.mentions[0])
#				player2=str(message.mentions[1])
#			elif len(message.mentions)==1:
#				player1 = str(message.author)
#				player2 = str(message.mentions[0])
#			else:
#				player1=str(mess[1])
#				player2=str(mess[3])
#			if score1 not in range(0,101):
#				error = "Player 1 score out of bounds\n"
#			if score2 not in range(0,101):
#				error += "Player 2 score out of bounds\n"
#			
#			
#			new_match = warhammermatch(str(message.author),player1, player2, score1, score2)
#			print(new_match.get_data())
#			new_match.save_data()
#			await message.channel.send("And the winner is: "+new_match.get_winner() + "\n" + "your match id is: "+str(new_match.get_match_id()))
#			
#		#Register a match
#		
#		elif re.match(r"^![Rr]egister:* \w+ \d+ [^\s]+ \d+", message.content):
#			mess = re.match(r"^![Rr]egister:* ([^\s]+) (\d+) ([^\s]+) (\d+)",message.content)
#			#If the message has mentions, set the mentioned player as player2 (opponent) and speaker to player1, ugly
#			if message.mentions:
#				player1=(str(message.author),int(mess[2]))
#				player2=(str(message.mentions[0]),int(mess[4]))
#			#If the message doesn't have mentions, take the values from the reg.
#			else:
#				player1 = (mess[1],int(mess[2]))
#				player2 = (mess[3],int(mess[4]))
#			wtc_points= min(10,int((abs(player1[1]-player2[1])-1)/5))
#			#This variable should be somewhere else
#			mem=""
#			#Sanitycheck the scores
#			if player1[1] not in range(0,101):
#				post = "Error: Score out of bounds"
#				print("Error: Score out of bounds")
#			#Why am i doing this twice?
#			elif player2[1] not in range(0,101):
#				post = "Error: Score out of bounds"
#				print("Error: Score out of bounds")
#
#			#Check who wins, build a list with values and an answer
#			elif player1[1] > player2[1]:
#				post = player1[0] + " wins with " + str(player1[1] - player2[1]) + " points" 
#				mem=[player1[0], player1[1], 10+wtc_points, player2[0],player2[1],10-wtc_points]
#			elif player2[1] > player1[1]:
#				post = player2[0] + " wins with " + str(player2[1] - player1[1]) + " points"
#				mem=[player1[0],player1[1], 10-wtc_points, player2[0],player2[1],10+wtc_points]
#			else:
#				post = "its a draw" 
#				mem=[player1[0],player1[1],10,player2[0],player2[1],10]
#			
#			#If the post is sane, post the results to chat
#			if not re.match("^Error.*",post):
#				post+=("\nin WTC terms that is " + str(10+wtc_points) + "-" + str(10-wtc_points) + ", thats nice")
#			
#			#This should be somewhere else. Randomize a number as the ID of a match. Collisions?
#			message_id=random.randint(1000000,9999999)
#			#If we have created a list that we want to remember, remember it and put it in a file.
#			#This should create the file if it doesnt exist. Fix later
#			if len(mem) > 0:
#				memory.append(mem)
#				with open("pointbot/memory", "a") as permanent_memory:
#					#Add date to the match
#					permanent_memory.write(str(message_id)+","+str(message.author) + ","+(''.join(str(item)+"," for item in mem))[:-1]+","+str(datetime.datetime.now())+"\n")
#			await message.channel.send(post+"\n your message id is: "+str(message_id))
#
#		#Delete unwanted matches
#		elif re.match(r"^![dD]elete:* \d+", message.content):
#			#Open memory file
#			#Find correct line
#			#Purge that line. Or just add something that marks it as deleted 
#			message_id=re.match(r"^![dD]elete:* (\d+)",message.content)[1]
#		#When i say "delete" i mean "Mark with a #"
#			with open("pointbot/memory","r") as permanent_memory_read:
#				lines=permanent_memory_read.readlines()
#				change_marker=False
#				try:
#					#Eww
#					with open("pointbot/memory","w") as permanent_memory_write:
#						for line in lines:
#							if re.match(message_id+","+str(message.author)+".*",line):
#								permanent_memory_write.write("#"+line)
#								change_marker=True
#							else:
#								permanent_memory_write.write(line)
#					if change_marker is True:
#						await message.channel.send("Did it work? Who knows?")
#					else: 
#						await message.channel.send("It did not work")
#				except Exception as e:
#					print(str(e))
#					await message.channel.send("It did not work, exception")
#
		#This should not be a separate thing. This should be integrated above. Lists a specified users matches
		elif re.match(r"^![lL]ist.*",message.content):
			matchlist=[["id","user","player1","score","wtc","player2","score","wtc"]]
			matches_found=False
			if len(message.mentions)!=1:
				user = str(message.author)
			else:
				user = str(message.mentions[0])
			
			try: 
				with open("pointbot/memory","r") as permanent_memory_read:
					lines=permanent_memory_read.readlines()
					for line in lines:
						if re.match(r"^\d+,"+user+".*",line):
							matchlist.append(line[:-1].split(","))
							matches_found=True
				if matches_found:
					post = ""
					for x in matchlist: 
						post+="\n"
						for y in x:
							if len(y)> 11:
								y=y[:10]
							post+=y.ljust(11," ")
	
					await message.channel.send("```"+post+"```")
					print(matchlist)
				else:
					await message.channel.send("No matches registered")
			except Exception as e:
				print(e)

		#Fredrik wanted this feature
		elif re.match(r"^[kK]an.*få.*snittet\?*",message.content):
			await message.channel.send("Nej "+message.author.nick)
		#meme?
		elif re.match(r"Kuken",message.content):
			await message.channel.send("Nu gick något åt helvete för "+message.author.nick)
		#Get average score of someone else, if mentioned
		elif re.match("!avg .*",message.content):
			if len(message.mentions)==1:
				with open("pointbot/memory","r") as permanent_memory_read:
					lines = permanent_memory_read.readlines()
					history=[]
					for line in lines:
						if re.match(r"^\d+,"+str(message.mentions[0])+".*",line):
							history.append(int(re.match(r"^\d+,"+str(message.mentions[0])+r",\w+,\d+,(\d+),.*",line)[1]))
					if len(history)>0:
						await message.channel.send(str(message.mentions[0])+" snitt är "+str(sum(history)/len(history)))
					else:
						await message.channel.send(str(message.mentions[0])+" har inte spelat några matcher, jag tänker inte dela med 0")
		#This should be integrated above
		elif message.content == "!avg" or re.match(r"[jJ]ag är snittet", message.content): 
			with open("pointbot/memory","r") as permanent_memory_read:
				lines = permanent_memory_read.readlines()
				history=[]
				for line in lines:
					if re.match(r"^\d+,"+str(message.author)+".*",line):
						history.append(int(re.match(r"^\d+,"+str(message.author)+r",\w+,\d+,(\d+),.*",line)[1]))
				if len(history)>0:
					await message.channel.send("Ditt snitt är "+str(sum(history)/len(history)))
				else:
					await message.channel.send("Du har inte spelat några matcher, jag tänker inte dela med 0")
		#Bobby tables
		elif message.content == "Robert'); DROP TABLE *;--":
				await message.channel.send("Dropping tables....\nOverwriting hard drive.....\ndeleting secret stash of porn...\nall matches are gone!\nhttps://xkcd.com/327/")
				#await message.channel.send(history)
		
with open("../disckey") as dt_file:
	dt = "".join(dt_file.readlines())
#	print("".join(dt)) 
intents.message_content=True
client = my_client(intents=intents) 

async def on_ready():
	print(client.guilds)
	print(client.tree.get_commands())
	print("Lets go!")
@client.tree.command(name="test",description="says hello")
async def test(interaction: discord.Interaction):
	await interaction.response.send_message(f"hello {interaction.user.mention}")

@client.tree.command(name="register_match",description="Register a match, use strings for players")
async def register(interaction: discord.Interaction, player1: discord.Member, score1: int, player2:discord.Member, score2:int):
	submitter = str(interaction.user) 
	post=client.register_match(interaction.user,player1.name,score1,player2.name,score2)
	
	await interaction.response.send_message(post)

@client.tree.command(description="Deletes a match based on id")
async def delete(interaction: discord.Interaction,match_id:int):
	post=client.delete_match(match_id,interaction.user)

	await interaction.response.send_message(post)

@client.tree.command()
async def list(interaction: discord.Interaction, user:discord.Member):
	print(user)
	post=client.list_matches(user.name)

	await interaction.response.send_message(post)

client.run(dt)

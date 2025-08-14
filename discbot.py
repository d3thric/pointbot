

#Remember source pointbot/bin/activate
import os
import discord
import re
import random
import datetime

intents=discord.Intents.default()
memory=[]


class my_client(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return
#        if message.content == 'derp':
#            await message.channel.send('herp')

        elif message.content == 'tell me a story':
            thingstosend=memory[-10:]
            post = ''.join(str(item)+"\n" for item in thingstosend)
            await message.channel.send(post)

        elif message.content == "!help" or message.content == "Hur fan funkar det här?":
            await message.channel.send("Pointbot är en dum bot, den har några funktioner. Främst så registerar den poäng och normaliserar dem enligt WTC-stil på en skala från 0 till 20 baserat på poängdiff.\n\n\n man kan använda \'!Register ditt_namn poäng motståndar_namn poäng\' för att registrera en match.\n Exempel:\n!Register: Clownen 15 Bananen 23\nEller ännu bättre:\n !Register me 15 @mention 30 - Regga med din egen och någon annans användare för att få ännu bättre spårbarhet i matcher \n\n !list - Lista dina egna matcher \n\n !list @mention - lista någon annans matcher\n\n !delete [int] - ta bort en match du har lagt till\n\n!avg - se ditt snittpoäng\n!avg @mention - se en annan persons snittpoäng\n\n\n")

        elif re.match(r"^![Rr]egister:* \w+ \d+ [^\s]+ \d+", message.content):
            mess = re.match(r"^![Rr]egister:* ([^\s]+) (\d+) ([^\s]+) (\d+)",message.content)
            if message.mentions:
                player1=(str(message.author),int(mess[2]))
                player2=(str(message.mentions[0]),int(mess[4]))
            else:
                player1 = (mess[1],int(mess[2]))
                player2 = (mess[3],int(mess[4]))
            wtc_points= min(10,int((abs(player1[1]-player2[1])-1)/5))
            mem=""
            if player1[1] not in range(0,101):
                post = "Error: Score out of bounds"
                print("Error: Score out of bounds")

            elif player2[1] not in range(0,101):
                post = "Error: Score out of bounds"
                print("Error: Score out of bounds")

            elif player1[1] > player2[1]:
                post = player1[0] + " wins with " + str(player1[1] - player2[1]) + " points" 
                mem=[player1[0], player1[1], 10+wtc_points, player2[0],player2[1],10-wtc_points]

            elif player2[1] > player1[1]:
                post = player2[0] + " wins with " + str(player2[1] - player1[1]) + " points"
                mem=[player1[0],player1[1], 10-wtc_points, player2[0],player2[1],10+wtc_points]

            else:
                post = "its a draw" 
                mem=[player1[0],player1[1],10,player2[0],player2[1],10]
                
            if not re.match("^Error.*",post):
                post+=("\nin WTC terms that is " + str(10+wtc_points) + "-" + str(10-wtc_points) + ", thats nice")
            

            message_id=random.randint(1000000,9999999)
            
            if len(mem) > 0:
                memory.append(mem)
                with open("pointbot/memory", "a") as permanent_memory:
                    #Add date to the match
                    permanent_memory.write(str(message_id)+","+str(message.author) + ","+(''.join(str(item)+"," for item in mem))[:-1]+","+str(datetime.datetime.now())+"\n")

            await message.channel.send(post+"\n your message id is: "+str(message_id))
        
        elif re.match(r"^![dD]elete:* \d+", message.content):
            #Open memory file
            #Find correct line
            #Purge that line. Or just add something that marks it as deleted 
            message_id=re.match(r"^![dD]elete:* (\d+)",message.content)[1]

            with open("pointbot/memory","r") as permanent_memory_read:
                lines=permanent_memory_read.readlines()
                change_marker=False
                try:
                    with open("pointbot/memory","w") as permanent_memory_write:
                        for line in lines:
                            if re.match(message_id+","+str(message.author)+".*",line):
                                print("This is where a delete should be done")
                                permanent_memory_write.write("#"+line)
                                change_marker=True
                            else:
                                permanent_memory_write.write(line)
                    if change_marker is True:
                        await message.channel.send("Did it work? Who knows?")
                    else: 
                        await message.channel.send("It did not work")
                except Exception as e:
                    print(str(e))
                    await message.channel.send("It did not work, exception")

        elif re.match(r"^![lL]ist$",message.content):
            matchlist=[["id","user","player1","score","wtc","player2","score","wtc","date"]]
            matches_found=False
            try: 
                with open("pointbot/memory","r") as permanent_memory_read:
                    lines=permanent_memory_read.readlines()
                    for line in lines:
                        if re.match(r"^\d+,"+str(message.author)+".*",line):
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
        
        elif re.match(r"^![lL]ist .*",message.content):
            matchlist=[["id","user","player1","score","wtc","player2","score","wtc"]]
            matches_found=False
            if len(message.mentions)==1:
                try: 
                    with open("pointbot/memory","r") as permanent_memory_read:
                        lines=permanent_memory_read.readlines()
                        for line in lines:
                            if re.match(r"^\d+,"+str(message.mentions[0])+".*",line):
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
    
        elif re.match(r"^[kK]an.*få.*snittet\?*",message.content):
            await message.channel.send("Nej "+message.author.nick)

        elif re.match(r"Kuken",message.content):
            await message.channel.send("Nu gick något åt helvete för "+message.author.nick)
        
        elif re.match("!avg .*",message.content):
            if len(message.mentions)==1:
                with open("pointbot/memory","r") as permanent_memory_read:
                    lines = permanent_memory_read.readlines()
                    history=[]
                    for line in lines:
                        if re.match(r"^\d+,"+str(message.mentions[0])+".*",line):
                            history.append(int(re.match(r"^\d+,"+str(message.mentions[0])+",\w+,\d+,(\d+),.*",line)[1]))
                    if len(history)>0:
                        await message.channel.send(str(message.mentions[0])+" snitt är "+str(sum(history)/len(history)))
                    else:
                        await message.channel.send(str(message.mentions[0])+" har inte spelat några matcher, jag tänker inte dela med 0")

        elif message.content == "!avg" or re.match(r"[jJ]ag är snittet", message.content): 
            with open("pointbot/memory","r") as permanent_memory_read:
                lines = permanent_memory_read.readlines()
                history=[]
                for line in lines:
                    if re.match(r"^\d+,"+str(message.author)+".*",line):
                        history.append(int(re.match(r"^\d+,"+str(message.author)+",\w+,\d+,(\d+),.*",line)[1]))
                if len(history)>0:
                    await message.channel.send("Ditt snitt är "+str(sum(history)/len(history)))
                else:
                    await message.channel.send("Du har inte spelat några matcher, jag tänker inte dela med 0")
        elif message.content == "Robert'); DROP TABLE *;--":
                await message.channel.send("Dropping tables....\nOverwriting hard drive.....\ndeleting secret stash of porn...\nall matches are gone!\nhttps://xkcd.com/327/")
                #await message.channel.send(history)

with open("../disckey") as dt_file:
    dt = "".join(dt_file.readlines())
    print("".join(dt)) 
intents.message_content=True
client = my_client(intents=intents) 
client.run(dt)

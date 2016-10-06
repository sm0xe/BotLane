#!/bin/env python
import math
import json
import discord
import logging
from discord.ext import commands
from os import listdir
from os.path import isfile,join


bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"),description="@BotLane help")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='BotLane.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
data = ""
with open('champs.json') as f:
    for line in f:
        data+=line
data = json.loads(data)
skins=""
with open('skins.json') as f:
    for line in f:
        skins+=line
skins = json.loads(skins)
@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("-----")
    await bot.change_presence(game=discord.Game(name='@BotLane help',url='',type=2))

@bot.event
async def on_message(message):
    if message.content.startswith("mid") or message.content.startswith("Mid"):
        avail = ["top","adc","supp","jng"]
        def check_call(m):
            return m.content.lower() in ["mid","top","jungle","jng","adc","sup","supp"]
        while True:
            call=await bot.wait_for_message(timeout=5.0, check=check_call)
            if call==None:
                break
            elif call.content.lower()=="top":
                avail.remove("top")
            elif call.content.lower()=="mid":
                avail.remove("mid")
            elif call.content.lower()=="adc":
                avail.remove("adc")
            elif call.content.lower()=="supp" or call.lower=="sup":
                avail.remove("supp")
            elif call.content.lower() in ["jng","jungle"]:
                avail.remove("jng")
        await bot.send_message(message.channel,avail[0])
    await bot.process_commands(message)

@bot.command()
async def fire_shots():
    await bot.say(discord.User(id="233159074705833984").mention+" \latex")
@bot.command(pass_context=True,description="Get champion info")
async def info(ctx,champ: str,char: str=None):
    if char.lower() == "capitalism": char="$"
    if char.lower() == "communism": char="☭"
    member = str(ctx.message.author)[:-5]
    if champ.title() not in data['data']:
        await bot.say("Champion \""+champ.title()+"\" not found")
        return
    if 'info' not in data['data'][champ.title()]:
        await bot.say("Champion \""+champ.title()+"\" has no info")
        return
    champ_name = data['data'][champ.title()]['name']+", "+data['data'][champ.title()]['title']
    champ_info = data['data'][champ.title()]['info']
    m="```"+champ_name+"\n"
    m+=format("","-<"+str(len(champ_name)))+"\n"
    if char==None:
        m+="Att. power: "+format("","=<"+str(champ_info['attack']))+"\n"
        m+="Def. power: "+format("","=<"+str(champ_info['defense']))+"\n"
        m+="Abl. power: "+format("","=<"+str(champ_info['magic']))+"\n"
        m+="Difficulty: "+format("","=<"+str(champ_info['difficulty']))+"```"
    elif char!="num":
        if char=="8=D" or char=="dick":
            atk = champ_info['attack']
            df = champ_info['defense']
            mgc = champ_info['magic']
            dif = champ_info['difficulty']
            if atk==1:
                m+="Att. power: 8\n"
            else:
                m+="Att. power: 8"+format("","=<"+str(atk-2))+"D\n"
            if df==1:
                m+="Def. power: 8\n"
            else:
                m+="Def. power: 8"+format("","=<"+str(df-2))+"D\n"
            if mgc==1:
                m+="Abl. power: 8\n"
            else:
                m+="Abl. power: 8"+format("","=<"+str(mgc-2))+"D\n"
            if dif==1:
                m+="Difficulty: 8\n"
            else:
                m+="Difficulty: 8"+format("","=<"+str(dif-2))+"D```"
        elif len(char)==1:
            m+="Att. power: "+format("",char+"<"+str(champ_info['attack']))+"\n"
            m+="Def. power: "+format("",char+"<"+str(champ_info['defense']))+"\n"
            m+="Abl. power: "+format("",char+"<"+str(champ_info['magic']))+"\n"
            m+="Difficulty: "+format("",char+"<"+str(champ_info['difficulty']))+"```"
        else:
            m+="Att. power: "+format("","=<"+str(champ_info['attack']))+"\n"
            m+="Def. power: "+format("","=<"+str(champ_info['defense']))+"\n"
            m+="Abl. power: "+format("","=<"+str(champ_info['magic']))+"\n"
            m+="Difficulty: "+format("","=<"+str(champ_info['difficulty']))+"```"
    else:
        m+="Att. power: "+str(champ_info['attack'])+"\n"
        m+="Def. power: "+str(champ_info['defense'])+"\n"
        m+="Abl. power: "+str(champ_info['magic'])+"\n"
        m+="Difficulty: "+str(champ_info['difficulty'])+"```"
    print("{}: {}'s info".format(member,champ.title()))
    await bot.say(m)

@bot.command(pass_context=True,description="Get champion stats")
async def stats(ctx,champ: str):
    member = str(ctx.message.author)[:-5]
    if champ.title() not in data['data']:
        await bot.say("Champion \""+champ.title()+"\" not found")
        return
    if 'stats' not in data['data'][champ.title()]:
        await bot.say("Champion \""+champ.title()+"\" has no stats")
        return
    champ_name = data['data'][champ.title()]['name']+", "+data['data'][champ.title()]['title']
    champ_stats = data['data'][champ.title()]['stats']
    m="```"+champ_name+"\n"
    m+=format("","-<"+str(len(champ_name)))+"\n"
    m+="Health: "+str(champ_stats['hp'])+" (+"+str(champ_stats['hpperlevel'])+")\n"
    m+="Health Regen: "+str(champ_stats['hpregen'])+" (+"+str(champ_stats['hpregenperlevel'])+")\n"
    m+="Mana: "+str(champ_stats['mp'])+" (+"+str(champ_stats['mpregenperlevel'])+")\n"
    m+="Mana Regen: "+str(champ_stats['mpregen'])+" (+"+str(champ_stats['mpregenperlevel'])+")\n"
    m+="Magic Resist.: "+str(champ_stats['spellblock'])+" (+"+str(champ_stats['spellblockperlevel'])+")\n"
    m+="Ranged: "+str(champ_stats['attackrange'])+"\n"
    m+="Attack Damage: "+str(champ_stats['attackdamage'])+" (+"+str(champ_stats['attackdamageperlevel'])+")\n"
    m+="Armor: "+str(champ_stats['armor'])+" (+"+str(champ_stats['armorperlevel'])+")\n"
    m+="Move. Speed: "+str(champ_stats['movespeed'])+"```"
    print("{}: {}'s stats".format(member,champ.title()))
    await bot.say(m)
@bot.command(pass_context=True,description="Get champion icon")
async def icon(ctx,champ: str,n: int=0):
    member = str(ctx.message.author)[:-5]
    path = get_image_path(champ,"icon",0)
    if path==None:
        await bot.say("{} does not have an icon".format(champ.title()))
    else:
        print("{}: {}'s icon".format(member,champ.title()))
        await bot.send_file(ctx.message.channel,path)

@bot.command(pass_context=True,description="Get champion splash image by number")
async def splash(ctx,champ: str,n: str="0"):
    member = str(ctx.message.author)[:-5]
    if n.isdigit():
        path = get_image_path(champ,"splash",n)
        if path==None:
            await bot.say("{} does not have a splash #{}".format(champ.title(),n))
        else:
            print("{}: {}'s splash #{}".format(member,champ.title(),n))
            await bot.send_file(ctx.message.channel,path)
    else:
        path = get_image_path_alias(champ,n)
        if not n.lower() in skins[c_format(champ)]:
            await bot.say("{} does not have a splash {}".format(champ.title(),n.title()))
        else:
            print("{}: {}'s splash {}".format(member,champ.title(),n.title()))
            await bot.send_file(ctx.message.channel,path)
"""
@bot.command(pass_context=True,description="Get champion splash image by name")
async def splash(ctx,champ: str,n: str="vanilla"):
    path = get_image_path_alias(champ,n)
    if not str in skins[c_format(champ)]:
        await bot.say("{} does not have a splash {}".format(champ.title(),n))
    else:
        print("{}: {}'s splash {}".format(member,champ.title(),n))
        await bot.send_file(ctx.message.channel,path)
"""
@bot.command(pass_context=True,description="Get champion roles")
async def role(ctx,champ: str):
    member = str(ctx.message.author)[:-5]
    if c_format(champ) not in data['data']:
        await bot.say("Champion \""+champ.title()+"\" not found")
        return
    if 'tags' not in data['data'][c_format(champ)]:
        await bot.say("Champion \""+champ.title()+"\" has no roles")
        return
    champ_name = data['data'][c_format(champ)]['name']+", "+data['data'][c_format(champ)]['title']
    m=champ_name+"\nPrimary: "+data['data'][c_format(champ)]['tags'][0]
    if len(data['data'][c_format(champ)]['tags'])>1:
        m+="\nSecondary: "+data['data'][c_format(champ)]['tags'][1]
    print("{}: {}'s role".format(member,champ.title()))
    await bot.say(m)
def c_format(champ):
    return champ.title().replace(" ","").replace("'","")
"""
def get_image_url(champ):
    champ = c_format(champ)
    if champ in images:
        return images[champ]
    else:
        return "None"
def download_champ(champ):
    url = get_image_url(champ)
    if url =="None": return None
    champ=c_format(champ)
    urllib.request.urlretrieve(url,join(champ_dir,champ+".png"))
    print("Downloaded {}".format(champ))
    return join(champ_dir,champ+".png")
"""
def get_image_path_alias(champ,alias):
    champ_dir="/home/gussefant/.wine32/drive_c/Riot Games/League of Legends/RADS/projects/lol_air_client/releases"
    for f in listdir(champ_dir):
        champ_dir = join(champ_dir,f)
    champ_dir = join(champ_dir,"deploy/assets/images/champions")
    file = c_format(champ)
    file+="_Splash_"+str(skins[c_format(champ)][alias.lower()])+".jpg"
    return join(champ_dir,file)

def get_image_path(champ, t, n):
    champ_dir="/home/gussefant/.wine32/drive_c/Riot Games/League of Legends/RADS/projects/lol_air_client/releases"
    for f in listdir(champ_dir):
        champ_dir = join(champ_dir,f)
    champ_dir = join(champ_dir,"deploy/assets/images/champions")
    file = c_format(champ)
    if t=="icon":
        file+="_Square_0.png"
    elif t=="splash": file+="_Splash_"+str(n)+".jpg"
    for f in listdir(champ_dir):
        if isfile(join(champ_dir,f)) and f==file:
                return join(champ_dir,f)
    return None
if __name__ == "__main__":
    bot.run('MjMzMzI5NzI3ODM2NzgyNTkz.Ctb5PA.XROr0CH-e31vX1PxXKS8gNOphXM')
    bot.close()

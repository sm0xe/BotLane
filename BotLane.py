#!/bin/env python
import math
import json
import discord
import logging
from discord.ext import commands
from os import listdir
from os.path import isfile,join

global bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"),description="@BotLane help")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='BotLane.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
aliases={
        "hotvixen":"Ahri",
        "satan":"Teemo"
        }
data=skins=viables=""
def load_json():
    global data,skins,viables
    data=skins=viables=""
    with open('champs.json') as f:
        for line in f:
            data+=line
    data = json.loads(data)
    with open('skins.json') as f:
        for line in f:
            skins+=line
    skins = json.loads(skins)
    with open('viable.json') as f:
        for line in f:
            viables+=line
    viables = json.loads(viables)
@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("-----")
    await bot.change_presence(game=discord.Game(name='@BotLane help',url='',type=2))
@bot.event
async def on_message(message):
    """
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
        """
    await bot.process_commands(message)
@bot.command(pass_context=True,description="Refresh JSON")
async def refresh(ctx):
    load_json()
    await bot.say("JSON refreshed")

def role_alias(role):
    if role.lower() in {"jungle","jng","jgl"}: return "jungle"
    elif role.lower() in {"mid","middle"}: return "mid"
    elif role.lower() in {"supp","support"}: return "supp"
    elif role.lower() in {"top","top lane"}: return "top"
    elif role.lower() in {"adc","carry"}: return "adc"
    else: return role
@bot.command(pass_context=True,description="Get champion info")
async def viable(ctx,role: str):
    role = role_alias(role)
    if role in viables:
        m = ""
        for c in viables[role]:
            m+=c+" - "+str(viables[role][c])+"/10\n"
        await bot.say(m)
        return
    elif c_format(role) in skins:
        roles = []
        for r in viables:
            for c in viables[r]:
                if c.lower()==role.lower():
                    roles.append(r.title())
        if len(roles)==0:
            await bot.say("No viable positions for {}".format(role))
        else: await bot.say("\n".join(r for r in roles))
        return
    else:
        await bot.say("No viable champions for {}".format(role))
@bot.command(pass_context=True,description="Get champion info")
async def info(ctx,champ: str,char: str=""):
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
async def stats(ctx,champ: str,filters: str=""):
    filters = filters.split(",")
    filters = list(map(str.lower,filters))
    filters = [ x.replace("health","hp") for x in filters]
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
    if filters[0]=='' or "hp" in filters:
        m+="Health: "+str(champ_stats['hp'])+" (+"+str(champ_stats['hpperlevel'])+")\n"
    if filters[0]=='' or "hpregen" in filters:
        m+="Health Regen: "+str(champ_stats['hpregen'])+" (+"+str(champ_stats['hpregenperlevel'])+")\n"
    if filters[0]=='' or "mana" in filters:
        m+="Mana: "+str(champ_stats['mp'])+" (+"+str(champ_stats['mpregenperlevel'])+")\n"
    if filters[0]=='' or "manaregen" in filters:
        m+="Mana Regen: "+str(champ_stats['mpregen'])+" (+"+str(champ_stats['mpregenperlevel'])+")\n"
    if filters[0]=='' or "resist" in filters:
        m+="Magic Resist.: "+str(champ_stats['spellblock'])+" (+"+str(champ_stats['spellblockperlevel'])+")\n"
    if filters[0]=='' or "ranged" in filters:
        m+="Ranged: "+str(champ_stats['attackrange'])+"\n"
    if filters[0]=='' or "damage" in filters:
        m+="Attack Damage: "+str(champ_stats['attackdamage'])+" (+"+str(champ_stats['attackdamageperlevel'])+")\n"
    if filters[0]=='' or "armor" in filters:
        m+="Armor: "+str(champ_stats['armor'])+" (+"+str(champ_stats['armorperlevel'])+")\n"
    if filters[0]=='' or "speed" in filters:
        m+="Move. Speed: "+str(champ_stats['movespeed'])
    m+="```"
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
        if not n.lower() in skins[c_format(champ)]:
            await bot.say("{} does not have a splash \"{}\"".format(champ.title(),n.title()))
        else:
            path = get_image_path_alias(champ,n)
            print("{}: {}'s splash {}".format(member,champ.title(),n.title()))
            await bot.send_file(ctx.message.channel,path)

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
    if champ.lower() in aliases:
        return aliases[champ]
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
    load_json()
    bot.run('MjMzMzI5NzI3ODM2NzgyNTkz.Ctb5PA.XROr0CH-e31vX1PxXKS8gNOphXM')
    bot.close()

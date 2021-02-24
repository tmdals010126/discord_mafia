import asyncio,discord,os,random,time
from discord.ext import commands

token_path = os.path.dirname(os.path.abspath(__file__))+"/token.txt"
t = open(token_path,"r",encoding="utf-8")
token = t.read().split()[0]
print("Token_key : ",token)

game = discord.Game("미완성입니다. 21-02-23 다시개발시작")
#$도움말
bot = commands.Bot(command_prefix="%",status=discord.Status.online,activity=game,help_command=None)
help_txt = """
마피아 봇 명령어 : 
`%도움말 (or %help)` - 명령어를 보여줍니다.
`%게임시작` - 마피아 게임을 시작합니다.
`%게임중지` - 마피아 게임을 중지합니다.

게임 최소인원 4명
필수직업 : 마피아, 경찰, 의사, 마피아 팀
6명 이상일때 마피아가 2명이 됩니다.
9명 이상일때 교주가 생깁니다.

`마피아 팀 : 마피아, 스파이, 도둑, 과학자, 마담`
`시민 팀 : 의사, 경찰, 사립탐정, 군인, 테러리스트, 도굴꾼, 영매, 정치인, 건달, 기자, 성직자, 연인`
`교주 팀 : 교주`
"""

"""
ctx.author.voice.channel.connect()  음성연결
ctx.author.voice.channel.members    음성채널에 있는 사람
await mute_user(ctx,person_job[i][0])   마이크끄기
"""

"""
마피아 팀
마피아 2
스파이 1
도둑 1
과학자 1
마담 1


시민 팀
의사 1
경찰 1
사립탐정 1
군인 1
테러리스트 1
도굴꾼 1
영매 1
정치인 1
건달 1
기자 1
성직자 1
연인 2


교주팀
교주 1
"""


job_list_mafia = ["스파이","도둑","과학자","마담"]
job_list_citizen_2 = ["사립탐정","군인","테러리스트","도굴꾼","영매","정치인","건달","기자","성직자","연인"]
job_list_citizen_1 = ["사립탐정","군인","테러리스트","도굴꾼","영매","정치인","건달","기자","성직자"]

@bot.event
async def on_ready():
    print("마피아봇 시작")

@bot.command()
async def 도움말(ctx):
    await ctx.send(help_txt)

@bot.command()
async def help(ctx):
    await ctx.send(help_txt)

@bot.command()
async def send_dm(ctx,user_name : discord.Member ,txt):
    channel = await user_name.create_dm()
    await channel.send(content="당신의 직업은 " + txt + "입니다.")

@bot.command()
async def 뮤트올(ctx):
    for i in ctx.author.voice.channel.members:
        await mute_user(ctx,i)

@bot.command()
async def 언뮤트(ctx):
    for i in ctx.author.voice.channel.members:
        await unmute_user(ctx,i)
        
@bot.command()
async def mute_user(ctx,user_name : discord.Member):
    await user_name.add_roles(discord.utils.get(ctx.guild.roles, name="죽은자"))

@bot.command()
async def unmute_user(ctx,user_name : discord.Member):
    await user_name.remove_roles(discord.utils.get(ctx.guild.roles, name="죽은자"))

#@bot.command()
#async def mafia_ablity(ctx,user_list,mafia_1,mafia_2):
    


#판결함수 마지막 찬반투표
@bot.command()
async def Judgment(ctx,user_name,user_list):
    await ctx.send("`" + str(user_name) + "`님의 최후의 변론")
    user_list.remove(user_name)
    for i in range(len(user_list)):
        await mute_user(ctx,user_list[i])
    talktime = 10
    text = await ctx.send("최후의 변론 시간이 `" + str(talktime) + "/" + str(10) + "초` 남았습니다")
    while(True):
        if(talktime <= 0):
            await text.edit(content="최후의 변론 시간이 다 되었습니다.")
            break
        else:
            await text.edit(content="최후의 변론 시간이 `" + str(talktime) + "/" + str(10) + "초` 남았습니다")
            await asyncio.sleep(1)
        if(talktime < 1):
            talktime = 0
        else:
            talktime -= 1
    agreement = await ctx.send("`찬성`")
    await agreement.add_reaction(emoji="🗳️")
    Opposition = await ctx.send("`반대`")
    await Opposition.add_reaction(emoji="🗳️")
    for i in range(len(user_list)):
        await unmute_user(ctx,user_list[i])
    talktime = 10
    text = await ctx.send("찬반투표 시간이 `" + str(talktime) + "/" + str(10) + "초` 남았습니다")
    while(True):
        if(talktime <= 0):
            await text.edit(content="찬반투표 시간이 다 되었습니다.")
            break
        else:
            await text.edit(content="찬반투표 시간이 `" + str(talktime) + "/" + str(10) + "초` 남았습니다")
            await asyncio.sleep(1)
        if(talktime < 1):
            talktime = 0
        else:
            talktime -= 1
    agreement_message =  await ctx.fetch_message(agreement.id)
    Opposition_message = await ctx.fetch_message(Opposition.id)
    agreement_emoji = discord.utils.get(agreement_message.reactions, emoji="🗳️")
    Opposition_emoji = discord.utils.get(Opposition_message.reactions, emoji="🗳️")
    if(agreement_emoji.count > Opposition_emoji.count):
        return "die"
    else:
        return "alive"

#투표함수
@bot.command()
async def vote(ctx, user_list):
    text = []
    for i in range(len(user_list)):
        text.append(await ctx.send("`" + str(user_list[i]) + "`"))
        await text[i].add_reaction(emoji="🗳️")
    await asyncio.sleep(20)
    voted = []
    for i in range(len(text)):
        message = await ctx.fetch_message(text[i].id)
        emoji = discord.utils.get(message.reactions, emoji="🗳️")
        voted.append(emoji.count)
    if(voted.count(max(voted)) == 1):
        return user_list[voted.index(max(voted))]
    else:
        return "None"



#대화시간함수
async def talktimeset(ctx):
    talktime = 90
    default_time = 6
    text = await ctx.send("낮 시간이 `" + str(talktime) + "/" + str(default_time*15) + "초` 남았습니다")
    await text.add_reaction(emoji="➕")
    await text.add_reaction(emoji="➖")
    count_p = 1
    count_m = 1
    while(True):
        message = await ctx.fetch_message(text.id)
        plus = discord.utils.get(message.reactions, emoji="➕")
        minus = discord.utils.get(message.reactions, emoji="➖")
        plus_count = plus.count - count_p
        if(plus_count < 0):
            plus_count = 0
        minus_count = minus.count - count_m
        if(minus_count < 0):
            minus_count = 0
        if(talktime <= 0):
            await text.edit(content="낮 시간이 다 되었습니다.")
            break
        else:
            await text.edit(content="낮 시간이 `" + str(talktime) + "/" + str(default_time*15) + "초` 남았습니다")
            await asyncio.sleep(1)
        if(talktime < 1):
            talktime = 0
        else:
            talktime -= 1
        for i in range(plus_count):
            await ctx.send("낮 시간이 연장되었습니다.")
            talktime += plus_count*15
            default_time += plus_count
            if(talktime < 1):
                talktime = 0
            if(default_time<1):
                default_time = 0
        for i in range(minus_count):
            await ctx.send("낮 시간이 단축되었습니다.")
            talktime -= minus_count*15
            default_time -= minus_count
            if(talktime < 1):
                talktime = 0
            if(default_time<1):
                default_time = 0
        count_m = minus.count
        count_p = plus.count
"""
@bot.command()
async def nighttimeset(ctx):
    nighttime = 30
    text = await ctx.send("밤 시간이 `" + str(nighttime) + "/" + str(30) + "초` 남았습니다")
    while(True):
        if(nighttime <= 0):
            await text.edit(content="밤 시간이 다 되었습니다.")
            break
        else:
            await text.edit(content="밤 시간이 `" + str(nighttime) + "/" + str(30) + "초` 남았습니다")
            await asyncio.sleep(1)
        if(nighttime < 1):
            nighttime = 0
        else:
            nighttime -= 1
"""

@bot.command()
async def 게임시작(ctx):
    person_num = len(ctx.author.voice.channel.members)
    print(ctx.author.voice.channel.members)
    job_list = ["마피아","경찰","의사"]
    job_list.append(random.choice(job_list_mafia))
    if(person_num >= 9):
        job_list.append("교주")
    if(person_num >= 6):
        job_list.append("마피아")
    if(person_num - len(job_list) == 1):
        job_list.append(random.choice(job_list_citizen_1))
    if(person_num - len(job_list) > 1):
        citizen_choices = random.sample(job_list_citizen_2,person_num-len(job_list))
        if "연인" in citizen_choices:
            citizen_choices.remove("연인")
            citizen_choices.remove(random.choice(citizen_choices))
            citizen_choices.append("연인(남)")
            citizen_choices.append("연인(여)")
            job_list += citizen_choices
        else:
            job_list += citizen_choices
    random.shuffle(job_list)
    person_job = []
    for i in range(person_num):
        person_job.append([])
        person_job[i].append(ctx.author.voice.channel.members[i])
        person_job[i].append(job_list[i])
    print(person_job)
    print(job_list)
    await ctx.send("게임이 시작되었습니다.")
    join_person_list = "참여인원 : " + str(len(person_job)) + "명\n"
    for i in range(len(person_job)):
        join_person_list += "`" + str(person_job[i][0]) + "`\n"

#    join_person_list += "이번판의 직업 : \n"
#    for i in range(len(person_job)):
#        join_person_list += "`" + str(job_list[i]) + "`\n"

    await ctx.send(content=join_person_list)
    for i in range(len(person_job)):
        await send_dm(ctx,person_job[i][0],person_job[i][1])
        await mute_user(ctx,person_job[i][0])
    day = 1
    while(True):
        await ctx.send(str(day) + "일차 밤이 되었습니다.")
        await asyncio.sleep(1)                                  #밤시간 설정
        await ctx.send(str(day)  + "일차 낮이 되었습니다.")
        for i in range(len(person_job)):
            await unmute_user(ctx,person_job[i][0])
        await talktimeset(ctx)
        person_job_list = []
        for i in range(len(person_job)):
            person_job_list.append(person_job[i][0])
        voted_person = await vote(ctx,person_job_list)
        if(voted_person == "None"):
            pass
        else:
            result_judg = await Judgment(ctx,voted_person,person_job_list)
            if(result_judg == "die"):
                for i in range(len(person_job)):
                    if(person_job[i][0] == voted_person):
                        del person_job[i]
                        break
                    else:
                        pass
                await ctx.send(str(voted_person) + "이(가) 투표로 사망하였습니다.")
                await mute_user(ctx,voted_person)
            else:
                pass
        day += 1


bot.run(token)
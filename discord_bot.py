import discord
import sys
import asyncio
from scraper import start_scraping
from datetime import datetime

TOKEN = '' #YOUR BOT TOKEN HERE
KEYWORDS = []
COOLTIME = 600
CURRENT_COOLTIME = 0
IS_RUNNING = False
CHANNEL_ID = #CHANNEL ID FOR BOT MESSEGE HERE
MENTION_USER = None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def on_every_second():
    global CURRENT_COOLTIME
    await client.wait_until_ready()

    while not client.is_closed():
        global IS_RUNNING
        if IS_RUNNING:
            if CURRENT_COOLTIME <= 0:
                results = await start_scraping(KEYWORDS)
                print(results)
                if len(results) != 0:
                    message = ""
                    has_found = False
                    for result in results:
                        keyword, found = result
                        if found: has_found = True
                        message = message + f'✅ [{keyword}] 를(을) 포함하는 공지글을 발견했습니다.\n' if found else message + f'❌ [{keyword}] 를(을) 포함하는 공지글을 발견하지 못했습니다.\n'

                    channel = client.get_channel(CHANNEL_ID)
                    if channel != None:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        await channel.send(f'```*스크래핑 성공*\n({current_time})\n\n{message}```' + (MENTION_USER.mention if has_found else ''))

                CURRENT_COOLTIME = COOLTIME
            else:
                CURRENT_COOLTIME = CURRENT_COOLTIME - 1

        await asyncio.sleep(1)  

@client.event
async def on_ready():
    print("HIGH Bot Logged In")
    client.loop.create_task(on_every_second())
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"검색 상태: {'ON' if IS_RUNNING else 'OFF'}"))

@client.event
async def on_message(message):
    global COOLTIME
    global IS_RUNNING

    msg = str(message.content)
    if message.content == '!help':
        await message.channel.send("```*도움말\n!키워드 - 검색 키워드 관리\n!쿨타임설정 - 검색 쿨타임 설정 (기본:600s)\n!시작 - 검색을 시작합니다.\n!중지 - 검색을 중지합니다.\n\n키워드를 추가한 뒤 !시작 으로 검색을 시작하세요.```")

    elif message.content == '!stop':
        await message.channel.send('Program stopped by !stop')
        await sys.exit('Program stopped by !stop')

    elif message.content == '!status':
        await message.channel.send('```' + ('🟢' if IS_RUNNING else '🔴') + ' HIGH Alarm Bot Status ' + ('(ON)' if IS_RUNNING else '(OFF)') + '\n\n' + f'검색 키워드: {KEYWORDS}\n검색 쿨타임: {COOLTIME}s\n다음 검색까지 남은 시간...{CURRENT_COOLTIME}s' + '```')

    elif msg.startswith("!키워드"):
        msg_list = msg.strip().split()
        msg_list.pop(0)
        if len(msg_list) == 0: msg_list.append("캬캬캬")
        
        if msg_list[0] == "목록":
            await message.channel.send(f"*추가된 키워드 목록*\n```{KEYWORDS}```")
        elif msg_list[0] == "추가":
            KEYWORDS.append(msg_list[1])
            await message.channel.send(f"*[{msg_list[1]}]*  가(이) 목록에 추가되었습니다.")
        elif msg_list[0] == "삭제":
            try:
                KEYWORDS.remove(msg_list[1])
                await message.channel.send(f"*[{msg_list[1]}]*  가(이) 목록에서 제거되었습니다.")
            except:
                await message.channel.send(f"*목록에서 [{msg_list[1]}]*  를(을) 발견하지 못했습니다.")
        else:
            await message.channel.send("```*올바른 명령어 사용법\n- !키워드 목록\n- !키워드 추가 [keyword]\n- !키워드 삭제 [keyword]```")

    elif msg.startswith("!쿨타임설정"):
        msg_list = msg.strip().split()
        msg_list.pop(0)
        if len(msg_list) == 0: msg_list.append("캬캬캬")
        try:
            cooltime = int(msg_list[0])
            COOLTIME = cooltime if cooltime > 60 else 60
            await message.channel.send(f"```쿨타임 설정됨: {COOLTIME}s```")
        except:
            await message.channel.send("```올바른 숫자를 입력해 주세요\n- !쿨타임설정 [숫자]```")
    
    elif msg.startswith("!시작"):
        global MENTION_USER
        MENTION_USER = message.author
        IS_RUNNING = True
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"검색 상태: {'ON' if IS_RUNNING else 'OFF'}"))
        await message.channel.send("```작동 상태를 [ON] 으로 변경했습니다.```")
    elif msg.startswith("!중지"):
        IS_RUNNING = False
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"검색 상태: {'ON' if IS_RUNNING else 'OFF'}"))
        await message.channel.send("```작동 상태를 [OFF] 으로 변경했습니다.```")

client.run(token=TOKEN)


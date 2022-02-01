import discord
import time
import asyncio
import bs4
import os
from discord import client
from discord import embeds
from discord.ext import commands
from selenium.webdriver.chrome import options
from youtube_dl import YoutubeDL
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix='!')
client = discord.Client()

user = []
musictitle = []
song_queue = []
musicnow = []

number = 1

userF = []
userFlist = []
allplaylist = []


def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    # chromedriver.exe 경로 위치
    driver = load_chrome_driver()
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()

    musictitle.append(music)
    musicnow.append(music)
    href = entireNum.get('href')
    url = 'https://www.youtube.com'+href
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()

    return music, URL


def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]  # 첫번째 곡 재생
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: play_next(ctx))


def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                    after=lambda e: play_next(ctx))
    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())


def again(ctx, url):
    global number
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if number:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        if not vc.is_playing():
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                    after=lambda e: again(ctx, url))


@bot.event  # 봇 실행 확인 문자
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    # 활동 상태 문구 수정창
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!흰쥐찰리 <- 부르기"))

    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')


def load_chrome_driver():

    options = webdriver.ChromeOptions()

    options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(executable_path=str(os.environ.get('CHROME_EXECUTABLE_PATH')), chrome_options=options)


@bot.command()
async def 흰쥐찰리(ctx):
    await ctx.send(embed=discord.Embed(title='찰리봇 도우미', description="""
찰리봇 주인 : https://github.com/jiho3894
오리 : http://duckpan.shop/
(2022.02.01)
마지막 업데이트 오류시 개인 이용자는 *오리*에 남겨주세요
다른 인원의 댓글은 건들지 말아주세요 부탁드립니다...

!흰쥐찰리 -> 찰리봇의 모든 명령어를 볼 수 있습니다.
\n!들어와잇 -> 찰리봇을 자신이 속한 채널로 부릅니다.
!나가잇 -> 찰리봇을 자신이 속한 채널에서 내보냅니다.
\n!재생 [노래이름] -> 찰리봇이 노래를 검색해 틀어줍니다.
* !재생 [가수명] [노래제목] 명령을 권장합니다 *
!반복 [노래이름] -> 노래를 반복 재생합니다.
* 반복 사용이후 명령어를 새로 입력해주세요 *
!다음 -> 현재 재생중인 노래 다음 곡을 재생합니다.
\n!일시정지 -> 현재 재생중인 노래를 일시정지시킵니다.
!다시재생 -> 일시정지시킨 노래를 다시 재생합니다.
\n!지금노래 -> 지금 재생되고 있는 노래의 제목을 알려줍니다.
\n!멜론차트 -> 최신 멜론차트를 재생합니다.
\n!즐겨찾기 -> 본인의 즐겨찾기 목록을 보여줍니다. (목록 추가후 !목록재생으로 사용)
!즐겨찾기추가 [가수명] [노래제목]-> 본인의 즐겨찾기 목록에 노래를 추가합니다.
!즐겨찾기삭제 [재생 순서 숫자]-> 본인의 즐겨찾기 목록에 노래를 삭제합니다.
\n!목록 -> 이어서 재생할 노래목록을 보여줍니다.
!목록재생 -> 목록에 추가된 노래를 재생합니다.
!목록초기화 -> 목록에 추가된 모든 노래를 지웁니다.
\n!대기열추가 [노래] -> 노래를 대기열에 추가합니다.
!대기열삭제 [숫자] -> 대기열에서 입력한 숫자에 해당하는 노래를 지웁니다.
\n!노래틀어 [노래 유튜브링크] -> 유튜브URL를 입력하면 찰리봇이 노래를 틀어줍니다.
(목록재생에서는 사용할 수 없습니다. 1회용입니다)""", color=0x00ffff))


@bot.command()
async def 들어와잇(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed=discord.Embed(title='찰리봇 도우미', description="""
찰리봇 주인 : https://github.com/jiho3894
오리 : http://duckpan.shop/
(2022.02.01)
마지막 업데이트 오류시 개인 이용자는 *오리*에 남겨주세요
다른 인원의 댓글은 건들지 말아주세요 부탁드립니다...

!흰쥐찰리 -> 찰리봇의 모든 명령어를 볼 수 있습니다.
\n!들어와잇 -> 찰리봇을 자신이 속한 채널로 부릅니다.
!나가잇 -> 찰리봇을 자신이 속한 채널에서 내보냅니다.
\n!재생 [노래이름] -> 찰리봇이 노래를 검색해 틀어줍니다.
* !재생 [가수명] [노래제목] 명령을 권장합니다 *
!반복 [노래이름] -> 노래를 반복 재생합니다.
* 반복 사용이후 명령어를 새로 입력해주세요 *
!다음 -> 현재 재생중인 노래 다음 곡을 재생합니다.
\n!일시정지 -> 현재 재생중인 노래를 일시정지시킵니다.
!다시재생 -> 일시정지시킨 노래를 다시 재생합니다.
\n!지금노래 -> 지금 재생되고 있는 노래의 제목을 알려줍니다.
\n!멜론차트 -> 최신 멜론차트를 재생합니다.
\n!즐겨찾기 -> 본인의 즐겨찾기 목록을 보여줍니다. (목록 추가후 !목록재생으로 사용)
!즐겨찾기추가 [가수명] [노래제목]-> 본인의 즐겨찾기 목록에 노래를 추가합니다.
!즐겨찾기삭제 [재생 순서 숫자]-> 본인의 즐겨찾기 목록에 노래를 삭제합니다.
\n!목록 -> 이어서 재생할 노래목록을 보여줍니다.
!목록재생 -> 목록에 추가된 노래를 재생합니다.
!목록초기화 -> 목록에 추가된 모든 노래를 지웁니다.
\n!대기열추가 [노래] -> 노래를 대기열에 추가합니다.
!대기열삭제 [숫자] -> 대기열에서 입력한 숫자에 해당하는 노래를 지웁니다.
\n!노래틀어 [노래 유튜브링크] -> 유튜브URL를 입력하면 찰리봇이 노래를 틀어줍니다.
(목록재생에서는 사용할 수 없습니다. 1회용입니다)""", color=0x00ffff))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 찰리봇이 없습니다.")


@bot.command()
async def 나가잇(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("간다잇")


@bot.command()
async def 노래틀어(ctx, *, url):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속 안했습니다.")

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed=discord.Embed(title="노래 재생", description="현재 " + url + "을(를) 재생하고 있습니다.", color=0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다.")


@bot.command()
async def 재생(ctx, *, msg):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속 안했습니다.")

    if not vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        driver = load_chrome_driver()
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl

        driver.quit()

        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed=discord.Embed(title="노래 재생", description="현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color=0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: play_next(ctx))
    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send("이미 노래가 재생 중이라" + result + "을(를) 대기열로 추가했습니다.")


@bot.command()
async def 반복(ctx, *, msg):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            pass

    global entireText
    global number
    number = 1
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if len(musicnow) - len(user) >= 1:
        for i in range(len(musicnow) - len(user)):
            del musicnow[0]

    driver = load_chrome_driver()
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    entireText = entireNum.text.strip()
    musicnow.insert(0, entireText)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    await ctx.send(embed=discord.Embed(title="반복재생", description="현재 " + musicnow[0] + "을(를) 반복재생하고 있습니다.", color=0x00ff00))
    again(ctx, url)


@bot.command()
async def 다음(ctx):
    if vc.is_playing():
        vc.stop()
        global number
        number = 0
        await ctx.send(embed=discord.Embed(title="노래끄기", description=musicnow[0] + "을(를) 종료했습니다.", color=0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")


@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed=discord.Embed(title="일시정지", description=musicnow[0] + "을(를) 일시정지 했습니다.", color=0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")


@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
        await ctx.send("지금 노래가 재생되지 않네요.")
    else:
        await ctx.send(embed=discord.Embed(title="다시재생", description=musicnow[0] + "을(를) 다시 재생했습니다.", color=0x00ff00))


@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되지 않네요.")
    else:
        await ctx.send(embed=discord.Embed(title="지금노래", description="현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color=0x00ff00))


@bot.command()
async def 멜론차트(ctx):

    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속 안했습니다.")

    if not vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        driver = load_chrome_driver()
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed=discord.Embed(title="노래 재생", description="현재 " + entireText + "을(를) 재생하고 있습니다.", color=0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없습니다.")


@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았습니다.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])

        await ctx.send(embed=discord.Embed(title="노래목록", description=Text.strip(), color=0x00ff00))


@bot.command()
async def 목록재생(ctx):

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았습니다.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있습니다.")


@bot.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed=discord.Embed(title="목록초기화", description="""목록이 정상적으로 초기화되었습니다. 노래를 등록해주세요.""", color=0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았습니다.")


@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했습니다.")


@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]

        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없습니다.")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다.")
            else:
                await ctx.send("숫자를 입력해주세요.")


@bot.command()
async def 즐겨찾기(ctx):
    global Ftext
    Ftext = ""
    correct = 0
    global Flist
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name):
            correct = 1  # 있으면 넘김
    if correct == 0:
        userF.append(str(ctx.message.author.name))
        userFlist.append([])
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            if len(userFlist[i]) >= 2:
                for j in range(1, len(userFlist[i])):
                    Ftext = Ftext + "\n" + str(j) + ". " + str(userFlist[i][j])
                titlename = str(ctx.message.author.name) + "님의 즐겨찾기"
                embed = discord.Embed(
                    title=titlename, description=Ftext.strip(), color=0x00ff00)
                embed.add_field(name="목록에 추가\U0001F4E5",
                                value="즐겨찾기에 모든 곡들을 목록에 추가합니다.", inline=False)
                embed.add_field(name="플레이리스트로 추가\U0001F4DD",
                                value="즐겨찾기에 모든 곡들을 새로운 플레이리스트로 저장합니다 (업데이트 예정)", inline=False)
                Flist = await ctx.send(embed=embed)
                await Flist.add_reaction("\U0001F4E5")
                # await Flist.add_reaction("\U0001F4DD")
            else:
                await ctx.send("아직 등록하신 즐겨찾기가 없어요.")


@bot.command()
async def 즐겨찾기추가(ctx, *, msg):
    correct = 0
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name):
            correct = 1
    if correct == 0:
        userF.append(str(ctx.message.author.name))
        userFlist.append([])
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):

            options = webdriver.ChromeOptions()
            options.add_argument("headless")

            driver = load_chrome_driver()
            driver.get(
                "https://www.youtube.com/results?search_query="+msg+"+lyrics")
            source = driver.page_source
            bs = bs4.BeautifulSoup(source, 'lxml')
            entire = bs.find_all('a', {'id': 'video-title'})
            entireNum = entire[0]
            music = entireNum.text.strip()

            driver.quit()

            userFlist[i].append(music)
            await ctx.send(music + "(이)가 정상적으로 등록되었어요!")


@bot.command()
async def 즐겨찾기삭제(ctx, *, number):
    correct = 0
    for i in range(len(userF)):
        if userF[i] == str(ctx.message.author.name):
            correct = 1
    if correct == 0:
        userF.append(str(ctx.message.author.name))
        userFlist.append([])
        userFlist[len(userFlist)-1].append(str(ctx.message.author.name))

    for i in range(len(userFlist)):
        if userFlist[i][0] == str(ctx.message.author.name):
            if len(userFlist[i]) >= 2:
                try:
                    del userFlist[i][int(number)]
                    await ctx.send("정상적으로 삭제되었습니다.")
                except:
                    await ctx.send("입력한 숫자가 잘못되었거나 즐겨찾기의 범위를 초과하였습니다.")
            else:
                await ctx.send("즐겨찾기에 노래가 없어서 지울 수 없어요!")


@bot.event
async def on_reaction_add(reaction, users):
    if users.bot == 1:
        pass
    else:
        try:
            await Flist.delete()
        except:
            pass
        else:
            if str(reaction.emoji) == '\U0001F4E5':
                await reaction.message.channel.send("노래 넣어요 (즐겨찾기 갯수가 많으면 지연될 수 있습니다.)")
                print(users.name)
                for i in range(len(userFlist)):
                    if userFlist[i][0] == str(users.name):
                        for j in range(1, len(userFlist[i])):
                            try:
                                driver = load_chrome_driver()
                                driver.close()
                            except:
                                print("NOT CLOSED")

                            user.append(userFlist[i][j])
                            result, URLTEST = title(userFlist[i][j])
                            song_queue.append(URLTEST)
                            await reaction.message.channel.send(userFlist[i][j] + "를 재생목록에 추가했어요!")
            elif str(reaction.emoji) == '\U0001F4DD':
                await reaction.message.channel.send("no code")

bot.run('OTI1MjU3NDM3MjM2MzIyMzk1.YcqfIw.fvKuSnUfibxhiKUHSOZkQaEqySw')

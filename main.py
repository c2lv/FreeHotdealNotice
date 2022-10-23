import asyncio
import discord
import aiocron
from datetime import datetime
from discord.ext import commands
from utils import *
from const import *
from scraping import scraping, scraping2

game = discord.Game("공지 정리")

intents = discord.Intents.all()

async def main():
    bot = commands.Bot(intents=intents, command_prefix=PREFIX, status=discord.Status.online, activity=game)

    '''
    Loops
    '''
    '''
    @aiocron.crontab('*/5 * * * *') # minute hour day month week second
    async def freeHotDealNotice():
        # Get channel id
        ch_freehotdeal_fmkorea = bot.get_channel(CH_FREEHOTDEAL_FMKOREA_ID)

        # Get notice
        freehotdeal_fmkorea_message = scraping()

        # Make message
        for d in freehotdeal_fmkorea_message:
            if 'error' in d:
                embed = discord.Embed(description=d['error'], color=0xFF0000)
                embed.set_author(name='실행중 문제가 발생했습니다.')
            else:
                description = f"쇼핑몰: {d['mall']} / 가격: {d['price']} / 배송: {d['delivery_fee']}\n" \
                    + f"카테고리: {d['category']} / 관련 URL 바로가기: {d['related_url']}\n" \
                    + f"글 내용: {d['content']}"
                embed = discord.Embed(description=description, color=0xFF5733)
                embed.set_author(name=d['title'], url=d['post_url'])
                embed.set_thumbnail(url=d['thumb'])

            # Send message to channel
            await ch_freehotdeal_fmkorea.send(embed=embed)
    '''

    @aiocron.crontab('1 15 * * *') # minute hour day month week second
    async def jirum2():
        # Get channel id
        ch_jirum2 = bot.get_channel(CH_JIRUM2_ID)

        # Get notice
        jirum2_message = scraping2()

        # Send message to channel
        for message in jirum2_message:
            await ch_jirum2.send(message)
    
    '''
    Commands
    '''
    @bot.command(aliases=['서버시간확인'])
    async def st(ctx):
        now = datetime.now()
        await ctx.send(now)
        await ctx.send(f"현재 서버 시간은 {now.year}년 {now.month}월 {now.day}일 {now.hour}시 {now.minute}분 {now.second}초입니다.")

    await bot.start(token=TOKEN)

'''
Run
'''
if __name__ == '__main__':
    asyncio.run(main())
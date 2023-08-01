import asyncio
import discord
import requests
import json
from discord.ext import commands
from discord.utils import get

token = "Your Token Here"

DiscordHacks = commands.Bot(description='DiscordHacks', command_prefix=';', self_bot=True)

DiscordHacks.lockgc = []
DiscordHacks.headers = {
    'authorization': token,
}

@DiscordHacks.event
async def lockloop():
    while True:
        if not DiscordHacks.lockgc == []:
            for gcid in DiscordHacks.lockgc:
                response = requests.put(f'https://discordapp.com/api/v8/channels/{gcid}/recipients/1337',headers=DiscordHacks.headers)
                if response.status_code == 429:
                    response_c = response.text
                    response_content = json.loads(response_c)
                    lockedsec = response_content.get('retry_after')
                else:
                    headers = {"Authorization": token}
                    payload = {"content": "__**This group is now locked, you cant kick or add anyone.**__", "nonce": gcid}
                    response = requests.post(url=f'https://discord.com/api/v9/channels/{gcid}/messages', headers=headers, json=payload)
                    for i in range(30):
                        response = requests.put(f'https://discordapp.com/api/v8/channels/{gcid}/recipients/1337',headers=DiscordHacks.headers)
        await asyncio.sleep(0.8)

@DiscordHacks.event
async def on_connect():
  print("Connected , use " ;lock GCID " and " ;unlock GCID " !")
  await lockloop()

@DiscordHacks.command()
async def lock(ctx, groupid):
    DiscordHacks.lockgc.extend([groupid] * 1)


@DiscordHacks.command()
async def unlock(ctx, groupid=None):
    await ctx.send('__**Unlocked the GC**__')
    if groupid:
        DiscordHacks.lockgc.pop(groupid)
        print(f'Unlocking {groupid} in 120 seconds Master !')
    else:
        DiscordHacks.lockgc.clear()
        print(f'Unlocked All Groups')

DiscordHacks.run(token, bot=False, reconnect=True)

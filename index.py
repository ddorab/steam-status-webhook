import discord
import json
from discord.ext import commands, tasks
import asyncio
import random
import time
import requests

webhook_url = 'https://discord.com/api/webhooks/883037032597835788/zEGGU6oGq4G6H28f_sTSEspbIUf5ioGmsQql4HAxiJLLaxLf9foofin9oddSfx2FyTb5'

get_url = 'https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=D49C65BDE7D2B24942052EE5F2DF0153'

data = {}

#r = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json'})

while True:
    message = input()
    r = requests.post(url, data={'content': message})
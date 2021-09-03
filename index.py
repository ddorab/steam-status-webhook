import discord
import json
import asyncio
from discord.webhook import AsyncWebhookAdapter, Webhook
import requests
import aiohttp
from datetime import date

webhook_url = (
    "https://discord.com/api/webhooks/883037032597835788"
    "/zEGGU6oGq4G6H28f_sTSEspbIUf5ioGmsQql4HAxiJLLaxLf9foofin9oddSfx2FyTb5"
)

get_url = (
    "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus"
    "/v1/?key=D49C65BDE7D2B24942052EE5F2DF0153&format=json"
)

today = date.today()


async def send_webhook():

    while True:
        r = requests.get(get_url)
        data = json.loads(r.text)

        sessions_logon = data["result"]["services"]["SessionsLogon"]
        matchmaking = data["result"]["matchmaking"]["scheduler"]
        version = data["result"]["app"]["version"]
        steam = data["result"]["services"]["SteamCommunity"]

        previous_status = "online"

        if sessions_logon == "offline" and previous_status == "online":

            previous_status = "offline"

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    webhook_url, adapter=AsyncWebhookAdapter(session)
                )
                embed_description = (
                    "[Detaylı Sunucu Durumu](https://steamstat.us/)\n"
                    "\n**Steam**: ***%s***\n"
                    "\n**CS:GO Oturumları**: ***%s***\n"
                    "\n**CS:GO Matchmaking**: ***%s***\n"
                    "\n**CS:GO Versiyonu**: ***%s***\n"
                    % (
                        steam.capitalize(),
                        sessions_logon.capitalize(),
                        matchmaking.capitalize(),
                        version,
                    )
                )

                webhook_embed = discord.Embed(
                    title="Servisler Çöktü!",
                    description=embed_description,
                    colour=discord.Colour.dark_red(),
                )
                webhook_embed.set_thumbnail(
                    # url=("https://steamstat.us/static/icons/csgo.jpg")
                    url=(
                        "https://cdn.cloudflare.steamstatic.com/steamcommunity"
                        "/public/images/avatars/e4"
                        "/e4346674a5511b07935eccaaa918a7f75e2f0f15_full.jpg"
                    )
                )
                webhook_embed.set_author(
                    name="Keldra",
                    url="",
                    icon_url=(
                        "https://cdn.discordapp.com/avatars"
                        "/299988629466382336/"
                        "a_3de4e6f90b77724d1732c8ad388acab1.webp?size=128"
                    ),
                )

                await webhook.send(embed=webhook_embed)
                await asyncio.sleep(45)
                print("Embed sent!: Date: ", today)
                continue
        elif sessions_logon == "surge":
            print("Surge! Date: ", today)
            print("sessions might be having issues")
        elif sessions_logon == "online" and previous_status == "offline":
            previous_status = "online"
            print("Back to normal! Date: ", today)


loop = asyncio.get_event_loop()
loop.run_until_complete(send_webhook())
loop.close()

from db import save_db, get_db
from telethon import TelegramClient, functions
from telethon.errors import ChatAdminRequiredError, ChannelsTooMuchError, ChannelPrivateError, SearchQueryEmptyError
from config import API_ID, API_HASH, SESSION
import sys

api_id = API_ID
api_hash = API_HASH
client = TelegramClient(SESSION, api_id, api_hash)


async def main():
    query = input("Enter you query: ")
    link = input("Your group chat link: ")

    try:
        result = await client(functions.contacts.SearchRequest(
            q=query,
            limit=10
        ))
        if not result.results:
            print("Couldn't find any channels with that name.")
    except SearchQueryEmptyError:
        print("You didn't enter any query!")
        sys.exit()

    for chat in result.chats:
        try:
            await client(functions.channels.JoinChannelRequest(chat))  # Join Channel
        except (ChannelsTooMuchError, ChannelPrivateError):
            print("Cant join this channel")

        try:
            users = await client.get_participants(chat, limit=3)  # Get Users
        except ChatAdminRequiredError:
            print("You dont have enough permissions to do that!")

        for user in users:
            if user.username is not None:
                post = {'username': user.username}
                save_db(post)

    usernames = get_db()
    for user in usernames:
        await client.send_message(user, link)  # Send invite to users of your group

with client:
    client.loop.run_until_complete(main())

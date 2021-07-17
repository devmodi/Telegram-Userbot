import sys
from time import sleep
from telethon import TelegramClient, functions
from telethon.errors import ChatAdminRequiredError, ChannelsTooMuchError, SearchQueryEmptyError, FloodWaitError
from db import save_posts_in_db, get_users_from_db
from config import API_ID, API_HASH, SESSION


api_id = API_ID
api_hash = API_HASH
client = TelegramClient(SESSION, api_id, api_hash)


async def main():

    async def process_channels_participants(chats):
        chat_processed_count = 0

        while chat_processed_count < len(chats):
            chat = chats[chat_processed_count]
            print(f"Processing chat {chat.id}")

            # Join Channels
            try:
                await client(functions.channels.JoinChannelRequest(chat))
            except (ChannelsTooMuchError, FloodWaitError) as e:
                if isinstance(e, FloodWaitError):
                    print(f"FloodWaitError occured, sleeping for {e.seconds} seconds.")
                    sleep(e.seconds)
                    continue
                print("You have reached channel limit! Can't join more channels.")

            # Get users
            try:
                users = await client.get_participants(chat, limit=4)
            except ChatAdminRequiredError:
                print("You don't have enough permissions to access users!")
                break

            me = await client.get_me()
            posts = []

            # Save usernames in db
            for user in users:
                if user.username is not None and user.username != me.username:
                    post = {'username': user.username}
                    posts.append(post)
            if posts:
                save_posts_in_db(posts)

            chat_processed_count += 1
            print(f"Processed chat {chat.id} successfully")

    query = input("Enter you query: ")
    message = input("Enter custom message: ")

    # Search channel
    try:
        result = await client(functions.contacts.SearchRequest(
            q=query,
            limit=2
        ))
        if not result.results:
            print("Couldn't find any channels with that name.")
    except SearchQueryEmptyError:
        print("You didn't enter any query!")
        sys.exit()

    await process_channels_participants(result.chats)

    users = get_users_from_db()
    messages_proccessed_count = 0

    # Send message to all the users
    while messages_proccessed_count < len(users):
        user = users[messages_proccessed_count]
        try:
            await client.send_message(user, message)
        except FloodWaitError as e:
            print(f"FloodWaitError occured, sleeping for {e.seconds}")
            sleep(e.seconds)
            continue
        messages_proccessed_count += 1
        print(f"Sent message to {user}")


with client:
    client.loop.run_until_complete(main())

from dotenv import load_dotenv

from logger_bot.process import client, main

load_dotenv()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())

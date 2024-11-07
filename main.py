import requests
import asyncio,random
from telegram import Bot

# Replace with your own Unsplash API key and Telegram bot token
UNSPLASH_ACCESS_KEY = 'iOT3nyIbIGPJ0DfDrgQRm5tVKA9xmNE9gERMQ-2QwvY'
TELEGRAM_BOT_TOKEN = '7751618525:AAGm6oPKz1IkfBh5ZrPyPz8RLO58ageJMmg'
TELEGRAM_CHANNEL_ID = '@free_wallpaper_8k'  # Format: @your_channel_id for public channels

def get_random_wallpaper():
    """Fetches a random wallpaper from Unsplash."""
    url = 'https://api.unsplash.com/photos/random'
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    params = {
        'query': 'Full 8k 4k HD Wallpaper',  # Search for wallpapers
        'orientation': random.choice(["landscape","potrait"])
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'image_url': data['urls']['regular'],  # URL to the wallpaper
            'alt_description': data.get('alt_description', 'Beautiful wallpaper'),
            'photo_by': data['user']['name'],
            'user_link': data['user']['links']['html']
        }
    else:
        print("Error fetching image:", response.status_code)
        return None

async def post_to_telegram(image_url, caption):
    """Posts the wallpaper to the specified Telegram channel."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_photo(
            chat_id=TELEGRAM_CHANNEL_ID,
            photo=image_url,
            caption=caption,
            parse_mode='Markdown'  # To format text with Markdown
        )
        print("Wallpaper posted successfully to Telegram channel!")
    except Exception as e:
        print(f"Error posting to Telegram: {e}")

async def main():
    # Get a random wallpaper from Unsplash
    wallpaper = get_random_wallpaper()
    if wallpaper:
        # Create a caption for the wallpaper post
        caption = (
            f"{wallpaper['alt_description'].capitalize()} 🌄\n\n"
            # f"Photo by [{wallpaper['photo_by']}]({wallpaper['user_link']}) on Unsplash"
        )
        # Post the wallpaper to Telegram
        await post_to_telegram(wallpaper['image_url'], caption)
    else:
        print("Failed to fetch wallpaper.")

# Run the main function with asyncio
if __name__ == "__main__":
    for i in range(10):
        asyncio.run(main())

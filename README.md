# AI multipurpose telegram bot

## This bot can generate images and videos based on users prompt, answer questions in conversational format and summarize videos

## Technologies and tools used in this project:
- Python - main programming language
- Base64 - library that is used to decode images
- BeautyfullSoup - library that is used for summarization
- PyTelegramBotAPI - library for creating telegram bots
- FusionBrain API - api key for generating images and videos

## Features
- Users can enter the /generate command with a text description, after which they are prompted to choose an image style.
- After the style is chosen, the image is generated and sent back to the user.
- Users can enter the /summarize command with a video link, after which the video is
- The /ask command allows users to ask questions, and the bot processes them using a question-answering model based on DeepPavlov.
- Ease of Use: User-friendly interface via Telegram.


## Usage
- /start or /help - starting a bot and showing all available commands
- /generate <promot> - generating an image
- /ask <prompt> - answers users query

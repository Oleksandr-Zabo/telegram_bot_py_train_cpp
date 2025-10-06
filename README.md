# 🤖 C/C++ Trainer Telegram Bot

Educational Telegram bot for learning C and C++ programming fundamentals.

## 📋 Description

C/C++ Trainer is an interactive bot that helps learn the basics of C and C++ programming. The bot includes:

- 📚 **Theoretical materials** - divided into 3 main topics
- 📝 **Interactive testing** - 5 questions with random selection of 3
- 🔗 **Useful links** - resources for self-learning

## 🔧 Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a bot in Telegram

1. Find @BotFather in Telegram
2. Send the `/newbot` command
3. Give your bot a name (e.g., "C/C++ Trainer")
4. Give your bot a username (must end with "bot", e.g., "cpp_trainer_bot")
5. Copy the received token

### 3. Token configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file and replace:
   ```
   BOT_TOKEN=YOUR_BOT_TOKEN_HERE
   ```
   with:
   ```
   BOT_TOKEN=your_bot_token
   ```

**⚠️ IMPORTANT:** Never add the `.env` file to Git! It's already added to `.gitignore`.

## 🚀 Running the bot

```bash
python bot.py
```

## 📚 Learning material structure

### Theoretical topics:
1. **🔤 C/C++ Basics** - history, features, program structure
2. **📊 Variables and data types** - int, float, double, char, constants
3. **� Operators** - arithmetic, comparison, logical

### Testing:
- 5 prepared questions
- Random selection of 3 questions for each test
- Percentage scoring system
- Detailed results with recommendations

## 🎯 Functionality

- **Main menu** with three main sections
- **Navigation** between sections with "Back" buttons
- **Interactive tests** with instant answer checking
- **Useful links** to documentation, online compilers, courses
- **Code and text formatting** support

## 🔧 Technical details

- **Programming language**: Python 3.7+
- **Library**: python-telegram-bot 20.6 / HTTP API
- **Architecture**: callback-based event handling
- **Data storage**: in memory (user_states dictionary)

## 📝 Usage example

1. Start the bot with the `/start` command
2. Choose "📚 Theory" section to study materials
3. Take a "📝 Test" to check your knowledge
4. Use "🔗 Links" for additional learning resources

## 🚀 Deployment

### Local development:
```bash
python bot.py
```

### Deploy to Render:
1. Push code to GitHub (token is safely hidden in `.env`)
2. Connect repository to Render
3. Add environment variable `BOT_TOKEN` with your token value
4. Render will automatically install dependencies from `requirements.txt`

## 🤝 Contributing

You can add new questions to the `QUESTIONS` list or extend theoretical materials in the `THEORY` dictionary.

## 📄 License

This project was created for educational purposes.
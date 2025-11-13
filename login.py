from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# ======= הגדרת רשימת משתמשים וסיסמאות =========
users = {
    "שחר דורון": "1234",
    "ברק גרשון": "1234"
}

# ======= מילון לשמירת מצב המשתמש =========
user_states = {}
STATE_WAIT_USERNAME = 1
STATE_WAIT_PASSWORD = 2

# ======= פונקציה לתיקון טקסט בעברית =========
def fix_rtl_text(text: str) -> str:
    reshaped_text = arabic_reshaper.reshape(text)      # מסדר את האותיות
    bidi_text = get_display(reshaped_text)             # הופך לכיוון RTL
    return bidi_text

# ======= פונקציית יצירת התמונה =========
def create_certificate(name, class_name):
    img = Image.open("fix.png")
    draw = ImageDraw.Draw(img)

    # פונטים
    font_name = ImageFont.truetype("arial.ttf", 40)
    font_class = ImageFont.truetype("arial.ttf", 40)

    # קואורדינטות (צריך להתאים לפי התבנית)
    name_position = (500, 372)
    class_position = (600, 260)

    # שימוש בתיקון RTL
    draw.text(name_position, fix_rtl_text(name), fill="black", font=font_name)
    draw.text(class_position, fix_rtl_text(class_name), fill="black", font=font_class)

    output_path = f"{name}_certificate.png"
    img.save(output_path)
    return output_path

# ======= התחלת הבוט =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_states[chat_id] = STATE_WAIT_USERNAME
    await update.message.reply_text("שלום! הכנס שם משתמש:")

# ======= טיפול בהודעות =========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if chat_id not in user_states:
        await update.message.reply_text("אנא התחל את הבוט עם /start")
        return

    if user_states[chat_id] == STATE_WAIT_USERNAME:
        if text in users:
            user_states[chat_id] = (STATE_WAIT_PASSWORD, text)
            await update.message.reply_text("מעולה! עכשיו הכנס סיסמה:")
        else:
            await update.message.reply_text("שם משתמש לא נכון. נסה שוב:")

    elif isinstance(user_states[chat_id], tuple) and user_states[chat_id][0] == STATE_WAIT_PASSWORD:
        username = user_states[chat_id][1]
        if users[username] == text:
            await update.message.reply_text(f"✅ נכנסת בהצלחה, {username}!")

            class_name = "'יא3"
            image_path = create_certificate(username, class_name)

            with open(image_path, "rb") as photo:
                await context.bot.send_photo(chat_id=chat_id, photo=photo)

            user_states.pop(chat_id)
        else:
            await update.message.reply_text("סיסמה שגויה. נסה שוב:")
            user_states[chat_id] = (STATE_WAIT_PASSWORD, username)

# ======= הרצה =========
def main():
    TOKEN = "8039465504:AAF0qPYFizhcGXtOoRmqNqPxXpixf5E6WbE"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

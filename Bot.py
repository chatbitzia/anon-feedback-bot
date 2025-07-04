import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler,
    MessageHandler, filters, ConversationHandler
)

TOKEN = "8077961165:AAGOcmrcXYXswfosdH8LMbwf5TLUqmHrIpM"
GROUP_CHAT_ID = -1002801579739

CATEGORY, FEEDBACK = range(2)

logging.basicConfig(level=logging.INFO)

categories = ["Обслуживание", "Условия труда", "Руководство", "Пожелания", "Другое"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(
        [[cat] for cat in categories], one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text("Выберите категорию:", reply_markup=reply_markup)
    return CATEGORY

async def category_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text
    await update.message.reply_text("Теперь оставьте отзыв (он будет отправлен анонимно):")
    return FEEDBACK

async def receive_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.user_data.get("category", "Без категории")
    feedback = update.message.text
    message = f"📬 *Новый анонимный отзыв:*\n\n*Категория:* {category}\n*Текст:* {feedback}"
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='Markdown')
    await update.message.reply_text("Спасибо! Ваш отзыв отправлен.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отзыв отменён.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category_chosen)],
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_feedback)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()

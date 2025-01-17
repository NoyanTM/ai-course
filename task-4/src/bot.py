import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, Updater
from sqlalchemy import insert, select, and_
from sqlalchemy import update as update_query

from src.config import TELEGRAM_BOT_TOKEN
from src.craft import generate_response, prompt
from src.database import get_session, Player, GameSession, Status

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# logger = logging.getLogger(__name__)


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = update.message.from_user
    telegram_user_id = user_data.id
    telegram_username = user_data.username 
    
    with get_session() as session:
        # проверяем что пользователь существует ли пользователь уже
        select_player = session.execute(
            select(Player)
            .where(Player.telegram_user_id == telegram_user_id)
        )
        select_player_result = select_player.scalar_one_or_none()
        
        # если нет то добавляем пользователя
        if select_player_result is None:
            insert_new_player = session.execute(
                insert(Player)
                .values(telegram_user_id=telegram_user_id, telegram_username=telegram_username)
                .returning(Player)
            )
            select_player_result = insert_new_player.scalar_one_or_none()
        
        # проверяем есть ли уже активная игровая сессия
        select_active_session = session.execute(
            select(GameSession)
            .where(GameSession.player_id == select_player_result.id)
            .where(GameSession.status == Status.ACTIVE)
        )
        active_session_result = select_active_session.scalar_one_or_none()
        
        # если нету то добавляем сессию
        if active_session_result is None:
            insert_new_game_session = session.execute(
                insert(GameSession)
                .values(
                    player_id=select_player_result.id,
                    inventory={"items": ["water", "earth", "fire", "air"]}
                )
                .returning(GameSession)
            )
            active_session_result = insert_new_game_session.scalar_one_or_none()
        
        session.commit()
        
        await update.message.reply_text(f"Hello {telegram_username}, your game session: {active_session_result.id}")


async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Here are the available commands:\n\n"
        "/start - Start interacting with the bot.\n"
        "/help - Display this help message.\n"
        "/status - View the items in your inventory.\n"
        "/craft - Craft new item.\n"
        "/stop - End your current game session.\n\n"
        "If you have any issues or need further assistance, feel free to ask!"
    )
    await update.message.reply_text(help_text)


# get game session stats and inventory
async def get_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = update.message.from_user
    telegram_user_id = user_data.id
    with get_session() as session:
        current_player = session.execute(
            select(Player)
            .where(Player.telegram_user_id == telegram_user_id)
        ).scalar_one_or_none()
        current_session = session.execute(
            select(GameSession)
            .where(
                and_(
                    GameSession.player_id == current_player.id,
                    GameSession.status == Status.ACTIVE
                )
            )
        ).scalar_one_or_none()
        if current_session or current_player is None:
            await update.message.reply_text("Check /help")
        session_info = (
            f"Game Session ID: {current_session.id}\n"
            f"Status: {current_session.status.name}\n"
            f"Player ID: {current_session.player_id}\n"
            f"Inventory: {current_session.inventory}"
        )
        await update.message.reply_text(session_info)


async def craft_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = update.message.from_user
    telegram_user_id = user_data.id
    
    # Extract the crafting items from the user's message
    try:
        _, item1, item2 = update.message.text.split()
    except ValueError:
        await update.message.reply_text("Please provide two items to craft, e.g., /craft sword shield")
        return

    with get_session() as session:
        # Get the current player
        current_player = session.execute(
            select(Player)
            .where(Player.telegram_user_id == telegram_user_id)
        ).scalar_one_or_none()
        
        if current_player is None:
            await update.message.reply_text("You are not registered. Use /start to begin.")
            return

        # Get the active game session
        current_session = session.execute(
            select(GameSession)
            .where(
                and_(
                    GameSession.player_id == current_player.id,
                    GameSession.status == Status.ACTIVE
                )
            )
        ).scalar_one_or_none()
        
        if current_session is None:
            await update.message.reply_text("No active game session found. Check /help for more details.")
            return

        # Check if both items are in the inventory
        inventory = current_session.inventory
        
        if not isinstance(inventory, dict):
            await update.message.reply_text("Your inventory is empty or invalid.")
            return
        
        if item1 not in inventory.get("items") or item2 not in inventory.get("items"):
            await update.message.reply_text(f"One or both items ({item1}, {item2}) are not in your inventory.")
            return

        # Simulate crafting logic
        crafted_item = generate_response(prompt=prompt, first_element=item1, second_element=item2)
        new_inventory = inventory.get("items")
        new_items = new_inventory + [crafted_item]
        
        # add crafted item to inventory
        session.execute(
            update_query(GameSession)
            .values(
                inventory={"items": new_items}
            )
            .where(GameSession.id == current_session.id)
        )
        
        session.commit()
        
        await update.message.reply_text(
            f"You successfully crafted {crafted_item} using {item1} and {item2}!"
        )
        


async def stop_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # проверяем такого пользователя с таким айдишником и заканчиваем его текующую сессию и т.ж.
    # если его нету пользователя то выводим сообщение о том что ознакомнитись с /help
    pass


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_game))
    application.add_handler(CommandHandler("help", get_help))
    application.add_handler(CommandHandler("status", get_status))
    application.add_handler(CommandHandler("craft", craft_item))
    application.add_handler(CommandHandler("stop", get_help))
    application.run_polling()


if __name__ == "__main__":
    main()

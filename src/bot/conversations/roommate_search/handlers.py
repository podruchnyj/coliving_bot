from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.roommate_search.buttons as buttons
import conversations.roommate_search.callback_funcs as callbacks
import conversations.roommate_search.states as states
from conversations.common_functions import common_buttons
from conversations.menu.buttons import SEARCH_NEIGHBOR_BUTTON
from conversations.roommate_search.buttons import AGE_RANGE_CALLBACK_PATTERN
from conversations.roommate_search.validators import (
    handle_text_input_instead_of_choosing_button,
)

roommate_search_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callbacks.start, rf"^{SEARCH_NEIGHBOR_BUTTON}$")
    ],
    states={
        states.AGE: [
            CallbackQueryHandler(
                callback=callbacks.set_age,
                pattern=AGE_RANGE_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.LOCATION: [
            CallbackQueryHandler(
                callback=callbacks.set_location,
                pattern=common_buttons.LOCATION_CALLBACK_PATTERN,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.NEXT_PROFILE: [
            CallbackQueryHandler(
                callback=callbacks.next_profile,
                pattern=rf"^{buttons.YES_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.end_of_search,
                pattern=rf"^{buttons.NO_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.NO_MATCHES: [
            CallbackQueryHandler(
                callback=callbacks.end_of_search,
                pattern=rf"^{buttons.WAIT_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.edit_settings,
                pattern=rf"^{buttons.EDIT_SETTINGS_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.PROFILE: [
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.LIKE_BTN}$"),
                callback=callbacks.profile_like,
            ),
            MessageHandler(
                filters=filters.Regex(rf"^{buttons.DISLIKE_BTN}$"),
                callback=callbacks.next_profile,
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.SEX: [
            CallbackQueryHandler(
                callback=callbacks.set_sex,
                pattern=rf"^({buttons.MALE_BTN}|{buttons.FEMALE_BTN})$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
        states.SEARCH_SETTINGS: [
            CallbackQueryHandler(
                callback=callbacks.ok_settings,
                pattern=rf"^{buttons.OK_SETTINGS_BTN}$",
            ),
            CallbackQueryHandler(
                callback=callbacks.edit_settings,
                pattern=rf"^{buttons.EDIT_SETTINGS_BTN}$",
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                handle_text_input_instead_of_choosing_button,
            ),
        ],
    },
    fallbacks=[CommandHandler("cancel", callbacks.end_of_search)],
)

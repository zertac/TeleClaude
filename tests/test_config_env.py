import importlib
import os
import sys
import types
import unittest
from unittest.mock import patch

telegram_module = types.ModuleType("telegram")
telegram_module.Update = object
telegram_ext_module = types.ModuleType("telegram.ext")
telegram_ext_module.Application = object
telegram_ext_module.CommandHandler = object
telegram_ext_module.MessageHandler = object
telegram_ext_module.filters = types.SimpleNamespace(TEXT=object())
telegram_ext_module.ContextTypes = types.SimpleNamespace(DEFAULT_TYPE=object())

sys.modules.setdefault("telegram", telegram_module)
sys.modules.setdefault("telegram.ext", telegram_ext_module)

import telegram_claude_bot


class ConfigEnvTests(unittest.TestCase):
    def test_parse_allowed_user_ids_json(self):
        parsed = telegram_claude_bot.parse_allowed_user_ids('[1, "2", 3]')
        self.assertEqual(parsed, [1, 2, 3])

    def test_parse_allowed_user_ids_csv(self):
        parsed = telegram_claude_bot.parse_allowed_user_ids("1, 2 3")
        self.assertEqual(parsed, [1, 2, 3])

    def test_parse_allowed_user_ids_invalid_tokens(self):
        parsed = telegram_claude_bot.parse_allowed_user_ids("1, abc, 2")
        self.assertEqual(parsed, [1, 2])

    def test_env_overrides_config(self):
        with patch.dict(
            os.environ,
            {
                "TELEGRAM_BOT_TOKEN": "test-token",
                "ALLOWED_USER_IDS": "123, 456",
                "WORKING_DIR": r"C:\Projects",
            },
            clear=False,
        ):
            module = importlib.reload(telegram_claude_bot)
            self.assertEqual(module.TELEGRAM_BOT_TOKEN, "test-token")
            self.assertEqual(module.ALLOWED_USER_IDS, [123, 456])
            self.assertEqual(module.WORKING_DIR, r"C:\Projects")


if __name__ == "__main__":
    unittest.main()

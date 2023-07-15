from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

keys = SimpleNamespace(
    random_connect=':envelope: Random Connect',
    settings=':gear: Settings',
    exit=':cross_mark: exit'
)

keyboards = SimpleNamespace(
    main=create_keyboard(keys.random_connect, keys.settings),
    exit=create_keyboard(keys.exit)
)

states = SimpleNamespace(
    main="MAIN",
    random_connect="RANDOM_CONNECT",
    connected="CONNECTED"
)

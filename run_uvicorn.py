import os

import uvicorn


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
    os.environ.setdefault("READ_ENV_FILE", "yes")
    uvicorn.run(
        "config.asgi:application",
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()

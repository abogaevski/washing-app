import os
import django
from scripts.mqtt.subscriber import main

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engine.settings_prod")

if __name__ == "__main__":
    django.setup()
    main()

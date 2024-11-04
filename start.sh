pip uninstall channels
pip uninstall daphne
pip install channels
pip install daphne
daphne Whisper.asgi:application --port $PORT --bind 0.0.0.0
# Uninstall and reinstall channels and daphne without prompt
pip uninstall -y channels daphne
pip install channels daphne
daphne Whisper.asgi:application --port $PORT --bind 0.0.0.0
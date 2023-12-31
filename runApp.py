import os
from app import create_app

app = create_app()

port = os.getenv("PORT", 80)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)

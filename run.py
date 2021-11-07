from financeTracker import create_app
import os

app = create_app()

# push app context


if __name__ == '__main__':
    app.run(debug=True)
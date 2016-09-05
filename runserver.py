"""
Runs the miniblog application using a development server
"""

from miniblog import app

print(__name__)
print(app)

if __name__ == '__main__':
    app.run()

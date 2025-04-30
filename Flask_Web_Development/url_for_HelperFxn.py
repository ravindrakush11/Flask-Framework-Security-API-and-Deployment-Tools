from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return f'Go to your <a href="{url_for("profile")}">Profile</a>'

@app.route('/jfdklsjfldskjfkldsjfiewojsfldk')
def profile():
    return 'Welcome to your profile page!'

if __name__ == '__main__':
    app.run(debug=True)


# 🎯 Takeaway:
# url_for() doesn't care about the actual route path (/jfdklsjfldskjfkldsjfiewojsfldk) — it cares about the function name (my_custom_route).

# This allows you to change the route path freely and Flask will take care of generating the correct URL dynamically.

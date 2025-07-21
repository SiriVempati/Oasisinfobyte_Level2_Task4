from flask import Flask, request, redirect, session, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {}
style = """
<style>
  body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    text-align: center;
    margin-top: 80px;
  }

  h2 {
    color: #333;
  }

  form {
    display: inline-block;
    background-color: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }

  input[type="text"], input[type="password"] {
    padding: 10px;
    margin: 8px 0;
    border: 1px solid #ccc;
    border-radius: 6px;
    width: 100%;
  }

  input[type="submit"] {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
  }

  input[type="submit"]:hover {
    background-color: #45a049;
  }

  a {
    text-decoration: none;
    color: #007BFF;
  }

  a:hover {
    text-decoration: underline;
  }

  .container {
    width: 300px;
    margin: 0 auto;
  }
</style>
"""
login_html = f'''
<!DOCTYPE html>
<html>
<head>
<title>Login</title>
{style}
</head>
<body>
  <div class="container">
    <h2>Login</h2>
    <form method="post">
      <input type="text" name="username" placeholder="Username" required><br>
      <input type="password" name="password" placeholder="Password" required><br><br>
      <input type="submit" value="Login">
    </form>
    <p>Don't have an account? <a href="/register">Register</a></p>
  </div>
</body>
</html>
'''

register_html = f'''
<!DOCTYPE html>
<html>
<head>
<title>Register</title>
{style}
</head>
<body>
  <div class="container">
    <h2>Register</h2>
    <form method="post">
      <input type="text" name="username" placeholder="Username" required><br>
      <input type="password" name="password" placeholder="Password" required><br><br>
      <input type="submit" value="Register">
    </form>
    <p>Already have an account? <a href="/login">Login</a></p>
  </div>
</body>
</html>
'''

dashboard_html = f'''
<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>
{style}
</head>
<body>
  <div class="container">
    <h2>Welcome, {{ username }}!</h2>
    <p>This is a secured page.</p>
    <a href="/logout">Logout</a>
  </div>
</body>
</html>
'''
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists!"
        users[username] = password
        return redirect(url_for('login'))
    return render_template_string(register_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials!"
    return render_template_string(login_html)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template_string(dashboard_html, username=session['user'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)

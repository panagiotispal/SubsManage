import os
import csv
import io
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv 

# Φόρτωση ρυθμίσεων από .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_key_12345')
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# --- ΡΥΘΜΙΣΕΙΣ EMAIL ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
scheduler = APScheduler()

# --- ΣΥΝΔΕΣΗ ΜΕ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ ---
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'amritpal'), 
        database=os.getenv('DB_NAME', 'subscription_tracker')
    )

def execute_query(query, params=(), fetch_one=False, fetch_all=False, commit=False):
    conn = None
    cursor = None
    result = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute(query, params)
        if commit: conn.commit()
        if fetch_one: result = cursor.fetchone()
        elif fetch_all: result = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"DB Error: {err}") 
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    return result

# --- ΒΟΗΘΗΤΙΚΗ: ΑΠΟΣΤΟΛΗ EMAIL ---
def send_email(to, subject, body):
    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
        msg.body = body
        with app.app_context():
            mail.send(msg)
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# --- SCHEDULER: ΕΛΕΓΧΟΣ ΑΝΑΝΕΩΣΕΩΝ ---
def check_upcoming_renewals():
    with app.app_context():
        query = "SELECT s.*, u.email, u.username FROM subscriptions s JOIN users u ON s.user_id = u.id"
        subscriptions = execute_query(query, fetch_all=True) or []
        
        today = date.today()
        target_date = today + timedelta(days=3)

        for sub in subscriptions:
            start = sub['start_date']
            if isinstance(start, str):
                try: start = datetime.strptime(start, '%Y-%m-%d').date()
                except ValueError: continue

            # Υπολογισμός Επόμενης Χρέωσης
            next_d = start
            while next_d <= today:
                if sub['billing_cycle'] == 'Monthly': next_d += relativedelta(months=1)
                elif sub['billing_cycle'] == 'Yearly': next_d += relativedelta(years=1)
                elif sub['billing_cycle'] == 'Weekly': next_d += relativedelta(weeks=1)
                else: break
            
            # Αν λήγει σε 3 μέρες
            if next_d == target_date:
                subject = f"⚠️ Υπενθύμιση: {sub['name']}"
                body = f"Γεια σου {sub['username']},\n\nΗ συνδρομή {sub['name']} ({sub['price']}€) ανανεώνεται σε 3 μέρες ({next_d})."
                send_email(sub['email'], subject, body)

# --- ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if execute_query("SELECT * FROM users WHERE email = %s", (email,), fetch_one=True):
            flash("Το email υπάρχει ήδη.")
            return redirect(url_for('register'))

        execute_query("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                      (username, email, hashed_password), commit=True)
        
        send_email(email, "Καλώς ήρθες!", f"Γεια σου {username}, καλώς ήρθες στο SubsManage! Ξεκίνα να καταγράφεις τις συνδρομές σου.")
        flash("Η εγγραφή πέτυχε! Κάνε είσοδο.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = execute_query("SELECT * FROM users WHERE email = %s", (email,), fetch_one=True)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['profile_pic'] = user.get('profile_pic', 'default.png')
            return redirect(url_for('home'))
        else:
            flash("Λάθος στοιχεία")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = execute_query("SELECT * FROM users WHERE email = %s", (email,), fetch_one=True)
        
        if user:
            # Δημιουργία τυχαίου κωδικού
            chars = string.ascii_letters + string.digits + "!@#$%"
            temp_password = ''.join(random.choice(chars) for i in range(8))
            hashed_pw = generate_password_hash(temp_password)
            
            execute_query("UPDATE users SET password = %s WHERE email = %s", (hashed_pw, email), commit=True)
            
            send_email(email, "🔐 Επαναφορά Κωδικού", f"Ο νέος προσωρινός κωδικός σας είναι:\n\n{temp_password}\n\nΑλλάξτε τον από το προφίλ σας.")
            flash("Εστάλη προσωρινός κωδικός στο email σας.")
            return redirect(url_for('login'))
        else:
            flash("Δεν βρέθηκε χρήστης με αυτό το email.")
    return render_template('forgot_password.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = execute_query("SELECT * FROM users WHERE id = %s", (session['user_id'],), fetch_one=True)

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']
        
        filename = user['profile_pic']
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"{session['user_id']}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if new_password:
            hashed = generate_password_hash(new_password)
            execute_query("UPDATE users SET username=%s, email=%s, password=%s, profile_pic=%s WHERE id=%s", 
                          (new_username, new_email, hashed, filename, session['user_id']), commit=True)
        else:
            execute_query("UPDATE users SET username=%s, email=%s, profile_pic=%s WHERE id=%s", 
                          (new_username, new_email, filename, session['user_id']), commit=True)
        
        session['username'] = new_username
        session['profile_pic'] = filename
        flash("Το προφίλ ενημερώθηκε!")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/')
@app.route('/')
def home():
    # Αρχικοποίηση μεταβλητών (για την περίπτωση που δεν είναι συνδεδεμένος)
    subscriptions = []
    total_monthly = 0.0
    total_yearly = 0.0
    total_spent = 0.0
    count = 0
    category_totals = {}
    username = "Επισκέπτης"
    profile_pic = "default.png"
    
    # ΜΟΝΟ αν είναι συνδεδεμένος τραβάμε δεδομένα από τη βάση
    if 'user_id' in session:
        subscriptions = execute_query("SELECT * FROM subscriptions WHERE user_id = %s", (session['user_id'],), fetch_all=True) or []
        user = execute_query("SELECT username, profile_pic FROM users WHERE id = %s", (session['user_id'],), fetch_one=True)
        if user:
            username = user['username']
            profile_pic = user.get('profile_pic', 'default.png')

        # --- ΥΠΟΛΟΓΙΣΜΟΙ (ΙΔΙΟΙ ΜΕ ΠΡΙΝ) ---
        SERVICE_DOMAINS = {
            'netflix': 'netflix.com', 'spotify': 'spotify.com',
            'youtube': 'youtube.com', 'google': 'google.com', 'apple': 'apple.com',
            'icloud': 'apple.com', 'amazon': 'amazon.com', 'prime': 'amazon.com',
            'disney': 'disneyplus.com', 'hulu': 'hulu.com', 'hbo': 'hbo.com',
            'playstation': 'playstation.com', 'xbox': 'xbox.com', 'steam': 'steampowered.com',
            'dropbox': 'dropbox.com', 'adobe': 'adobe.com', 'canva': 'canva.com',
            'slack': 'slack.com', 'zoom': 'zoom.us', 'openai': 'openai.com',
            'gym': 'gymshark.com' 
        }

        today = date.today()

        for sub in subscriptions:
            # Logo Logic
            name_lower = sub['name'].lower()
            domain = 'google.com'
            found = False
            for key, d in SERVICE_DOMAINS.items():
                if key in name_lower:
                    domain = d
                    found = True
                    break
            if not found: domain = f"{name_lower.replace(' ', '')}.com"
            sub['logo'] = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"

            # Date Logic
            start = sub['start_date']
            if isinstance(start, str): 
                try: start = datetime.strptime(start, '%Y-%m-%d').date()
                except ValueError: start = today

            price = float(sub['price'])
            
            # Category Stats
            cat = sub.get('category', 'Other')
            if cat not in category_totals: category_totals[cat] = 0
            category_totals[cat] += price

            # Calculations
            paid_count = 0
            temp_d = start
            while temp_d <= today:
                paid_count += 1
                if sub['billing_cycle'] == 'Monthly': temp_d += relativedelta(months=1)
                elif sub['billing_cycle'] == 'Yearly': temp_d += relativedelta(years=1)
                elif sub['billing_cycle'] == 'Weekly': temp_d += relativedelta(weeks=1)
                else: break
            total_spent += (paid_count * price)

            next_d = start
            while next_d <= today:
                if sub['billing_cycle'] == 'Monthly': next_d += relativedelta(months=1)
                elif sub['billing_cycle'] == 'Yearly': next_d += relativedelta(years=1)
                elif sub['billing_cycle'] == 'Weekly': next_d += relativedelta(weeks=1)
                else: break
            sub['next_billing'] = next_d

            if sub['billing_cycle'] == 'Monthly':
                total_monthly += price
                total_yearly += price * 12
            elif sub['billing_cycle'] == 'Yearly':
                total_monthly += price / 12
                total_yearly += price
            elif sub['billing_cycle'] == 'Weekly':
                total_monthly += price * 4.33
                total_yearly += price * 52

    # Επιστροφή template (είτε με δεδομένα είτε κενό)
    return render_template('index.html', subscriptions=subscriptions, username=username,
                           profile_pic=profile_pic, total_monthly=round(total_monthly, 2),
                           total_yearly=round(total_yearly, 2), total_spent=round(total_spent, 2),
                           count=count, category_totals=category_totals)

@app.route('/add', methods=['GET', 'POST'])
def add_subscription():
    if 'user_id' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        category = request.form.get('category', 'Other')
        execute_query("INSERT INTO subscriptions (name, price, billing_cycle, start_date, category, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
                      (request.form['name'], request.form['price'], request.form['billing_cycle'], request.form['start_date'], category, session['user_id']), commit=True)
        return redirect(url_for('home'))
    return render_template('add.html')

# --- ROUTE: EDIT SUBSCRIPTION (Η συνάρτηση που έλειπε) ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_subscription(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    # 1. Βρίσκουμε τη συνδρομή
    subscription = execute_query("SELECT * FROM subscriptions WHERE id = %s AND user_id = %s", 
                                 (id, session['user_id']), fetch_one=True)

    if not subscription:
        flash("Η συνδρομή δεν βρέθηκε.")
        return redirect(url_for('home'))

    # 2. Αποθήκευση αλλαγών (POST)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        billing_cycle = request.form['billing_cycle']
        start_date = request.form['start_date']
        category = request.form.get('category', 'Other')

        execute_query("""
            UPDATE subscriptions 
            SET name=%s, price=%s, billing_cycle=%s, start_date=%s, category=%s 
            WHERE id=%s AND user_id=%s
            """, (name, price, billing_cycle, start_date, category, id, session['user_id']), commit=True)
        
        flash("Η συνδρομή ενημερώθηκε!")
        return redirect(url_for('home'))

    # 3. Εμφάνιση της φόρμας (GET)
    return render_template('edit.html', sub=subscription)

@app.route('/export')
def export_data():
    if 'user_id' not in session: return redirect(url_for('login'))
    subscriptions = execute_query("SELECT name, price, billing_cycle, start_date, category FROM subscriptions WHERE user_id = %s", (session['user_id'],), fetch_all=True)
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Name', 'Price', 'Billing Cycle', 'Start Date', 'Category']) 
    for sub in subscriptions:
        cw.writerow([sub['name'], sub['price'], sub['billing_cycle'], sub['start_date'], sub['category']])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=my_subscriptions.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/delete/<int:id>')
def delete_subscription(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    execute_query("DELETE FROM subscriptions WHERE id=%s AND user_id=%s", (id, session['user_id']), commit=True)
    return redirect(url_for('home'))

if __name__ == '__main__':
    scheduler.add_job(id='Scheduled Task', func=check_upcoming_renewals, trigger="interval", days=1)
    scheduler.start()
    # ΑΛΛΑΓΗ ΕΔΩ: host='0.0.0.0' σημαίνει "να είσαι ανοιχτός στο δίκτυο"
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
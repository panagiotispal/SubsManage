# ⚡ SubsManage - Ultimate Subscription Tracker

Το **SubsManage** είναι μια ολοκληρωμένη **Full-Stack Web Εφαρμογή** για την οργάνωση, παρακολούθηση και διαχείριση συνδρομητικών υπηρεσιών (SaaS, Streaming, Utilities, Gym κ.λπ.).

Σκοπός της εφαρμογής είναι να δώσει στον χρήστη τον πλήρη έλεγχο των οικονομικών του, προσφέροντας εργαλεία προϋπολογισμού (Budgeting), αναλυτικά στατιστικά και έξυπνες ειδοποιήσεις, μέσα από ένα μοντέρνο και φιλικό περιβάλλον χρήστη (UI).
<img width="1699" height="785" alt="Screenshot_23" src="https://github.com/user-attachments/assets/ba62566a-ce23-4224-a3ea-f88230a62f34" />
<img width="1709" height="941" alt="Screenshot_20" src="https://github.com/user-attachments/assets/5fc6428b-ae19-4f1f-8a9b-d239d3332d87" />
<img width="1082" height="885" alt="Screenshot_19" src="https://github.com/user-attachments/assets/86c6b93a-6e77-4659-bb3e-de384da965fc" />

---

## 🚀 Βασικές Λειτουργίες (Features)

### 👤 Διαχείριση Χρήστη & Ασφάλεια
* **Authentication:** Πλήρες σύστημα Εγγραφής & Σύνδεσης.
* **Persistent Session:** Λειτουργία "Να με θυμάσαι" (Remember Me) για παραμονή σύνδεσης έως 30 μέρες.
* **Password Reset:** Διαδικασία ανάκτησης κωδικού μέσω Email (με προσωρινό κωδικό).
* **Προφίλ:** Δυνατότητα αλλαγής στοιχείων, κωδικού και φωτογραφίας προφίλ (με αυτόματη προσαρμογή/crop σε κύκλο).

### 💸 Οικονομικός Έλεγχος & Budgeting
* **Dashboard:** Συγκεντρωτική εικόνα Μηνιαίου/Ετήσιου κόστους και Συνολικών Εξόδων (Lifetime).
* **Smart Budget:** Ορισμός μηνιαίου χρηματικού ορίου.
    * **Οπτική Μπάρα Προόδου:** Γεμίζει δυναμικά και αλλάζει χρώμα (Πράσινο -> Κίτρινο -> Κόκκινο) ανάλογα με την κατανάλωση.
* **Analytics:** Δυναμικό γράφημα (Doughnut Chart) για την κατανομή εξόδων ανά κατηγορία.

### 📋 Διαχείριση Συνδρομών (CRUD)
* **Προσθήκη & Επεξεργασία:** Εύκολη εισαγωγή συνδρομών με επιλογή κύκλου χρέωσης (Μηνιαία, Ετήσια, Εβδομαδιαία).
* **Smart Pricing Logic:** Αυτόματη συμπλήρωση τιμών για δημοφιλείς υπηρεσίες (π.χ. Netflix, Spotify) μέσω JavaScript.
* **Κατηγοριοποίηση:** Ταξινόμηση με χρωματιστά Neon Badges (Entertainment, Work, Health, κλπ.).
* **Αναζήτηση & Export:** Ζωντανή αναζήτηση (Search) και εξαγωγή δεδομένων σε αρχείο **CSV**.
* **Visuals:** Αυτόματη ανίχνευση και εμφάνιση λογοτύπων (Favicons) των υπηρεσιών.

### ⚙️ Αυτοματισμοί
* **Email Alerts:** Αυτόματη αποστολή ενημερωτικού Email 3 μέρες πριν την ανανέωση μιας συνδρομής (μέσω Python APScheduler).

### 🎨 UI/UX Design
* **Glassmorphism:** Μοντέρνος σχεδιασμός με εφέ γυαλιού, διαφάνειες και θόλωμα (Blur).
* **Responsive:** Πλήρως προσαρμόσιμο σε κινητά τηλέφωνα (Mobile App Layout με κάτω μπάρα πλοήγησης).
* **Animations:** Κινούμενο Gradient Background και ομαλές μεταβάσεις (Fade In/Up).

---

## 🛠️ Τεχνολογίες & Βιβλιοθήκες

Το project αναπτύχθηκε χρησιμοποιώντας τις εξής τεχνολογίες:

### Backend (Python)
* **Flask:** Το βασικό Web Framework.
* **MySQL Connector:** Για τη σύνδεση με τη βάση δεδομένων.
* **Flask-Mail:** Για την αποστολή emails (Reset Password & Ειδοποιήσεις).
* **Flask-APScheduler:** Για τον προγραμματισμό εργασιών στο παρασκήνιο (Cron jobs).
* **Werkzeug Security:** Για την ασφαλή κρυπτογράφηση κωδικών (Hashing).
* **Python-Dotenv:** Για τη διαχείριση ευαίσθητων δεδομένων (.env).

### Frontend
* **HTML5 / CSS3**: Custom CSS με χρήση CSS Variables, Flexbox και Animations.
* **JavaScript (Vanilla)**: Για τη λογική του Frontend (Live Preview, Smart Pricing, Search).
* **Bootstrap 5**: Για το Grid System και τα UI Components.
* **Chart.js**: Για την απεικόνιση των γραφημάτων.
* **FontAwesome**: Για τα εικονίδια.
* **Google Fonts (Inter)**: Για τη μοντέρνα τυπογραφία.

### Database
* **MySQL**: Σχεσιακή βάση δεδομένων για αποθήκευση χρηστών και συνδρομών.

---

## 📦 Οδηγίες Εγκατάστασης (Setup Guide)

Ακολουθήστε τα παρακάτω βήματα για να τρέξετε την εφαρμογή τοπικά.

### 1. Κλωνοποίηση (Clone)
Κατεβάστε τον κώδικα στον υπολογιστή σας:
```bash
git clone [https://github.com/ΤΟ_ONOMA_ΣΟΥ/SubsManage.git](https://github.com/ΤΟ_ONOMA_ΣΟΥ/SubsManage.git)
cd SubsManage
Φυσικά! Παρακάτω είναι όλο το περιεχόμενο συγκεντρωμένο σε ένα ενιαίο κείμενο, έτοιμο να το κάνεις αντιγραφή και επικόλληση στο αρχείο README.md του GitHub σου.

Περιλαμβάνει τα πάντα: περιγραφή, τεχνολογίες, οδηγίες εγκατάστασης και τον κώδικα για τη βάση δεδομένων.

Markdown

# ⚡ SubsManage - Ultimate Subscription Tracker

Το **SubsManage** είναι μια ολοκληρωμένη **Full-Stack Web Εφαρμογή** για την οργάνωση, παρακολούθηση και διαχείριση συνδρομητικών υπηρεσιών (SaaS, Streaming, Utilities, Gym κ.λπ.).

Σκοπός της εφαρμογής είναι να δώσει στον χρήστη τον πλήρη έλεγχο των οικονομικών του, προσφέροντας εργαλεία προϋπολογισμού (Budgeting), αναλυτικά στατιστικά και έξυπνες ειδοποιήσεις, μέσα από ένα μοντέρνο και φιλικό περιβάλλον χρήστη (UI).

---

## 🚀 Βασικές Λειτουργίες (Features)

### 👤 Διαχείριση Χρήστη & Ασφάλεια
* **Authentication:** Πλήρες σύστημα Εγγραφής & Σύνδεσης.
* **Persistent Session:** Λειτουργία "Να με θυμάσαι" (Remember Me) για παραμονή σύνδεσης έως 30 μέρες.
* **Password Reset:** Διαδικασία ανάκτησης κωδικού μέσω Email (με προσωρινό κωδικό).
* **Προφίλ:** Δυνατότητα αλλαγής στοιχείων, κωδικού και φωτογραφίας προφίλ (με αυτόματη προσαρμογή/crop σε κύκλο).

### 💸 Οικονομικός Έλεγχος & Budgeting
* **Dashboard:** Συγκεντρωτική εικόνα Μηνιαίου/Ετήσιου κόστους και Συνολικών Εξόδων (Lifetime).
* **Smart Budget:** Ορισμός μηνιαίου χρηματικού ορίου.
    * **Οπτική Μπάρα Προόδου:** Γεμίζει δυναμικά και αλλάζει χρώμα (Πράσινο -> Κίτρινο -> Κόκκινο) ανάλογα με την κατανάλωση.
* **Analytics:** Δυναμικό γράφημα (Doughnut Chart) για την κατανομή εξόδων ανά κατηγορία.

### 📋 Διαχείριση Συνδρομών (CRUD)
* **Προσθήκη & Επεξεργασία:** Εύκολη εισαγωγή συνδρομών με επιλογή κύκλου χρέωσης (Μηνιαία, Ετήσια, Εβδομαδιαία).
* **Smart Pricing Logic:** Αυτόματη συμπλήρωση τιμών για δημοφιλείς υπηρεσίες (π.χ. Netflix, Spotify) μέσω JavaScript.
* **Κατηγοριοποίηση:** Ταξινόμηση με χρωματιστά Neon Badges (Entertainment, Work, Health, κλπ.).
* **Αναζήτηση & Export:** Ζωντανή αναζήτηση (Search) και εξαγωγή δεδομένων σε αρχείο **CSV**.
* **Visuals:** Αυτόματη ανίχνευση και εμφάνιση λογοτύπων (Favicons) των υπηρεσιών.

### ⚙️ Αυτοματισμοί
* **Email Alerts:** Αυτόματη αποστολή ενημερωτικού Email 3 μέρες πριν την ανανέωση μιας συνδρομής (μέσω Python APScheduler).

### 🎨 UI/UX Design
* **Glassmorphism:** Μοντέρνος σχεδιασμός με εφέ γυαλιού, διαφάνειες και θόλωμα (Blur).
* **Responsive:** Πλήρως προσαρμόσιμο σε κινητά τηλέφωνα (Mobile App Layout με κάτω μπάρα πλοήγησης).
* **Animations:** Κινούμενο Gradient Background και ομαλές μεταβάσεις (Fade In/Up).

---

## 🛠️ Τεχνολογίες & Βιβλιοθήκες

Το project αναπτύχθηκε χρησιμοποιώντας τις εξής τεχνολογίες:

### Backend (Python)
* **Flask:** Το βασικό Web Framework.
* **MySQL Connector:** Για τη σύνδεση με τη βάση δεδομένων.
* **Flask-Mail:** Για την αποστολή emails (Reset Password & Ειδοποιήσεις).
* **Flask-APScheduler:** Για τον προγραμματισμό εργασιών στο παρασκήνιο (Cron jobs).
* **Werkzeug Security:** Για την ασφαλή κρυπτογράφηση κωδικών (Hashing).
* **Python-Dotenv:** Για τη διαχείριση ευαίσθητων δεδομένων (.env).

### Frontend
* **HTML5 / CSS3**: Custom CSS με χρήση CSS Variables, Flexbox και Animations.
* **JavaScript (Vanilla)**: Για τη λογική του Frontend (Live Preview, Smart Pricing, Search).
* **Bootstrap 5**: Για το Grid System και τα UI Components.
* **Chart.js**: Για την απεικόνιση των γραφημάτων.
* **FontAwesome**: Για τα εικονίδια.
* **Google Fonts (Inter)**: Για τη μοντέρνα τυπογραφία.

### Database
* **MySQL**: Σχεσιακή βάση δεδομένων για αποθήκευση χρηστών και συνδρομών.

---

## 📦 Οδηγίες Εγκατάστασης (Setup Guide)

Ακολουθήστε τα παρακάτω βήματα για να τρέξετε την εφαρμογή τοπικά.

### 1. Κλωνοποίηση (Clone)
Κατεβάστε τον κώδικα στον υπολογιστή σας:
```bash
git clone [https://github.com/ΤΟ_ONOMA_ΣΟΥ/SubsManage.git](https://github.com/ΤΟ_ONOMA_ΣΟΥ/SubsManage.git)
cd SubsManage
2. Εγκατάσταση Απαιτήσεων
Δημιουργήστε ένα virtual environment (προαιρετικά) και εγκαταστήστε τις βιβλιοθήκες:

Bash

pip install -r requirements.txt
(Αν δεν έχετε αρχείο requirements.txt, εγκαταστήστε τα χειροκίνητα: pip install Flask mysql-connector-python Flask-Mail Flask-APScheduler python-dotenv python-dateutil)

3. Ρύθμιση Βάσης Δεδομένων (MySQL)
Ανοίξτε τη MySQL και τρέξτε τον παρακάτω κώδικα για να δημιουργηθούν οι πίνακες:

SQL

CREATE DATABASE subscription_tracker;
USE subscription_tracker;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_pic VARCHAR(255) DEFAULT 'default.png',
    monthly_budget DECIMAL(10,2) DEFAULT 0.00
);

CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    billing_cycle VARCHAR(50),
    start_date DATE,
    category VARCHAR(50) DEFAULT 'Other',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
4. Ρύθμιση Περιβάλλοντος (.env)
Δημιουργήστε ένα αρχείο με όνομα .env στον κεντρικό φάκελο και προσθέστε τα δικά σας στοιχεία:

Απόσπασμα κώδικα

SECRET_KEY=μια_τυχαία_φράση_ασφαλείας
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=ο_κωδικός_της_mysql_σου
DB_NAME=subscription_tracker

# Ρυθμίσεις Email (π.χ. για Gmail χρησιμοποιήστε App Password)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=το_email_σου@gmail.com
MAIL_PASSWORD=ο_κωδικός_εφαρμογής_σου
5. Εκτέλεση Εφαρμογής
Bash

python app.py
Η εφαρμογή θα είναι διαθέσιμη στη διεύθυνση: http://localhost:5000

📱 Χρήση από Κινητό (Local Network)
Για να δείτε την εφαρμογή από το κινητό σας (ενώ είστε στο ίδιο Wi-Fi):

Βρείτε την IP του υπολογιστή σας (εντολή ipconfig ή ifconfig).

Στο app.py, βεβαιωθείτε ότι έχετε: app.run(host='0.0.0.0').

Ανοίξτε τον browser του κινητού και πληκτρολογήστε: http://192.168.X.X:5000

📄 License
This project is for educational purposes.

Made with ❤️ by [PANAGIOTIS PAL]

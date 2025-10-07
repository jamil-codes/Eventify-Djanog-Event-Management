# 🎟️ Eventify — Discover, Create & Manage Events

**Eventify** is a modern event management platform built with **Django**.  
It enables organizers to create, manage, and sell tickets for events — while attendees can explore, book, and check in seamlessly.

---

## 🚀 Features

### 🎫 For Attendees
- Browse upcoming and featured events
- Secure online payments via **Stripe**
- Instant digital ticket generation
- View purchase history and ticket QR codes
- Smooth check-in experience (real-time status updates)

### 🧑‍💼 For Organizers / Admins
- Create and manage events (restricted to verified organizers/admins)
- Configure multiple ticket types per event (price, quantity, limits)
- Track attendees and sales
- Automated reservation expiry and pending handling
- Manage Stripe integration directly from the dashboard

### 💬 General Features
- Contact form
- Dynamic homepage with featured events and locations
- Fully responsive design (Tailwind + DaisyUI)
- Clean, modular Django app structure

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|----------------|
| **Frontend** | TailwindCSS + DaisyUI | 
| **Backend** | Django| |
| **Database** | SQLite (dev)| 
| **Payments** | Stripe | 
| **Authentication** | Complete Custom Authentication |
| **Media Handling** | Django ImageField + Thumbnail |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/jamil-codes/eventify.git
cd eventify
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # (Windows)
source venv/bin/activate  # (Linux / macOS)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables (`.env`)

Create a `.env` file in the root directory with:

```
SECRET_KEY = "j!(!zeuh@e=l*3*i&gdfqq60g8kk3m_y%4p@2nqetzh3cp9ptl8c_nh=t#4sh8)1pfx489j0hav+xplt@m8mvn90utsiaxal9r(c"
DEBUG=1
MAX_EVENTS_PER_PAGE=12
STRIPE_API_KEY = Your Stripe Key Here 
```

### 5️⃣ Apply Migrations & Run

```
python manage.py migrate
python manage.py runserver
```

Access at → [http://127.0.0.1:8000](http://127.0.0.1:8000)


> [!WARNING]   
> If you encounter issues related to *WeasyPrint* while generating PDFs, refer to the **[official WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/latest/first_steps.html)**.  
> WeasyPrint requires additional **system dependencies** — especially on **Windows** — such as:
> - GTK  
> - Pango  
> - libgobject  
>
> Make sure these are installed properly to enable full PDF rendering support.


---

## 🧠 User Roles

| Role                              | Permissions                               |
| --------------------------------- | ----------------------------------------- |
| **Admin (is_staff=True)**         | Full access to all events, tickets, users |
| **Organizer (is_organizer=True)** | Can create/manage own events              |
| **Attendee (default)**            | Can browse & purchase tickets only        |

---

## 📁 Project Structure

```
eventify/
├── events/               # Core event app
│   ├── models.py         # Event, Ticket, TicketType models
│   ├── views.py          # CRUD logic & Stripe integration
│   ├── urls.py
│   └── templates/events/
│       ├── add_event.html
│       ├── event_detail.html
│       └── events_grid.html
├── static/               # Tailwind + assets
├── templates/            # base.html, index.html, etc.
├── eventify/             # main Django config
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

---

## 🧾 Stripe Integration

* Each `TicketType` auto-creates a Stripe Product + Price.
* `Ticket` model stores Stripe session, price, and product IDs.
* Automatic conversion to cents (`price * 100`).
* Pending reservations expire after 15 minutes.

---

## 📧 Contact Form

Visitors can send inquiries directly from the homepage.


## 💡 Developer Notes

* Default superuser created with `python manage.py createsuperuser`
* Organizers can be toggled via admin panel (`is_organizer=True`)
* Event creation form restricted using `@user_passes_test`
* Fully timezone-aware (`django.utils.timezone`)
* Designed to be deployed on **Render / Railway / Vercel + PostgreSQL**

---

## 🧍 Author

**👨‍💻 Jamil Ahmed**
Full-Stack Web Developer (Next.js + Django REST)
🌐 [jamilcodes.com](https://jamilcodes.com)
✉️ [hello@jamilcodes.com](mailto:hello@jamilcodes.com)
🐙 [github.com/jamil-codes](https://github.com/jamil-codes)

---

## 🛡️ License

Licensed under the **MIT License** — feel free to use and modify with credit.
Copyright © 2025 **Jamil Codes**

---

> “Discipline is the bridge between goals and accomplishment.” — Jim Rohn


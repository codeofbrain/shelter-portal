
# Social Portal for Shelter & Community Hub

A Django-based web platform designed to streamline communication and coordination between **residents (refugees from Ukraine)**, **shelter management (administration)**, and **housemasters (technical/maintenance staff)**.

This project was built to automate internal processes, improve response times for maintenance requests, and ensure vital organizational updates reach every resident instantly.

---

## Key Features

The portal is split into logical workflows tailored for three distinct user roles:

* **For Residents:**
    * **Personal Dashboard:** View housing rules, assignment details, and status updates.
    * **Interactive Duty Roster:** View the digital shift schedule to see current cleaning duties and community tasks in real-time.
    * **Announcement Board:** View official updates from management and publish personal notices (e.g., lost and found items,communitysuggestions, or initiatives). 
    * **Maintenance Requests:** Easily submit technical tickets directly to housemasters for room repairs or utility issues.
* **For Housemasters (Technical Staff):**
    * **Issue Tracker:** A streamlined dashboard to view pending, ongoing, and completed repair requests submitted by residents.
    * **Status Management:** Update ticket statuses in real-time to keep residents and administration informed.
* **For Management (Administration):**
    * **Global Announcements:** Publish important notices and regulatory guidelines that instantly appear on all resident dashboards.
    * **Overview Control:** Monitor shelter-wide requests and operational statuses through the integrated Django administrative panel.
    * **Roster Management:** Easily generate, update, and manage the room cleaning and duty schedules for all residents.

---

## Tech Stack

* **Backend:** Python 3, Django (Full-stack Framework)
* **Database:** SQLite (Local development) / Structured for easy migration to production-grade relational databases.
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap5

---

## Local Installation & Setup

1. **Clone the repository:**
   git clone [https://github.com/codeofbrain/shelter-portal.git](https://github.com/codeofbrain/shelter-portal.git)
   cd shelter-portal

2. **Create and activate a virtual environment:**
     python -m venv my_env
     # For Windows:
     my_env\Scripts\activate

3. **Install dependencies:**
     pip install django
     Or pip install -r requirements.txt if a     requirements  file is present

4. **Apply database migrations:**
     python manage.py migrate

5. **Run the local development server:**
     python manage.py runserver

* **The portal will be accessible in your browser at: http://127.0.0.1:8000/

Author
codeofbrain — GitHub Profile
   ```bash
   git clone [https://github.com/codeofbrain/shelter-portal.git](https://github.com/codeofbrain/shelter-portal.git)
   cd shelter-portal

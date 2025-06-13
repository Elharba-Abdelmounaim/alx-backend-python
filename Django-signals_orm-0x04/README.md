# Django Signals: User Notification System

This project demonstrates how to use **Django signals** to implement a simple user notification system. When a user receives a new message, a notification is automatically created using Django’s `post_save` signal.

---

## 📌 Objective

Automatically notify users when they receive a new message using Django signals.

---

## 📂 Models

- **Message**
  - `sender`: User who sent the message.
  - `receiver`: User who receives the message.
  - `content`: Text content of the message.
  - `timestamp`: Auto-generated timestamp.

- **Notification**
  - `user`: User who will receive the notification.
  - `message`: The related message.
  - `is_read`: Boolean flag.
  - `created_at`: Auto-generated timestamp.

---

## ⚙️ Signal

`post_save` signal on the `Message` model triggers a `Notification` instance creation for the receiving user.

```python
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

```

## 🧪 Testing
The project includes a basic unit test to verify that a notification is created when a message is sent.

```

python manage.py test

```

## 🚀 Setup Instructions

```

# Step 1: Install dependencies
pip install django

# Step 2: Apply migrations
python manage.py makemigrations
python manage.py migrate

# Step 3: Run server
python manage.py runserver

```

### 📁 Project Structure

```

Django-signals_orm-0x04/
├── main_project/
├── messaging/
│   ├── models.py
│   ├── signals.py
│   ├── apps.py
│   ├── tests.py
├── db.sqlite3
├── manage.py
└── README.md

```

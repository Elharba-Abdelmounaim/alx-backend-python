# chats/middleware.py

from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    # Constructor: called once when the server starts
    def __init__(self, get_response):
        self.get_response = get_response

    # This method is called for each request
    def __call__(self, request):
        # Get username if authenticated, else Anonymous
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"
        
        # Create the log entry string
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Append the log entry to a file
        with open("chats/requests.log", "a") as log_file:
            log_file.write(log_entry)

        # Call the next middleware or view
        return self.get_response(request)
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour

        # Block access if time is NOT between 18:00 and 21:00 (6PM to 9PM)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Chat access is restricted at this time.")

        return self.get_response(request)
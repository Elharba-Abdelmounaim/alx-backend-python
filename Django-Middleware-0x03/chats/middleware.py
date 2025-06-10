# chats/middleware.py

from datetime import datetime
import time
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
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        # Call the next middleware or view
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour > 22:  # خارج الفترة من 6 مساءً إلى 9 مساءً
            return HttpResponseForbidden("❌ Chat access is restricted at this time.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # { ip_address: [timestamps] }

    def __call__(self, request):
        # نراقب فقط POST requests للرسائل (مثلاً لمسار /chat/send)
        if request.method == "POST" and request.path.startswith("/chat"):
            ip = self.get_client_ip(request)
            now = time.time()

            timestamps = self.message_log.get(ip, [])
            # حذف الطوابع الزمنية الأقدم من دقيقة (60 ثانية)
            timestamps = [ts for ts in timestamps if now - ts < 60]

            if len(timestamps) >= 5:
                return HttpResponseForbidden("🚫 Message rate limit exceeded. Try later.")

            # إضافة الطابع الزمني الحالي
            timestamps.append(now)
            self.message_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        # الطريقة الشائعة لجلب IP العميل
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # نفترض أن user.role موجود ويحتوي على اسم الدور
        # إذا لم يكن المستخدم مسجل دخول أو دوره غير مسموح به
        if not user or not user.is_authenticated or user.role not in ["admin", "moderator"]:
            return HttpResponseForbidden("🚫 You do not have permission to access this resource.")

        return self.get_response(request)
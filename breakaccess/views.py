from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import authenticate, login as auth_login 
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        faculty= request.POST['faculty']
        department = request.POST['department']
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, faculty=faculty, department=department)
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user) 
            return redirect(f'/home/{user.id}/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def home(request, user_id):
    try:
        user_profile_data = User.objects.get(pk=user_id)
        profile = None
        try:
            profile = Profile.objects.get(user=user_profile_data)
        except Profile.DoesNotExist:
            pass

        # ****** ตรวจสอบบรรทัดนี้ให้แน่ใจว่าถูกต้อง ******
        # ค่านี้ต้องเป็น True สำหรับ Admin และ False สำหรับ Non-Admin
        is_current_user_admin = request.user.is_staff or request.user.is_superuser

        context = {
            'user': user_profile_data,
            'profile': profile,
            'is_admin_user': is_current_user_admin, # ค่านี้ถูกส่งไป
            'current_user_id': request.user.id
        }
        return render(request, 'home.html', context)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('login')
    
@login_required
def admin_dashboard_js_controlled(request):
    # ส่งสถานะ is_admin ไปยัง template
    is_admin_user = request.user.is_staff or request.user.is_superuser
    all_users = User.objects.all().exclude(username=request.user.username) # ไม่รวมตัวเอง
    return render(request, 'admin_dashboard_js_controlled.html', {
        'is_admin_user': is_admin_user,
        'users': all_users
    })

# ฟังก์ชันสำหรับลบผู้ใช้ - **นี่คือจุดที่มีช่องโหว่**
# ไม่มี Decorator ตรวจสอบสิทธิ์ Admin ที่นี่!
@login_required # ต้องล็อกอินถึงจะเข้าถึงได้ แต่ไม่ต้องเป็น Admin
def insecure_delete_user_js_controlled(request, user_id):
    if request.method == 'POST':
        # ตรวจสอบว่าเป็นผู้ใช้ที่ล็อกอินอยู่หรือไม่ เพื่อไม่ให้ลบตัวเอง
        if request.user.id == user_id:
            return HttpResponseForbidden("You cannot delete your own account.")

        try:
            user_to_delete = User.objects.get(pk=user_id)
            user_to_delete.delete()
            # redirect ไปหน้า dashboard หรือแสดงข้อความสำเร็จ
            return redirect('admin_dashboard_js_controlled')
        except User.DoesNotExist:
            return HttpResponse("User not found.", status=404)
    return HttpResponseForbidden("Invalid request method.")
    
def logout_view(request):
    logout(request)
    return redirect('login')
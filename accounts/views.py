import email
from os import name
from urllib import request

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from requests import request
from .models import Leave
from .models import Admin as AdminModel
from .models import Attendance
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Timesheet
from .models import Employee
from .models import  Asset
from datetime import datetime
from .models import  PayDetails
def login(request):
    
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Empty field checking
        if not email or not password:
            messages.error(request, "Please fill all the fields.")
            return redirect('login')

        # Search user by email
        user = User.objects.filter(email=email).first()

        # Email not registered
        if user is None:
            messages.warning(request, "Please register yourself first.")
            return redirect('register')

        # Wrong password
        if not user.check_password(password):
            messages.error(request, "Invalid password.")
            return redirect('login')

        # Successful login
        auth_login(request, user)
        messages.success(request, "Login successful.")
        return redirect('dashboard')

    return render(request, 'login.html')


def register(request):

    if request.method == "POST":

        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Empty field checking
        if not name or not email or not password:
            messages.error(request, "Please fill all the fields.")
            return redirect("register")

        # Check username
        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("register")

        # Create user
        User.objects.create_user(
            username=name,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful.")
        return redirect("login")

    if request.GET.get("from_login"):
        messages.warning(request, "Please register yourself first.")

    return render(request, "register.html")


def Dashboard(request):
    return render(request, 'Dashboard.html')

from django.shortcuts import render
from .models import Leave


@login_required
def Leaves(request):
    try:
        leaves = Leave.objects.filter(user=request.user)
    except Exception as e:
        leaves = []  # Fallback to an empty list if the table/query fails

    return render(request, "leaves.html", {
        "leaves": leaves
    })
    
@login_required
def applyleave(request):
    if request.method == "POST":
        leave_type = request.POST.get("leave_type", "").strip()
        from_date = request.POST.get("from_date", "").strip()
        to_date = request.POST.get("to_date", "").strip()
        reason = request.POST.get("reason", "").strip()

        # Check if required fields are empty
        if not all([leave_type, from_date, to_date, reason]):
            messages.error(request, "Please fill all the fields.")
            return render(request, "applyleave.html")

        # Automatically use the logged-in user's info
        Leave.objects.create(
            user=request.user,
            name=request.user.get_full_name() or request.user.username,
            email=request.user.email,
            leave_type=leave_type,
            from_date=from_date,
            to_date=to_date,
            reason=reason,
        )

        messages.success(request, "Leave application submitted successfully.")
        return redirect("leaves")

    return render(request, "applyleave.html")

def admin(request):
    
    leaves = Leave.objects.all().order_by("-id")
    attendances = Attendance.objects.all().order_by("-date")
    timesheets = Timesheet.objects.all().order_by("-created_at")

    context={
            "leaves": leaves,
            "attendances": attendances,
            "timesheets": timesheets,
        }
    return render(request, "admin.html", context)

def approve_leave(request,id):
    
    leave = Leave.objects.get(id=id)

    leave.status = "Approved"

    leave.save()

    return redirect('admin')

def reject_leave(request,id):
    
    leave = Leave.objects.get(id=id)

    leave.status = "Rejected"

    leave.save()

    return redirect('admin')



def adminlogin(request):
    
    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        role = request.POST.get("role", "").strip()

        # Check if all fields are filled
        if not email or not password or not role:
            messages.error(request, "Please fill all the details.")
            return redirect("adminlogin")

        # If User is selected, do not allow admin login
        if role == "User":
            messages.error(request, "You are not an Admin. Please select the role properly.")
            return redirect("adminlogin")

        # Check Admin table
        admin = AdminModel.objects.filter(email=email).first()

        if admin is None:
            messages.error(request, "Admin email not found.")
            return redirect("adminlogin")

        if admin.password != password:
            messages.error(request, "Wrong password.")
            return redirect("adminlogin")

        messages.success(request, "Admin login successful.")
        return redirect("admin")

    return render(request, "adminlogin.html")
    
    
def adminregister(request):
    
    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Check for empty fields
        if not username or not email or not password:
            messages.error(request, "Please fill all the details.")
            return redirect("adminregister")   # Replace with your URL name

        # Create admin account
        AdminModel.objects.create(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Admin registered successfully."
        )

        return redirect("adminlogin")   # Redirect to login page after registration
    return render(request, "adminregister.html")


@login_required
def checkin(request):

    today = timezone.localdate()

    attendance = Attendance.objects.filter(
        user=request.user,
        date=today
    ).first()


    if attendance:

        messages.warning(
            request,
            "You have already checked in today."
        )

    else:

        Attendance.objects.create(

            user=request.user,

            date=today,

            check_in=timezone.localtime().time(),

            status="Present"

        )

        messages.success(
            request,
            "Check In successful."
        )


    return redirect("swipedata")

@login_required
def checkout(request):

    today = timezone.localdate()

    attendance = Attendance.objects.filter(
        user=request.user,
        date=today
    ).first()


    if attendance is None:

        messages.error(
            request,
            "Please check in first."
        )

        return redirect("swipedata")


    if attendance.check_out:

        messages.warning(
            request,
            "You have already checked out today."
        )

        return redirect("swipedata")


    attendance.check_out = timezone.localtime().time()

    attendance.save()


    messages.success(
        request,
        "Check Out successful."
    )


    return redirect("swipedata")

@login_required
def swipedata(request):

    attendances = Attendance.objects.filter(
        user=request.user
    ).order_by("-date")


    context = {

        "today": timezone.localdate(),

        "attendances": attendances

    }

    return render(
        request,
        "swipedata.html",
        context
    )


def addentry(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        date = request.POST['date']
        project = request.POST['project']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        task = request.POST['task']
        description = request.POST['description']

        # Empty field checking
        if (name == "" or email == "" or date == "" or
            project == "" or checkin == "" or
            checkout == "" or task == "" or
            description == ""):

            messages.error(request, "Please fill all the fields.")
            return redirect('addentry')

        # Check user email exists
        user = User.objects.filter(email=email).first()

        if user is None:
            messages.error(request, "Email not registered. Please register first.")
            return redirect('register')

        # Save Timesheet Entry
        Timesheet.objects.create(

            user=user,
            name=name,
            email=email,
            date=date,
            project=project,
            check_in=checkin,
            check_out=checkout,
            task=task,
            description=description,
            status="Pending",

        )

        messages.success(request, "Timesheet entry added successfully.")
        return redirect('timesheet')

    return render(request, "addentry.html")


def timesheet(request):
    
    timesheets = Timesheet.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "Timesheet.html", {
        "timesheets": timesheets
    })
    
    
def verify_timesheet(request, id):
    
    timesheet = Timesheet.objects.get(id=id)

    timesheet.status = "Verified"
    timesheet.save()

    return redirect("admin")


def notverify_timesheet(request, id):
    
    timesheet = Timesheet.objects.get(id=id)

    timesheet.status = "Not Verified"
    timesheet.save()

    return redirect("admin")


def employee(request):
    
    if request.method == "POST":

        email = request.POST.get("email")

        # Check if the email is registered
        user = User.objects.filter(email=email).first()

        if user is None:
            messages.error(request, "This email is not registered. Please register first.")
            return redirect("register")

        # Prevent duplicate employee records
        if Employee.objects.filter(email=email).exists():
            messages.error(request, "Employee details already exist.")
            return redirect("employee")

        joining_date = request.POST.get("joining_date")

        # Save employee first
        employee = Employee.objects.create(
            name=request.POST.get("name"),
            email=email,
            mobile=request.POST.get("mobile"),
            department=request.POST.get("department"),
            designation=request.POST.get("designation"),
            address=request.POST.get("address"),
            pincode=request.POST.get("pincode"),
            state=request.POST.get("state"),
            bank_name=request.POST.get("bank_name"),
            account_number=request.POST.get("account_number"),
            ifsc=request.POST.get("ifsc"),
            joining_date=joining_date,
            dob=request.POST.get("dob"),
        )

        # Generate Employee ID
        date_part = datetime.strptime(joining_date, "%Y-%m-%d").strftime("%Y%m%d")

        count = Employee.objects.filter(
            joining_date=employee.joining_date
        ).count()

        employee.employee_id = f"EMP-{date_part}-{count:03d}"
        employee.save()

        messages.success(request, "Employee details saved successfully.")
        return redirect("dashboard")

    return render(request, "employee.html")


def profile(request):
    employee = Employee.objects.filter(email=request.user.email).first()

    return render(request, "profile.html", {
        "employee": employee
    })
    
    
@login_required
def assets(request):

    # Check if the logged-in user is an employee
    employee = Employee.objects.filter(
        email=request.user.email
    ).first()

    # User is not an employee
    if employee is None:
        return render(request, "assets.html", {
            "not_employee": True,
        })

    # Get assigned assets
    assets = Asset.objects.filter(employee=employee)

    return render(request, "assets.html", {
        "employee": employee,
        "assets": assets,
        "not_employee": False,
    })
    
    
def assetdetails(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        Asset.objects.create(
            employee=employee,
            asset_name=request.POST.get("asset_name"),
            brand=request.POST.get("brand"),
            model=request.POST.get("model"),
            serial_number=request.POST.get("serial_number"),
            issue_date=request.POST.get("issue_date"),
        )

        messages.success(request, "Asset assigned successfully.")
        return redirect("employee_profiles")

    return render(request, "assetdetails.html", {
        "employee": employee
    })


def employee_profiles(request):
    
    employees = Employee.objects.all()

    return render(
        request,
        "employee_profiles.html",
        {
            "employees": employees
        }
    )
    
def paydetails(request, employee_id):
    
    employee = get_object_or_404(Employee, id=employee_id)

    pay = PayDetails.objects.filter(employee=employee).first()

    if request.method == "POST":

        basic_salary = request.POST.get("basic_salary")

        # Validation
        if not basic_salary:
            messages.error(request, "Please update the employee's basic salary.")
            return render(request, "paydetails.html", {
                "employee": employee,
                "pay": pay,
            })

        if pay is None:
            pay = PayDetails(employee=employee)

        pay.basic_salary = basic_salary
        pay.hra = request.POST.get("hra") or 0
        pay.da = request.POST.get("da") or 0
        pay.special_allowance = request.POST.get("special_allowance") or 0
        pay.bonus = request.POST.get("bonus") or 0
        pay.professional_tax = request.POST.get("professional_tax") or 0
        pay.income_tax = request.POST.get("income_tax") or 0
        pay.payment_mode = request.POST.get("payment_mode")
        pay.payment_date = request.POST.get("payment_date") or None

        pay.save()

        messages.success(request, "Pay details updated successfully.")
        return redirect("employee_profiles")

    return render(request, "paydetails.html", {
        "employee": employee,
        "pay": pay,
    })

@login_required
def payslip(request):

    employee = Employee.objects.filter(
        email=request.user.email
    ).first()

    # User is not an employee
    if employee is None:
        return render(request, "payslip.html", {
            "not_employee": True,
        })

    pay = PayDetails.objects.filter(
        employee=employee
    ).first()

    gross_salary = 0
    total_deduction = 0
    net_salary = 0

    if pay:
        gross_salary = (pay.basic_salary +pay.hra +pay.da +pay.special_allowance +pay.bonus)

        total_deduction = (pay.professional_tax +pay.income_tax)

        net_salary = gross_salary - total_deduction

    context = {
        "employee": employee,
        "pay": pay,
        "gross_salary": gross_salary,
        "total_deduction": total_deduction,
        "net_salary": net_salary,
    }

    return render(request, "payslip.html", context)


def delete_employee(request, id):
    
    employee = get_object_or_404(Employee, id=id)

    # Delete related records
    Asset.objects.filter(employee=employee).delete()
    PayDetails.objects.filter(employee=employee).delete()

    Leave.objects.filter(email=employee.email).delete()
    Attendance.objects.filter(user__email=employee.email).delete()
    Timesheet.objects.filter(email=employee.email).delete()

    # Delete login account
    User.objects.filter(email=employee.email).delete()

    # Delete employee profile
    employee.delete()

    messages.success(
        request,
        "Employee and all related records deleted successfully."
    )

    return redirect("employee_profiles")

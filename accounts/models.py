from django.db import models
from django.contrib.auth.models import User


class Leave(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    email = models.EmailField()

    leave_type = models.CharField(max_length=50)

    from_date = models.DateField()

    to_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    approver = models.CharField(
        max_length=100,
        default="Admin"
    )


    def __str__(self):
        return self.name
    
    


class Admin(models.Model):

    username = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=200
    )


    def __str__(self):
        return self.username
    
    
    
    
class Attendance(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField(
        auto_now_add=True
    )

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="Absent"
    )


    def __str__(self):

        return f"{self.user.username} - {self.date}"
    
    
class Timesheet(models.Model):
    
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Verified", "Verified"),
        ("Not Verified", "Not Verified"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()

    date = models.DateField()

    project = models.CharField(max_length=100)

    check_in = models.TimeField()
    check_out = models.TimeField()

    task = models.CharField(max_length=200)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} ({self.status})"



class Employee(models .Model):
        employee_id = models.CharField(max_length=20, unique=True, blank=True,null=True)
        name = models.CharField(max_length=100)
        email = models.EmailField(unique=True)
        mobile = models.CharField(max_length=15)
        address = models.TextField()
        pincode = models.CharField(max_length=10)
        state = models.CharField(max_length=50)
        department = models.CharField(max_length=100, blank=True, null=True)
        designation = models.CharField(max_length=100, blank=True, null=True)
        bank_name = models.CharField(max_length=100)
        account_number = models.CharField(max_length=30)
        ifsc = models.CharField(max_length=20)
        joining_date = models.DateField()
        dob = models.DateField()

        def __str__(self):
            return self.name
    
class PayDetails(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    da = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_mode = models.CharField(max_length=50, default="Bank Transfer")
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.employee.name
    
#class Payslip(models.Model):   #system

class Asset(models.Model):
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    asset_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    issue_date = models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.asset_name}"
    
from django.shortcuts import render, HttpResponse, redirect
from .models import Admin, User
from api.models import Product
from api.serializers import ProductSerializer
import requests
import csv
from decouple import config
import smtplib

API_URL = "http://127.0.0.1:8000/api-auth/"

def startup(request):
    if request.session.get("admin_id"): return redirect(adminhome)
    if request.session.get("user_id"): return redirect(home)
    return render(request, 'index.html')

def login(request):
    if not request.session.get("user_id"):
        msg = {}
        if request.method == "POST":
            email, password = request.POST.get("email"), request.POST.get("password")
            users = User.objects.filter(email=email)
            for user in users:
                if user.password == password:
                    request.session['user_id'] = user.id
                    return redirect(home)
            msg["registered"] = 0
        return render(request, "bothlogin.html", msg)
    return redirect(home)

def register(request):
    if not request.session.get("user_id"):
        msg = {}
        if request.method == "POST":
            registered = 0
            username, email, password = request.POST.get("username"), request.POST.get("email"), request.POST.get("password")
            try:
                user = User(username=username, email=email, password=password)
                user.save()
                registered = 1
            except:
                registered = 2
            msg["registered"] = registered
        return render(request, 'reg.html', msg)
    return redirect(home)

def adminlogin(request):
    msg = {}
    if request.session.get("admin_id"): return redirect(adminhome)
    if request.method == "POST":
        email, password = request.POST.get("email"), request.POST.get("password")
        print(email, password)
        admins = Admin.objects.filter(email=email)
        for admin in admins:
            if admin.password == password:
                request.session["admin_id"] = admin.id 
                msg["username"] = admin.username
                return redirect(adminhome)
        msg["registered"] = 0
    return render(request, "bothlogin.html", msg)

def adminhome(request):
    msg = {}
    if request.session.get("admin_id"):
        msg["username"] = Admin.objects.get(id=request.session.get("admin_id")).username
        return render(request, "admin/index.html", msg)
    return redirect(adminlogin)

def home(request):
    if request.session.get("user_id"):
        msg = {}
        username = User.objects.get(id=request.session["user_id"]).username
        msg["username"] = username
        return render(request, "user/index.html", msg)
    return redirect(login)

def logout(request):
    if request.session.get("user_id"):
        del request.session["user_id"]
        return redirect(login)
    elif request.session.get("admin_id"):
        del request.session["admin_id"]
        return redirect(startup)
    return redirect(startup)

def adminview(request):
    if request.session.get("admin_id"):
        msg = {}
        URL = API_URL+"view/"
        imported, exported = analyze()
        totalimp, totalexp = sum(list(imported.values())), sum(list(exported.values()))
        data = requests.get(URL).json()
        for product in data:
            if totalimp>0:
                product["imported"] = (product["totalamount"]/totalimp)*100
            else:
                product["imported"] = "-"
            if totalexp>0:
                product["exported"] = (product["totalamount"]/totalexp)*100
            else:
                product["exported"] = "-"
        writecsv()
        msg["data"] = data 
        
        return render(request, "admin/view.html", msg)
    return redirect(adminlogin)

def adminadd(request):
    if request.session.get("admin_id"):
        msg = {}
        added = 0
        if request.method == "POST":
            name, category, description = request.POST.get("name"), request.POST.get("category"), request.POST.get("description")
            amount, quantity, mode = int(request.POST.get("amount")), int(request.POST.get("quantity")), request.POST.get("mode")
            data = {"name": name, "amount": amount, "quantity": quantity , "category": category, "mode": mode, "totalamount": amount*quantity , "description": description}
            URL = API_URL+"add/"
            try:
                response = requests.post(URL, data=data)
                print(response)
            except:
                added = 2
            added = 1
        msg["added"] = added
        return render(request, "admin/add.html", msg)
    return redirect(adminlogin)

def adminupdate(request):
    if request.session.get("admin_id"):
        msg = {}
        updated = 0
        response = ""
        if request.method == "POST":
            data = {}
            id = request.POST.get("id")
            name, category, description = request.POST.get("name"), request.POST.get("category"), request.POST.get("description")
            amount, quantity, mode = request.POST.get("amount"), request.POST.get("quantity"), request.POST.get("mode")
            URL = API_URL+"update/"+str(id)
            if name:
                data["name"] = name
            if amount:
                data["amount"] = amount
            if quantity:
                data["quantity"] = quantity
            if category!="Choose...":
                data["category"] = category
            if mode!="Choose...":
                data["mode"] = mode
            if description:
                data["description"] = description
            response = requests.put(URL, data=data)
            updated = 1
        
        data = requests.get(API_URL+"view").json()
        msg["data"] = data
        msg["updated"] = updated
        return render(request, "admin/update.html", msg)
    return redirect(adminlogin)
    
    
def admindelete(request):
    if request.session.get("admin_id"):
        msg = {}
        deleted = 0
        response = ""
        if request.method == "POST":
            id = request.POST.get("id")
            URL = API_URL+"delete/"+str(id)
            response = requests.delete(URL).json()
            deleted = 1
        msg["response"] = response
        msg["deleted"] = deleted
        URL = API_URL+"view/"
        data = requests.get(URL).json()
        msg["data"] = data
        return render(request, "admin/delete.html", msg)
    return redirect(adminlogin)

def userview(request):
    if request.session.get("user_id"):
        msg = {}
        URL = API_URL+"view"
        data = requests.get(URL).json()
        msg["data"] = data
        return render(request, "user/view.html", msg)
    return redirect(login)

def analyze():
    products = Product.objects.all()
    imported = {}
    exported = {}
    for product in products:
        if product.mode == "Import":
            imported[product.category] = imported.get(product.category, 0) + product.totalamount
        else:
            exported[product.category] = exported.get(product.category, 0) + product.totalamount
    return imported, exported

def writecsv():
    fields = ["Id", "Name", "Amount per Kg/L", "Quantity", "Category", "Mode", "Total Amount", "Description", "Time", "percentage Imported", "percentage Exported"]
    rows = []
    imported, exported = analyze()
    totalimp, totalexp = sum(list(imported.values())), sum(list(exported.values()))
    URL = API_URL+"view/"
    products = requests.get(URL).json()
    print(products)
    for product in products:
        if totalimp>0:
            product["imported"] = (product["totalamount"]/totalimp)*100
        else:
            product["imported"] = "-"
        if totalexp>0:
            product["exported"] = (product["totalamount"]/totalexp)*100
        else:
            product["exported"] = "-"
    print(products)
    for product in products:
        lst = [product["id"], product["name"], product["amount"], product["quantity"], product["category"], product["mode"], product["totalamount"], product["description"], product["time"], product["imported"], product["exported"]]
        rows.append(lst)
    filename = "C:/Users/dhana/coding/Personal Projects/BitBuild/bitbuild/static/reports.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
        
class Mail:
    def __init__(self) -> None:
        self.email = 'dhananjay2002pai@gmail.com'
        self.password = config("PASSWORD")
        
    def sendto(self, receiver, name):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            
            smtp.login(self.email, self.password)
            
            subject = "Reports Generated for your Warehouse"
            body = f"Hi {name}!\nHere are your reports\n<a href='http://127.0.0.1:8000/static/reports.csv'>Download</a>\n\nRegards, \n ZKBuilders"
            msg = f"Subject:{subject}\n\n{body}"
            
            smtp.sendmail(self.email, receiver, msg)
            
def mail(request):
    if request.session.get("admin_id"):
        admin = Admin.objects.get(id=request.session["admin_id"])
        mail = Mail()
        mail.sendto(admin.email, admin.username)
        print("sent")
        return redirect(adminview)
    return redirect(adminlogin)
        
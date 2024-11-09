from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Q  # Import the Q object
from datetime import datetime
from django.utils import timezone
from datetime import datetime
from .models import *
from django.db.models import Q
from django.db.models import Sum
# Create your views here.

def index(request):
    
    return render(request, 'hoome.html')

def admin(request):
    
    return render(request,'admin.html')

def user_page(request):
    
    return render(request,'user_page.html')

def farmer_page(request):
    data=Products.objects.all()
    if request.method=="POST":
        btn=request.POST["submit"]
        if request.POST["category"]=="All":
            data=Products.objects.all()
        else:
            data=Products.objects.filter(product_category=request.POST["category"])

    print(data)
    return render(request,'farmer_page.html',{"data":data})

def logout(request):
    
    return render(request,'hoome.html')

def all_login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        passwd = request.POST['password']
        
        try:
            q = login.objects.get(username=uname, password=passwd)
            request.session['login_id']=q.pk
            request.session['lid'] = q.pk
            request.session["bmid"]=0
            if q :
                if q.usertype == 'admin':
                    return HttpResponse("<script>alert('Login successful'); window.location='/myapp/adminn'</script>")
                elif q.usertype == 'user':
                    qq=user_registration.objects.get(login_id=request.session['login_id'])
                    if qq:
                        request.session['u_id']=qq.pk
                        print(">>>>>>>>>",request.session['u_id'])
                    return HttpResponse("<script>alert('Login successful'); window.location='/myapp/user_page#m'</script>")
                elif q.usertype == 'farmer':
                    qq=farmer_registration.objects.get(login_id=request.session['login_id'])
                    if qq:
                        request.session['f_id']=qq.pk
                        print(">>>>>>>>>",request.session['f_id'])
                    return HttpResponse("<script>alert('Login successful'); window.location='/myapp/farmer_page#m'</script>")
            else:
                return HttpResponse("<script>alert('Invalid login credentials'); window.location='/myapp/all_login'</script>")
        except login.DoesNotExist:
            return HttpResponse("<script>alert('Invalid login credentials'); window.location='/myapp/all_login'</script>")

    return render(request, 'login.html')

def user_registrationxxx(request):
    if request.method == 'POST':
        # Retrieve form data
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        eemail = request.POST['email']
        pphone = request.POST['phone']
        address = request.POST['address']
        district = request.POST['district']
        state=request.POST['state']
        country=request.POST['country']
        uname = request.POST['username']
        passwd = request.POST['passw']

        qry = login.objects.filter(username=uname)
        
        if qry:
            return HttpResponse("<script> alert('User already exists!'),window.location='/myapp/user_register' </script>")
        else:
            q = login(username=uname, password=passwd, usertype='user')
            q.save()
            obj=user_registration(login=q,first_name=fname, last_name=lname, email=eemail,phone=pphone,address=address,district=district,state=state,country=country)
            obj.save()

    return render(request,'user_signup.html')

def farmer_fav_product(request,id):
    g=Favourites.objects.filter(LOGIN_id=request.session["lid"],PRODUCTS_id=id)
    if g.exists():
        return HttpResponse("<script> alert('Already Added to Favourites'),window.location='/myapp/farmer_page#m' </script>")

    else:
        f=Favourites()
        f.LOGIN_id=request.session["lid"]
        f.PRODUCTS_id=id
        f.save()
        return   HttpResponse("<script> alert('Added to Favourites'),window.location='/myapp/farmer_page#m' </script>")

def farmer_register(request):

    if request.method == 'POST':
        # Retrieve form data
        
        uname = request.POST['user_name']
        passwd = request.POST['passw']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        eemail = request.POST['email']
        pphone = request.POST['phone']
        category=request.POST['category']
        aadar= request.POST['aadar']
        address = request.POST['address']
        district = request.POST['district']
        state=request.POST['state']
        country=request.POST['country']
        qry = login.objects.filter(username=uname)
        if qry:
            return HttpResponse("<script> alert('User already exists!'),window.location='/myapp/user_register' </script>")
        else:
            q = login(username=uname, password=passwd, usertype='farmer')
            q.save()
            obj =farmer_registration(login=q,farmer_first_name=fname, farmer_last_name=lname,farmer_email=eemail,farmer_phone=pphone,farmer_category=category,farmer_aadar=aadar,farmer_address=address,farmer_district=district,farmer_state=state,farmer_country=country)
            obj.save()

    return render(request, 'farmer_signup.html')

def eartag_register(request):
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    if qq:
        fid=qq[0].id
    if request.method =='POST':
        
        species = request.POST['species']
        breed=request.POST['breed']
        gender=request.POST['gender']
        registerdate=request.POST['regidate']
        dateofbirth=request.POST['dob']
        colour=request.POST['colour']
        sireid=request.POST['sireid']
        pregnancy=request.POST['pregnancy']
        pregnancymonth=request.POST['pregnancy_month']
        milkingstatus=request.POST['milking_status']
        
    
        obj=farmer_eartag_application(species=species,breed=breed,gender=gender,regidate=registerdate,dob=dateofbirth,colour=colour,sire_id=sireid,pregnancy=pregnancy,pregnancymonth=pregnancymonth,milkingstatus=milkingstatus,farmer_id=fid,eartag_status='pending')
        obj.save()
        
    return render(request,'farmer_eartag_application.html')

def admin_add_product(request):
    
    if request.method == 'POST':
        img=request.FILES['pro']
        fss=FileSystemStorage()
        fn=fss.save(img.name,img)
        product_name=request.POST['product_name']
        product_price=request.POST['product_price']
        productquantity=request.POST['productquantity']
        productcategory = request.POST['category']
        product_description=request.POST['product_description']
        obj=Products(product_name=product_name, product_image=fss.url(fn), product_price=product_price, product_quantity=productquantity,product_description=product_description,product_category=productcategory)
        obj.save()
        
    var=Products.objects.all()
    
    return render(request, 'admin_add_product.html',{'viewpro':var})


def update_product(request,id):
    q=Products.objects.get(id=id)
    if request.method == 'POST':

        q.product_name =request.POST['product_name']
        if 'productimg' in request.FILES:
            img=request.FILES['productimg']
            fss=FileSystemStorage()
            fn=fss.save(img.name,img)
            q.product_image=fss.url(fn)
        q.product_price=request.POST['product_price']
        res=request.POST['qtyquantity']
        q.product_category=request.POST["category"]
        q.product_quantity=res
        q.product_description=request.POST['product_description']
        q.save()
        return HttpResponse("<script> alert('updated succesfully!'),window.location='/myapp/admin_add_product#m' </script>")
    return render(request,'admin_add_product.html',{'q':q})



def delete_product(request, id):
    
    q=Products.objects.get(id=id)
    q.delete()
    
    return HttpResponse("<script> alert('deleted succesfully!'),window.location='/myapp/admin_add_product#m' </script>")


def admin_view_farmers(request):
    var = farmer_registration.objects.all()
    if request.method == 'POST':
        name=request.POST["farmer_name"]
        var = farmer_registration.objects.filter(Q(farmer_first_name__icontains=name)|Q(farmer_last_name__icontains=name))


    total=len(var)
    return render(request, 'admin_view_farmers.html', {'viewpro': var,"total":total})


def admin_view_eartag_report(request):
    if request.method == 'POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        vals = request.POST['vals']  # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx", from_dates)
            print("Request1yyyyyyy", to_dates)
            views = farmer_eartag_application.objects.filter(regidate__range=[from_date_str, to_date_str])
            print("reportxxx", views)
        else:
            views = farmer_eartag_application.objects.filter(
                farmer__farmer_first_name__icontains=vals) | farmer_eartag_application.objects.filter(
                eartag_status__icontains=vals) | farmer_eartag_application.objects.filter(
                species__icontains=vals) | farmer_eartag_application.objects.filter(
                breed__icontains=vals)



    else:
        views = farmer_eartag_application.objects.all()
    total=len(views)
    #if total==0:
        #return HttpResponse("<script>alert('invalid date'); window.location='/myapp/admin_view_eartag_report'</script>")    
    return render(request, 'admin_view_eartag_report.html', {'view': views,"total":total})


def admin_view_one_eartag_request(request,ek):
    
    var=farmer_eartag_application.objects.filter(id=ek)
    
    dic={'key': var}
    
    return render(request,'admin_1_eartag_view.html',dic)

def admin_view_eartag_request(request):
    if request.method == 'POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request",from_date_str)
        print("Request1",to_date_str)
        vals = request.POST['vals'] # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx",from_dates)
            print("Request1yyyyyyy",to_dates)
            views = farmer_eartag_application.objects.filter(regidate__range=[from_date_str, to_date_str])
            print("reportxxx", views)
        else:
             views = farmer_eartag_application.objects.filter(farmer__farmer_first_name__icontains=vals)|farmer_eartag_application.objects.filter(eartag_status__icontains=vals)|farmer_eartag_application.objects.filter(species__icontains=vals)|farmer_eartag_application.objects.filter(breed__icontains=vals)|farmer_eartag_application.objects.filter(gender__icontains=vals)
    


    else:
        views = farmer_eartag_application.objects.all()

    return render(request,'admin_view_eartag_request.html',{'view': views})

def admin_view_farmers_cattle(request,id):
    views = farmer_eartag_application.objects.filter(eartag_status="Accepted",farmer_id=id)

    return render(request, 'admin_view_farmers_cattles.html', {'view': views})


def admin_accept(request, id,farmer_email):
    
    try:
        # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
        
        # Get the eartag application and update its status
        application = farmer_eartag_application.objects.get(id=id)
        application.eartag_status = 'Accepted'
        application.save()
        # Send approval email
        subject = 'Your Eartag Application Request Has Been Approved'
        message = f'Dear {first_name},\n\nWe are pleased to inform you that your application for an eartag has been approved. This is an important step towards ensuring the health and safety of your livestock. We congratulate you on taking this initiative to manage your animals effectively.\n\nHere are the details of your approved application:\nSpecies: {application.species}\nBreed: {application.breed}\nRegistration Date: {application.regidate}\n\nOur team is dedicated to providing you with the best service. Soon, one of our representatives will get in touch with you on your registered mobile number to discuss further details and guide you through the next steps. If you have any questions or need assistance, please do not hesitate to contact our customer support team at 8956-9656-5445-5454 or dairyhubservice@gmail.com.\n\nThank you!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [farmer_email]
        send_mail( subject, message, email_from, recipient_list )

        return HttpResponse("<script> alert('Request Accepted!'),window.location='/myapp/admin_view_eartag_request' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_view_eartag_request' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_view_eartag_request' </script>")

def admin_reject(request,id,farmer_email):
    
    try:
        
        # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
        
        # Get the eartag application and update its status
        application = farmer_eartag_application.objects.get(id=id)
        application.eartag_status = 'Rejected'
        application.save()
        # Send approval email
        subject = 'Eartag Application Rejection'
        message = f'Dear {first_name},\n\nWe regret to inform you that your application for an eartag has been rejected. \n\nHere are the details of your application:\nSpecies: {application.species}\nBreed: {application.breed}\nRegistration Date: {application.regidate}\n\nAfter careful review, we found that the application did not meet the necessary requirements due to insufficient or improper details submitted. In order to proceed with the application, we kindly request you to get in touch with our dedicated service team at your earliest convenience. Our team can be reached via email at dairyhubservice@gmail.com or by phone at 8956-9656-5445-5454. They will be able to guide you through the necessary steps to reapply and provide the proper information for processing your eartag application.\n\nWe understand that this might be disappointing news, but our goal is to ensure the accuracy and effectiveness of the eartag application process for all livestock owners. We value your commitment to the well-being of your animals and hope to assist you in completing the application successfully.If you have any questions or require further assistance, please do not hesitate to contact our customer support team. We appreciate your understanding and cooperation.Thank you for considering our services. \n\nTEAM DIARYHUB \nThank you!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )

        return HttpResponse("<script> alert('Request Rejected!'),window.location='/myapp/admin_view_eartag_request' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_view_eartag_request' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_view_eartag_request' </script>")


def farmer_view_eartag(request):

    lid = request.session['login_id']
    qq = farmer_registration.objects.filter(login_id=lid)
    if qq:
        fid = qq[0].id

    myvar = farmer_eartag_application.objects.filter(farmer_id=fid)

    dic = {'key': myvar}
    return render(request,'farmer_eartagview_all.html',dic)
        
def farmer_1_eartag_view(request,id):
    
    var=farmer_eartag_application.objects.filter(id=id)
    
    dic={'key': var}
    
    return render(request,'farmer_1_eartagview.html',dic)

        
def eartag_re_request(request,id,regidate):
    print(regidate)
    from datetime import datetime

    # Input date string
    date_string = regidate

    # Convert the string to a datetime object
    try:
        date_object = datetime.strptime(date_string, "%B %d, %Y")
    except:
        date_object = datetime.strptime(date_string, "%b. %d, %Y")
    # Print the result
    print("Converted Date:", date_object)
    ses=str(date_object).split(" ")
    request.session["regi_date"]=ses[0]
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    if qq:
        fid=qq[0].id
    
    if request.method == 'POST':
        
        preveartagno=request.POST['preveartagno']                
        prev_regi_date=request.session["regi_date"]
        new_regi_date=request.POST['new_regi_date']
        missing_date=request.POST['missing_date']
        add_details=request.POST['add_details']
     
        
        obj=farmer_eartag_re_application(eartag_id=id,
                                         new_eartag_regi_date=new_regi_date,
                                         prev_eartag_no=preveartagno,
                                         prev_eartag_regi_date=prev_regi_date,
                                         missing_date=missing_date,
                                         additional_details=add_details,
                                         farmer_id=fid,
                                         eartag_miss_status='pending')
        obj.save()
        
       
    return render(request,'farmer_re_eartag.html',{'regidate':regidate})

def farmer_view_misseartag(request):
    
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    if qq:
        fid=qq[0].id
    
    
    myvar=farmer_eartag_re_application.objects.filter(farmer_id=fid)
    
    dic={'key':myvar}
    
    return render(request,'farmer_misseartag_view.html',dic)

def admin_view_orders(request):

    data=bookingmaster.objects.all()

    print(data)
    total = 0
    l = []
    for i in data:
        total += int(i.bm_total)

        lob = login.objects.get(id=i.login_id)
        if lob.usertype == "farmer":
            f = farmer_registration.objects.get(login_id=i.login_id)
            name = f.farmer_first_name + " " + f.farmer_last_name
            phone = f.farmer_phone
            address = f.farmer_address
            district = f.farmer_district
            state = f.farmer_state
            country = f.farmer_country
        else:
            f = user_registration.objects.get(login_id=i.login_id)
            name = f.first_name + " " + f.last_name
            phone = f.phone
            address = f.address
            district = f.district
            state = f.state
            country = f.country

        l.append({"bm_date": i.bm_date, "bm_total": i.bm_total, "bm_status": i.bm_status,
                  "bookingmaster_id": i.bookingmaster_id, "name": name, "phone": phone, "address": address,
                  "district": district, "state": state, "country": country})

    if request.method == "POST":
        l=[]
        start=request.POST["start_date"]
        end=request.POST["end_date"]
        if start and end:
            data = bookingmaster.objects.filter(bm_date__range=[start,end])
            for i in data:
                total += int(i.bm_total)

                lob = login.objects.get(id=i.login_id)
                if lob.usertype == "farmer":
                    f = farmer_registration.objects.get(login_id=i.login_id)
                    name = f.farmer_first_name + " " + f.farmer_last_name
                    phone = f.farmer_phone
                    address = f.farmer_address
                    district = f.farmer_district
                    state = f.farmer_state
                    country = f.farmer_country
                else:
                    f = user_registration.objects.get(login_id=i.login_id)
                    name = f.first_name + " " + f.last_name
                    phone = f.phone
                    address = f.address
                    district = f.district
                    state = f.state
                    country = f.country

                l.append({"bm_date": i.bm_date, "bm_total": i.bm_total, "bm_status": i.bm_status,
                          "bookingmaster_id": i.bookingmaster_id, "name": name, "phone": phone, "address": address,
                          "district": district, "state": state, "country": country})
        else:
            vals = request.POST['vals']
            if vals =="":
                l=[]
                data=bookingmaster.objects.all()
                for i in data:
                    total += int(i.bm_total)

                    lob = login.objects.get(id=i.login_id)
                    if lob.usertype == "farmer":
                        f = farmer_registration.objects.get(login_id=i.login_id)
                        name = f.farmer_first_name + " " + f.farmer_last_name
                        phone = f.farmer_phone
                        address = f.farmer_address
                        district = f.farmer_district
                        state = f.farmer_state
                        country = f.farmer_country
                    else:
                        f = user_registration.objects.get(login_id=i.login_id)
                        name = f.first_name + " " + f.last_name
                        phone = f.phone
                        address = f.address
                        district = f.district
                        state = f.state
                        country = f.country

                    l.append({"bm_date": i.bm_date, "bm_total": i.bm_total, "bm_status": i.bm_status,
                              "bookingmaster_id": i.bookingmaster_id, "name": name, "phone": phone, "address": address,
                              "district": district, "state": state, "country": country})
            else:

                l=[]
                data =bookingmaster.objects.all()
                for i in data:
                    total += int(i.bm_total)

                    lob = login.objects.get(id=i.login_id)
                    if lob.usertype == "farmer":

                            f1 = farmer_registration.objects.filter(login_id=i.login_id,farmer_first_name__icontains=vals)|farmer_registration.objects.filter(login_id=i.login_id,farmer_last_name__icontains=vals)
                            if f1.exists():
                                f = farmer_registration.objects.get(login_id=i.login_id)
                                name = f.farmer_first_name + " " + f.farmer_last_name
                                phone = f.farmer_phone
                                address = f.farmer_address
                                district = f.farmer_district
                                state = f.farmer_state
                                country = f.farmer_country
                                l.append({"bm_date": i.bm_date, "bm_total": i.bm_total, "bm_status": i.bm_status,
                                          "bookingmaster_id": i.bookingmaster_id, "name": name, "phone": phone,
                                          "address": address,
                                          "district": district, "state": state, "country": country})

                    else:

                            f1 = user_registration.objects.filter(login_id=i.login_id,first_name__icontains=vals)|user_registration.objects.filter(login_id=i.login_id,last_name__icontains=vals)
                            if f1.exists():
                                f=user_registration.objects.get(login_id=i.login_id)
                                name = f.first_name + " " + f.last_name
                                phone = f.phone
                                address = f.address
                                district = f.district
                                state = f.state
                                country = f.country

                                l.append({"bm_date": i.bm_date, "bm_total": i.bm_total, "bm_status": i.bm_status,
                                      "bookingmaster_id": i.bookingmaster_id, "name": name, "phone": phone, "address": address,
                                      "district": district, "state": state, "country": country})

    count=len(data)
    print(data)

    return render(request,"admin_view_orders.html",{"data":l,"total":total,"count":count})


def admin_view_all_products_report(request):


    if request.method=="POST":
        vals=request.POST["vals"]
        d=Products.objects.filter(product_name__icontains=vals)

    else:
        d = Products.objects.all()

    l=[]
    tot=0
    for i in d:
        if booking_child.objects.filter(product_id=i.id).exists():
            qty=booking_child.objects.filter(product_id=i.id).aggregate(Sum("bc_qty"))
            total=booking_child.objects.filter(product_id=i.id).aggregate(Sum("bc_amount"))
            tot+=int(total["bc_amount__sum"])
            print(tot)
            l.append({"id":i.id,"product_name":i.product_name,"product_image":i.product_image,"product_price":i.product_price,"qty":qty["bc_qty__sum"],"total":total["bc_amount__sum"]})
        else:

            l.append({"id": i.id, "product_name": i.product_name, "product_image": i.product_image,
                      "product_price": i.product_price, "qty": "0", "total": "0"})
    print(l)
    total=tot
    print(total)
    return render(request,"admin_view_all_products_report.html",{"data":l,"total":total})

def admin_view_order_more(request,id):
    request.session["rid"]=id
    data=booking_child.objects.filter(bookingmaster=bookingmaster.objects.get(pk=id))
    l=[]
    for i in data:


        l.append({"id":i.bookingchild_id,"product_name":i.product.product_name,"image":i.product.product_image,"product_price":i.product.product_price,"qty":i.bc_qty,"amount":i.bc_amount})

    total=bookingmaster.objects.get(pk=id).bm_total
    print(l)

    f=delivery_address.objects.get(BOOKING_id=id)
    return render(request,"admin_view_order_more.html",{"data":l,"total":total,'f':f})

def admin_view_cattles_report(request):
    l=farmer_eartag_application.objects.filter(eartag_status="Accepted")
    if request.method=="POST":
        vals=request.POST["vals"]
        if vals == "All":
            l=farmer_eartag_application.objects.filter(eartag_status="Accepted")
        else:
            l = farmer_eartag_application.objects.filter(eartag_status="Accepted",species__icontains=vals)
    total=len(l)
    return render(request,"admin_view_cattles_report.html",{"data":l,"total":total})
def admin_view_cattles_report_more(request,id):
    l=farmer_registration.objects.get(id=id)

    return render(request,"admin_view_cattles_report_more.html",{"i":l})

def admin_update_status(request):
    re=request.POST["status"]
    id=request.session["rid"]
    s=bookingmaster.objects.filter(pk=id).update(bm_status=re)


    return HttpResponse("<script> alert('Updated'),window.location='/myapp/admin_view_orders' </script>")


def admin_1_misseartag_view(request,id):
    
    
    var=farmer_eartag_re_application.objects.filter(id=id)
    
    dic={'key': var}
    
    return render(request,'admin_view_one_eartag_request.html',dic)

def admin_misseartag_view(request):
    
    if request.method=='POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        vals = request.POST['vals']  # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx", from_dates)
            print("Request1yyyyyyy", to_dates)
            view = farmer_eartag_re_application.objects.filter(new_eartag_regi_date__range=[from_date_str, to_date_str])
            print("reportxxx", view)
        else:
            view=farmer_eartag_re_application.objects.filter(eartag_miss_status__icontains=vals)|farmer_eartag_re_application.objects.filter(farmer__farmer_first_name__icontains=vals)|farmer_eartag_re_application.objects.filter(prev_eartag_no__icontains=vals)|farmer_eartag_re_application.objects.filter(eartag__species__icontains=vals)|farmer_eartag_re_application.objects.filter(eartag__breed__icontains=vals)
    else: 
        view=farmer_eartag_re_application.objects.all()
        print("virewwwwww", view)

    return render(request,'admin_misseartag_view.html',{'view':view})


def admin_misseartag_view_report(request):
    if request.method == 'POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        vals = request.POST['vals']  # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx", from_dates)
            print("Request1yyyyyyy", to_dates)
            view = farmer_eartag_re_application.objects.filter(new_eartag_regi_date__range=[from_date_str, to_date_str])
        else:
            vals = request.POST['vals']
            view = farmer_eartag_re_application.objects.filter(
                eartag_miss_status__icontains=vals) | farmer_eartag_re_application.objects.filter(
                farmer__farmer_first_name__icontains=vals) | farmer_eartag_re_application.objects.filter(
                prev_eartag_no__icontains=vals) | farmer_eartag_re_application.objects.filter(
                eartag__species__icontains=vals) | farmer_eartag_re_application.objects.filter(
                eartag__breed__icontains=vals)
    else:
        view = farmer_eartag_re_application.objects.all()
        print("virewwwwww", view)
    total=len(view)
    return render(request, 'admin_misseartag_view_report.html', {'view': view,"total":total})


def admin_miss_accept(request,id):
    try:
        # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
        
        # Get the eartag application and update its status
        application =farmer_eartag_re_application.objects.get(id=id)
        application.eartag_miss_status = 'Accepted'
        application.save()
        # Send approval email
        subject = 'Your Re-Eartag Application Request Has Been Approved'
        message = f'Dear {first_name},\n\nWe are pleased to inform you that your Re-Eartag application has been approved. Your proactive approach towards improving the genetics and breeding of your livestock is truly commendable. Congratulations on taking this important step towards enhancing the quality of your animals.\n\nHere are the details of your approved application:\nPrevious Eartag Number: {application.prev_eartag_no}\nMissing Date: {application.missing_date}\nPrevious Eartag Registration Date: {application.prev_eartag_regi_date}\nSpecies: {application.eartag.species}\nBreed: {application.eartag.breed}\n\nOur dedicated team is committed to providing you with exceptional service. In the coming days, one of our representatives will contact you using your registered contact number to discuss the next steps and address any questions you may have.If you require any assistance or have further inquiries, please do not hesitate to reach out to our customer support team at 8956-9656-5445-5454 or via email at dairyhubservice@gmail.com\n\nThank you!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )

        return HttpResponse("<script> alert('Request Accepted!'),window.location='/myapp/admin_misseartag_view' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_misseartag_view' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_view_eartag_request' </script>")
    
   

def admin_miss_reject(request,id):
    
    try:
        
        # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
        
        # Get the eartag application and update its status
        application = farmer_eartag_re_application.objects.get(id=id)
        application.eartag_miss_status = 'Rejected'
        application.save()
        # Send approval email
        subject = 'Artificial Insemination Request Rejection'
        message = f'Dear {first_name},\n\nWe regret to inform you that your request for artificial insemination has been rejected. We understand your desire to improve your livestocks\' breeding, and we appreciate your initiative to manage your animals effectively.\n\nHowever, after careful review, we found that the application did not meet the necessary requirements due to insufficient or improper details submitted. In order to proceed with the artificial insemination request, we kindly request you to get in touch with our dedicated service team at your earliest convenience. Our team can be reached via email at dairyhubservice@gmail.com or by phone at 8956-9656-5445-5454. They will be able to guide you through the necessary steps to reapply and provide the proper information for processing your artificial insemination request.\n\nTEAM DAIRYHUB \nThank you!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)


        return HttpResponse("<script> alert('Request Rejected!'),window.location='/myapp/admin_misseartag_view' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_misseartag_view' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_misseartag_view' </script>")
    
    
        
    
def AI_request(request):
    
    lid = request.session['login_id']
    qq = farmer_registration.objects.filter(login_id=lid)
    pp=farmer_eartag_application.objects.filter(farmer=qq[0])
    
    if qq:
        fid = qq[0].id
        
        
    if request.method == 'POST':
        prefered_date = request.POST['prefered_date']
        near_hospital = request.POST['near_hospital']
        insemi_before = request.POST['insemi_before']
        is_first_insemi = request.POST['is_first_insemi']
        no_of_insemi = request.POST['no_of_insemi']
        cattle=request.POST['cattle']
    
        obj = farmer_AI_application(
            ai_status='pending',
            prefered_date=prefered_date,
            near_veterinary_hospital=near_hospital,
            inseminated_before=insemi_before,
            is_first_insemination=is_first_insemi,
            no_of_inseminations=no_of_insemi,
            eartagai_id=cattle, 
            farmerai_id=fid,  
        )
        obj.save()
    
    return render(request, 'farmer_ai_request.html',{"pp":pp}) 



def farmer_view_ai_all(request):
    
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    if qq:
        fid=qq[0].id
    
    
    var=farmer_AI_application.objects.filter(farmerai_id=fid)
    
    dic={'key':var}
    
    return render(request,'farmer_ai_viewall.html',dic)


def admin_ai_accept(request,id):
    
    try:
        # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
            application = farmer_AI_application.objects.get(id=id)
            application.ai_status = 'Accepted'
            application.save()
            # Send approval email
            subject = 'Your Artificial insemination Application Request Has Been Approved'
            message = f'Dear {first_name},\n\nWe are pleased to inform you that your application for an Artificial insemination has been approved. This is an important step towards ensuring the health and safety of your livestock. We congratulate you on taking this initiative to manage your animals effectively.\n\nHere are the details of your approved application:\nSpecies: {application.eartagai.species}\nBreed: {application.eartagai.breed}\nRegistration Date: {application.eartagai.regidate} \nNearby veterinary Hospital :{application. near_veterinary_hospital}  \nPreferred Date :{application.prefered_date} \n\nOur team is dedicated to providing you with the best service. Soon, one of our representatives will get in touch with you on your registered mobile number to discuss further details and guide you through the next steps. If you have any questions or need assistance, please do not hesitate to contact our customer support team at 8956-9656-5445-5454 or dairyhubservice@gmail.com.\n\n TEAM DIARYHUB \nThank you!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )

        return HttpResponse("<script> alert('Request Accepted!'),window.location='/myapp/admin_view_ai_all' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_view_ai_all' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_view_ai_all' </script>")

def admin_ai_reject(request,id): 
    try:
        # # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
            
            # Get the eartag application and update its status
        application = farmer_AI_application.objects.get(id=id)
        application.ai_status = 'Rejected'
        application.save()
        # Send approval email
        subject = 'Artficial Insemination Application Rejection'
        message = message = f'Dear {first_name},\n\nWe regret to inform you that your request for artificial insemination has been rejected. We understand your desire to improve your livestock\'s breeding, and we appreciate your initiative to manage your animals effectively.\n\nHowever, after careful review, we found that the application did not meet the necessary requirements due to insufficient or improper details submitted. In order to proceed with the artificial insemination request, we kindly request you to get in touch with our dedicated service team at your earliest convenience. Our team can be reached via email at dairyhubservice@gmail.com or by phone at 8956-9656-5445-5454. They will be able to guide you through the necessary steps to reapply and provide the proper information for processing your artificial insemination request.\n\nTEAM DAIRYHUB \nThank you!'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
                


        return HttpResponse("<script> alert('Request Rejected!'),window.location='/myapp/admin_view_ai_all' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_view_ai_all' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_view_ai_all' </script>")


def farmer_view_re_ai(request):
    
    lid=request.session['login_id']
    qq=farmer_registration.objects.get(login_id=lid)
    request.session['f_id']=qq.pk
    # if qq:
    #     fid=qq.pk
    
    
    var=farmer_AI_re_application.objects.filter(farmerai_id= request.session['f_id'])
    
    dic={'key':var}
    
    return render(request,'farmer_view_re_ai.html',dic)


def admin_re_ai_view(request):
    
    var=farmer_AI_re_application.objects.all()
    

    if request.method=='POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        vals = request.POST['vals']  # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx", from_dates)
            print("Request1yyyyyyy", to_dates)
            var = farmer_AI_re_application.objects.filter(prefered_date__range=[from_date_str, to_date_str])
            print("reportxxx", var)
        else:
            var=farmer_AI_re_application.objects.filter(ai_re_status__icontains=vals)|farmer_AI_re_application.objects.filter(farmerai__farmer_first_name__icontains=vals)|farmer_AI_re_application.objects.filter(eartagai__species__icontains=vals)|farmer_AI_re_application.objects.filter(eartagai__breed__icontains=vals)

    dic = {'key': var}
    
    return render(request,'admin_re_ai_view.html',dic)

def admin_re_ai_report(request):
    var = farmer_AI_re_application.objects.all()
    if request.method == 'POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        if from_date_str and to_date_str:
            var = farmer_AI_re_application.objects.filter(prefered_date__range=[from_date_str, to_date_str])
        else:

            vals = request.POST['vals']
            var = farmer_AI_re_application.objects.filter(
                ai_re_status__icontains=vals) | farmer_AI_re_application.objects.filter(
                farmerai__farmer_first_name__icontains=vals) | farmer_AI_re_application.objects.filter(
                eartagai__species__icontains=vals) | farmer_AI_re_application.objects.filter(
                eartagai__breed__icontains=vals)| farmer_AI_re_application.objects.filter(nearby_hospital__icontains=vals)
    total=len(var)
    dic = {'key': var,"total":total}
    return render(request, 'admin_re_ai_view_report.html', dic)
def admin_re_ai_accept(request,id):
    
    try:
        # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
        
        # Get the eartag application and update its status
        application =farmer_AI_re_application.objects.get(id=id)
        application.ai_re_status = 'Accepted'
        application.save()
        # Send approval email
        subject = 'Your Re-Artificial Insemination Request Has Been Accepted'
        message = f'Dear {first_name},\n\nWe are delighted to inform you that your Artificial Insemination request has been accepted. Your commitment to improving the breeding of your livestock is truly commendable. Congratulations on taking this significant step towards enhancing the quality of your animals.\n\nHere are the details of your accepted request:\nSpecies: {application.eartagai.species}\nBreed: {application.eartagai.breed}\nPrefered Date: {application.prefered_date}\nNear by Veterinary Hospital :{application.nearby_hospital}\n Previous insemination date : {application.prev_insemination_date}\n\nOur dedicated team is committed to providing you with exceptional service. In the coming days, one of our representatives will contact you using your registered contact number to arrange for the Artificial Insemination process and discuss further details. If you have any questions or need assistance, please dont hesitate to reach out to our customer support team at 8956-9656-5445-5454 or via email at dairyhubservice@gmail.com\n\nThank you!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )

        return HttpResponse("<script> alert('Request Accepted!'),window.location='/myapp/admin_re_ai_view' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_re_ai_view' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_re_ai_view' </script>")
    
    
def AI_re_request(request,id,near_veterinary_hospital):
    
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    if qq:
        fid=qq[0].id
    
    if request.method == 'POST':
        
        prev_insemi_date=request.POST['prev_insemi_date']
        nearby_hospital=request.POST['nearby_hospital']
        reason=request.POST['reason']
        pref_date=request.POST['pref_date']
     
        
        obj=farmer_AI_re_application(nearby_hospital=nearby_hospital,eartagai_id=fid,farmerai_id=fid,prev_insemination_date=prev_insemi_date,reason_for_re_request=reason, prefered_date=pref_date,ai_re_status='pending')
                                     
        obj.save()
            
    return render(request,'farmer_ai_re_request.html',{'near_veterinary_hospital':near_veterinary_hospital})  

   


def admin_re_ai_reject(request,id):
    
    
    
    try:
        # # email = request.session['login_id']
        user = farmer_registration.objects.all()
        if user:
            email = user[0].farmer_email
            first_name=user[0].farmer_first_name
            
            # Get the eartag application and update its status
        application = farmer_AI_re_application.objects.get(id=id)
        application.ai_status = 'Rejected'
        application.save()
        # Send approval email
        subject = 'Re-Artficial Insemination Application Rejection'
        message = message = f'Dear {first_name},\n\nWe regret to inform you that your request for artificial insemination has been rejected. We understand your desire to improve your livestock\'s breeding, and we appreciate your initiative to manage your animals effectively.\n\nHowever, after careful review, we found that the application did not meet the necessary requirements due to insufficient or improper details submitted. In order to proceed with the artificial insemination request, we kindly request you to get in touch with our dedicated service team at your earliest convenience. Our team can be reached via email at dairyhubservice@gmail.com or by phone at 8956-9656-5445-5454. They will be able to guide you through the necessary steps to reapply and provide the proper information for processing your artificial insemination request.\n\nTEAM DAIRYHUB \nThank you!'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
                


        return HttpResponse("<script> alert('Request Rejected!'),window.location='/myapp/admin_re_ai_view' </script>")
    except farmer_registration.DoesNotExist:
        return HttpResponse("<script> alert('Error: User not found!'),window.location='/myapp/admin_re_ai_view' </script>")
    except farmer_eartag_application.DoesNotExist:
        return HttpResponse("<script> alert('Error: Eartag application not found!'),window.location='/myapp/admin_re_ai_view' </script>")


def admin_view_ai_report(request):
    var = farmer_AI_application.objects.all()
    if request.method == 'POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
          # Use get() and provide a default value

        # from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
        # to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
        # print("Requestxxxxxxxx", from_dates)
        # print("Request1yyyyyyy", to_dates)
        if from_date_str and to_date_str:
            var = farmer_AI_application.objects.filter(prefered_date__range=[from_date_str, to_date_str])
        else:
            vals = request.POST['vals']
            var = farmer_AI_application.objects.filter(
                ai_status__icontains=vals) | farmer_AI_application.objects.filter(
                farmerai__farmer_first_name__icontains=vals) |  farmer_AI_application.objects.filter(
                eartagai__species__icontains=vals) | farmer_AI_application.objects.filter(
                eartagai__breed__icontains=vals)|farmer_AI_application.objects.filter(near_veterinary_hospital__icontains=vals)



    total=len(var)
    dic = {'key': var,"total":total}

    return render(request, 'admin_view_ai_report.html', dic)


def admin_view_ai_all(request):
    
    var=farmer_AI_application.objects.all()
    if request.method=='POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        vals = request.POST['vals']  # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx", from_dates)
            print("Request1yyyyyyy", to_dates)
            var = farmer_AI_application.objects.filter(prefered_date__range=[from_date_str, to_date_str])
            print("reportxxx", var)
        else:
            var=farmer_AI_application.objects.filter(ai_status__icontains=vals)|farmer_AI_application.objects.filter(farmerai__farmer_first_name__icontains=vals)|farmer_AI_application.objects.filter(eartagai__species__icontains=vals)|farmer_AI_application.objects.filter(eartagai__breed__icontains=vals)

    dic={'key':var}

    
    return render(request,'admin_view_ai_all.html',dic)

def admin_1_ai_view(request,id):
    
    var=farmer_AI_application.objects.filter(id=id)
    
    dic={'key': var}
    
    return render(request,'admin_1_ai_view.html',dic)


def farmer_view_one_product(request, pro_id):
    lid = request.session['login_id']

    request.session["pro_id"] = pro_id

    # if request.method=="POST":
    #     tot=request.POST['to']
    #     rate=request.POST['rate']
    #     qty=request.POST['qty']
    #     current_date = timezone.now().date()
    #     q=bookingmaster.objects.filter(bm_status='pending',login_id=request.session['u_id'])
    #     if q:
    #         bk_id=q[0].bookingmaster_id
    #         total=q[0].bm_total.split(".")
    #         print('........',bk_id)
    #         qqq=booking_child.objects.filter(product_id=pro_id,bookingmaster_id=bk_id)
    #         if qqq:
    #             bc_id=qqq[0].bookingchild_id
    #             bc_qty=qqq[0].bc_qty
    #             bc_amt=qqq[0].bc_amount
    #             qq=booking_child.objects.get(bookingchild_id=bc_id)
    #             qq.bc_qty=int(qty)+int(bc_qty)
    #             qq.bc_amount=int(bc_amt)+int(tot)
    #             qq.save()
    #             q2=bookingmaster.objects.get(bookingmaster_id=bk_id)
    #             q2.bm_total=int(total[0])+int(tot)
    #             q2.save()
    #             # return HttpResponse("<script>alert('Product added to cart');window.location='/customer_view_product/%s'</script>" %id)
    #             return HttpResponse("<script>alert('Product added to cart');window.location='/user_cart_details_view'</script>")
    #         else:
    #             rates=int(qty)*int(rate)
    #             kq=booking_child(bc_qty=qty,bc_amount=tot,bookingmaster_id=bk_id,product_id=pro_id)
    #             kq.save()
    #             q1=bookingmaster.objects.get(bookingmaster_id=bk_id)
    #             q1.bm_total=int(total[0])+int(tot)
    #             q1.save()
    #             # return HttpResponse("<script>alert('Product added to cart');window.location='/customer_view_product/%s'</script>" %id)
    #             return HttpResponse("<script>alert('Product added to cart');window.location='/user_cart_details_view'</script>")
    #     else:
    #         rates=int(qty)*int(rate)
    #         q=bookingmaster(bm_total=tot,bm_date=current_date,bm_status='pending',login_id=request.session['u_id'] )
    #         q.save()
    #         q1=booking_child(bc_qty=qty,bc_amount=tot,bookingmaster_id=q.bookingmaster_id,product_id=pro_id)
    #         q1.save()
    #         # return HttpResponse("<script>alert('Product added to cart ');window.location='/customer_view_product/%s'</script>" %id)
    #         return HttpResponse("<script>alert('Product added to cart');window.location='/user_cart_details_view'</script>")
    # var= Products.objects.get(id=product_id)
    tt = Products.objects.get(id=pro_id)
    ss = {}
    ss['product_name'] = tt.product_name
    ss['amount'] = tt.product_price
    ss['product_description'] = tt.product_description
    ss['product_image'] = tt.product_image

    return render(request, 'farmer_view_one_product.html', ss)
    
def farmer_healthcheckup(request,id):
    
     
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    pp=farmer_eartag_application.objects.filter(farmer=qq[0])
    if qq:
        fid=qq[0].id
    print(qq)
    
    if request.method == 'POST':
        
        conditixxxx=request.POST['medicial_condition']
        symptom=request.POST['symptoms']
        add_services=request.POST['add_services']
        nearby=request.POST['nearby_hospital']
        pref_date=request.POST['preferred_date']
        ii=request.POST['cattle']
    
    
        obj=farmer_health_checkups(check_status='pending',eartag_id=ii,farmer_id=fid,nearby_hospital=nearby,additional_services=add_services,medical_condition=conditixxxx,symptoms=symptom,prefered_date=pref_date)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",obj)
        obj.save()
    
    return render(request, 'farmer_healthcheckup.html',{"pp":pp})
   
    
def farmer_healthcheckup(request):
    
     
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    pp=farmer_eartag_application.objects.filter(farmer=qq[0])
    if qq:
        fid=qq[0].id
    print(qq)
    
    if request.method == 'POST':
        
        conditixxxx=request.POST['medicial_condition']
        symptom=request.POST['symptoms']
        add_services=request.POST['add_services']
        nearby=request.POST['nearby_hospital']
        pref_date=request.POST['preferred_date']
        ii=request.POST['cattle']
    
    
        obj=farmer_health_checkups(check_status='pending',eartag_id=ii,farmer_id=fid,nearby_hospital=nearby,additional_services=add_services,medical_condition=conditixxxx,symptoms=symptom,prefered_date=pref_date)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",obj)
        obj.save()
    
    return render(request, 'farmer_healthcheckup.html',{"pp":pp})

    
def farmer_checkups(request):
    
    
    var=farmer_eartag_application.objects.filter(farmer_id= request.session['f_id'])
    
    dic={'key':var,"pp":var}
    
    return render(request,'farmer_healthcheckup.html',dic)

def farmer_add_to_cart(request):
    tot = request.POST['to']
    rate = request.POST['rate']
    qty = request.POST['qty']
    current_date = timezone.now().date()
    pid=request.session["pro_id"]
    p = Products.objects.get(id=request.session["pro_id"])
    if int(p.product_quantity) < int(qty):
        return HttpResponse("<script> alert('requested qty not available');window.location='/myapp/farmer_view_one_product/"+pid+"#m' </script>")

    else:
        qqq = Cart.objects.filter(PRODUCTS_id=request.session["pro_id"], LOGIN_id=request.session["lid"])
        if qqq.exists():
            cart_id = qqq[0].id
            cart_qty = qqq[0].qty
            print("und")

            qq = Cart.objects.get(id=cart_id)
            qq.qty = int(qty) + int(cart_qty)
            qq.save()
        else:
            qq = Cart()
            qq.qty = int(qty)
            qq.LOGIN_id=request.session["lid"]
            qq.PRODUCTS_id=request.session["pro_id"]
            qq.save()
        return  HttpResponse("<script> alert('Added to cart'),window.location='/myapp/farmer_page#m' </script>")


def farmer_cart_details_view(request):
    l = []

    rot = 0

    var = Cart.objects.filter(LOGIN_id=request.session["lid"])
    for i in var:
        amount = int(i.PRODUCTS.product_price) * int(i.qty)
        rot += amount
        l.append({"id": i.id, "product_name": i.PRODUCTS.product_name, "image": i.PRODUCTS.product_image,
                  "product_price": i.PRODUCTS.product_price, "qty": i.qty, "amount": amount})
    dic = {'item': l, "total": rot}
    print(dic)
    request.session["carttotal"] = rot
    return render(request, 'farmer_cart_details_view.html', dic)


def farmer_fav_view(request):
    l = []

    rot = 0

    var = Favourites.objects.filter(LOGIN_id=request.session["lid"])

    dic = {'item': var}
    print(dic)

    return render(request, 'farmer_fav_view.html', dic)

def farmer_removecart(request, id):
    cart = Cart.objects.filter(id=id).delete()
    return HttpResponse("<script> alert('Removed from cart'),window.location='/myapp/farmer_cart_details_view' </script>")


def farmer_sa(request):
    current_date = timezone.now().date()
    if request.session["bmid"]==0:
        q = bookingmaster()
        q.bm_date = current_date
        q.bm_total = request.session["carttotal"]
        q.login_id = request.session["lid"]
        q.bm_status = "pending"
        q.save()
        print ("meeeee",q.bookingmaster_id)
        request.session["bmid"]=q.bookingmaster_id
    return render(request, "farmer_sa.html", {"total": request.session["carttotal"]})

def farmer_sa_post(request):

    toname = request.POST["toname"]
    address = request.POST["address"]
    place = request.POST["place"]
    post = request.POST["post"]
    pin = request.POST["pin"]
    district = request.POST["district"]
    state = request.POST["state"]
    phone = request.POST["phone"]
    email = request.POST["email"]
    q = delivery_address()
    q.BOOKING_id=request.session["bmid"]
    q.dname = toname
    q.daddress = address
    q.dplace = place
    q.dpin = pin
    q.ddistrict=district
    q.dphone=phone
    q.dpost=post
    q.demail=email
    q.dstate=state

    q.save()
#     return render(request, "farmer_sa.html", {"total": request.session["carttotal"]})
#
    return render(request, "farmer_make_full_payment.html", {"total": request.session["carttotal"]})


def farmer_pay(request):
    return render(request,"farmer_make_full_payment.html",{"total":request.session["carttotal"]})


def farmer_pay_post(request):
    cno=request.POST["cno"]
    edate=request.POST["edate"]
    names=request.POST["names"]
    cvv=request.POST["cvv"]
    print(cvv,names,edate,cno)
    f=Bank.objects.filter(cvv=cvv,expiry=edate,name=names,number=cno)
    if f.exists():
        d=Bank.objects.get(cvv=cvv,expiry=edate,name=names,number=cno)
        if int(d.balance)<request.session["carttotal"]:
            return HttpResponse("<script> alert('Insufficient Balance'),window.location='/myapp/farmer_pay' </script>")
        else:
            qqq = Cart.objects.filter(LOGIN_id=request.session["lid"])



            for i in qqq:
                total=int(i.PRODUCTS.product_price)*int(i.qty)

                kq=booking_child(bc_qty=i.qty,bc_amount=total,bookingmaster_id=request.session["bmid"],product_id=i.PRODUCTS.id)
                kq.save()

                p = Products.objects.get(id=i.PRODUCTS.id)
                p.product_quantity=int(p.product_quantity)-int(i.qty)
                p.save()

                dc=Cart.objects.get(id=i.id)
                dc.delete()

            q1=bookingmaster.objects.filter(pk=request.session["bmid"]).update(bm_status="Payment Done")

            d.balance=int(d.balance)-int(request.session["carttotal"])
            d.save()
            request.session["bmid"]=0
            return HttpResponse("<script> alert('Success'),window.location='/myapp/farmer_view_own_orders' </script>")

    else:
        return HttpResponse("<script> alert('Invalid Card Details'),window.location='/myapp/farmer_pay' </script>")
def farmer_view_own_orders(request):
    data=bookingmaster.objects.filter(login_id=request.session["lid"])

    return render(request,"farmer_view_own_orders.html",{"data":data})

def farmer_view_order_more(request,id):

    data=booking_child.objects.filter(bookingmaster=bookingmaster.objects.get(pk=id))
    l=[]
    for i in data:


        l.append({"id":i.bookingchild_id,"product_name":i.product.product_name,"image":i.product.product_image,"product_price":i.product.product_price,"qty":i.bc_qty,"amount":i.bc_amount})

    total=bookingmaster.objects.get(pk=id).bm_total
    print(l)
    f = delivery_address.objects.get(BOOKING_id=id)
    return render(request,"farmer_order_more.html",{"data":l,"total":total,'f':f})
def farmer_view_checkup(request):
    
    lid=request.session['login_id']
    qq=farmer_registration.objects.get(login_id=lid)
    request.session['f_id']=qq.pk
    # if qq:
    #     fid=qq.pk
    
    
    var=farmer_health_checkups.objects.filter(farmer_id= request.session['f_id'])
    
    dic={'key':var}
    
    return render(request,'farmer_view_checkup.html',dic)


def admin_view_checkups(request):
    
    var=farmer_health_checkups.objects.all()
    if request.method == 'POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        vals = request.POST['vals']  # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx", from_dates)
            print("Request1yyyyyyy", to_dates)
            var = farmer_health_checkups.objects.filter(prefered_date__range=[from_date_str, to_date_str])
            print("reportxxx", var)
        else:
            var = farmer_health_checkups.objects.filter(
                check_status__icontains=vals) | farmer_health_checkups.objects.filter(
                farmer__farmer_first_name__icontains=vals) | farmer_health_checkups.objects.filter(
                eartag__species__icontains=vals) | farmer_health_checkups.objects.filter(
                eartag__breed__icontains=vals)

    dic={'key':var}
    
    return render(request,'admin_view_checkups.html',dic)


def admin_view_checkups_report(request):
    var = farmer_health_checkups.objects.all()


    if request.method == 'POST':
        from_date_str = request.POST['start_date']
        to_date_str = request.POST['end_date']
        print("Request", from_date_str)
        print("Request1", to_date_str)
        # Use get() and provide a default value
        if from_date_str and to_date_str:
            from_dates = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_dates = datetime.strptime(to_date_str, '%Y-%m-%d')
            print("Requestxxxxxxxx", from_dates)
            print("Request1yyyyyyy", to_dates)
            var = farmer_health_checkups.objects.filter(prefered_date__range=[from_date_str, to_date_str])
            print("reportxxx", var)
        else:
            vals=request.POST["vals"]
            var = farmer_health_checkups.objects.filter(
                check_status__icontains=vals) | farmer_health_checkups.objects.filter(
                farmer__farmer_first_name__icontains=vals) | farmer_health_checkups.objects.filter(
                eartag__species__icontains=vals) | farmer_health_checkups.objects.filter(
                eartag__breed__icontains=vals)

    total=len(var)
    dic = {'key': var,"total":total}
    return render(request, 'admin_view_checkups_reports.html', dic)
def admin_1_view_checkup(request,id):
    
    var=farmer_health_checkups.objects.filter(id=id)
    
    dic={'key': var}
    
    return render(request,'admin_1_view_checkup.html',dic)


def admin_checkup_accept(request,id):
    
    q=farmer_health_checkups.objects.get(id=id)
    q.check_status='Accepted'
    q.save()
    
    return HttpResponse("<script> alert('Request Accepted!'),window.location='/myapp/admin_view_checkups' </script>")


def admin_checkup_reject(request,id):
    
    
    q=farmer_health_checkups.objects.get(id=id)
    
    q.check_status='Rejected'
    q.save()
    
    return HttpResponse("<script> alert('Request Rejected!'),window.location='/myapp/admin_view_checkups' </script>")


def farmer_view_profile(request):
    data=farmer_registration.objects.get(login_id=request.session["lid"])
    return render(request,"farmer_profile.html",{"data":data})



#############users #############


def user_home(request):
    
    
    return render(request, 'uindex.html')

def user_page(request):
    products=Products.objects.filter(product_category="Dairy")
    print("haiiiiiiiiiiiiiiiiiiiii",products)
    return render(request, 'user_page.html', {'products':products})


def user_view_one_product(request, pro_id):
    
    lid=request.session['login_id']
    qq=user_registration.objects.get(login_id=lid)
    request.session["pro_id"]=pro_id
    request.session['u_id']=qq.pk
    # if request.method=="POST":
    #     tot=request.POST['to']
    #     rate=request.POST['rate']
    #     qty=request.POST['qty']
    #     current_date = timezone.now().date()
    #     q=bookingmaster.objects.filter(bm_status='pending',login_id=request.session['u_id'])
    #     if q:
    #         bk_id=q[0].bookingmaster_id
    #         total=q[0].bm_total.split(".")
    #         print('........',bk_id)
    #         qqq=booking_child.objects.filter(product_id=pro_id,bookingmaster_id=bk_id)
    #         if qqq:
    #             bc_id=qqq[0].bookingchild_id
    #             bc_qty=qqq[0].bc_qty
    #             bc_amt=qqq[0].bc_amount
    #             qq=booking_child.objects.get(bookingchild_id=bc_id)
    #             qq.bc_qty=int(qty)+int(bc_qty)
    #             qq.bc_amount=int(bc_amt)+int(tot)
    #             qq.save()
    #             q2=bookingmaster.objects.get(bookingmaster_id=bk_id)
    #             q2.bm_total=int(total[0])+int(tot)
    #             q2.save()
    #             # return HttpResponse("<script>alert('Product added to cart');window.location='/customer_view_product/%s'</script>" %id)
    #             return HttpResponse("<script>alert('Product added to cart');window.location='/user_cart_details_view'</script>")
    #         else:
    #             rates=int(qty)*int(rate)
    #             kq=booking_child(bc_qty=qty,bc_amount=tot,bookingmaster_id=bk_id,product_id=pro_id)
    #             kq.save()
    #             q1=bookingmaster.objects.get(bookingmaster_id=bk_id)
    #             q1.bm_total=int(total[0])+int(tot)
    #             q1.save()
    #             # return HttpResponse("<script>alert('Product added to cart');window.location='/customer_view_product/%s'</script>" %id)
    #             return HttpResponse("<script>alert('Product added to cart');window.location='/user_cart_details_view'</script>")
    #     else:
    #         rates=int(qty)*int(rate)
    #         q=bookingmaster(bm_total=tot,bm_date=current_date,bm_status='pending',login_id=request.session['u_id'] )
    #         q.save()
    #         q1=booking_child(bc_qty=qty,bc_amount=tot,bookingmaster_id=q.bookingmaster_id,product_id=pro_id)
    #         q1.save()
    #         # return HttpResponse("<script>alert('Product added to cart ');window.location='/customer_view_product/%s'</script>" %id)
    #         return HttpResponse("<script>alert('Product added to cart');window.location='/user_cart_details_view'</script>")
    # var= Products.objects.get(id=product_id)
    tt=Products.objects.get(id=pro_id)
    ss={}
    ss['product_name']=tt.product_name
    ss['amount']=tt.product_price
    ss['product_description']=tt.product_description
    ss['product_image']=tt.product_image
    

    return render(request, 'user_view_one_product.html',ss)

def user_add_to_cart(request):
    tot = request.POST['to']
    rate = request.POST['rate']
    qty = request.POST['qty']
    current_date = timezone.now().date()



    qqq = Cart.objects.filter(PRODUCTS_id=request.session["pro_id"], LOGIN_id=request.session["lid"])
    if qqq.exists():
        cart_id = qqq[0].id
        cart_qty = qqq[0].qty
        print("und")

        qq = Cart.objects.get(id=cart_id)
        qq.qty = int(qty) + int(cart_qty)
        qq.save()
    else:
        qq = Cart()
        qq.qty = int(qty)
        qq.LOGIN_id=request.session["lid"]
        qq.PRODUCTS_id=request.session["pro_id"]
        qq.save()
    return  HttpResponse("<script> alert('Added to cart'),window.location='/myapp/user_page' </script>")

def user_cart_details_view(request):
    
    l=[]


    rot=0

    var=Cart.objects.filter(LOGIN_id=request.session["lid"])
    for i in var:
        amount=int(i.PRODUCTS.product_price)*int(i.qty)
        rot+=amount
        l.append({"id":i.id,"product_name":i.PRODUCTS.product_name,"image":i.PRODUCTS.product_image,"product_price":i.PRODUCTS.product_price,"qty":i.qty,"amount":amount})
    dic={'item':l,"total":rot}
    print(dic)
    request.session["carttotal"]=rot
    return render(request,'user_cart_details_view.html',dic)


def user_removecart(request,id):
    cart=Cart.objects.filter(id=id).delete()
    return HttpResponse("<script> alert('Removed from cart'),window.location='/myapp/user_cart_details_view' </script>")


def farmer_removecart(request, id):
    cart = Cart.objects.filter(id=id).delete()
    return HttpResponse("<script> alert('Removed from cart'),window.location='/myapp/farmer_cart_details_view' </script>")


def user_view_profile(request):
    data=user_registration.objects.get(login_id=request.session["lid"])
    return render(request,"user_profile.html",{"data":data})


def user_sa(request):
    current_date = timezone.now().date()
    if request.session["bmid"]==0:
        q = bookingmaster()
        q.bm_date = current_date
        q.bm_total = request.session["carttotal"]
        q.login_id = request.session["lid"]
        q.bm_status = "pending"
        q.save()

        request.session["bmid"]=q.bookingmaster_id
    return render(request, "user_sa.html", {"total": request.session["carttotal"]})

def user_sa_post(request):

    toname = request.POST["toname"]
    address = request.POST["address"]
    place = request.POST["place"]
    post = request.POST["post"]
    pin = request.POST["pin"]
    district = request.POST["district"]
    state = request.POST["state"]
    phone = request.POST["phone"]
    email = request.POST["email"]
    q = delivery_address()
    q.BOOKING_id=request.session["bmid"]
    q.dname = toname
    q.daddress = address
    q.dplace = place
    q.dpin = pin
    q.ddistrict=district
    q.dphone=phone
    q.dpost=post
    q.demail=email
    q.dstate=state

    q.save()
#     return render(request, "farmer_sa.html", {"total": request.session["carttotal"]})
#
    return render(request, "user_make_full_payment.html", {"total": request.session["carttotal"]})



def user_pay(request):

    return render(request,"user_make_full_payment.html",{"total":request.session["carttotal"]})


def user_pay_post(request):
    cno=request.POST["cno"]
    edate=request.POST["edate"]
    names=request.POST["names"]
    cvv=request.POST["cvv"]
    print(cvv,names,edate,cno)
    f=Bank.objects.filter(cvv=cvv,expiry=edate,name=names,number=cno)
    if f.exists():
        d=Bank.objects.get(cvv=cvv,expiry=edate,name=names,number=cno)
        if int(d.balance)<request.session["carttotal"]:
            return HttpResponse("<script> alert('Insufficient Balance'),window.location='/myapp/user_pay' </script>")
        else:
            qqq = Cart.objects.filter(LOGIN_id=request.session["lid"])
            # current_date = timezone.now().date()
            # q=bookingmaster()
            # q.bm_date=current_date
            # q.bm_total=request.session["carttotal"]
            # q.login_id=request.session["lid"]
            # q.status="pending"
            # q.save()
            for i in qqq:
                total=int(i.PRODUCTS.product_price)*int(i.qty)

                kq=booking_child(bc_qty=i.qty,bc_amount=total,bookingmaster_id=request.session["bmid"],product_id=i.PRODUCTS.id)
                kq.save()

                dc = Cart.objects.get(id=i.id)
                dc.delete()

            q1=bookingmaster.objects.filter(pk=request.session["bmid"]).update(bm_status="Payment Done")

            d.balance=int(d.balance)-int(request.session["carttotal"])
            d.save()
            request.session["bmid"] = 0
            return HttpResponse("<script> alert('Success'),window.location='/myapp/user_view_own_orders' </script>")

    else:
        return HttpResponse("<script> alert('Invalid Card Details'),window.location='/myapp/user_pay#m' </script>")


def user_view_own_orders(request):
    data=bookingmaster.objects.filter(login_id=request.session["lid"])

    return render(request,"user_view_own_orders.html",{"data":data})

def user_view_order_more(request,id):

    data=booking_child.objects.filter(bookingmaster=bookingmaster.objects.get(pk=id))
    l=[]
    for i in data:


        l.append({"id":i.bookingchild_id,"product_name":i.product.product_name,"image":i.product.product_image,"product_price":i.product.product_price,"qty":i.bc_qty,"amount":i.bc_amount})

    total=bookingmaster.objects.get(pk=id).bm_total
    print(l)
    f = delivery_address.objects.get(BOOKING_id=id)
    return render(request,"user_order_more.html",{"data":l,"total":total,'f':f})

def user_fav_view(request):
    l = []

    rot = 0

    var = Favourites.objects.filter(LOGIN_id=request.session["lid"])

    dic = {'item': var}
    print(dic)

    return render(request, 'user_fav_view.html', dic)

def user_fav_product(request,id):
    g = Favourites.objects.filter(LOGIN_id=request.session["lid"], PRODUCTS_id=id)
    if g.exists():
        return HttpResponse("<script> alert('Already Added to Favourites'),window.location='/myapp/user_page#m' </script>")

    else:
        f = Favourites()
        f.LOGIN_id = request.session["lid"]
        f.PRODUCTS_id = id
        f.save()
        return   HttpResponse("<script> alert('Added to Favourites'),window.location='/myapp/user_page#m' </script>")

def farmer_delete_fav(request,id):
    d=Favourites.objects.filter(PRODUCTS_id=id).delete()
    return HttpResponse("<script> alert('deleted'),window.location='/myapp/farmer_fav_view#m' </script>")
def user_delete_fav(request,id):
    d = Favourites.objects.filter(PRODUCTS_id=id).delete()
    return HttpResponse("<script> alert('deleted'),window.location='/myapp/user_fav_view#m' </script>")

def farmer_healthcheckup(request):
    
     
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    pp=farmer_eartag_application.objects.filter(farmer=qq[0])
    if qq:
        fid=qq[0].id
    print(qq)
    
    if request.method == 'POST':
        
        conditixxxx=request.POST['medicial_condition']
        symptom=request.POST['symptoms']
        add_services=request.POST['add_services']
        nearby=request.POST['nearby_hospital']
        pref_date=request.POST['preferred_date']
        ii=request.POST['cattle']
    
    
        obj=farmer_health_checkups(check_status='pending',eartag_id=ii,farmer_id=fid,nearby_hospital=nearby,additional_services=add_services,medical_condition=conditixxxx,symptoms=symptom,prefered_date=pref_date)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",obj)
        obj.save()
    
    return render(request, 'farmer_healthcheckup.html',{"pp":pp})
'''
def farmer_vaccine(request): 
    lid=request.session['login_id']
    qq=farmer_registration.objects.filter(login_id=lid)
    pp=farmer_eartag_application.objects.filter(farmer=qq[0])
    if qq:
        fid=qq[0].id
    print(qq)
    
    if request.method == 'POST':
        vacc_type=request.POST['vaccine']
        prefered_dat=request.POST['prefered_date']
        nearby=request.POST['nearby_hospital']
        ii=request.POST['cattle']
        
        obj=vaccine(check_status='pending',eartag_id=ii,farmer_id=fid,nearby_hospital=nearby, vaccination_type=vacc_type,prefered_date=prefered_dat)
        print(obj)
        obj.save()
    return render(request, 'farmer_vaccine.html',{"pp":pp})


def farmer_view_vaccine(request):
    
    lid=request.session['login_id']
    qq=farmer_registration.objects.get(login_id=lid)
    request.session['f_id']=qq.pk
    # if qq:
    #     fid=qq.pk
    
    
    var=vaccine.objects.filter(farmer_id= request.session['f_id'])
    
    dic={'key':var}
    
    return render(request,'farmer_view_vaccine.html',dic)
        
    '''
    
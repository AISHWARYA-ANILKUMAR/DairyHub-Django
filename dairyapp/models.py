from django.db import models

# Create your models here.

class login(models.Model):
     
     username = models.CharField(max_length=64)
     password = models.CharField(max_length=64)
     usertype=models.CharField(max_length=64)
 
    
class user_registration(models.Model): 
     login=models.ForeignKey('login',on_delete=models.CASCADE)
     first_name=models.CharField(max_length=50)
     last_name=models.CharField(max_length=50)
     email=models.EmailField(null=True)
     phone=models.BigIntegerField()
     address = models.CharField(max_length=200)
     district = models.CharField(max_length=100)
     state = models.CharField(max_length=100)
     country = models.CharField(max_length=100)
     
     
class farmer_registration(models.Model):
     
     login=models.ForeignKey('login',on_delete=models.CASCADE)
     farmer_first_name=models.CharField(max_length=50)
     farmer_last_name=models.CharField(max_length=50)
     farmer_email=models.EmailField(null=True)
     farmer_phone=models.BigIntegerField()
     farmer_category = models.CharField(max_length=10)
     farmer_aadar = models.BigIntegerField()
     farmer_address = models.CharField(max_length=200)
     farmer_district = models.CharField(max_length=100)
     farmer_state = models.CharField(max_length=100)
     farmer_country = models.CharField(max_length=100)
     
class farmer_eartag_application(models.Model):
    
    farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    regidate = models.DateField()
    dob = models.DateField()
    colour = models.CharField(max_length=50)
    sire_id = models.CharField(max_length=50)
    pregnancy = models.CharField(max_length=50)
    pregnancymonth =models.CharField(max_length=50)
    milkingstatus = models.CharField(max_length=50)
    eartag_status = models.CharField(max_length=50)
    
class Products(models.Model):
     
     product_name = models.CharField(max_length=100)
     product_image = models.CharField(max_length=200)
     product_price = models.FloatField()
     product_quantity = models.IntegerField()
     product_category = models.CharField(max_length=100,default="Dairy")
     product_description = models.CharField(max_length=200)
     
class farmer_eartag_re_application(models.Model):
     
     farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
     eartag=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
     prev_eartag_no=models.CharField(default="",max_length=50)
     prev_eartag_regi_date=models.DateField()
     new_eartag_regi_date=models.DateField()
     missing_date=models.DateField()
     additional_details=models.CharField(max_length=200)
     eartag_miss_status = models.CharField(max_length=50)


class farmer_AI_application(models.Model):

    farmerai=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    eartagai=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
    prefered_date=models.DateField()
    near_veterinary_hospital=models.CharField(max_length=100)
    inseminated_before=models.CharField(max_length=10)
    is_first_insemination=models.CharField(max_length=10)
    no_of_inseminations=models.CharField(max_length=10)
    ai_status=models.CharField(max_length=10)


class farmer_AI_re_application(models.Model):
    
    farmerai=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    eartagai=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
    nearby_hospital=models.CharField(max_length=50)
    prev_insemination_date=models.DateField()
    reason_for_re_request=models.TextField()
    prefered_date=models.DateField()
    ai_re_status=models.CharField(max_length=20)
    
    

class farmer_health_checkups(models.Model):
    
    farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    eartag=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
    medical_condition=models.CharField(max_length=200)
    symptoms=models.CharField(max_length=200)
    additional_services=models.CharField(max_length=50)
    nearby_hospital=models.CharField(max_length=100)
    prefered_date=models.DateField()
    check_status=models.CharField(max_length=50)
    
class bookingmaster(models.Model):
     
     bookingmaster_id=models.AutoField(primary_key=True)
     bm_date=models.DateField(default="2023-10-10")
     bm_total=models.FloatField()
     login_id=models.CharField(max_length=56)
     bm_status=models.CharField(max_length=56)
     
class booking_child(models.Model):
     
     bookingchild_id=models.AutoField(primary_key=True)
     bookingmaster=models.ForeignKey('bookingMaster',on_delete=models.CASCADE)
     product=models.ForeignKey('Products', on_delete=models.CASCADE)
     bc_qty=models.IntegerField()
     bc_amount=models.FloatField()
     
class Cart(models.Model):
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)
    PRODUCTS=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty=models.IntegerField()
class Bank(models.Model):
    name=models.CharField(max_length=50)
    number=models.BigIntegerField()
    cvv=models.BigIntegerField()
    expiry=models.CharField(max_length=50)
    balance=models.BigIntegerField()

class Favourites(models.Model):
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)
    PRODUCTS=models.ForeignKey(Products,on_delete=models.CASCADE)



class delivery_address(models.Model):
    BOOKING = models.ForeignKey(bookingmaster, on_delete=models.CASCADE)
    dname = models.CharField(max_length=50)
    daddress = models.CharField(max_length=50)
    dplace=models.CharField(max_length=50,default="")
    dpin = models.IntegerField()
    ddistrict=models.CharField(max_length=50)
    dphone = models.BigIntegerField()
    dpost = models.CharField(max_length=64)
    demail = models.EmailField(null=True)
    dstate = models.CharField(max_length=10)
    
class vaccine(models.Model):
    
    farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    eartag=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
    vaccination_type=models.CharField(max_length=64)
    nearby_hospital=models.CharField(max_length=100)
    prefered_date=models.DateField()
    check_status=models.CharField(max_length=50)
    
    
    
 




     
     
    
    
   
     
    
     


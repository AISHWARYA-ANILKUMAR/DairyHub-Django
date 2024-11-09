''''
class farmer_eartag_re_request(models.Model):
     
     farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
     eartag=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
     prev_eartag_no=models.CharField(max_length=20)
     prev_eartag_issue_date=models.DateField()
     missing_date=models.DateField()
     additional_details=models.CharField(max_length=200)
     
     
def eartag_re_request(request):
    
    if request.method == 'POST':
        
        prev_eartagno=request.POST['prev_eartagno']
        prev_eartag_issue_date=request.POST['prev_eartag_issue_date']
        missing_date=request.POST['missing_date']
        additional_details=request.POST['additional_details']
        farmerid=request.POST['farmerid']
        eartagid=request.POST['eartagid']
        
        q=farmer_register.objects.all()
        obj=farmer_eartag_re_request(eartag_id=eartagid,prev_eartag_no=prev_eartagno,rev_eartag_issue_date=prev_eartag_issue_date,missing_date=missing_date,additional_details=additional_details,farmer_id=farmerid)
        obj.save()
        
       
    return render(request,'farmer_eartag_re_request.html',{'farmerdrop':q})

class farmer_AI_application(models.Model):
    
    farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    eartag=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
    prefered_date=models.DateField()
    
    
       
def  AI_request(request):
    
    
    prefered_date =request.POST['prefered_date']
    farmerid=request.POST['farmerid']
    eartagid=request.POST['eartagid']
    
    obj=farmer_AI_application(eartag_id=eartagid,farmer_id=farmerid,prefered_date=prefered_date)
    obj.save()
    
    return render(request,'farmer_AI_request.html')


class farmer_AI_re_application(models.Model):
    
    farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    eartag=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
    prev_insemination_date=models.DateTimeField()
    reason_for_re_request=models.Charfield(max_length=200)
    prefered_date=models.DateTimeField()
   
def AI_re_request(request):
    
    
    prev_insemination_date=request.POST['prev_insemination_date']
    reason_for_re_request=request.POST['reason_for_re_request']
    prefered_date=request.POST['prefered_date']
    farmerid=request.POST['farmerid']
    eartagid=request.POST['eartagid']
    
    obj=farmer_AI_re_application(eartag_id=eartagid,farmer_id=farmerid,prev_insemination_date=prev_insemination_date,reason_for_re_request=reason_for_re_request,prefered_date=prefered_date)
    obj.save()
    
    return render(request,'farmer_AI_re_request.html')

class farmer_heath_checkup(models.Model):
    
    farmer=models.ForeignKey('farmer_registration',on_delete=models.CASCADE)
    eartag=models.ForeignKey('farmer_eartag_application',on_delete=models.CASCADE)
    pregnancy_care=models.CharField(max_length=20)
    medical_condition=models.CharField(max_length=200)
    symptoms=models.CharField(max_length=200)
    prefered_date=models.DateField()
    
def health_checkup(request):
    
    pregnancy_care=request.POST['pregnancy_care']
    medicial_condition=request.POST['medicial_condition']
    symptoms=request.POST['symptoms']
    prefered_date=request.POST['preferred_date']
    farmerid=request.POST['farmerid']
    eartagid=request.POST['eartagid']
    
    obj=farmer_heath_checkup(eartag_id=eartagid,farmer_id=farmerid,pregnancy_care=pregnancy_care,medicial_condition=medicial_condition,symptoms=symptoms,prefered_date=prefered_date)
    obj.save()
    
    
    path('eartag_re_request',views.eartag_re_request),
    path(' AI_request',views.AI_request),
    path(' AI_re_request',views.AI_re_request),
    path('health_checkup',views.health_checkup),
    
    '''
'''   
def admin_accept(request,id):
    
    lid=request.session['login_id']
    email=farmer_registration.objects.get(login_id=lid)
    request.session['f_id']=email
    
    q=farmer_eartag_application.objects.all()
    q.eartag_status='Accepted'
    q.save()
    
    subject = 'Your Eartag Application Request Has Been Approved'
        # message = f"Accepted  \n Having Wonderful day"
    message = f'Hello {farmer_registration.username},\n\n  We are pleased to inform you that your application for an eartag has been approved.This is an important step towards ensuring the health and safety of your livestock. We congratulate you on taking this initiative to manage your animals effectively.Here are the details of your approved application:Species: {species} Breed:{breed} Registration Date :{regidate}.Our team is dedicated to providing you with the best service. Soon, one of our representatives will get in touch with you on your registered mobile number to discuss further details and guide you through the next steps.if you have any questions or need assistance, please do not hesitate to contact our customer support team at 8956-9656-5445-5454 or dairyhubservice@gmail.com.\n\nThank you!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
        # subject = 'Your Login Credentials'
        # message = f'Hello {tbl_login.username},\n\nYour login credentials are:\nUsername: {{uname}}\nPassword: {{passs}}\n\nThank you!'
        # from_email = 'your_email@gmail.com'  # Replace with your Gmail email address or any other email address
        # # Send the email
        # # send_mail(subject, message, from_email, [tbl_voter.v_email])
   
    return HttpResponse("<script> alert('Request Accepted!'),window.location='/admin_view_eartag_request' </script>")
'''

'''


def admin_view_eartag_request(request):
      
    if request.method=='POST':
        #check=request.POST['check']
        vals=request.POST['vals']
        #print(check)
        view=farmer_eartag_application.objects.filter(farmer__farmer_first_name__icontains=vals)|farmer_eartag_application.objects.filter(eartag_status__icontains=vals)|farmer_eartag_application.objects.filter(species__icontains=vals)|farmer_eartag_application.objects.filter(breed__icontains=vals)|farmer_eartag_application.objects.filter(gender__icontains=vals)
    
    else:
        view=farmer_eartag_application.objects.all()
        # dic={'key':var}
        
    return render(request,'admin_view_eartag_request.html',{'view':view})
    
    
    <form method="post">
        <div class="row">
            <div class="col-md-6 offset-md-3">
                <div class="input-group mb-3">
                    <input type="text" class="form-control" placeholder="Search for details" name="vals">
                    <div class="input-group-append">
                        <button class="btn btn-outline-secondary" type="submit">search</button>
                            
                            
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </form>
    
    
    
    '''
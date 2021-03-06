 
#importing loading from django template  
from django.template import loader  
# Create your views here.  

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.http import FileResponse

# reportlab headers
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Frame

from reportlab.lib.colors import red, yellow, green

import io, base64

import cv2
from imageio import imread
import matplotlib.pyplot as plt

from mailer import Mailer
from mailer import Message


###################################Email LIBS#########################################
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

from babel.numbers import format_decimal
from babel.numbers import format_number
from babel.numbers import format_currency

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound

from email.mime.application import MIMEApplication
from os.path import basename
import email
import email.mime.application
 
import re
import os


from babel import Locale
from babel.numbers import decimal
import numpy as np
from PIL import Image, ImageDraw

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))

def custom_format_currency(value, currency, locale):
    value = decimal.Decimal(value)
    locale = Locale.parse(locale)
    pattern = locale.currency_formats['standard']
    force_frac = ((0, 0) if value == int(value) else None)
    return pattern.apply(value, locale, currency=currency, force_frac=force_frac)

# Create your views here.
def index(request):
    return render(request,'index.html')

def template1(request,userId=None):
   
    userId = request.GET["userId"]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from usData,us_image where usData.id=us_image.id and usData.id='{}'".format(userId))
        myresult = cursor.fetchall()
        # print('myresult:',myresult)
        if not myresult:
            template = loader.get_template('notFound.html') # getting our template  
            return HttpResponse(template.render())       # rendering the template in HttpResponse 
            return render(request,'notFound.html') 
        for x in myresult:
    
            var = myresult[0]
            
            PersonName=x[0]
            FullName = x[1]+' '+x[2]
            Fname = x[1]
            Lname = x[2]
            
            Per_Age             =x[3]
            if not Per_Age:
                Per_Age='NA'
            Address             =x[4] #+','+x[45]
            if not Address:
                Address='NA'
            Spouse_Age          =x[5]
            
            if not Spouse_Age:
                Spouse_Age          ='NA'
            else:
                Spouse_Age          ='Age:  '+x[5]
                
            Dep_Employment      =x[6]
            
            if not Dep_Employment:
                Dep_Employment          ='NA'
                               
            Dep_Salary          =x[7]
            
            if not Dep_Salary:
                Dep_Salary          ='NA'
            else:
                Dep_Salary = x[7]
                print(Dep_Salary)
                
                Dep_Salary = int(float(Dep_Salary))
                Dep_Salary = custom_format_currency(Dep_Salary, 'USD', locale='en_US')    
            Dep_Media           =x[8]
            if not Dep_Media:
                Dep_Media='NA'
                
            Education           =x[9]
            if not Education:
                Education          ='NA'
            
            Per_Employment      =x[10]
            
            if Per_Employment:
                perEmpl=Per_Employment.split(',')
            else:
                perEmpl=''

            
            Job_Desc            =x[11]
            if Job_Desc:
                JobDesc=Job_Desc.split(',')
            else:
                JobDesc=''
            
                
            Per_Salary          =x[12]
            if not Per_Salary:
                Per_Salary          ='NA'
            else:
                Per_Salary = x[12]
                # Per_Salary = round(Per_Salary)
                Per_Salary = int(float(Per_Salary))
                Per_Salary = custom_format_currency(Per_Salary, 'USD', locale='en_US')
            Input_Pop           =x[13]
            if not Input_Pop:
                Input_Pop='NA'
            Median_HouseHold_Val=x[14]
            if not Median_HouseHold_Val:
                Median_HouseHold_Val='NA'
            else:
                Median_HouseHold_Val=x[14]
                # Median_HouseHold_Val = round(Median_HouseHold_Val)
                Median_HouseHold_Val = custom_format_currency(Median_HouseHold_Val, 'USD', locale='en_US')
            Home_Val            =x[15]
            if not Home_Val:
                Home_Val='NA'
            else:
                Home_Val=x[15]
                Home_Val = custom_format_currency(Home_Val, 'USD', locale='en_US')
            Esti_Home_Equi      =x[16]
            if not Esti_Home_Equi:
                Esti_Home_Equi='NA'
            else:
                Esti_Home_Equi      =x[16]
                Esti_Home_Equi = int(float(Esti_Home_Equi))
                
                Esti_Home_Equi = custom_format_currency(Esti_Home_Equi, 'USD', locale='en_US')
            Mort_Amt            =x[17]
            if not Mort_Amt:
                Mort_Amt='NA'
            else:
                Mort_Amt            =x[17]
                Mort_Amt = int(float(Mort_Amt))
                
                Mort_Amt = custom_format_currency(Mort_Amt, 'USD', locale='en_US')
            Mort_Date           =x[18]
            
            if not Mort_Date:
                Mort_Date='NA'
                
            Vehicle_det         =x[19]
            # print('Vehicle_det',Vehicle_det)
            if Vehicle_det:
                regVehicles=Vehicle_det.split(',')
            else:
                regVehicles=''
            
            Per_facebook        =x[20]
            if not Per_facebook:
                Per_facebook          ='NA'
                
            Per_LinkedIn        =x[21]
            if not Per_LinkedIn:
                Per_LinkedIn          ='NA'
                
            per_Email           =x[22]
            if not per_Email:
                per_Email          ='NA'
            Per_Tel             =x[23]
            if not Per_Tel:
                Per_Tel          ='NA'
            else:
                Per_Tel = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}', Per_Tel));
           
            Per_Hobbies         =x[24]
            if Per_Hobbies:
                hobbies=Per_Hobbies.split(',')
            else:
                hobbies=''
                    
            
            Criminal_Fill_Date  =x[25]
            if Criminal_Fill_Date:
                crimeDate=Criminal_Fill_Date.split(',')
            else:
                crimeDate=''
                     
            
            Offense_Desc        =x[26]
            if Offense_Desc:
                offenceDesc=Offense_Desc.split(',')
            else:
                offenceDesc=''
            
                       
            Bankrupt_Fill_Date  =x[27]
            if Bankrupt_Fill_Date:
                bankrupt=Bankrupt_Fill_Date.split(',')
            else:
                bankrupt=''
                  
            
            Bank_Fill_Status    =x[28]
            if Bank_Fill_Status:
                bankOffence=Bank_Fill_Status.split(',')
            else:
                bankOffence=''
            
            
            Evic_Fill_Date      =x[29]
            if Evic_Fill_Date:
                evictionDate=Evic_Fill_Date.split(',')
            else:
                evictionDate=''
            
            
            Evic_Fill_Type      =x[30]
            if Evic_Fill_Type:
                evictionType=Evic_Fill_Type.split(',')
            else:
                evictionType=''
            
            
                           
            Per_Image           =x[31]
            House_Image         =x[32]
            enterdDate          =x[33]
            enterdBy            =x[34]
            spouse_name            =x[35]
            
            if not spouse_name:
                spouse_name='NA'
                
            updateFlag            =x[36]
            updatedBy            =x[37]
            Dep_Designation            =x[38]
            Dep_Media2            =x[39]
            if not Dep_Media2:
                Dep_Media2='NA'
            currentValue            =x[40]
            purchaseDate            =x[41]
            purchasePrice            =x[42]
            qualityFlag            =x[43]
            qualityCheckedBy            =x[44]
            pincode            =x[45]
            city            =x[46]
            state            =x[47]
            
            cityState=x[46]+', '+x[47]
            
            university            =x[48]
            
            if not university:
                university='NA'
            qaRemarks            =x[49]
            personSex            =x[50]
            qualityCheckedDate            =x[51]
            startTime            =x[52]
            endTime            =x[53]
            noData            =x[54]
            houseType            =x[55]
            medianHouseValue            =x[56]
            corpFilingDates            =x[57]
            corpFilingNames            =x[58]
            spouseBankruptDate            =x[59]
            spouseBankruptDetails            =x[60]
            Per_instagram            =x[61]
            Per_twitter            =x[62]
            judments            =x[63]
            Dep_instagram            =x[64]
            Dep_twitter            =x[65]
            selectedCity            =x[66]
            relationStatus            =x[67]
            if not relationStatus:
                relationStatus          ='NA'    
            
            licence_det            =x[68]
            licence_date            =x[69]
            edit_startTime            =x[70]
            edit_endTime            =x[71]
            Home_Val2            =x[72]
            Home_Val3            =x[73]
            Esti_Home_Equi2            =x[74]
            Esti_Home_Equi3            =x[75]
            Address2            =x[76]
            Address3            =x[77]
            pincode2            =x[78]
            pincode3            =x[79]
            state2            =x[80]
            state3            =x[81]
            city2            =x[82]
            city3            =x[83]
            spouceEducation            =x[84]
            spouceUniversity            =x[85]
            profLicence            =x[86]
            if not profLicence:
                profLicence = 'NA'
            
            prev_Per_Employment      =x[87]
            
            if prev_Per_Employment:
                perPrevEmpl=prev_Per_Employment.split(';')
            else:
                perPrevEmpl=''
            
            prev_Job_Desc      =x[88]
            
            if prev_Job_Desc:
                perPrevJob=prev_Job_Desc.split(';')
            else:
                perPrevJob=''
                
            ####image data
            
            imageId            =x[89]
            person_image            =x[90]
            home_image            =x[91]
            name            =x[92]
            dateAndTime            =x[93]
            
            # print(person_image)
            profileString = person_image.decode()

            # reconstruct image as an numpy array
            img = imread(io.BytesIO(base64.b64decode(profileString)))

            # show image
            plt.figure()
            plt.imshow(img, cmap="gray")
            
            cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite("profileImage.jpg", cv2_img)
            plt.show()
            
            houseString = home_image.decode()

            # reconstruct image as an numpy array
            img1 = imread(io.BytesIO(base64.b64decode(houseString)))

            # show image
            plt.figure()
            plt.imshow(img1, cmap="gray")
            
            cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
            cv2.imwrite("houseImage.jpg", cv2_img1)
            plt.show()
        
        if len(regVehicles) == 0:
            vehicle1 = 'NA'
            vehicle2 = 'NA'
            vehicle3 = 'NA'   
        elif len(regVehicles) == 1:
            vehicle1 = regVehicles[0]
            vehicle2 = 'NA'
            vehicle3 = 'NA'
        
        elif len(regVehicles) == 2:
            vehicle1 = regVehicles[0]
            vehicle2 = regVehicles[1]
            vehicle3 = 'NA'
        
        else:
            vehicle1 = regVehicles[0]
            vehicle2 = regVehicles[1]
            vehicle3 = regVehicles[2]
        
        if len(crimeDate) == 0:
            CHFdate1 = 'NA'
            CHFdate2 = 'NA'
        elif len(crimeDate) == 1:
            CHFdate1 = crimeDate[0]
            CHFdate2 = 'NA'
        else:
            CHFdate1 = crimeDate[0]
            CHFdate2 = crimeDate[1]
        
        if len(hobbies) == 0:
            hobby1 = 'NA'
            hobby2 = 'NA'
        elif len(hobbies) == 1:
            hobby1 = hobbies[0]
            hobby2 = 'NA'
        else:
            hobby1 = hobbies[0]
            hobby2 = hobbies[1]
        
        if len(offenceDesc) == 0:
            CHOdate1 = 'NA'
            CHOdate2 = 'NA'
        elif len(offenceDesc) == 1:
            CHOdate1 = offenceDesc[0]
            CHOdate2 = 'NA'
            
        else:
            CHOdate1 = offenceDesc[0]
            CHOdate2 = offenceDesc[1]
        
        if len(bankrupt) == 0:
            BRFdate1 = 'NA'
            BRFdate2 = 'NA'
        elif len(bankrupt) == 1:
            BRFdate1 = bankrupt[0]
            BRFdate2 = 'NA'
            
        else:
            BRFdate1 = bankrupt[0]
            BRFdate2 = bankrupt[1]
        
        if len(bankOffence) == 0:
            BROdate1 = 'NA'
            BROdate2 = 'NA'
        elif len(bankOffence) == 1:
            BROdate1 = bankOffence[0]
            BROdate2 = 'NA'
            
        else:
            BROdate1 = bankOffence[0]
            BROdate2 = bankOffence[1]
        
        if len(evictionDate) == 0:
            EVFdate1 = 'NA'
            EVFdate2 = 'NA'
        elif len(evictionDate) == 1:
            EVFdate1 = evictionDate[0]
            EVFdate2 = 'NA'
            
        else:
            EVFdate1 = evictionDate[0]
            EVFdate2 = evictionDate[1]
        
        if len(evictionType) == 0:
            EVOdate1 = 'NA'
            EVOdate2 = 'NA'
        elif len(evictionType) == 1:
            EVOdate1 = evictionType[0]
            EVOdate2 = 'NA'
            
        else:
            EVOdate1 = evictionType[0]
            EVOdate2 = evictionType[1]
        
        if len(JobDesc) == 0:
            JOB1 = 'NA'
            JOB2 = 'NA'
        elif len(JobDesc) == 1:
            JOB1 = JobDesc[0]
            JOB2 = 'NA'
            
        else:
            JOB1 = JobDesc[0]
            JOB2 = JobDesc[1]
        
        if len(perEmpl) == 0:
            comp1 = 'NA'
            comp2 = 'NA'
        elif len(perEmpl) == 1:
            comp1 = perEmpl[0]
            comp2 = 'NA'
            
        else:
            comp1 = perEmpl[0]
            comp2 = perEmpl[1]
        
        
        ####################################################HEight Calculation#######################################
        
        
        if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA': 
            contactHeight=5
        else:
            contactHeight=0
            
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA': 
            contactHeight=0
        if len(hobbies) == 0:
            hobbyHeight = 2.5
            contactHeight+=hobbyHeight
        else:
            hobbyHeight = 0
        if len(crimeDate) == 0:
            crimeHeight=2.5
        else:
            crimeHeight=0
        if len(bankrupt) == 0:
            bankHeight=5
        else:
            bankHeight=0
            
         
         #######################################End of Height Calculation#######################################
        
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment''filename="{}"'.format(FullName)
        response['Content-Disposition'] = 'filename={0}.pdf'.format(FullName)
        # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        buffer = BytesIO()
        # pdf = canvas.Canvas(buffer)
        
        
        #enable this to store pdf in root folder and disable buffer canvas
        pdf = canvas.Canvas(FullName+'.pdf', pagesize=A4)
        # pdf = canvas.Canvas(FullName+'.pdf', pagesize=letter)
        pdf.setTitle(FullName)
         # Start writing the PDF here
        fs = FileSystemStorage()
        filename = FullName+'.pdf'
        print(filename)
        # pdf.drawImage('/home/pdfImages/Background.png',0*cm,0*cm,21.2*cm,29.7*cm);
        pdf.drawImage('/home/pdfImages/BG1.png',0*cm,0*cm,21.2*cm,29.7*cm);
        # pdf.drawImage('/home/pdfImages/bg.png',0*cm,0*cm,21.2*cm,29.7*cm);
        pdf.setFont('VeraBd', 14);
        pdf.drawCentredString((12.5/2)*cm,28.2*cm,FullName.upper());
        pdf.setFont('Vera', 14);
        # pdf.setDash([2,2,2,2],0)
        pdf.line(2*cm,28*cm,10.5*cm,28*cm);
        # pdf.setDash([0,0,0,0],0)
        if len(Job_Desc) >=90:
                jobFont=9
        else:
                jobFont=14
        ##################################JOBS DISPLAY #############################        
        if JOB2 =='NA' and comp2 != 'NA':
            job2Height=0.5
        else:
            job2Height=0
        if JOB1 !='NA':
            pdf.setFillColorRGB(0,0.5,0.5)
            pdf.setFont('Vera', jobFont);
            if comp1 != 'NA':
                JOB1=JOB1+','
            pdf.drawCentredString((12.5/2)*cm,27.35*cm,JOB1);
        pdf.setFillColorRGB(0,0,0)    
        if comp1 != 'NA':
            pdf.drawCentredString((12.5/2)*cm,26.75*cm,comp1);
           
        if JOB2 !='NA' or comp2 != 'NA':
            if JOB2 !='NA':
                if comp2 !='NA':
                    JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((12.5/2)*cm,26.2*cm,JOB2);
            pdf.setFillColorRGB(0,0,0)
            if comp2 !='NA':
                pdf.drawCentredString((12.5/2)*cm,(25.6+job2Height)*cm,comp2);
            pdf.line(2*cm,25.45*cm,10.5*cm,25.45*cm)

        ##################################JOBS DISPLAY #############################        
        # pdf.drawImage('/home/pdfImages/default_men.png',14.05*cm,24.05*cm,3.9*cm,3.9*cm,preserveAspectRatio=False);
        pdf.drawImage('profileImage.jpg',12.5*cm,20.4*cm,8*cm,8.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.setLineWidth(2)
        pdf.setFillColorRGB(0.5,0,0)
        pdf.roundRect(12.5*cm, 20.4*cm, 8*cm, 8.8*cm, 4, stroke=1, fill=0);
        pdf.setFillColorRGB(0,0,0)
        
       
        if Per_Age !='NA':
            pdf.drawImage('/home/pdfImages/design1/age.png',15.75*cm,20.45*cm,4.7*cm,0.9*cm,preserveAspectRatio=False,mask='auto');
            
            if personSex =='Female':
                pdf.drawImage('/home/pdfImages/design1/female.png',17*cm,20.5*cm,0.7*cm,0.7*cm,preserveAspectRatio=True, mask='auto');
                
            else:
                pdf.drawImage('/home/pdfImages/design1/male.png',17*cm,20.5*cm,0.7*cm,0.7*cm,preserveAspectRatio=True, mask='auto');
                   
            pdf.setFillColorRGB(0,0,0);
            pdf.setFont('VeraBd', 11);
            pdf.drawCentredString(18.75*cm,20.6*cm,"AGE:  "+Per_Age);
            # pdf.drawCentredString(14.6*cm,20.3*cm,Per_Age);

        #################### Left components ##########################################
        pdf.setFillColorRGB(0,0,0);
        if Job_Desc != 'NA' and Per_Salary !='NA':
            pdf.setFont('VeraBd', 11);
            pdf.drawCentredString((12.5/2)*cm,25*cm,"ESTIMATED YEARLY SALARY");
            pdf.drawImage('/home/pdfImages/design1/salary.png', 3.3*cm, 24.05*cm, width=5.8*cm, height=.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.setFont('VeraBd', 11);
            pdf.setFillColorRGB(255,0,0)
            pdf.drawCentredString((12.5/2)*cm,24.29*cm,Per_Salary);
        pdf.setFillColorRGB(0,0,0)
        
        if Address != 'NA':
            pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(22.65)*cm,3.25*cm,0.5*cm,preserveAspectRatio=False);
            pdf.drawImage('houseImage.jpg',2.55*cm,(17.6)*cm,7.3*cm,5*cm,preserveAspectRatio=False);
            
            pdf.roundRect(2.55*cm, (17.6)*cm, 7.3*cm, 5*cm, 2, stroke=1, fill=0);
           
            pdf.setFont('Vera', 12);
            pdf.drawCentredString((12.5/2)*cm,17*cm,Address);
            pdf.drawCentredString((12.5/2)*cm,16.45*cm,cityState+' '+pincode);
            

        print('Education',Education)
        if Education != 'NA':
            educationHeight=0
            pdf.drawImage('/home/pdfImages/Education.png', 3*cm, 13.25*cm, width=8.5*cm, height=2.25*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.setFont('VeraBd', 12);
            pdf.drawCentredString((12.5/2)*cm,12.5*cm,Education); 
            if university != 'NA':
                pdf.drawCentredString((12.5/2)*cm,11.95*cm,university.title());    
        else:
            educationHeight=4
        ###########################VEHICLES DETAILS#################################
        if len(regVehicles) == 0:
            vehicleLength=4
        else:
            vehicleLength=0
        if len(regVehicles) != 0:
            pdf.drawImage('/home/pdfImages/design1/vehicles.png',1.5*cm,(9.75+educationHeight)*cm,8.5*cm,0.9*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 12);
        if vehicle1 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(8.8+educationHeight)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2.4*cm,(8.8+educationHeight)*cm,vehicle1);
        if vehicle2 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(8+educationHeight)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2.4*cm,(8+educationHeight)*cm,vehicle2);
        if vehicle3 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(7.2+educationHeight)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2.4*cm,(7.2+educationHeight)*cm,vehicle3);
        
        
        
        if Input_Pop != 'NA':
            
            pdf.setLineWidth(1)
            pdf.line(1.3*cm,(6.5+educationHeight+vehicleLength)*cm,12*cm,(6.5+educationHeight+vehicleLength)*cm)
            # pdf.roundRect(1.3*cm, (3.4)*cm, 10*cm, 2.6*cm, 4, stroke=1, fill=0);
            pdf.setFont('VeraBd', 14);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,FullName.upper());
            pdf.drawCentredString((12.5/2)*cm,(5.2+educationHeight+vehicleLength)*cm,"City:  "+cityState);
            pdf.drawImage('/home/pdfImages/dot.png',3*cm,(4.2+educationHeight+vehicleLength)*cm,0.4*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 11);
            pdf.drawCentredString((6.25/2)*cm,(3.6+educationHeight+vehicleLength)*cm,"POPULATION");
            pdf.setFont('Vera', 11);
            pdf.drawCentredString((6.25/2)*cm,(3+educationHeight+vehicleLength)*cm,Input_Pop);

            pdf.setLineWidth(0.5);
            
        if Median_HouseHold_Val != 'NA':
            pdf.drawImage('/home/pdfImages/dot.png',8.5*cm,(4.2+educationHeight+vehicleLength)*cm,0.4*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawCentredString(8.5*cm,(3.6+educationHeight+vehicleLength)*cm,"MEDIAN HOUSEHOLD INCOME");
            
            pdf.drawCentredString(8.5*cm,(3+educationHeight+vehicleLength)*cm,Median_HouseHold_Val);
    
        ################################ Right_Template_Contents ##################################################
        pdf.setFont('Vera', 9);
        if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA':
            
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            fb_url = []
            raw_addr = Per_facebook
            address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
            address = '<link href="' + raw_addr + '">' + address + '</link>'
            fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
            
            f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(fb_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            ld_url = []
            # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
            raw_addr2 = Per_LinkedIn
            address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
            address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
            ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
           
            f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(ld_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            gmail_url = []
            #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
            raw_addr3 = per_Email
            address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
            address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
            gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

            f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(gmail_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFillColorRGB(255,255,255)
            pdf.drawString(14.75*cm,13*cm,Per_Tel)
    
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA': 
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            
            if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA':
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
               
                
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA':
                
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

            
            elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA':
                
                # pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)


                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr3 = per_Email
                address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA':
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:32]+'<br/>'+raw_addr[33:64]+'<br/>'+raw_addr[65:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                
                f = Frame(14.5*cm, 15.4*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                                      
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[33:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 15.4*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                
            
            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,14.5*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,13*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 14*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                ld_url = []
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:25]+'<br/>'+raw_addr2[25:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 12.5*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[33:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
              
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                               
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                
                
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
                
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                              
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                 
            
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[33:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA':
            
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr3 = per_Email
                address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
            
            
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
             
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.75*cm,14.2*cm,Per_Tel)
            
            
         ################### Hobbies ########################
        if hobby1 != 'NA' and hobby2 !='NA':
            pdf.setFillColorRGB(255,255,255)
            pdf.setFont('Vera', 8);
            pdf.drawString(13.7*cm,(12.2+contactHeight)*cm,'________________________________________________')
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(11.55+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(11.35+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 12);
            pdf.drawCentredString(15.55*cm,(11.36+contactHeight)*cm,'HOBBIES');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10.6+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 8);
            pdf.drawString(14.6*cm,(10.65+contactHeight)*cm,hobby1)
            pdf.drawString(14.6*cm,(10.05+contactHeight)*cm,hobby2)
            pdf.drawString(13.7*cm,(9.7+contactHeight)*cm,'________________________________________________')
        elif hobby1 != 'NA' and hobby2 =='NA':
            pdf.setFillColorRGB(255,255,255)
            pdf.setFont('Vera', 8);
            pdf.drawString(13.7*cm,(12.2+contactHeight)*cm,'________________________________________________')
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(11.35+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 12);
            pdf.drawCentredString(15.55*cm,(11.36+contactHeight)*cm,'HOBBIES');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10.6+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
           
            pdf.setFont('Vera', 8);
            pdf.drawString(14.6*cm,(10.65+contactHeight)*cm,hobby1)
            
            pdf.drawString(13.7*cm,(9.7+contactHeight)*cm,'________________________________________________')
       
        ################### Criminal History,Bankruptcies,Evictions ##########################
        
        
        if CHFdate1 != 'NA' and CHFdate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(8.9+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(8.95+contactHeight)*cm,'CRIMINAL HISTORY');
            pdf.setFont('Vera', 9);
            pdf.drawString(14.25*cm,(8.45+contactHeight)*cm,'Filing Date   Offense Description');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.8+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(7.82+contactHeight)*cm,CHFdate1)
            pdf.drawString(16.2*cm,(7.82+contactHeight)*cm,CHOdate1)
            pdf.drawString(14.25*cm,(7.25+contactHeight)*cm,CHFdate2)
            pdf.drawString(16.2*cm,(7.25+contactHeight)*cm,CHOdate2)
        
        # extraHeight=2
        
        elif CHFdate1 != 'NA' and CHFdate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(8.9+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.5*cm,(8.95+contactHeight)*cm,'CRIMINAL HISTORY');
            pdf.setFont('Vera', 9);
            pdf.drawString(14.25*cm,(8.45+contactHeight)*cm,'Filing Date   Offense Description');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.8+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(7.82+contactHeight)*cm,CHFdate1)
            pdf.drawString(16.2*cm,(7.82+contactHeight)*cm,CHOdate1)
         
        if BRFdate1 != 'NA' and BRFdate2 != 'NA':
            contactHeight=contactHeight+0.85
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(5.5+contactHeight+crimeHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(5.55+contactHeight+crimeHeight)*cm,'BANKRUPTCIES');
            pdf.setFont('Vera', 9);      
            pdf.drawString(14.25*cm,(5+contactHeight+crimeHeight)*cm,'Filing Date   Filing Status');
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(4.5+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(4.5+contactHeight+crimeHeight)*cm,BRFdate1)
            pdf.drawString(16.2*cm,(4.5+contactHeight+crimeHeight)*cm,BROdate1)
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(4+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(3.93+contactHeight+crimeHeight)*cm,BRFdate2)
            pdf.drawString(16.2*cm,(3.93+contactHeight+crimeHeight)*cm,BROdate2)
        elif BRFdate1 != 'NA' and BRFdate2 == 'NA':
            contactHeight=contactHeight+0.85
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(5.5+contactHeight+crimeHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(5.55+contactHeight+crimeHeight)*cm,'BANKRUPTCIES');
            pdf.setFont('Vera', 9);      
            pdf.drawString(14.25*cm,(5+contactHeight+crimeHeight)*cm,'Filing Date   Filing Status');
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(4.5+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(4.5+contactHeight+crimeHeight)*cm,BRFdate1)
            pdf.drawString(16.2*cm,(4.5+contactHeight+crimeHeight)*cm,BROdate1)
            
        if EVFdate1 != 'NA' and EVFdate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(3.1+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(3.15+contactHeight+crimeHeight+bankHeight)*cm,'EVICTIONS');
            pdf.setFont('Vera', 9);
            pdf.drawString(14.25*cm,(2.55+contactHeight+crimeHeight+bankHeight)*cm,'Filing Date   Filing Type');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(1.95+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(1.95+contactHeight+crimeHeight+bankHeight)*cm,EVFdate1)
            pdf.drawString(16.2*cm,(1.95+contactHeight+crimeHeight+bankHeight)*cm,EVOdate1)
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,EVFdate2)
            pdf.drawString(16.2*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,EVOdate2)
            
        elif EVFdate1 != 'NA' and EVFdate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(1.75+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawCentredString(15.65*cm,(1.75+contactHeight+crimeHeight+bankHeight)*cm,'EVICTIONS');
            pdf.setFont('Vera', 9);
            pdf.drawCentredString(16.1*cm,(1.25+contactHeight+crimeHeight+bankHeight)*cm,'Filing Date     Filing Type');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(0.7+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(0.7+contactHeight+crimeHeight+bankHeight)*cm,EVFdate1)
            pdf.drawString(16.2*cm,(0.7+contactHeight+crimeHeight+bankHeight)*cm,EVOdate1)
            
      
        pdf.showPage()
        pdf.save()

        pdf = buffer.getvalue()
        # store = FileResponse(buffer, as_attachment=True, filename=FullName+'.pdf')
        # print('store',store);
        buffer.close()
        response.write(pdf)
        
        FNMAE = FullName+'.pdf'
        print('fs',FNMAE)
        if fs.exists(FNMAE):
            with fs.open(FNMAE) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename=FNMAE'
                # return "HELLO"
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')
 
def template2(request,userId=None):
   
    userId = request.GET["userId"]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from usData,us_image where usData.id=us_image.id and usData.id='{}'".format(userId))
        myresult = cursor.fetchall()
        # print('myresult:',myresult)
        if not myresult:
            template = loader.get_template('notFound.html') # getting our template  
            return HttpResponse(template.render())       # rendering the template in HttpResponse 
            return render(request,'notFound.html') 
        for x in myresult:
    
            var = myresult[0]
            
            PersonName=x[0]
            FullName = x[1]+' '+x[2]
            Fname = x[1]
            Lname = x[2]
            
            Per_Age             =x[3]
            if not Per_Age:
                Per_Age='NA'
            Address             =x[4] #+','+x[45]
            if not Address:
                Address='NA'
            Spouse_Age          =x[5]
            
            if not Spouse_Age:
                Spouse_Age          ='NA'
            else:
                Spouse_Age          ='Age:  '+x[5]
                
            Dep_Employment      =x[6]
            
            if not Dep_Employment:
                Dep_Employment          ='NA'
                               
            Dep_Salary          =x[7]
            
            if not Dep_Salary:
                Dep_Salary          ='NA'
            else:
                Dep_Salary = x[7]
                print(Dep_Salary)
                
                Dep_Salary = int(float(Dep_Salary))
                Dep_Salary = custom_format_currency(Dep_Salary, 'USD', locale='en_US')    
            Dep_Media           =x[8]
            if not Dep_Media:
                Dep_Media='NA'
                
            Education           =x[9]
            if not Education:
                Education          ='NA'
            
            Per_Employment      =x[10]
            
            if Per_Employment:
                perEmpl=Per_Employment.split(',')
            else:
                perEmpl=''

            
            Job_Desc            =x[11]
            if Job_Desc:
                JobDesc=Job_Desc.split(',')
            else:
                JobDesc=''
            
                
            Per_Salary          =x[12]
            if not Per_Salary:
                Per_Salary          ='NA'
            else:
                Per_Salary = x[12]
                # Per_Salary = round(Per_Salary)
                Per_Salary = int(float(Per_Salary))
                Per_Salary = custom_format_currency(Per_Salary, 'USD', locale='en_US')
            Input_Pop           =x[13]
            if not Input_Pop:
                Input_Pop='NA'
            Median_HouseHold_Val=x[14]
            if not Median_HouseHold_Val:
                Median_HouseHold_Val='NA'
            else:
                Median_HouseHold_Val=x[14]
                # Median_HouseHold_Val = round(Median_HouseHold_Val)
                Median_HouseHold_Val = custom_format_currency(Median_HouseHold_Val, 'USD', locale='en_US')
            Home_Val            =x[15]
            if not Home_Val:
                Home_Val='NA'
            else:
                Home_Val=x[15]
                Home_Val = custom_format_currency(Home_Val, 'USD', locale='en_US')
            Esti_Home_Equi      =x[16]
            if not Esti_Home_Equi:
                Esti_Home_Equi='NA'
            else:
                Esti_Home_Equi      =x[16]
                Esti_Home_Equi = int(float(Esti_Home_Equi))
                
                Esti_Home_Equi = custom_format_currency(Esti_Home_Equi, 'USD', locale='en_US')
            Mort_Amt            =x[17]
            if not Mort_Amt:
                Mort_Amt='NA'
            else:
                Mort_Amt            =x[17]
                Mort_Amt = int(float(Mort_Amt))
                
                Mort_Amt = custom_format_currency(Mort_Amt, 'USD', locale='en_US')
            Mort_Date           =x[18]
            
            if not Mort_Date:
                Mort_Date='NA'
                
            Vehicle_det         =x[19]
            # print('Vehicle_det',Vehicle_det)
            if Vehicle_det:
                regVehicles=Vehicle_det.split(',')
            else:
                regVehicles=''
            
            Per_facebook        =x[20]
            if not Per_facebook:
                Per_facebook          ='NA'
                
            Per_LinkedIn        =x[21]
            if not Per_LinkedIn:
                Per_LinkedIn          ='NA'
                
            per_Email           =x[22]
            if not per_Email:
                per_Email          ='NA'
            Per_Tel             =x[23]
            if not Per_Tel:
                Per_Tel          ='NA'
            else:
                Per_Tel = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}', Per_Tel));
            # print(Per_Tel)
            socialDetails = {
            "personFB": Per_facebook,
            "personLinkd": Per_LinkedIn,
            "personEmail": per_Email,
            "personTel": Per_Tel
            }
            # print(socialDetails)
            
            # socialDetails.insert(1, )
            # print('socialDetails:',socialDetails)
            Per_Hobbies         =x[24]
            if Per_Hobbies:
                hobbies=Per_Hobbies.split(',')
            else:
                hobbies=''
                    
            
            Criminal_Fill_Date  =x[25]
            if Criminal_Fill_Date:
                crimeDate=Criminal_Fill_Date.split(',')
            else:
                crimeDate=''
                     
            
            Offense_Desc        =x[26]
            if Offense_Desc:
                offenceDesc=Offense_Desc.split(',')
            else:
                offenceDesc=''
            
                       
            Bankrupt_Fill_Date  =x[27]
            if Bankrupt_Fill_Date:
                bankrupt=Bankrupt_Fill_Date.split(',')
            else:
                bankrupt=''
            print('bankrupt',len(bankrupt))      
            print('bankrupt')      
            
            Bank_Fill_Status    =x[28]
            if Bank_Fill_Status:
                bankOffence=Bank_Fill_Status.split(',')
            else:
                bankOffence=''
            
            
            Evic_Fill_Date      =x[29]
            if Evic_Fill_Date:
                evictionDate=Evic_Fill_Date.split(',')
            else:
                evictionDate=''
            
            
            Evic_Fill_Type      =x[30]
            if Evic_Fill_Type:
                evictionType=Evic_Fill_Type.split(',')
            else:
                evictionType=''
            
            
                           
            Per_Image           =x[31]
            House_Image         =x[32]
            enterdDate          =x[33]
            enterdBy            =x[34]
            spouse_name            =x[35]
            
            if not spouse_name:
                spouse_name='NA'
                
            updateFlag            =x[36]
            updatedBy            =x[37]
            Dep_Designation            =x[38]
            Dep_Media2            =x[39]
            if not Dep_Media2:
                Dep_Media2='NA'
            currentValue            =x[40]
            purchaseDate            =x[41]
            purchasePrice            =x[42]
            qualityFlag            =x[43]
            qualityCheckedBy            =x[44]
            pincode            =x[45]
            city            =x[46]
            state            =x[47]
            
            cityState=x[46]+', '+x[47]
            
            university            =x[48]
            
            if not university:
                university='NA'
            qaRemarks            =x[49]
            personSex            =x[50]
            qualityCheckedDate            =x[51]
            startTime            =x[52]
            endTime            =x[53]
            noData            =x[54]
            houseType            =x[55]
            medianHouseValue            =x[56]
            corpFilingDates            =x[57]
            corpFilingNames            =x[58]
            spouseBankruptDate            =x[59]
            spouseBankruptDetails            =x[60]
            Per_instagram            =x[61]
            Per_twitter            =x[62]
            judments            =x[63]
            Dep_instagram            =x[64]
            Dep_twitter            =x[65]
            selectedCity            =x[66]
            relationStatus            =x[67]
            if not relationStatus:
                relationStatus          ='NA'    
                
            licence_det            =x[68]
            licence_date            =x[69]
            edit_startTime            =x[70]
            edit_endTime            =x[71]
            Home_Val2            =x[72]
            Home_Val3            =x[73]
            Esti_Home_Equi2            =x[74]
            Esti_Home_Equi3            =x[75]
            Address2            =x[76]
            Address3            =x[77]
            pincode2            =x[78]
            pincode3            =x[79]
            state2            =x[80]
            state3            =x[81]
            city2            =x[82]
            city3            =x[83]
            spouceEducation            =x[84]
            spouceUniversity            =x[85]
            profLicence            =x[86]
            if not profLicence:
                profLicence = 'NA'
            
            prev_Per_Employment      =x[87]
            
            if prev_Per_Employment:
                perPrevEmpl=prev_Per_Employment.split(';')
            else:
                perPrevEmpl=''
            
            prev_Job_Desc      =x[88]
            
            if prev_Job_Desc:
                perPrevJob=prev_Job_Desc.split(';')
            else:
                perPrevJob=''
                
            ####image data
            
            imageId            =x[89]
            person_image            =x[90]
            home_image            =x[91]
            name            =x[92]
            dateAndTime            =x[93]
            
            # print(person_image)
            profileString = person_image.decode()

            # reconstruct image as an numpy array
            img = imread(io.BytesIO(base64.b64decode(profileString)))

            # show image
            plt.figure()
            plt.imshow(img, cmap="gray")
            
            cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite("profileImage.jpg", cv2_img)
            plt.show()
            
            houseString = home_image.decode()

            # reconstruct image as an numpy array
            img1 = imread(io.BytesIO(base64.b64decode(houseString)))

            # show image
            plt.figure()
            plt.imshow(img1, cmap="gray")
            
            cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
            cv2.imwrite("houseImage.jpg", cv2_img1)
            plt.show()
        
        if len(regVehicles) == 0:
            vehicle1 = 'NA'
            vehicle2 = 'NA'
            vehicle3 = 'NA'   
        elif len(regVehicles) == 1:
            vehicle1 = regVehicles[0]
            vehicle2 = 'NA'
            vehicle3 = 'NA'
        
        elif len(regVehicles) == 2:
            vehicle1 = regVehicles[0]
            vehicle2 = regVehicles[1]
            vehicle3 = 'NA'
        
        else:
            vehicle1 = regVehicles[0]
            vehicle2 = regVehicles[1]
            vehicle3 = regVehicles[2]
        
        if len(crimeDate) == 0:
            CHFdate1 = 'NA'
            CHFdate2 = 'NA'
        elif len(crimeDate) == 1:
            CHFdate1 = crimeDate[0]
            CHFdate2 = 'NA'
        else:
            CHFdate1 = crimeDate[0]
            CHFdate2 = crimeDate[1]
        
        if len(hobbies) == 0:
            hobby1 = 'NA'
            hobby2 = 'NA'
        elif len(hobbies) == 1:
            hobby1 = hobbies[0]
            hobby2 = 'NA'
        else:
            hobby1 = hobbies[0]
            hobby2 = hobbies[1]
        
        if len(offenceDesc) == 0:
            CHOdate1 = 'NA'
            CHOdate2 = 'NA'
        elif len(offenceDesc) == 1:
            CHOdate1 = offenceDesc[0]
            CHOdate2 = 'NA'
            
        else:
            CHOdate1 = offenceDesc[0]
            CHOdate2 = offenceDesc[1]
        
        if len(bankrupt) == 0:
            BRFdate1 = 'NA'
            BRFdate2 = 'NA'
        elif len(bankrupt) == 1:
            BRFdate1 = bankrupt[0]
            BRFdate2 = 'NA'
            
        else:
            BRFdate1 = bankrupt[0]
            BRFdate2 = bankrupt[1]
        
        if len(bankOffence) == 0:
            BROdate1 = 'NA'
            BROdate2 = 'NA'
        elif len(bankOffence) == 1:
            BROdate1 = bankOffence[0]
            BROdate2 = 'NA'
            
        else:
            BROdate1 = bankOffence[0]
            BROdate2 = bankOffence[1]
        
        if len(evictionDate) == 0:
            EVFdate1 = 'NA'
            EVFdate2 = 'NA'
        elif len(evictionDate) == 1:
            EVFdate1 = evictionDate[0]
            EVFdate2 = 'NA'
            
        else:
            EVFdate1 = evictionDate[0]
            EVFdate2 = evictionDate[1]
        
        if len(evictionType) == 0:
            EVOdate1 = 'NA'
            EVOdate2 = 'NA'
        elif len(evictionType) == 1:
            EVOdate1 = evictionType[0]
            EVOdate2 = 'NA'
            
        else:
            EVOdate1 = evictionType[0]
            EVOdate2 = evictionType[1]
        
        if len(JobDesc) == 0:
            JOB1 = 'NA'
            JOB2 = 'NA'
        elif len(JobDesc) == 1:
            JOB1 = JobDesc[0]
            JOB2 = 'NA'
            
        else:
            JOB1 = JobDesc[0]
            JOB2 = JobDesc[1]
        
        if len(perEmpl) == 0:
            comp1 = 'NA'
            comp2 = 'NA'
        elif len(perEmpl) == 1:
            comp1 = perEmpl[0]
            comp2 = 'NA'
            
        else:
            comp1 = perEmpl[0]
            comp2 = perEmpl[1]
        
        
        ####################################################HEight Calculation#######################################
        
        if Per_LinkedIn != 'NA':
            linkdHeight=0
        else:
            linkdHeight=0
            
        if Per_facebook == 'NA':
            fbHeight=2.5
        else:
            fbHeight=0
            
        if per_Email != 'NA':
            emailHeight=0
        else:
            emailHeight=0
            
        if Per_Tel != 'NA':
            telHeight=0
        else:
            telHeight=0
            
        
        if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA': 
            contactHeight=5
        else:
            contactHeight=0
            
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA': 
            contactHeight=0
        if len(hobbies) == 0:
            hobbyHeight = 2.5
            contactHeight+=hobbyHeight
        else:
            hobbyHeight = 0
        if len(crimeDate) == 0:
            crimeHeight=2.5
        else:
            crimeHeight=0
        if len(bankrupt) == 0:
            bankHeight=2.5
        else:
            bankHeight=0
            
        print('len(bankrupt)',len(bankrupt)) 
         #######################################End of Height Calculation#######################################
        
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment''filename="{}"'.format(FullName)
        response['Content-Disposition'] = 'filename={0}.pdf'.format(FullName)
        # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        buffer = BytesIO()
        # pdf = canvas.Canvas(buffer)
        
        
        #enable this to store pdf in root folder and disable buffer canvas
        pdf = canvas.Canvas(FullName+'.pdf', pagesize=A4)
        # pdf = canvas.Canvas(FullName+'.pdf', pagesize=letter)
        pdf.setTitle(FullName)
         # Start writing the PDF here
        fs = FileSystemStorage()
        filename = FullName+'.pdf'
        print(filename)
        # pdf.drawImage('/home/pdfImages/Background.png',0*cm,0*cm,21.2*cm,29.7*cm);
        pdf.drawImage('/home/pdfImages/BG1.png',0*cm,0*cm,21.2*cm,29.7*cm);
        # pdf.drawImage('/home/pdfImages/bg.png',0*cm,0*cm,21.2*cm,29.7*cm);
        pdf.setFont('VeraBd', 14);
        pdf.drawCentredString((12.5/2)*cm,28.2*cm,FullName.upper());
        pdf.setFont('Vera', 14);
        
        pdf.line(2*cm,28*cm,10.5*cm,28*cm);
        
        if len(Job_Desc) >=90:
                jobFont=9
        else:
                jobFont=14
        ##################################JOBS DISPLAY #############################        
        if JOB2 =='NA' and comp2 != 'NA':
            job2Height=0.5
        else:
            job2Height=0
        if JOB1 !='NA':
            pdf.setFillColorRGB(0,0.5,0.5)
            pdf.setFont('Vera', jobFont);
            if comp1 != 'NA':
                JOB1=JOB1+','
            pdf.drawCentredString((12.5/2)*cm,27.35*cm,JOB1);
        pdf.setFillColorRGB(0,0,0)    
        if comp1 != 'NA':
            pdf.drawCentredString((12.5/2)*cm,26.75*cm,comp1);
           
        if JOB2 !='NA' or comp2 != 'NA':
            if JOB2 !='NA':
                if comp2 !='NA':
                    JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((12.5/2)*cm,26.2*cm,JOB2);
            pdf.setFillColorRGB(0,0,0)
            if comp2 !='NA':
                pdf.drawCentredString((12.5/2)*cm,(25.6+job2Height)*cm,comp2);
            pdf.line(2*cm,25.45*cm,10.5*cm,25.45*cm)

        ##################################JOBS DISPLAY #############################        
        # pdf.drawImage('/home/pdfImages/default_men.png',14.05*cm,24.05*cm,3.9*cm,3.9*cm,preserveAspectRatio=False);
        pdf.drawImage('profileImage.jpg',12.5*cm,20.4*cm,8*cm,8.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.setLineWidth(2)
        pdf.setFillColorRGB(0.5,0,0)
        pdf.roundRect(12.5*cm, 20.4*cm, 8*cm, 8.8*cm, 4, stroke=1, fill=0);
        pdf.setFillColorRGB(0,0,0)
        
        
        
        
        if Per_Age !='NA':
            pdf.drawImage('/home/pdfImages//design1/pie.png',10.75*cm,20.15*cm,3*cm,2.85*cm,preserveAspectRatio=False,mask='auto');
            # pdf.drawImage('/home/pdfImages/age.png',13.4*cm,23.85*cm,0.75*cm,1*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/pie.png',12.4*cm,22.5*cm,2.5*cm,2.5*cm,preserveAspectRatio=False);
            if personSex =='Female':
                pdf.drawImage('/home/pdfImages/design1/female.png',12.12*cm,21.65*cm,1.2*cm,1.2*cm,preserveAspectRatio=False, mask='auto');
                
            else:
                pdf.drawImage('/home/pdfImages/design1/male.png',12.12*cm,21.65*cm,1.2*cm,1.2*cm,preserveAspectRatio=True, mask='auto');
                   
            pdf.setFillColorRGB(0,0,0);
            pdf.setFont('VeraBd', 11);
            pdf.drawCentredString(12.4*cm,21.15*cm,"AGE:  "+Per_Age);
            # pdf.drawCentredString(14.6*cm,20.3*cm,Per_Age);

        


        #################### Left components ##########################################
        pdf.setFillColorRGB(0,0,0);
        if Job_Desc != 'NA' and Per_Salary !='NA':
            pdf.setFont('VeraBd', 11);
            pdf.drawCentredString((12.5/2)*cm,25*cm,"ESTIMATED YEARLY SALARY");
            pdf.drawImage('/home/pdfImages/design1/salary.png', 3.3*cm, 24.05*cm, width=5.8*cm, height=.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.setFont('VeraBd', 11);
            pdf.setFillColorRGB(255,0,0)
            pdf.drawCentredString((12.5/2)*cm,24.29*cm,Per_Salary);
        pdf.setFillColorRGB(0,0,0)
        if Address != 'NA':
            pdf.drawImage('/home/pdfImages/personHome.png',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
            pdf.drawImage('houseImage.jpg',0.75*cm,(20.4)*cm,4.3*cm,3*cm,preserveAspectRatio=False);
            
            pdf.roundRect(0.75*cm, (20.4)*cm, 4.3*cm, 3.05*cm, 4, stroke=1, fill=0);
           
            pdf.setFont('VeraBd', 9);
            
            pdf.drawString(5.62*cm,(22.25)*cm,Address);
            pdf.drawString(5.62*cm,(21.75)*cm,cityState+' '+pincode);
            # pdf.drawString(5.62*cm,(21.25)*cm,pincode);
            
            
        

        if Home_Val !='NA':
            pdf.drawImage('/home/pdfImages/dot.png',3*cm,(19.9)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((6.25/2)*cm,(19.4)*cm,"ESTIMATED HOME VALUE");
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((6.25/2)*cm,(19)*cm,Home_Val);

            pdf.setLineWidth(0.5);
            pdf.line(6.25*cm,(20.3)*cm,6.25*cm,(17.2)*cm)
            
        if Esti_Home_Equi !='NA':
            pdf.drawImage('/home/pdfImages/dot.png',9.2*cm,(19.9)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawCentredString(9.375*cm,(19.4)*cm,"ESTIMATED HOME EQUITY");
            pdf.setFont('Vera', 8);
            pdf.drawCentredString(9.375*cm,(19)*cm,Esti_Home_Equi);

        if Mort_Date !='NA':
            pdf.drawImage('/home/pdfImages/dot.png',3*cm,(18.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((6.25/2)*cm,(17.8)*cm,"MORTGAGE DATE");
            pdf.drawCentredString((6.25/2)*cm,(17.4)*cm,Mort_Date);
        
        
            pdf.drawImage('/home/pdfImages/dot.png',9.2*cm,(18.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 8);
            pdf.drawCentredString(9.375*cm,(17.8)*cm,"MORTGAGE AMOUNT");
            pdf.drawCentredString(9.375*cm,(17.4)*cm,Mort_Amt);

            pdf.line(1.3*cm,(17)*cm,11.2*cm,(17)*cm)

        # if Education != 'NA':
            # pdf.drawImage('/home/pdfImages/Education.png', 4.1*cm, 15.4*cm, width=4.5*cm, height=0.75*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            # if len(Education) >= 66:
                # eduFont=8
            # else:
                # eduFont=10

            # pdf.setFont('VeraBd', eduFont);
           
            # pdf.drawCentredString((12.5/2)*cm,15*cm,Education); 
            # if university != 'NA':
                # pdf.drawCentredString((12.5/2)*cm,14.55*cm,university.title());    

            


         ############################# About Family ################################
        
        
        if spouse_name != 'NA' :
            pdf.drawImage('/home/pdfImages/family.png',0.75*cm,(14)*cm,9.5*cm,0.65*cm,preserveAspectRatio=False, mask='auto');
             # pdf.drawImage('/home/pdfImages/Male.png',11.7*cm,18.7*cm,1.75*cm,1.75*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/spouse.png',1.5*cm,(11.75)*cm,3.25*cm,0.25*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/business.png',1.5*cm,(10.5)*cm,0.5*cm,1*cm,preserveAspectRatio=False, mask='auto');
         
            pdf.setFont('VeraBd', 12);
            pdf.drawString(2.3*cm,(11)*cm,spouse_name);
            
            if Spouse_Age != 'NA':
                pdf.setFont('Vera', 8);
                pdf.drawString(2.3*cm,(10.6)*cm,Spouse_Age);
            
            if Dep_Employment != 'NA':
                pdf.drawImage('/home/pdfImages/work.png',1.5*cm,(9.7)*cm,0.5*cm,0.6*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFont('Vera', 10);
                pdf.setFillColorRGB(0,0.5,0.5)
                pdf.drawString(2.3*cm,(10)*cm,Dep_Designation+',');
                pdf.setFont('Vera', 8);
                pdf.setFillColorRGB(0,0,0)
                pdf.drawString(2.3*cm,(9.6)*cm,Dep_Employment);
            
            if Dep_Salary != 'NA':
                pdf.setFont('VeraBd', 8);
                pdf.drawCentredString((12.5/2)*cm,(9)*cm,"ESTIMATED YEARLY SALARY");
                pdf.drawImage('/home/pdfImages/design1/salary.png', 4.2*cm, (8)*cm, width=4.2*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.setFont('VeraBd', 8);
                pdf.setFillColorRGB(255,0,0)
                pdf.drawCentredString((12.5/2)*cm,(8.3)*cm,Dep_Salary);
                
            
            pdf.setFillColorRGB(0,0,0)
            if Dep_Media !='NA':
                pdf.drawImage('/home/pdfImages/fb_blue.png',1.5*cm,(7.35)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                fb_url_right = []
                raw_addr = Dep_Media
                # print('fbRaw',raw_addr[0:64])
                addr = raw_addr[0:64]+'<br/>'+raw_addr[64:]
                addr = '<link href="' + raw_addr + '">' + addr + '</link>'
                fb_url_right.append(Paragraph(addr,styleN))
                f = Frame(2*cm, (5.6)*cm, 8.5*cm, 2.5*cm, showBoundary=0)
                f.addFromList(fb_url_right,pdf)
            
            if Dep_Media2 != 'NA':
                pdf.drawImage('/home/pdfImages/linkedin_blue.png',1.5*cm,(6.55)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                ld_url_right = []
                raw_addr2 = Dep_Media2
                addr2 = raw_addr2[0:64]+'<br/>'+raw_addr2[64:]
                addr2 = '<link href="' + raw_addr2 + '">' + addr2 + '</link>'
                ld_url_right.append(Paragraph(addr2,styleN))
                
                f = Frame(2*cm, (4.8)*cm, 8.5*cm, 2.5*cm, showBoundary=0)
                f.addFromList(ld_url_right,pdf)
         ############################# About Family ################################
         
        ###########################VEHICLES DETAILS#################################
      
        if spouse_name != 'NA' :
            pdf.line(1.3*cm,(6)*cm,11.2*cm,(6)*cm)
        if len(regVehicles) != 0:
            # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
            pdf.setFont('VeraBd', 12);
            pdf.drawCentredString(4*cm,(5.6)*cm,"REGISTERED Vehicle(s)");
            pdf.setFont('Vera', 10);
        if vehicle1 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(4.9)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2*cm,(4.9)*cm,vehicle1);
        if vehicle2 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(4.2)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2*cm,(4.2)*cm,vehicle2);
        if vehicle3 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(3.5)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2*cm,(3.45)*cm,vehicle3);
        
        
        
        if Input_Pop != 'NA':
            # pdf.line(1.3*cm,(2.9)*cm,11.2*cm,(2.9)*cm)
            pdf.roundRect(1.3*cm, (0.4)*cm, 10*cm, 2.6*cm, 4, stroke=1, fill=0);
            pdf.setFont('VeraBd', 10);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,FullName.upper());
            pdf.drawCentredString((12.5/2)*cm,(2.4)*cm,"City:  "+cityState);
            pdf.drawImage('/home/pdfImages/dot.png',3*cm,(1.75)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((6.25/2)*cm,(1.2)*cm,"POPULATION");
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((6.25/2)*cm,(0.8)*cm,Input_Pop);

            pdf.setLineWidth(0.5);
            
        if Median_HouseHold_Val != 'NA':
            pdf.drawImage('/home/pdfImages/dot.png',7.5*cm,(1.75)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawCentredString(7.5*cm,(1.2)*cm,"MEDIAN HOUSEHOLD INCOME");
            pdf.setFont('Vera', 8);
            pdf.drawCentredString(7.5*cm,(0.8)*cm,Median_HouseHold_Val);
        
        ################################ Right_Template_Contents ##################################################
        pdf.setFont('Vera', 9);
        
        if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA':
            
            
            
            pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            ld_url = []
            # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
            raw_addr2 = Per_LinkedIn
            address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
            address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
            ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
           
            f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(ld_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            gmail_url = []
            #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
            raw_addr3 = per_Email
            address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
            address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
            gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

            f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(gmail_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFillColorRGB(255,255,255)
            pdf.drawString(14.75*cm,13*cm,Per_Tel)
    
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA': 
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            
            if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA':
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
               
                
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA':
                
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

            
            elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA':
                
                # pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)


                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr3 = per_Email
                address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA':
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:32]+'<br/>'+raw_addr[33:64]+'<br/>'+raw_addr[65:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                
                f = Frame(14.5*cm, 15.4*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                                      
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[33:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 15.4*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                
            
            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,14.5*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,13*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 14*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                ld_url = []
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:25]+'<br/>'+raw_addr2[25:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 12.5*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[33:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
              
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                               
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                
                
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
                
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                              
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                 
            
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                
                
                # pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[35:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
        
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[33:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
            
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA':
            
                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr3 = per_Email
                address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
            
            
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
             
                pdf.drawImage('/home/pdfImages/Facebook.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:34]+'<br/>'+raw_addr[34:64]+'<br/>'+raw_addr[65:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                pdf.drawImage('/home/pdfImages/Linkedin.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:34]+'<br/>'+raw_addr2[34:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.75*cm,14.2*cm,Per_Tel)
            
            
         ################### Hobbies ########################
        if hobby1 != 'NA' and hobby2 !='NA':
            pdf.setFillColorRGB(255,255,255)
            pdf.setFont('Vera', 8);
            pdf.drawString(13.7*cm,(12.2+contactHeight)*cm,'________________________________________________')
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(11.55+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(11.35+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 12);
            pdf.drawCentredString(15.55*cm,(11.36+contactHeight)*cm,'HOBBIES');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10.6+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 8);
            pdf.drawString(14.6*cm,(10.65+contactHeight)*cm,hobby1)
            pdf.drawString(14.6*cm,(10.05+contactHeight)*cm,hobby2)
            pdf.drawString(13.7*cm,(9.7+contactHeight)*cm,'________________________________________________')
        elif hobby1 != 'NA' and hobby2 =='NA':
            pdf.setFillColorRGB(255,255,255)
            pdf.setFont('Vera', 8);
            pdf.drawString(13.7*cm,(12.2+contactHeight)*cm,'________________________________________________')
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(11.35+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 12);
            pdf.drawCentredString(15.55*cm,(11.36+contactHeight)*cm,'HOBBIES');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10.6+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
           
            pdf.setFont('Vera', 8);
            pdf.drawString(14.6*cm,(10.65+contactHeight)*cm,hobby1)
            
            pdf.drawString(13.7*cm,(9.7+contactHeight)*cm,'________________________________________________')
       
        ################### Criminal History,Bankruptcies,Evictions ##########################
        
        
        if CHFdate1 != 'NA' and CHFdate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(8.9+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(8.95+contactHeight)*cm,'CRIMINAL HISTORY');
            pdf.setFont('Vera', 9);
            pdf.drawString(14.25*cm,(8.45+contactHeight)*cm,'Filing Date   Offense Description');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.8+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(7.82+contactHeight)*cm,CHFdate1)
            pdf.drawString(16.2*cm,(7.82+contactHeight)*cm,CHOdate1)
            pdf.drawString(14.25*cm,(7.25+contactHeight)*cm,CHFdate2)
            pdf.drawString(16.2*cm,(7.25+contactHeight)*cm,CHOdate2)
        
        # extraHeight=2
        
        elif CHFdate1 != 'NA' and CHFdate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(8.9+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.5*cm,(8.95+contactHeight)*cm,'CRIMINAL HISTORY');
            pdf.setFont('Vera', 9);
            pdf.drawString(14.25*cm,(8.45+contactHeight)*cm,'Filing Date   Offense Description');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.8+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(7.82+contactHeight)*cm,CHFdate1)
            pdf.drawString(16.2*cm,(7.82+contactHeight)*cm,CHOdate1)
         
        if BRFdate1 != 'NA' and BRFdate2 != 'NA':
            contactHeight=contactHeight+0.85
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(5.5+contactHeight+crimeHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(5.55+contactHeight+crimeHeight)*cm,'BANKRUPTCIES');
            pdf.setFont('Vera', 9);      
            pdf.drawString(14.25*cm,(5+contactHeight+crimeHeight)*cm,'Filing Date   Filing Status');
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(4.5+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(4.5+contactHeight+crimeHeight)*cm,BRFdate1)
            pdf.drawString(16.2*cm,(4.5+contactHeight+crimeHeight)*cm,BROdate1)
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(4+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(3.93+contactHeight+crimeHeight)*cm,BRFdate2)
            pdf.drawString(16.2*cm,(3.93+contactHeight+crimeHeight)*cm,BROdate2)
        elif BRFdate1 != 'NA' and BRFdate2 == 'NA':
            contactHeight=contactHeight+0.85
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(5.5+contactHeight+crimeHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(5.55+contactHeight+crimeHeight)*cm,'BANKRUPTCIES');
            pdf.setFont('Vera', 9);      
            pdf.drawString(14.25*cm,(5+contactHeight+crimeHeight)*cm,'Filing Date   Filing Status');
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(4.5+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(4.5+contactHeight+crimeHeight)*cm,BRFdate1)
            pdf.drawString(16.2*cm,(4.5+contactHeight+crimeHeight)*cm,BROdate1)
            
        if EVFdate1 != 'NA' and EVFdate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(3.1+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(3.15+contactHeight+crimeHeight+bankHeight)*cm,'EVICTIONS');
            pdf.setFont('Vera', 9);
            pdf.drawString(14.25*cm,(2.55+contactHeight+crimeHeight+bankHeight)*cm,'Filing Date   Filing Type');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(1.95+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(1.95+contactHeight+crimeHeight+bankHeight)*cm,EVFdate1)
            pdf.drawString(16.2*cm,(1.95+contactHeight+crimeHeight+bankHeight)*cm,EVOdate1)
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,EVFdate2)
            pdf.drawString(16.2*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,EVOdate2)
            
        elif EVFdate1 != 'NA' and EVFdate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(1.75+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawCentredString(15.65*cm,(1.75+contactHeight+crimeHeight+bankHeight)*cm,'EVICTIONS');
            pdf.setFont('Vera', 9);
            pdf.drawCentredString(16.1*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,'Filing Date     Filing Type');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(0.85+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(0.85+contactHeight+crimeHeight+bankHeight)*cm,EVFdate1)
            pdf.drawString(16.2*cm,(0.85+contactHeight+crimeHeight+bankHeight)*cm,EVOdate1)
            
      
        pdf.showPage()
        pdf.save()

        pdf = buffer.getvalue()
        # store = FileResponse(buffer, as_attachment=True, filename=FullName+'.pdf')
        # print('store',store);
        buffer.close()
        response.write(pdf)
        
        FNMAE = FullName+'.pdf'
        print('fs',FNMAE)
        if fs.exists(FNMAE):
            with fs.open(FNMAE) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename=FNMAE'
                # return "HELLO"
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')
  
def pdf_gen(request,userId=None):
   
    userId = request.GET["userId"]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from usData,us_image where usData.id=us_image.id and usData.id='{}'".format(userId))
        myresult = cursor.fetchall()
        # print('myresult:',myresult)
        if not myresult:
            template = loader.get_template('notFound.html') # getting our template  
            return HttpResponse(template.render())       # rendering the template in HttpResponse 
            return render(request,'notFound.html') 
        for x in myresult:
    
            var = myresult[0]
            
            PersonName=x[0]
            FullName = x[1]+' '+x[2]
            Fname = x[1]
            Lname = x[2]
            
            Per_Age             =x[3]
            if not Per_Age:
                Per_Age='NA'
                
            Address             =x[4]
            if not Address:
                Address ='NA'
                            
            Spouse_Age          =x[5]
            
            if not Spouse_Age:
                Spouse_Age          ='NA'
            else:
                Spouse_Age          ='Age:  '+x[5]
                
            Dep_Employment      =x[6]
            
            if not Dep_Employment:
                Dep_Employment          ='NA'
                               
            Dep_Salary          =x[7]
            
            if not Dep_Salary:
                Dep_Salary          ='NA'
                calDepSal          = 0
            else:
                Dep_Salary = x[7]
                calDepSal = int(float(Dep_Salary))
                Dep_Salary = int(float(Dep_Salary))
                Dep_Salary = custom_format_currency(Dep_Salary, 'USD', locale='en_US')    
            Dep_Media           =x[8]
            if not Dep_Media:
                Dep_Media='NA'
                
            Education           =x[9]
            if Education:
                edu=Education.split(';')
            else:
                edu=''
            
            Per_Employment      =x[10]
            
            if Per_Employment:
                perEmpl=Per_Employment.split(';')
            else:
                perEmpl=''

            # print('n(perEmpl',perEmpl)
            Job_Desc            =x[11]
            if Job_Desc:
                JobDesc=Job_Desc.split(';')
            else:
                JobDesc=''
            
                
            Per_Salary          =x[12]
            
            if not Per_Salary:
                Per_Salary          ='NA'
                calPerSal          = 0
            else:
                Per_Salary = x[12]
                # Per_Salary = round(Per_Salary)
                
                calPerSal = int(float(Per_Salary))
                Per_Salary = custom_format_currency(Per_Salary, 'USD', locale='en_US')
            Input_Pop           =x[13]
            if not Input_Pop:
                Input_Pop='NA'
            Median_HouseHold_Val=x[14]
            if not Median_HouseHold_Val:
                Median_HouseHold_Val='NA'
            else:
                Median_HouseHold_Val=x[14]
                # Median_HouseHold_Val = round(Median_HouseHold_Val)
                Median_HouseHold_Val = custom_format_currency(Median_HouseHold_Val, 'USD', locale='en_US')
                
           
                
            Home_Val            =x[15]
            
            if Home_Val:
               
                allHomeVal=Home_Val.split(';')
            else:
                allHomeVal=''
                
                
            Esti_Home_Equi      =x[16]
            
            if Esti_Home_Equi:
                Esti_Home_Equi = int(float(Esti_Home_Equi))
               
                homeEqu1 = custom_format_currency(Esti_Home_Equi, 'USD', locale='en_US')
                # allHomeEqui=Esti_Home_Equi.split(',')
                
            else:
                homeEqu1='$0'
                
                # Esti_Home_Equi = int(float(Esti_Home_Equi))
              
            Mort_Amt            =x[17]
            if not Mort_Amt:
                Mort_Amt='NA'
            else:
                Mort_Amt            =x[17]
                Mort_Amt = int(float(Mort_Amt))
                
                Mort_Amt = custom_format_currency(Mort_Amt, 'USD', locale='en_US')
            Mort_Date           =x[18]
            
            if not Mort_Date:
                Mort_Date='NA'
                
            Vehicle_det         =x[19]
            # print('Vehicle_det',Vehicle_det)
            if Vehicle_det:
                regVehicles=Vehicle_det.split(';')
            else:
                regVehicles=''
            
            Per_facebook        =x[20]
            if not Per_facebook:
                Per_facebook          ='NA'
                
            Per_LinkedIn        =x[21]
            if not Per_LinkedIn:
                Per_LinkedIn          ='NA'
                
            per_Email           =x[22]
            if not per_Email:
                per_Email          ='NA'
            Per_Tel             =x[23]
            if not Per_Tel:
                Per_Tel          ='NA'
            else:
                Per_Tel = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}', Per_Tel));
            # print(Per_Tel)
            
            
            Per_Hobbies         =x[24]
            if Per_Hobbies:
                hobbies=Per_Hobbies.split(';')
            else:
                hobbies=''
                    
            
            Criminal_Fill_Date  =x[25]
            if Criminal_Fill_Date:
                crimeDate=Criminal_Fill_Date.split(';')
            else:
                crimeDate=''
                     
            
            Offense_Desc        =x[26]
            if Offense_Desc:
                offenceDesc=Offense_Desc.split(';')
            else:
                offenceDesc=''
            
                       
            Bankrupt_Fill_Date  =x[27]
            if Bankrupt_Fill_Date:
                bankrupt=Bankrupt_Fill_Date.split(';')
            else:
                bankrupt=''
                  
            # print('bankrupt',len(bankrupt))
            Bank_Fill_Status    =x[28]
            if Bank_Fill_Status:
                bankOffence=Bank_Fill_Status.split(';')
            else:
                bankOffence=''
            
            
            Evic_Fill_Date      =x[29]
            if Evic_Fill_Date:
                evictionDate=Evic_Fill_Date.split(';')
            else:
                evictionDate=''
            
            
            Evic_Fill_Type      =x[30]
            if Evic_Fill_Type:
                evictionType=Evic_Fill_Type.split(';')
            else:
                evictionType=''
                     
            Per_Image           =x[31]
            House_Image         =x[32]
            enterdDate          =x[33]
            enterdBy            =x[34]
            spouse_name            =x[35]
            
            if not spouse_name:
                spouse_name='NA'
                
            updateFlag            =x[36]
            updatedBy            =x[37]
            Dep_Designation            =x[38]
            if not Dep_Designation:
                Dep_Designation='NA'
            Dep_Media2            =x[39]
            if not Dep_Media2:
                Dep_Media2='NA'
            currentValue            =x[40]
            purchaseDate            =x[41]
            purchasePrice            =x[42]
            qualityFlag            =x[43]
            qualityCheckedBy            =x[44]
            
            pincode            =x[45]
            # if pincode:
                # pin=pincode.split(',')
            # else:
                # pin=''
            
            
            city            =x[46]
            # if city:
                # cityy=city.split(',')
            # else:
                # cityy=''
                
            state            =x[47]
            # if state:
                # states=state.split(',')
            # else:
                # states=''
                
            cityState=x[46]+', '+x[47]
            
            university            =x[48]
            if university:
                univ=university.split(';')
            else:
                univ=''
                
            # if not university:
                # university='NA'
            qaRemarks            =x[49]
            personSex            =x[50]
            qualityCheckedDate            =x[51]
            startTime            =x[52]
            endTime            =x[53]
            noData            =x[54]
            houseType            =x[55]
            medianHouseValue            =x[56]
            
            if not medianHouseValue:
                medianHouseValue='NA'
            else:
                medianHouseValue=x[56]
                medianHouseValue = custom_format_currency(medianHouseValue, 'USD', locale='en_US')
           
            corpFilingDates            =x[57]
            if corpFilingDates:
                corpDate=corpFilingDates.split(';')
            else:
                corpDate=''
        
            corpFilingNames            =x[58]
            if corpFilingNames:
                corpFiling=corpFilingNames.split(';')
            else:
                corpFiling=''
           
            spouseBankruptDate            =x[59]
            if spouseBankruptDate:
                spBankruptDate=spouseBankruptDate.split(';')
            else:
                spBankruptDate=''
                
            spouseBankruptDetails            =x[60]
            if spouseBankruptDetails:
                spBankDet=spouseBankruptDetails.split(';')
            else:
                spBankDet=''
            
            
            # if not spouseBankruptDetails:
                # spouseBankruptDetails='NA'
                
            Per_instagram            =x[61]
            
            if not Per_instagram:
                Per_instagram          ='NA'
                
            Per_twitter            =x[62]
            if not Per_twitter:
                Per_twitter          ='NA'
            judments            =x[63]
            if not judments:
                judments='NA'
                
            Dep_instagram            =x[64]
            if not Dep_instagram:
                Dep_instagram          ='NA'
            Dep_twitter            =x[65]
            if not Dep_twitter:
                Dep_twitter          ='NA'
                
            selectedCity            =x[66]
            if not selectedCity:
                selectedCity          ='NA'
            
            relationStatus            =x[67]
            if not relationStatus:
                relationStatus          ='NA'    
                
            licence_det            =x[68]
            if licence_det:
                licences=licence_det.split(';')
            else:
                licences=''
                
            licence_date            =x[69]
            edit_startTime            =x[70]
            edit_endTime            =x[71]
            
            Home_Val2            =x[72]
            
            if Home_Val2:
                # hom3=np.array(Home_Val)
                # print('hom3',np.mean(hom3))
                allHomeVal2=Home_Val2.split(';')
            else:
                allHomeVal2=''
             
            Home_Val3            =x[73]
            if Home_Val3:
                allHomeVal3=Home_Val3.split(';')
            else:
                allHomeVal3=''
                
            Esti_Home_Equi2            =x[74]
            if Esti_Home_Equi2:
                Esti_Home_Equi2 = int(float(Esti_Home_Equi2))
                homeEqu2 = custom_format_currency(Esti_Home_Equi2, 'USD', locale='en_US')
                
                # allHomeEqui=Esti_Home_Equi.split(',')
                
            else:
                homeEqu2='$0'
                # Esti_Home_Equi = int(float(Esti_Home_Equi))
            
            
            Esti_Home_Equi3            =x[75]
            if Esti_Home_Equi3:
                Esti_Home_Equi3 = int(float(Esti_Home_Equi3))
                homeEqu3 = custom_format_currency(Esti_Home_Equi3, 'USD', locale='en_US')
                # allHomeEqui=Esti_Home_Equi.split(',')
                
            else:
                homeEqu3='$0'
                # Esti_Home_Equi = int(float(Esti_Home_Equi))
                
            Address2            =x[76]
            if not Address2:
                Address2 = 'NA'
            Address3            =x[77]
            if not Address3:
                Address3 = 'NA'
                
            # print('Address2',Address2)
            # print('Address3',Address3)
            
            pincode2            =x[78]
            if not pincode2:
                pincode2 = 'NA'
            pincode3            =x[79]
            if not pincode3:
                pincode3 = 'NA'
            state2            =x[80]
            if not state2:
                state2 = 'NA'
            state3            =x[81]
            if not state3:
                state3 = 'NA'
            city2            =x[82]
            if not city2:
                city2 = 'NA'
            city3            =x[83]
            if not city3:
                city3 = 'NA'
            
            spouceEducation            =x[84]
            if spouceEducation:
                spoEdu=spouceEducation.split(';')
            else:
                spoEdu=''
            
            spouceUniversity            =x[85]
            if spouceUniversity:
                spoUni=spouceUniversity.split(';')
            else:
                spoUni=''
            profLicence            =x[86]
            if not profLicence:
                profLicence = 'NA'
            
            prev_Per_Employment      =x[87]
            
            if prev_Per_Employment:
                perPrevEmpl=prev_Per_Employment.split(';')
            else:
                perPrevEmpl=''
            
            prev_Job_Desc      =x[88]
            
            
            if prev_Job_Desc:
                perPrevJob=prev_Job_Desc.split(';')
            else:
                perPrevJob=''
            
            editTimeDiff      =x[89]            
            mailSent      =x[90]            
            ####image data
            
            imageId            =x[91]
            person_image            =x[92]
            home_image            =x[93]
            name            =x[94]
            dateAndTime            =x[95]
            personImageFlag            =x[96]
            homeImageFlag            =x[97]
            # print(person_image)
            profileString = person_image.decode()

            # reconstruct image as an numpy array
            img = imread(io.BytesIO(base64.b64decode(profileString)))

            # show image
            plt.figure()
            plt.imshow(img, cmap="gray")
            
            cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite("profileImage.jpg", cv2_img)
            plt.show()
            
            houseString = home_image.decode()

            # reconstruct image as an numpy array
            img1 = imread(io.BytesIO(base64.b64decode(houseString)))

            # show image
            plt.figure()
            plt.imshow(img1, cmap="gray")
            
            cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
            cv2.imwrite("houseImage.jpg", cv2_img1)
            plt.show()
        
        if Address2 == 'NA' and Address3 == 'NA':
            Addr = 1
        else:
            Addr = 2
            
        if len(allHomeVal) == 0:
            hv1 = 0
            hv2 = 0
           
        elif len(allHomeVal) == 1:
            hv1 = allHomeVal[0]
            hv2 = 0
                  
        else:
            hv1 = allHomeVal[0]
            hv2 = allHomeVal[1]
           
        
        hvTotal1 = int(hv1)+int(hv2)
        if hv1 == 0 or hv2 == 0:
            homeValu1 = int(hvTotal1)
        else:
            homeValu1 = int(int(hvTotal1)/2)
        
        homeEquiForSal = int(float(homeValu1))
        homeValu1 = custom_format_currency(homeValu1, 'USD', locale='en_US')
        
        
        if len(allHomeVal2) == 0:
            hv21 = 0
            hv22 = 0
           
        elif len(allHomeVal2) == 1:
            hv21 = allHomeVal2[0]
            hv22 = 0
                  
        else:
            hv21 = allHomeVal2[0]
            hv22 = allHomeVal2[1]
           
        
        hvTotal2 = int(hv21)+int(hv22)
        if hv21 == 0 or hv22 == 0:
            homeValu2 = int(hvTotal2)
        else:
            homeValu2 = int(int(hvTotal2)/2)
            homeValu2 = int(float(homeValu2))
           
        homeValu2 = custom_format_currency(homeValu2, 'USD', locale='en_US')
        
        if len(allHomeVal3) == 0:
            hv31 = 0
            hv32 = 0
           
        elif len(allHomeVal3) == 1:
            hv31 = allHomeVal3[0]
            hv32 = 0
                  
        else:
            hv31 = allHomeVal3[0]
            hv32 = allHomeVal3[1]
           
        
        hvTotal3 = int(hv31)+int(hv32)
        if hv31 == 0 or hv32 == 0:
            homeValu3 = int(hvTotal3)
        else:
            homeValu3 = int(int(hvTotal3)/2)
            # homeValu3 = int(float(int(homeValu3)))
        homeValu3 = custom_format_currency(homeValu3, 'USD', locale='en_US')
        
        # print('homeValu3homeValu3:',homeValu3)
        
        if len(edu) == 0:
            edu1 = 'NA'
            edu2 = 'NA'
            edu3 = 'NA'
            
        elif len(edu) == 1:
            edu1 = edu[0]
            edu2 = 'NA'
            edu3 = 'NA'
        elif len(edu) == 2:
            edu1 = edu[0]
            edu2 = edu[1]
            edu3 = 'NA'
            
        else:
            edu1 = edu[0]
            edu2 = edu[1]
            edu3 = edu[2]
            
         
        if len(univ) == 0:
            univ1 = 'NA'
            univ2 = 'NA'
            univ3 = 'NA'
            
        elif len(univ) == 1:
            univ1 = univ[0]
            univ2 = 'NA'
            univ3 = 'NA'
            
        elif len(univ) == 2:
            univ1 = univ[0]
            univ2 = univ[1]
            univ3 = 'NA'
            
        else:
            univ1 = univ[0]
            univ2 = univ[1]
            univ3 = univ[2]
        
        if len(spoEdu) == 0:
            spedu1 = 'NA'
            spedu2 = 'NA'
            
            
        elif len(spoEdu) == 1:
            spedu1 = spoEdu[0]
            spedu2 = 'NA'
                    
        else:
            spedu1 = spoEdu[0]
            spedu2 = spoEdu[1]
            
        if len(spoUni) == 0:
            spUni1 = 'NA'
            spUni2 = 'NA'
            
            
        elif len(spoUni) == 1:
            spUni1 = spoUni[0]
            spUni2 = 'NA'
                    
        else:
            spUni1 = spoUni[0]
            spUni2 = spoUni[1]
            
        
        if len(regVehicles) == 0:
            vehicle1 = 'NA'
            vehicle2 = 'NA'
            vehicle3 = 'NA'   
        elif len(regVehicles) == 1:
            vehicle1 = regVehicles[0]
            vehicle2 = 'NA'
            vehicle3 = 'NA'
        
        elif len(regVehicles) == 2:
            vehicle1 = regVehicles[0]
            vehicle2 = regVehicles[1]
            vehicle3 = 'NA'
        
        else:
            vehicle1 = regVehicles[0]
            vehicle2 = regVehicles[1]
            vehicle3 = regVehicles[2]
        
        if len(crimeDate) == 0:
            CHFdate1 = 'NA'
            CHFdate2 = 'NA'
        elif len(crimeDate) == 1:
            CHFdate1 = crimeDate[0]
            CHFdate2 = 'NA'
        else:
            CHFdate1 = crimeDate[0]
            CHFdate2 = crimeDate[1]
        
        if len(hobbies) == 0:
            hobby1 = 'NA'
            hobby2 = 'NA'
        elif len(hobbies) == 1:
            hobby1 = hobbies[0]
            hobby2 = 'NA'
        else:
            hobby1 = hobbies[0]
            hobby2 = hobbies[1]
        
        if len(offenceDesc) == 0:
            CHOdate1 = 'NA'
            CHOdate2 = 'NA'
        elif len(offenceDesc) == 1:
            CHOdate1 = offenceDesc[0]
            CHOdate2 = 'NA'
            
        else:
            CHOdate1 = offenceDesc[0]
            CHOdate2 = offenceDesc[1]
        
        if len(bankrupt) == 0:
            BRFdate1 = 'NA'
            BRFdate2 = 'NA'
        elif len(bankrupt) == 1:
            BRFdate1 = bankrupt[0]
            BRFdate2 = 'NA'
            
        else:
            BRFdate1 = bankrupt[0]
            BRFdate2 = bankrupt[1]
        
        if len(bankOffence) == 0:
            BROdate1 = 'NA'
            BROdate2 = 'NA'
        elif len(bankOffence) == 1:
            BROdate1 = bankOffence[0]
            BROdate2 = 'NA'
            
        else:
            BROdate1 = bankOffence[0]
            BROdate2 = bankOffence[1]
        
        if len(evictionDate) == 0:
            EVFdate1 = 'NA'
            EVFdate2 = 'NA'
        elif len(evictionDate) == 1:
            EVFdate1 = evictionDate[0]
            EVFdate2 = 'NA'
            
        else:
            EVFdate1 = evictionDate[0]
            EVFdate2 = evictionDate[1]
        
        if len(evictionType) == 0:
            EVOdate1 = 'NA'
            EVOdate2 = 'NA'
        elif len(evictionType) == 1:
            EVOdate1 = evictionType[0]
            EVOdate2 = 'NA'
            
        else:
            EVOdate1 = evictionType[0]
            EVOdate2 = evictionType[1]
        
        if len(JobDesc) == 0:
            JOB1 = 'NA'
            JOB2 = 'NA'
        elif len(JobDesc) == 1:
            JOB1 = JobDesc[0]
            JOB2 = 'NA'
            
        else:
            JOB1 = JobDesc[0]
            JOB2 = JobDesc[1]
        
        
        if len(perEmpl) == 0:
            comp1 = 'NA'
            comp2 = 'NA'
            
        elif len(perEmpl) == 1:
            comp1 = perEmpl[0]
            comp2 = 'NA'
            
        else:
            comp1 = perEmpl[0]
            comp2 = perEmpl[1]
        
        if len(perPrevEmpl) == 0:
            prevComp1 = 'NA'
            prevComp2 = 'NA'
            
        elif len(perPrevEmpl) == 1:
            prevComp1 = perPrevEmpl[0]
            prevComp2 = 'NA'
            
        else:
            prevComp1 = perPrevEmpl[0]
            prevComp2 = perPrevEmpl[1]
        
        if len(perPrevJob) == 0:
            prevJOB1 = 'NA'
            prevJOB2 = 'NA'
            
        elif len(perPrevJob) == 1:
            prevJOB1 = perPrevJob[0]
            prevJOB2 = 'NA'
            
        else:
            prevJOB1 = perPrevJob[0]
            prevJOB2 = perPrevJob[1]
        
        
        if len(corpDate) == 0:
            corDate1 = 'NA'
            corDate2 = 'NA'
        elif len(corpDate) == 1:
            corDate1 = corpDate[0]
            corDate2 = 'NA'
        else:
            corDate1 = corpDate[0]
            corDate2 = corpDate[1]
        
        if len(corpFiling) == 0:
            corpFile1 = 'NA'
            corpFile2 = 'NA'
        elif len(corpFiling) == 1:
            corpFile1 = corpFiling[0]
            corpFile2 = 'NA'
            
        else:
            corpFile1 = corpFiling[0]
            corpFile2 = corpFiling[1]
        if len(spBankruptDate) == 0:
            spBank1 = 'NA'
            spBank2 = 'NA'
        elif len(spBankruptDate) == 1:
            spBank1 = spBankruptDate[0]
            spBank2 = 'NA'

        else:
            spBank1 = spBankruptDate[0]
            spBank2 = spBankruptDate[1]
        if len(spBankDet) == 0:
            spBankDet1 = 'NA'
            spBankDet2 = 'NA'
        elif len(spBankDet) == 1:
            spBankDet1 = spBankDet[0]
            spBankDet2 = 'NA'

        else:
            spBankDet1 = spBankDet[0]
            spBankDet2 = spBankDet[1]
        
        # print('licences',type(licences))
        if len(licences) == 0:
            licence1 = 'NA'
            licence2 = 'NA'
            licence3 = 'NA'
        
        elif len(licences) == 1:
            licence1 = licences[0]
            licence2 = 'NA'
            licence3 = 'NA'
        elif len(licences) == 2:
            licence1 = licences[0]+', '+licences[1]
            licence2 = 'NA'
            licence3 = 'NA'
        elif len(licences) == 3:
            licence1 = licences[0]+', '+licences[1]
            licence2 = licences[2]
            licence3 = 'NA'
        elif len(licences) == 4:
            licence1 = licences[0]+', '+licences[1]
            licence2 = licences[2]+', '+licences[3]
            licence3 = 'NA'
        elif len(licences) == 5:
            licence1 = licences[0]+', '+licences[1]
            licence2 = licences[2]+', '+licences[3]
            licence3 = licences[4]
        else:
            licence1 = licences[0]+', '+licences[1]
            licence2 = licences[2]+', '+licences[3]
            licence3 = licences[4]+', '+licences[5]
        
        
        
        ####################################################HEight Calculation#######################################
        # print('len(perEmpl)',len(perEmpl))
        # print('len(JobDesc)',len(JobDesc))
        # print('Per_Salary',Per_Salary)
        
        if  comp1 == 'NA' and comp2 == 'NA' and JOB1 == 'NA' and JOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA' and prevJOB1 =='NA' and prevJOB2 == 'NA' or  Per_Salary =='NA':
                # homeHeight=2.5
                homeHeight=0
                # print('homeHeight',homeHeight)
        else:
            homeHeight=0
            
        # if Education =='NA':
            # qualHeight=3
        # else:
            # qualHeight=0
        # homeHeight+= qualHeight   
        if spouse_name == 'NA':
            vehHeight=7.6+homeHeight
        else:
            vehHeight=0+homeHeight    
        
        if Per_LinkedIn != 'NA':
            linkdHeight=0
        else:
            linkdHeight=0
            
        if Per_facebook == 'NA':
            fbHeight=2.5
        else:
            fbHeight=0
            
        if per_Email != 'NA':
            emailHeight=0
        else:
            emailHeight=0
            
        if Per_Tel != 'NA':
            telHeight=0
        else:
            telHeight=0
            
        
        if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA': 
            contactHeight=5
        else:
            contactHeight=0
            
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA': 
            contactHeight=0
        if len(hobbies) == 0:
            # hobbyHeight = 2.5
            hobbyHeight = 0
            contactHeight+=hobbyHeight
        else:
            hobbyHeight = 0
        # if len(crimeDate) == 0:
        if len(corpFiling) == 0:
            crimeHeight=2.3
            # crimeHeight=0
        else:
            crimeHeight=0
            
        if len(bankrupt) == 0:
            bankHeight=2.15#2.25
        else:
            bankHeight=0
            
         
         #######################################End of Height Calculation#######################################
         
         
         
         #######################################LETS ROCK#######################################
        
        response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment''filename="{}"'.format(FullName)
        response['Content-Disposition'] = 'filename={0}.pdf'.format(FullName)
        # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        buffer = BytesIO()
        # pdf = canvas.Canvas(buffer)
        
        
        #enable this to store pdf in root folder and disable buffer canvas
        pdf = canvas.Canvas(FullName+'.pdf', pagesize=A4)
        # pdf = canvas.Canvas(FullName+'.pdf', pagesize=letter)
        pdf.setTitle(FullName)
         # Start writing the PDF here
        fs = FileSystemStorage()
        filename = FullName+'.pdf'
        print(filename)
        # pdf.drawImage('/home/pdfImages/Background.png',0*cm,0*cm,21.2*cm,29.7*cm);
        
        pdf.drawImage('/home/pdfImages/BG1.png',0*cm,0*cm,21.2*cm,29.7*cm);
        
        # pdf.drawImage('/home/pdfImages/bg.png',0*cm,0*cm,21.2*cm,29.7*cm);
        pdf.setFont('VeraBd', 14);
        
        print('personImageFlag',personImageFlag)
        if personImageFlag == 2:
            noImageMargin = 22
            lineMargin1 = 5.5
            lineMargin2 = 16
            salImgMargin = 8.2
        else:
           noImageMargin = 12.5
           lineMargin1 = 2
           lineMargin2 = 10.5
           salImgMargin = 3.3
            
        
        pdf.drawCentredString((noImageMargin/2)*cm,28.8*cm,FullName.upper());
        # pdf.setDash([2,2,2,2],0)
        pdf.line(lineMargin1*cm,28.6*cm,lineMargin2*cm,28.6*cm)
        # pdf.setDash([0,0,0,0],0)
        pdf.setFont('Vera', 14);


        if len(Job_Desc) >=90:
                jobFont=9
        else:
                jobFont=14
                
        ##################################JOBS DISPLAY #############################   
        # print('JOB1',JOB1)
        # print('JOB2',JOB2)
        # print('comp1',comp1)
        # print('comp2',comp2)
        # print('prevJOB1',prevJOB1)
        # print('prevJOB2',prevJOB2)
        
        # print('prevJOB2',prevJOB2)
        # print('prevComp1',prevComp1)
        # print('prevComp2',prevComp2)
        
        if JOB2 =='NA' and comp2 != 'NA':
            job2Height=0.5
        else:
            job2Height=0
            jobsHeight=0
        
        if JOB1 != 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,27.5*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,26.8*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,26.15*cm,comp1.upper());
            pdf.line(lineMargin1*cm,(25.45)*cm,lineMargin2*cm,(25.45)*cm)
        
        elif JOB1 != 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,27.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,26.45*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            pdf.line(lineMargin1*cm,(25.45)*cm,lineMargin2*cm,(25.45)*cm)
        
        elif JOB1 == 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,27.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,26.45*cm,comp1.upper());    
            pdf.line(lineMargin1*cm,(25.45)*cm,lineMargin2*cm,(25.45)*cm)
            
        elif JOB1 != 'NA' and comp1 != 'NA' and JOB2 != 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper()); 

            if JOB2 !='NA' :
                if JOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and JOB2 !='NA':
                        JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((12.5/2)*cm,26.2*cm,JOB2);
            pdf.setFillColorRGB(0,0,0)
            pdf.line(lineMargin1*cm,(25.45)*cm,lineMargin2*cm,(25.45)*cm)
            
        elif JOB1 != 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 != 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            if comp2 !='NA':
                if comp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,comp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
                
        elif JOB1 != 'NA' and comp1 != 'NA' and JOB2 != 'NA' and comp2 != 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            if JOB2 !='NA' :
                if JOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and JOB2 !='NA':
                        JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,JOB2);
            pdf.setFillColorRGB(0,0,0)
            
            if comp2 !='NA':
                if comp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,comp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 != 'NA' and JOB2 != 'NA' and comp2 != 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            if JOB2 !='NA' :
                if JOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and JOB2 !='NA':
                        JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,JOB2);
            pdf.setFillColorRGB(0,0,0)
            
            if comp2 !='NA':
                if comp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,comp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 != 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            if JOB2 !='NA' :
                if JOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and JOB2 !='NA':
                        JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,JOB2);
            pdf.setFillColorRGB(0,0,0)
            
            if comp2 !='NA':
                if comp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,comp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 != 'NA' and JOB2 != 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            if JOB2 !='NA' :
                if JOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and JOB2 !='NA':
                        JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,JOB2);
            pdf.setFillColorRGB(0,0,0)
            
            if comp2 !='NA':
                if comp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,comp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
            
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 != 'NA' and prevJOB2 != 'NA' and prevComp2 != 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,28.2*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,prevComp1.upper());   
            
            if prevJOB2 !='NA' :
                if prevJOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp2 !='NA' and prevJOB2 !='NA':
                        prevJOB2=prevJOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB2);
            pdf.setFillColorRGB(0,0,0)
            
            if prevComp2 !='NA':
                if prevComp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
            
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevComp1 != 'NA' and prevJOB2 != 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,28.2*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,prevComp1.upper());   
            
            if prevJOB2 !='NA' :
                if prevJOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp2 !='NA' and prevJOB2 !='NA':
                        prevJOB2=prevJOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB2);
            pdf.setFillColorRGB(0,0,0)
            
            if prevComp2 !='NA':
                if prevComp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
            
        elif JOB1 != 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 == 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
              
            
            if prevJOB1 !='NA' :
                if prevJOB1 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp2 !='NA' and prevJOB1 !='NA':
                        prevJOB1=prevJOB1+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB1);
            pdf.setFillColorRGB(0,0,0)
            
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
            
        elif JOB1 != 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                # pdf.drawCentredString((12.5/2)*cm,27.15*cm,prevComp1.upper());   
                pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp1.upper());
            
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
           
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 == 'NA' and prevJOB2 != 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,27.4*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,26.8*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            
            if prevJOB2 !='NA' :
                if prevJOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp2 !='NA' and prevJOB2 !='NA':
                        prevJOB2=prevJOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB2);
            pdf.setFillColorRGB(0,0,0)
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,26.5*cm,prevComp1.upper());   
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm) 
        
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 != 'NA' and prevJOB2 != 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,28.2*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,prevComp1.upper());   
            
            if prevJOB2 !='NA' :
                if prevJOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp2 !='NA' and prevJOB2 !='NA':
                        prevJOB2=prevJOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB2);
            pdf.setFillColorRGB(0,0,0)
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 != 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,26.5*cm,prevComp1.upper());   
            
            # if prevJOB2 !='NA' :
                # if prevJOB2 !='NA':
                    # pdf.setFont('Vera', jobFont);
                    # if prevComp2 !='NA' and prevJOB2 !='NA':
                        # prevJOB2=prevJOB2+','
                    # pdf.setFillColorRGB(0,0.5,0.5)
                    # pdf.drawCentredString((12.5/2)*cm,26.2*cm,prevJOB2);
            # pdf.setFillColorRGB(0,0,0)
            
            if prevComp2 !='NA':
                if prevComp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
              
        elif JOB1 != 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            if prevJOB1 !='NA' :
                if prevJOB1 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp1 !='NA' and prevJOB1 !='NA':
                        prevJOB1=prevJOB1+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB1);
            pdf.setFillColorRGB(0,0,0)
            
            if prevComp1 !='NA':
                if prevComp1 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp1.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 != 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            if prevJOB1 !='NA' :
                if prevJOB1 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp1 !='NA' and prevJOB1 !='NA':
                        prevJOB1=prevJOB1+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB1);
            pdf.setFillColorRGB(0,0,0)
            
            if prevComp1 !='NA':
                if prevComp1 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp1.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            if prevJOB1 !='NA' :
                if prevJOB1 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp1 !='NA' and prevJOB1 !='NA':
                        prevJOB1=prevJOB1+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB1);
            pdf.setFillColorRGB(0,0,0)
            
            if prevComp1 !='NA':
                if prevComp1 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp1.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 != 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 == 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            if prevJOB1 !='NA' :
                if prevJOB1 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and prevJOB1 !='NA':
                        prevJOB1=prevJOB1+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB1);
            pdf.setFillColorRGB(0,0,0)
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)    
        
        elif JOB1 != 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            # if prevJOB1 !='NA' :
                # if prevJOB1 !='NA':
                    # pdf.setFont('Vera', jobFont);
                    # if comp2 !='NA' and prevJOB1 !='NA':
                        # prevJOB1=prevJOB1+','
                    # pdf.setFillColorRGB(0,0.5,0.5)
                    # pdf.drawCentredString((12.5/2)*cm,26.2*cm,prevJOB1);
            # pdf.setFillColorRGB(0,0,0)
            
            if prevComp1 !='NA':
                if prevComp1 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp1.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevComp1 == 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,27.3*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,26.75*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,26.15*cm,comp1.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
            
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,27.25*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
               
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,26.75*cm,prevComp1.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)       
        
        elif JOB1 != 'NA' or comp1 != 'NA' and JOB2 != 'NA' or comp2 != 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':        
            # print('qwqwq')
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());
            
            if JOB2 !='NA' :
                if JOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and JOB2 !='NA':
                        JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,JOB2);
                pdf.setFillColorRGB(0,0,0)
            if comp2 !='NA':
                if comp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,comp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
       
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevComp1 != 'NA' and prevJOB2 != 'NA' and prevComp2 != 'NA':
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,28.2*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,prevComp1.upper());   
            
            if prevJOB2 !='NA' :
                if prevJOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if prevComp2 !='NA' and prevJOB2 !='NA':
                        prevJOB2=prevJOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB2);
            pdf.setFillColorRGB(0,0,0)
            
            if prevComp2 !='NA':
                if prevComp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp2.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 != 'NA' and prevComp2 != 'NA':        
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,28.2*cm,"[Previous Employment]");
            # pdf.drawCentredString((12.5/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if prevComp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,prevComp1.upper());
            
            if JOB2 !='NA' :
                if JOB2 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and JOB2 !='NA':
                        JOB2=JOB2+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,JOB2);
                pdf.setFillColorRGB(0,0,0)
            if prevComp2 !='NA':
                if prevComp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp2.upper());
                pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)

        elif JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 != 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 != 'NA':        
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,27.2*cm,"[Previous Employment]");
            # pdf.drawCentredString((12.5/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if prevJOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if prevComp1 != 'NA':
                    prevJOB1=prevJOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,26.75*cm,prevJOB1);
                pdf.setFillColorRGB(0,0,0)    
           
            if prevComp2 !='NA':
                if prevComp2 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.6+job2Height)*cm,prevComp2.upper());
                    pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        elif JOB1 == 'NA' and comp1 != 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevComp1 != 'NA' and prevJOB2 == 'NA' and prevComp2 == 'NA':
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,"[Current Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            if JOB1 !='NA':
                pdf.setFillColorRGB(0,0.5,0.5)
                if comp1 != 'NA':
                    JOB1=JOB1+','
                pdf.drawCentredString((noImageMargin/2)*cm,27.75*cm,JOB1);
                pdf.setFillColorRGB(0,0,0)    
            if comp1 != 'NA':
                pdf.setFont('Vera', jobFont);
                pdf.drawCentredString((noImageMargin/2)*cm,27.15*cm,comp1.upper());   
            
            pdf.setFillColorRGB(0.35,0,0.1)
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((noImageMargin/2)*cm,26.7*cm,"[Previous Employment]");
            pdf.setFillColorRGB(0,0,0)
            pdf.setFont('Vera', jobFont);
            
            if prevJOB1 !='NA' :
                if prevJOB1 !='NA':
                    pdf.setFont('Vera', jobFont);
                    if comp2 !='NA' and prevJOB1 !='NA':
                        prevJOB1=prevJOB1+','
                    pdf.setFillColorRGB(0,0.5,0.5)
                    pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,prevJOB1);
            pdf.setFillColorRGB(0,0,0)
            
            if prevComp1 !='NA':
                if prevComp1 != 'NA':
                    
                    pdf.setFillColorRGB(0,0,0)
                    pdf.setFont('Vera', jobFont);
                    pdf.drawCentredString((noImageMargin/2)*cm,(25.8+job2Height)*cm,prevComp1.upper());
            pdf.line(lineMargin1*cm,(25.45+job2Height)*cm,lineMargin2*cm,(25.45+job2Height)*cm)
        
        
        
        ##################################JOBS DISPLAY #############################            
          
        if personImageFlag == 2:
            print('skipp')
            
            if personSex =='Female' and Per_Age =='NA':
                pdf.drawImage('/home/pdfImages/design1/age.png',12.75*cm,20.45*cm,8*cm,1.2*cm,preserveAspectRatio=False,mask='auto');
                pdf.drawImage('/home/pdfImages/design1/female1.png',16.25*cm,20.5*cm,1.5*cm,1*cm,preserveAspectRatio=True, mask='auto');
                
            else:
                pdf.drawImage('/home/pdfImages/design1/age.png',12.75*cm,20.45*cm,8*cm,1.2*cm,preserveAspectRatio=False,mask='auto');
                pdf.drawImage('/home/pdfImages/design1/male.png',16.25*cm,20.5*cm,1.5*cm,1*cm,preserveAspectRatio=True, mask='auto');
            
            
            if Per_Age !='NA' and personSex !='NA' :
                pdf.setFillColorRGB(0,0,0);
                pdf.setFont('VeraBd', 18);
        
                pdf.drawImage('/home/pdfImages/design1/age.png',12.75*cm,20.45*cm,8*cm,1.2*cm,preserveAspectRatio=False,mask='auto');
                if personSex =='Female':
                    pdf.drawImage('/home/pdfImages/design1/female1.png',15*cm,20.5*cm,1.5*cm,1*cm,preserveAspectRatio=True, mask='auto');
                else:
                    pdf.drawImage('/home/pdfImages/design1/male.png',15*cm,20.5*cm,1.5*cm,1*cm,preserveAspectRatio=True, mask='auto');
                    
                pdf.drawCentredString(17.8*cm,20.75*cm,"AGE:  "+Per_Age);
                # pdf.drawCentredString(14.6*cm,20.3*cm,Per_Age);
        else:
        
            # pdf.drawImage('/home/pdfImages/default_men.png',14.05*cm,24.05*cm,3.9*cm,3.9*cm,preserveAspectRatio=False);
            pdf.drawImage('profileImage.jpg',12.5*cm,20.4*cm,8*cm,8.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.setLineWidth(2)
            pdf.setFillColorRGB(0.5,0,0)
            pdf.roundRect(12.5*cm, 20.4*cm, 8*cm, 8.8*cm, 4, stroke=1, fill=0);
            pdf.setFillColorRGB(0,0,0)
            
            
            # if Per_Age !='NA':
                # pdf.drawImage('/home/pdfImages/design1/age.png',15.75*cm,20.45*cm,4.7*cm,0.9*cm,preserveAspectRatio=False,mask='auto');
                
            if personSex =='Female' and Per_Age =='NA':
                pdf.drawImage('/home/pdfImages/design1/age.png',18.75*cm,20.45*cm,1.7*cm,0.9*cm,preserveAspectRatio=False,mask='auto');
                pdf.drawImage('/home/pdfImages/design1/female1.png',19.25*cm,20.5*cm,0.7*cm,0.7*cm,preserveAspectRatio=True, mask='auto');
                
            else:
                pdf.drawImage('/home/pdfImages/design1/age.png',18.75*cm,20.45*cm,1.7*cm,0.9*cm,preserveAspectRatio=False,mask='auto');
                pdf.drawImage('/home/pdfImages/design1/male.png',19.25*cm,20.5*cm,0.7*cm,0.7*cm,preserveAspectRatio=True, mask='auto');
            
            if Per_Age !='NA' and personSex !='NA' :
                pdf.setFillColorRGB(0,0,0);
                pdf.setFont('VeraBd', 11);
        
                pdf.drawImage('/home/pdfImages/design1/age.png',15.75*cm,20.45*cm,4.7*cm,0.9*cm,preserveAspectRatio=False,mask='auto');
                if personSex =='Female':
                    pdf.drawImage('/home/pdfImages/design1/female1.png',17*cm,20.5*cm,0.7*cm,0.7*cm,preserveAspectRatio=True, mask='auto');
                else:
                    pdf.drawImage('/home/pdfImages/design1/male.png',17*cm,20.5*cm,0.7*cm,0.7*cm,preserveAspectRatio=True, mask='auto');
                    
                pdf.drawCentredString(18.75*cm,20.6*cm,"AGE:  "+Per_Age);
                # pdf.drawCentredString(14.6*cm,20.3*cm,Per_Age);

        #################### Left components ##########################################
        pdf.setFillColorRGB(0,0,0);
        
        # if homeEquiForSal
        # print('calDepSal',calDepSal+calPerSal)
        # print('halfHomeEqui',halfHomeEqui)
        # print('totalFamilyEarning',totalFamilyEarning)
        # print('homeEquiForSal',type(homeEquiForSal))
        # print('homeEquiForSalNumber',homeEquiForSalNumber)
        
        if homeEquiForSal != 0:
            homeEquiForSalNumber = int(float(homeEquiForSal))
            
            halfHomeEqui = int(float(homeEquiForSal)/2)
            
            homeEqui120 = homeEquiForSalNumber + int(float(homeEquiForSal)*0.2)
            
            # print('homeEqui120', homeEqui120)
            totalFamilyEarning = calDepSal + calPerSal
            
            if int(float(calPerSal)) > halfHomeEqui and houseType == 'Own':
                calPerSal = int(float(homeEquiForSal))*0.45
                calPerSal = int(float(calPerSal))
                Per_Salary = custom_format_currency(calPerSal, 'USD', locale='en_US')
                print('calPerSal',calPerSal)
            elif  totalFamilyEarning > homeEqui120:
                print('GREATER')
                calPerSal = int(float(homeEquiForSal))*0.45
                calPerSal = int(float(calPerSal))
                Per_Salary = custom_format_currency(calPerSal, 'USD', locale='en_US')
                
                calDepSal = int(float(homeEquiForSal))*0.35
                calDepSal = int(float(calDepSal))
                Dep_Salary = custom_format_currency(calDepSal, 'USD', locale='en_US')
                
            elif houseType == 'Rented'  or houseType == 'Rented Apartment'  or houseType == 'Apartment':
                print('calPerSal',calPerSal)
                if calPerSal > 70000:
                    Per_Salary = custom_format_currency(68500, 'USD', locale='en_US')
                    Dep_Salary = custom_format_currency(38500, 'USD', locale='en_US')
                
            
            
        if JOB1 != 'NA' and Per_Salary !='NA':
            pdf.setFont('VeraBd', 11);
            pdf.drawCentredString((noImageMargin/2)*cm,25*cm,"ESTIMATED YEARLY SALARY");
            pdf.drawImage('/home/pdfImages/design1/salary.png', salImgMargin*cm, 24.05*cm, width=5.8*cm, height=.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.setFont('VeraBd', 11);
            pdf.setFillColorRGB(255,0,0)
            
            pdf.drawCentredString((noImageMargin/2)*cm,24.29*cm,Per_Salary);
        pdf.setFillColorRGB(0,0,0)
        
        if prevJOB1 != 'NA' and Per_Salary !='NA':
            pdf.setFont('VeraBd', 11);
            pdf.drawCentredString((noImageMargin/2)*cm,25*cm,"ESTIMATED YEARLY SALARY");
            pdf.drawImage('/home/pdfImages/design1/salary.png', salImgMargin*cm, 24.05*cm, width=5.8*cm, height=.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.setFont('VeraBd', 11);
            pdf.setFillColorRGB(255,0,0)
            
            pdf.drawCentredString((noImageMargin/2)*cm,24.29*cm,Per_Salary);
        pdf.setFillColorRGB(0,0,0)
        
        # if Address1 != 'NA':
        
        
        
        if Addr == 1:
            pdf.drawImage('/home/pdfImages/personHome.png',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
            
            if houseType =='Rented Apartment' or houseType =='Apartment':
                pdf.drawImage('/home/pdfImages/rentedApt.png',0.75*cm,(20.4)*cm,4.3*cm,3*cm,preserveAspectRatio=False);
                # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
            else:
                pdf.drawImage('houseImage.jpg',0.75*cm,(20.4)*cm,4.3*cm,3*cm,preserveAspectRatio=False);
            
            pdf.roundRect(0.75*cm, (20.4)*cm, 4.3*cm, 3.05*cm, 4, stroke=1, fill=0);
           
            pdf.setFont('VeraBd', 9);
            
            pdf.drawString(5.62*cm,(22.25)*cm,Address);
            pdf.drawString(5.62*cm,(21.75)*cm,city+', '+state.title()+' '+pincode);
            # pdf.drawString(5.62*cm,(21.25)*cm,pincode);
            
            if houseType =='Rented Apartment' or houseType =='Rented': 
                pdf.drawImage('/home/pdfImages/rented.png',5.7*cm,(20.8)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
            if houseType =='For Sale':  
                pdf.drawImage('/home/pdfImages/sale.png',5.7*cm,(20.8)*cm,2.75*cm,0.8*cm,preserveAspectRatio=False);
                
            if homeValu1 !='$0':
            
                pdf.drawImage('/home/pdfImages/dot.png',1*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFont('Vera', 8);
                pdf.drawCentredString((6.25/2)*cm,(19.2)*cm,"ESTIMATED HOME VALUE");
                pdf.setFont('Vera', 8);
                pdf.drawCentredString((6.25/2)*cm,(18.8)*cm,homeValu1);

                pdf.setLineWidth(0.5);
                pdf.line(6.25*cm,(19.5)*cm,6.25*cm,(18.65)*cm)
            
            if homeEqu1 != '$0':
                pdf.drawImage('/home/pdfImages/dot.png',7.20*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawCentredString(9.375*cm,(19.2)*cm,"ESTIMATED HOME EQUITY");
                pdf.setFont('Vera', 8);
                pdf.drawCentredString(9.375*cm,(18.8)*cm,homeEqu1);
                
        else:
            pdf.drawImage('/home/pdfImages/personHome.png',1.7*cm,(22.50)*cm,2*cm,0.35*cm,preserveAspectRatio=False);
            ## pdf.roundRect(0.75*cm, (20.4)*cm, 4.3*cm, 3.05*cm, 4, stroke=1, fill=0);
            pdf.roundRect(0.55*cm, (19.4)*cm, 4.45*cm, 3.15*cm, 4, stroke=1, fill=0);
            if houseType =='Rented Apartment' or houseType =='Apartment':
                # pdf.drawImage('/home/pdfImages/rentedApt.png',0.55*cm,(20.45)*cm,4.3*cm,3*cm,preserveAspectRatio=False);  
                pdf.drawImage('/home/pdfImages/rentedApt.png',0.6*cm,(19.45)*cm,4.25*cm,2.95*cm,preserveAspectRatio=False);
            else:
                # pdf.drawImage('houseImage.jpg',0.55*cm,(20.45)*cm,4.3*cm,3*cm,preserveAspectRatio=False);      
                pdf.drawImage('houseImage.jpg',0.6*cm,(19.5)*cm,4.35*cm,2.95*cm,preserveAspectRatio=False);
            
            if houseType =='Rented Apartment' or houseType =='Rented': 
                pdf.drawImage('/home/pdfImages/rented.png',5.4*cm,(23.25)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
            if houseType =='For Sale': 
                pdf.drawImage('/home/pdfImages/sale.png',5.4*cm,(23.25)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                
            if Address != 'NA':
                pdf.setFont('Vera', 8);
                
                ## pdf.drawString(5.62*cm,(22.25)*cm,Address1+', '+city1+', '+state1+' '+pin1);
                pdf.drawString(5.1*cm,(22.7)*cm,"1.");
                pdf.setFont('Vera', 8);
                pdf.drawString(5.6*cm,(22.7)*cm,Address);
                pdf.drawString(5.6*cm,(22.40)*cm,city+', '+state.title()+' '+pincode);
                if homeEqu1 != '$0':
                    pdf.drawString(5.6*cm,(22.03)*cm,"ESTIMATED HOME EQUITY: "+homeEqu1);
                if homeEqu1 == '$0':
                    Equiheight = 0.35;
                else:
                    Equiheight = 0;
                # pdf.drawCentredString(7.7*cm,(21.45)*cm,Esti_Home_Equi);
                # print('homeValu1',homeValu1)
                if homeValu1 != '$0':
                    pdf.drawString(5.6*cm,(21.63+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE: "+homeValu1);
                
                # pdf.drawCentredString(7.7*cm,(20.55)*cm,Home_Val);
                pdf.setFillColorRGB(0,0,1)
                pdf.drawString(5.6*cm,(21.55)*cm,'_______________________________')
                pdf.setFillColorRGB(0,0,0)
                
            if Address2 != 'NA':
                pdf.setFont('Vera', 8);
                
                ## pdf.drawString(5.62*cm,(22.25)*cm,Address1+', '+city1+', '+state1+' '+pin1);
                pdf.drawString(5.1*cm,(21.20)*cm,"2.");
                pdf.setFont('Vera', 8);
                pdf.drawString(5.6*cm,(21.20)*cm,Address2);
                pdf.drawString(5.6*cm,(20.90)*cm,city2+', '+state2.title()+' '+pincode2);
                
                # if homeValu2 == '0' or homeValu2 != '$0':
                if homeEqu2 != '$0':
                    pdf.drawString(5.6*cm,(20.53)*cm,"ESTIMATED HOME EQUITY: "+homeEqu2);
                if homeEqu2 == '$0':
                    Equiheight = 0.35;
                else:
                    Equiheight = 0;
                if homeValu2 != '$0':
                    pdf.drawString(5.6*cm,(20.13+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  "+homeValu2);
                pdf.setFillColorRGB(0,0,1)
                pdf.drawString(5.6*cm,(20.05)*cm,'_______________________________')
                pdf.setFillColorRGB(0,0,0)
                
            if Address3 != 'NA':
                pdf.setFont('Vera', 8);
                
                ##pdf.drawString(5.62*cm,(22.25)*cm,Address1+', '+city1+', '+state1+' '+pin1);
                pdf.drawString(5.1*cm,(19.7)*cm,"3.");
                pdf.setFont('Vera', 8);
                pdf.drawString(5.6*cm,(19.7)*cm,Address3);
                pdf.drawString(5.6*cm,(19.40)*cm,city3+', '+state3.title()+' '+pincode3);
                if homeEqu3 != '$0':
                # if homeEqu3 != 0:
                    pdf.drawString(5.6*cm,(19.03)*cm,"ESTIMATED HOME EQUITY: "+homeEqu3);
                if homeEqu3 == '$0':
                    Equiheight = 0.35;
                else:
                    Equiheight = 0;
                if homeValu3 != '$0':
                    pdf.drawString(5.6*cm,(18.63+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  "+homeValu3);
            
       
        ####DIVORCED IMG
        
        # pdf.drawImage('/home/pdfImages/divorce.png',2.55*cm,(10.4)*cm,3.8*cm,2*cm,preserveAspectRatio=False, mask='auto');    
        if spouse_name != 'NA' or  edu1 != 'NA' or univ1 != 'NA' or edu2 != 'NA' or univ2 != 'NA': 
            pdf.line(1.3*cm,(18.23)*cm,11.2*cm,(18.23)*cm)
        
        
        # if Education != 'NA' or university != 'NA':
        if len(edu) == 1 and len(univ) == 1:
            pdf.drawImage('/home/pdfImages/Education.png', 2.1*cm, (17)*cm, width=8.5*cm, height=0.75*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            if univ1 != 'NA':
            
                pdf.setFont('VeraBd', 8);
                pdf.setFillColorRGB(0.5,0.2,0.1)
                pdf.drawCentredString((12.5/2)*cm,(16.5)*cm,univ1.upper());
                pdf.setFillColorRGB(0,0,0)
            if edu1 != 'NA':
                pdf.drawCentredString((12.5/2)*cm,(16.05)*cm,edu1); 
                
        else:
            
            # pdf.drawImage('/home/pdfImages/Education1.png', 1.1*cm, (15)*cm, width=1.3*cm, height=3.5*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            if univ1 != 'NA':
                pdf.drawImage('/home/pdfImages/Education.png', 2*cm, (17.3)*cm, width=8.5*cm, height=0.75*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.setFont('VeraBd', 8);
                pdf.setFillColorRGB(0.5,0.2,0.1)
                pdf.drawCentredString((12.5/2)*cm,(16.9)*cm,univ1.upper());
                pdf.setFillColorRGB(0,0,0)
                
            if edu1 != 'NA':
                pdf.drawImage('/home/pdfImages/Education.png', 2*cm, (17.3)*cm, width=8.5*cm, height=0.75*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.drawCentredString((12.5/2)*cm,(16.5)*cm,edu1);
                pdf.setFillColorRGB(0,1,1)
                pdf.drawCentredString(6.25*cm,(16.35)*cm,'_______________________________')
                pdf.setFillColorRGB(0,0,0)    
            
            if univ2 != 'NA':
            
                pdf.setFont('VeraBd', 8);
                pdf.setFillColorRGB(0.5,0.2,0.1)
                pdf.drawCentredString((12.5/2)*cm,(15.94)*cm,univ2.upper());
                pdf.setFillColorRGB(0,0,0)
                
                
            if edu2 != 'NA':
                if univ2 == 'NA':
                    uniHeight = 0.5;
                else:
                    uniHeight = 0;
                pdf.drawCentredString((12.5/2)*cm,(15.54+homeHeight+uniHeight)*cm,edu2);
               
                # pdf.setFillColorRGB(0,1,1)
                # pdf.drawCentredString(6.25*cm,(14.9)*cm,'_______________________________')
                # pdf.setFillColorRGB(0,0,0) 
            # if edu3 != 'NA':
            
                # pdf.setFont('VeraBd', 8);
                # pdf.drawCentredString((12.5/2)*cm,(16.4)*cm,edu3); 
            # if univ3 != 'NA':
                # pdf.drawCentredString((12.5/2)*cm,(16)*cm,univ3.title());
           
         ############################# About Family ################################
        
        if edu1 == 'NA' and edu2 == 'NA' and univ1 == 'NA' and univ2 == 'NA':
            qualiHeight = 2.5
        else:
            qualiHeight = 0
        
        if spouse_name == 'NA' :
            spouseHeight= 8+qualiHeight;
        elif edu1 == 'NA' and edu2 == 'NA' and univ1 == 'NA' and univ2 == 'NA' and spouse_name != 'NA':
            spouseHeight= qualiHeight;
        else:
            spouseHeight= 0;
        
        if vehicle1 == 'NA' and vehicle2 == 'NA' and vehicle3 == 'NA' :
            vehicleHeight=2
        else:
            vehicleHeight = 0
        
      #############################SPOUSE SPACING##########################
      
        if spUni1 =="NA" and spedu1 =="NA":
            spEduHt=0.55
        else:
            spEduHt=0
        if Dep_Designation =="NA" and Dep_Employment =="NA":
            spWorkHt=1.25
        # elif Dep_Designation =="NA" and Dep_Employment !="NA":
            # spWorkHt=1.25
        else:
            spWorkHt=0
        if Dep_Salary == 'NA':
            depSalHt=1.2
        else:
            depSalHt=0
        if Dep_Media == 'NA':
            depFbHt=0.6
        else:
            depFbHt=0

        if Dep_Media2 == 'NA':
            depLinkHt=0.2
        else:
            depLinkHt=0
        
      #######################################################
        
        if spouse_name != 'NA' :
            if relationStatus != 'NA' : 
                pdf.setFillColorRGB(1,0,0.2)
                pdf.setFont('Vera', 12);
                pdf.drawString(7*cm,(14.7+qualiHeight)*cm,'['+relationStatus+']');
                pdf.setFillColorRGB(0,0,00)
            pdf.drawImage('/home/pdfImages/family.png',0.75*cm,(14.5+qualiHeight)*cm,9.5*cm,0.65*cm,preserveAspectRatio=False, mask='auto');
             # pdf.drawImage('/home/pdfImages/Male.png',11.7*cm,18.7*cm,1.75*cm,1.75*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/spouse.png',1.5*cm,(12.6)*cm,3.25*cm,0.25*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/business.png',1.5*cm,(13.25+qualiHeight)*cm,0.5*cm,1*cm,preserveAspectRatio=False, mask='auto');
         
            pdf.setFont('VeraBd', 12);
            if Spouse_Age == 'NA':
                pdf.drawString(2.3*cm,(13.55+qualiHeight)*cm,spouse_name);
            else:
                pdf.drawString(2.3*cm,(13.8+qualiHeight)*cm,spouse_name);
            
            if Spouse_Age != 'NA':
                pdf.setFont('Vera', 9);
                pdf.drawString(2.3*cm,(13.3+qualiHeight)*cm,Spouse_Age);
            
            # if spUni1 == 'NA' and spedu1 == 'NA':
                # homeHeight = homeHeight+1
            
            if spUni1 !="NA":
                pdf.drawImage('/home/pdfImages/edu.png',1.25*cm,(12.3+qualiHeight)*cm,0.9*cm,0.7*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFillColorRGB(0.5,0.2,0.1)
                if spedu1 != 'NA':
                    spUni1=spUni1+','
                    pdf.drawString(2.3*cm,(12.75+qualiHeight)*cm,spUni1.upper());
                else:
                    pdf.drawString(2.3*cm,(12.55+qualiHeight)*cm,spUni1.upper());
                pdf.setFillColorRGB(0,0,0)
            if spedu1 !="NA":
                pdf.drawImage('/home/pdfImages/edu.png',1.25*cm,(12.3+qualiHeight)*cm,0.9*cm,0.7*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(2.3*cm,(12.35+qualiHeight)*cm,spedu1);
           
            
            if Dep_Designation != 'NA':
                pdf.drawImage('/home/pdfImages/work.png',1.5*cm,(11.3+qualiHeight+spEduHt)*cm,0.6*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFont('Vera', 10);
                pdf.setFillColorRGB(0,0.5,0.5)
                
                if Dep_Employment != 'NA':
                    pdf.drawString(2.3*cm,(11.7+qualiHeight+spEduHt)*cm,Dep_Designation+',');
                else:
                    pdf.drawString(2.3*cm,(11.5+qualiHeight+spEduHt)*cm,Dep_Designation);
                
                
                if Dep_Salary != 'NA':
                    pdf.setFont('VeraBd', 8);
                    pdf.drawCentredString((12.5/2)*cm,(10.8+qualiHeight+spEduHt)*cm,"ESTIMATED YEARLY SALARY");
                    pdf.drawImage('/home/pdfImages/design1/salary.png', 4.2*cm, (9.8+qualiHeight+spEduHt)*cm, width=4.2*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBd', 8);
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawCentredString((12.5/2)*cm,(10.1+qualiHeight+spEduHt)*cm,Dep_Salary);
             
             
            if Dep_Employment != 'NA':
                pdf.drawImage('/home/pdfImages/work.png',1.5*cm,(11.3+qualiHeight+spEduHt)*cm,0.6*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFont('Vera', 8);
                pdf.setFillColorRGB(0,0,0)
                if Dep_Designation == 'NA':
                    # depWorkHt=0.35
                    depWorkHt=0
                else:
                    depWorkHt=0
                pdf.drawString(2.3*cm,(11.3+depWorkHt+qualiHeight+spEduHt)*cm,Dep_Employment.upper());
            
            pdf.setFillColorRGB(0,0,0)
               
            if Dep_Media =='NA':
                Dep_Media = Dep_instagram
                fbSmall = '/home/pdfImages/insta.png'
            else:
                Dep_Media = Dep_Media
                fbSmall = '/home/pdfImages/fb_blue.png'
            
            # print('Dep_Media',Dep_Media)
            if Dep_Media !='NA':
                pdf.drawImage(fbSmall,1.5*cm,(9.2+qualiHeight+spEduHt+spWorkHt+depSalHt)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                fb_url_right = []
                raw_addr = Dep_Media
                # print('fbRaw',raw_addr[0:64])
                addr = raw_addr[0:64]+'<br/>'+raw_addr[64:]
                addr = '<link href="' + raw_addr + '">' + addr+ '</link>'
                fb_url_right.append(Paragraph(addr,styleN))
                f = Frame(2*cm, (7.4+qualiHeight+spEduHt+spWorkHt+depSalHt)*cm, 8.5*cm, 2.5*cm, showBoundary=0)
                f.addFromList(fb_url_right,pdf)
                
            if Dep_Media2 =='NA':
                Dep_Media2=Dep_twitter
                linkedSmall = '/home/pdfImages/twitter.png'
            else:
                Dep_Media2=Dep_Media2
                linkedSmall = '/home/pdfImages/linkedin_blue.png'
                
            if Dep_Media2 != 'NA':
                pdf.drawImage(linkedSmall,1.5*cm,(8.35+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                ld_url_right = []
                raw_addr2 = Dep_Media2
                addr2 = raw_addr2[0:64]+'<br/>'+raw_addr2[64:]
                addr2 = '<link href="' + raw_addr2 + '">' + addr2 + '</link>'
                ld_url_right.append(Paragraph(addr2,styleN))
                
                f = Frame(2*cm, (6.6+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt)*cm, 8.05*cm, 2.5*cm, showBoundary=0)
                f.addFromList(ld_url_right,pdf)
            
            # if spBank1 != 'NA' and spouseBankruptDate != 'NA':
            if spBank1 != 'NA' :
                
                pdf.setFont('Vera', 12);
                pdf.drawImage('/home/pdfImages/leftBullet.png',1.5*cm,(7.6+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(2.5*cm,(7.6+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'POSSIBLE BANKRUPTCIES');
                pdf.setFont('Vera', 9);      
                # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year    Filing Status');
                pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year');
                
                pdf.drawImage('/home/pdfImages/arrow_blue.png',1.75*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(2.25*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1)
                
                # if spBankDet1 != 'NA':
                    # pdf.drawString(3.35*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBankDet1)
   
        
        
        # print('qualiHeight',qualiHeight)
        # print('spEduHt',spEduHt)
        # print('spWorkHt',spWorkHt)
        # print('depSalHt',depSalHt)
        # print('depFbHt',depFbHt)
        # print('depLinkHt',depLinkHt)
         ############################# About Family ################################
         
         
        ###########################VEHICLES DETAILS#################################
        if spBank1 == 'NA' and spBankDet1 == 'NA':
            spBankHt = 1.5
        else: 
            spBankHt = 0
        spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
        # spouseSpacing = 0;
        
        if vehicle1 !='NA' or vehicle2 !='NA' or vehicle2 !='NA':
            pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
            # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
            pdf.setFont('VeraBd', 12);
            pdf.drawCentredString(4*cm,(5.6+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
            pdf.setFont('Vera', 10);
        if vehicle1 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(4.9+spouseHeight+spBankHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2*cm,(4.9+spouseHeight+spBankHt)*cm,vehicle1);
        if vehicle2 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(4.2+spouseHeight+spBankHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2*cm,(4.2+spouseHeight+spBankHt)*cm,vehicle2);
        
        if vehicle3 !='NA':
            pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(3.5+spouseHeight+spBankHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(2*cm,(3.45+spouseHeight+spBankHt)*cm,vehicle3);
        
        
        if selectedCity == city:
            cityData = city+', '+state.title()
        elif selectedCity == city2:
            cityData = city2+', '+state2.title()
        elif selectedCity == city2:
            cityData = city3+', '+state3.title()
        elif selectedCity == 'NA':
            cityData = city+', '+state.title()
        else:
            cityData = city+', '+state.title()
        # print('Input_Pop',Input_Pop) 
        # vehicleHeight = 0
        if Input_Pop != 'NA' or Median_HouseHold_Val != 'NA' or medianHouseValue !='NA':
            pdf.setFont('Vera', 12);
            pdf.roundRect(1*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
        if Input_Pop != 'NA':
            # pdf.line(1.3*cm,(2.9)*cm,11.2*cm,(2.9)*cm)
            
            pdf.setFont('VeraBd', 10);
            # pdf.drawCentredString((12.5/2)*cm,28.2*cm,FullName.upper());
            pdf.drawCentredString((13.5/2)*cm,(2.4+spouseHeight+vehicleHeight+spBankHt)*cm,"City:  "+cityData);
            pdf.drawImage('/home/pdfImages/dot.png',2.25*cm,(1.75+spouseHeight+vehicleHeight+spBankHt)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFont('Vera', 8);
            pdf.drawString((1.5)*cm,(1.2+spouseHeight+vehicleHeight+spBankHt)*cm,"POPULATION");
            pdf.setFont('Vera', 8);
            pdf.drawCentredString((4.7/2)*cm,(0.8+spouseHeight+vehicleHeight+spBankHt)*cm,Input_Pop);

            pdf.setLineWidth(0.5);
            
        if Median_HouseHold_Val != 'NA':
            pdf.drawImage('/home/pdfImages/dot.png',6*cm,(1.75+spouseHeight+vehicleHeight+spBankHt)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(3.7*cm,(1.2+spouseHeight+vehicleHeight+spBankHt)*cm,"MEDIAN HOUSEHOLD INCOME");
            pdf.setFont('Vera', 8);
            pdf.drawCentredString(6*cm,(0.8+spouseHeight+vehicleHeight+spBankHt)*cm,Median_HouseHold_Val);
            
        if medianHouseValue != 'NA':
            pdf.drawImage('/home/pdfImages/dot.png',10*cm,(1.75+spouseHeight+vehicleHeight+spBankHt)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(8.5*cm,(1.2+spouseHeight+vehicleHeight+spBankHt)*cm,"MEDIAN HOME VALUE");
            pdf.setFont('Vera', 8);
            pdf.drawCentredString(10.2*cm,(0.8+spouseHeight+vehicleHeight+spBankHt)*cm,medianHouseValue);
            
    
        ################################ Right_Template_Contents ##################################################
        pdf.setFont('Vera', 9);
        
        
        if Per_facebook == 'NA':
            Per_facebook=Per_instagram
            facebookLogo='/home/pdfImages/insta.png'
        else:
            Per_facebook=Per_facebook
            facebookLogo='/home/pdfImages/Facebook.png'
            
        if Per_LinkedIn == 'NA':
            Per_LinkedIn=Per_twitter
            linkedinLogo='/home/pdfImages/twitter.png'
        else:
            Per_LinkedIn=Per_LinkedIn
            linkedinLogo='/home/pdfImages/Linkedin.png'
        
        
        
        if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA':
            
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            fb_url = []
            raw_addr = Per_facebook
            address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
            address = '<link href="' + raw_addr + '">' + address + '</link>'
            fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
            
            f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(fb_url,pdf)
            
            pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            ld_url = []
            # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
            raw_addr2 = Per_LinkedIn
            address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
            address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
            ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
           
            f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(ld_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            gmail_url = []
            #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
            raw_addr3 = per_Email
            address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
            address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
            gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

            f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(gmail_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            pdf.setFillColorRGB(255,255,255)
            pdf.drawString(14.75*cm,13*cm,Per_Tel)
    
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA': 
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            
            if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA':
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                 
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA':
                
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

            elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA':
                
                # pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)


                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr3 = per_Email
                address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[33:64]+'<br/>'+raw_addr3[65:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA':
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:32]+'<br/>'+raw_addr[33:64]+'<br/>'+raw_addr[65:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                
                f = Frame(14.5*cm, 15.4*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                                      
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[32:64]+'<br/>'+raw_addr2[65:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 15.4*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
              
            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage(facebookLogo,13.5*cm,14.5*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage(linkedinLogo,13.5*cm,13*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:64]+'<br/>'+raw_addr[64:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 14*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                ld_url = []
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 12.5*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[56:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[32:64]+'<br/>'+raw_addr2[64:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA':
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[26:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
              
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                               
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address2 = raw_addr[0:28]+'<br/>'+raw_addr[28:58]+'<br/>'+raw_addr[58:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                              
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
               
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA':
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[56:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = per_Email
                address2 = raw_addr2[0:32]+'<br/>'+raw_addr2[32:64]+'<br/>'+raw_addr2[64:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA':
            
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address2 = raw_addr[0:28]+'<br/>'+raw_addr[28:58]+'<br/>'+raw_addr[58:]
                address2 = '<link href="' + raw_addr + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                #raw_addr3 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr3 = per_Email
                address3 = raw_addr3[0:32]+'<br/>'+raw_addr3[32:64]+'<br/>'+raw_addr3[64:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
             
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA':
             
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[56:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)

                pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.75*cm,14.2*cm,Per_Tel)
        # pdf.drawString(13.7*cm,(12.2+contactHeight)*cm,'________________________________________________') 
        
        contactHeight+=2.65 # comment it when hobbies are needed in the report
           
         ################### Removed as per client requirement dated on 24-01-2020 ########################
         ################### Hobbies ########################
        # if hobby1 != 'NA' and hobby2 !='NA':
            # pdf.setFillColorRGB(255,255,255)
            # pdf.setFont('Vera', 8);
            # pdf.drawString(13.7*cm,(12.2+contactHeight)*cm,'________________________________________________')
            #pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(11.55+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(11.35+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.setFont('Vera', 12);
            # pdf.drawCentredString(15.55*cm,(11.36+contactHeight)*cm,'HOBBIES');
            # pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10.6+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
            # pdf.setFont('Vera', 8);
            # pdf.drawString(14.6*cm,(10.65+contactHeight)*cm,hobby1)
            # pdf.drawString(14.6*cm,(10.05+contactHeight)*cm,hobby2)
            # pdf.drawString(13.7*cm,(9.7+contactHeight)*cm,'________________________________________________')
        # elif hobby1 != 'NA' and hobby2 =='NA':
            # pdf.setFillColorRGB(255,255,255)
            # pdf.setFont('Vera', 8);
            # pdf.drawString(13.7*cm,(12.2+contactHeight)*cm,'________________________________________________')
            # pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(11.35+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.setFont('Vera', 12);
            # pdf.drawCentredString(15.55*cm,(11.36+contactHeight)*cm,'HOBBIES');
            # pdf.drawImage('/home/pdfImages/Bullet_2.png',14*cm,(10.6+contactHeight)*cm,0.4*cm,0.3*cm,preserveAspectRatio=False, mask='auto');
           
            # pdf.setFont('Vera', 8);
            # pdf.drawString(14.6*cm,(10.65+contactHeight)*cm,hobby1)
            
            # pdf.drawString(13.7*cm,(9.7+contactHeight)*cm,'________________________________________________')
       
       
        ################### Criminal History,Bankruptcies,Evictions ##########################
        
        
        if corDate1 != 'NA' and corDate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(9.1+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawString(14.5*cm,(8.95+contactHeight)*cm,'CRIMINAL HISTORY');#Removed as per clients requirement dated on 24012020
            pdf.drawString(14.5*cm,(9.15+contactHeight)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45+contactHeight)*cm,'CORPORATE FILINGS ');
            if corDate1 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(8.4+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(8.44+contactHeight)*cm,corDate1)
                # print('len:',len(CHOdate1))
                pdf.drawString(16.2*cm,(8.44+contactHeight)*cm,corpFile1)
            if corDate2 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.88+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(7.88+contactHeight)*cm,corDate2)
                pdf.drawString(16.2*cm,(7.88+contactHeight)*cm,corpFile2)
        
            # extraHeight=2
        
        elif corDate1 != 'NA' and corDate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(9.1+contactHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            
            # pdf.drawString(14.5*cm,(8.95+contactHeight)*cm,'CRIMINAL HISTORY');
            pdf.drawString(14.5*cm,(9.15+contactHeight)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45+contactHeight)*cm,'CORPORATE FILINGS');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(8.4+contactHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(8.44+contactHeight)*cm,corDate1)
            pdf.drawString(16.2*cm,(8.44+contactHeight)*cm,corpFile1)
        
        
        if BRFdate1 != 'NA' and BRFdate2 != 'NA':
            # contactHeight=contactHeight+0.85
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(7.15+contactHeight+crimeHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(7.2+contactHeight+crimeHeight)*cm,'POSSIBLE BANKRUPTCIES');
            pdf.setFont('Vera', 9);      
            # pdf.drawString(14.25*cm,(5+contactHeight+crimeHeight)*cm,'Filing Date   Filing Status');
            pdf.drawString(14.25*cm,(6.6+contactHeight+crimeHeight)*cm,'Year');
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(6+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(6+contactHeight+crimeHeight)*cm,BRFdate1)
            # if BROdate1 != 'NA':
                # pdf.drawString(15.3*cm,(6+contactHeight+crimeHeight)*cm,BROdate1)
            
            if BRFdate2 != 'NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(5.4+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(5.4+contactHeight+crimeHeight)*cm,BRFdate2)
            # if BROdate2 != 'NA':
                # pdf.drawString(15.3*cm,(5.4+contactHeight+crimeHeight)*cm,BROdate2)
        elif BRFdate1 != 'NA' and BRFdate2 == 'NA':
            # print('BRFdate2',BRFdate2)
            contactHeight=contactHeight+0.85
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(6.15+contactHeight+crimeHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(6.2+contactHeight+crimeHeight)*cm,'POSSIBLE BANKRUPTCIES');
            pdf.setFont('Vera', 9);      
            # pdf.drawString(14.25*cm,(5+contactHeight+crimeHeight)*cm,'Filing Date   Filing Status');
            pdf.drawString(14.25*cm,(5.6+contactHeight+crimeHeight)*cm,'Year');
            
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(5+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(5+contactHeight+crimeHeight)*cm,BRFdate1)
            # if BROdate1 != 'NA':
                # pdf.drawString(15.3*cm,(5+contactHeight+crimeHeight)*cm,BROdate1)
            
            # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(4.4+contactHeight+crimeHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawString(14.25*cm,(4.4+contactHeight+crimeHeight)*cm,BRFdate2)
        bankHeight=bankHeight+1;    
        if EVFdate1 != 'NA' and EVFdate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(3.5+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(3.55+contactHeight+crimeHeight+bankHeight)*cm,'EVICTIONS');
            pdf.setFont('Vera', 9);
            pdf.drawString(14.25*cm,(2.95+contactHeight+crimeHeight+bankHeight)*cm,'Filing Date   Filing Type');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(2.45+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(2.45+contactHeight+crimeHeight+bankHeight)*cm,EVFdate1)
            
            if EVOdate1 !='NA':
                pdf.drawString(16.4*cm,(2.45+contactHeight+crimeHeight+bankHeight)*cm,EVOdate1)
            
            if EVFdate2 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(1.85+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(1.85+contactHeight+crimeHeight+bankHeight)*cm,EVFdate2)
            if EVOdate2 !='NA':
                pdf.drawString(16.2*cm,(1.85+contactHeight+crimeHeight+bankHeight)*cm,EVOdate2)
            
        elif EVFdate1 != 'NA' and EVFdate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(3.5+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawCentredString(15.65*cm,(3.5+contactHeight+crimeHeight+bankHeight)*cm,'EVICTIONS');
            pdf.setFont('Vera', 9);
            pdf.drawCentredString(16.1*cm,(2.95+contactHeight+crimeHeight+bankHeight)*cm,'Filing Date     Filing Type');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(2.45+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            
            pdf.drawString(14.25*cm,(2.45+contactHeight+crimeHeight+bankHeight)*cm,EVFdate1)
            if EVOdate1 !='NA':
                pdf.drawString(16.2*cm,(2.45+contactHeight+crimeHeight+bankHeight)*cm,EVOdate1)
        pdf.setFont('Vera', 12);    
        
        
        #####JUDGEMENTS###########
        if judments !='NA':
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(1+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(1+contactHeight+crimeHeight+bankHeight)*cm,'POSSIBLE JUDGMENTS');
            pdf.setFont('Vera', 8);
            # pdf.drawString(14.5*cm,(0.65+contactHeight+crimeHeight+bankHeight)*cm,'(OVER $1,000 in past 15 Years)');
            pdf.setFont('Vera', 11);
           
            if judments == 'Yes' or judments == 'yes':
                pdf.drawImage('/home/pdfImages/yes.png',14*cm,(0.005+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.6*cm,preserveAspectRatio=False, mask='auto');
            else:
                pdf.drawImage('/home/pdfImages/no.png',14*cm,(0.005+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.6*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/yes.png',14.75*cm,(-0.40+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False);
            pdf.drawString(14.75*cm,(0.1+contactHeight+crimeHeight+bankHeight)*cm,judments)
            # pdf.drawString(16.2*cm,(1.95+contactHeight+crimeHeight+bankHeight)*cm,EVOdate1)
         
            # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(-0.80+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawString(14.25*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,EVFdate2)
            # pdf.drawString(16.2*cm,(1.35+contactHeight+crimeHeight+bankHeight)*cm,EVOdate2)
            
        if len(licences) == 0:
            licenLen=2
        else:
            licenLen=0
        bankHeight=bankHeight-0.35
        if len(licences) != 0:
            pdf.drawImage('/home/pdfImages/design1/bullet.png',13.65*cm,(-0.55+contactHeight+crimeHeight+bankHeight)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(-0.5+contactHeight+crimeHeight+bankHeight)*cm,'LICENSES');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(-0.9+contactHeight+crimeHeight+bankHeight)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            if licence1 !='NA':
                pdf.drawString(14.25*cm,(-0.9+contactHeight+crimeHeight+bankHeight)*cm,licence1)
            if licence2 !='NA':
                pdf.drawString(14.25*cm,(-1.35+contactHeight+crimeHeight+bankHeight)*cm,licence2)
            if licence3 !='NA':
                pdf.drawString(14.25*cm,(-1.75+contactHeight+crimeHeight+bankHeight)*cm,licence3)
        # print('len(licences)',len(licences))
        
        if len(licences) == 0:
            licenHt=1.5
        else:
            licenHt=0
        if profLicence != 'NA':
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(-2.+contactHeight+crimeHeight+bankHeight+licenLen)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.25*cm,(-2.25+contactHeight+crimeHeight+bankHeight+licenHt)*cm,"Professional Licence:")
            profLic = []
            pdf.setFillColorRGB(0,0,0)
            raw_addr = profLicence.title()
            address = raw_addr[0:35]+'<br/>'+raw_addr[35:60]+'<br/>'+raw_addr[60:]
            # address = '<link href="' + raw_addr + '">' + address + '</link>'
            profLic.append(Paragraph('<font color="white">'+address+'</font>',styleN))
            
            f = Frame(14.1*cm, (-3.9+contactHeight+crimeHeight+bankHeight+licenHt)*cm, 12*cm, 1.8*cm, showBoundary=0)
            f.addFromList(profLic,pdf)
            pdf.setFillColorRGB(0,0,0)
            
            # pdf.drawString(14.25*cm,(-1.55+contactHeight+crimeHeight+bankHeight)*cm,'Professional Licences: '+profLicence)
            
            # raw_addr = licence_det
            # licence_det = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[56:]
            # pdf.drawString(14.25*cm,(-1.85+contactHeight+crimeHeight+bankHeight)*cm,licence_det)
           
        pdf.showPage()
        pdf.save()

        pdf = buffer.getvalue()
        # store = FileResponse(buffer, as_attachment=True, filename=FullName+'.pdf')
        # print('store',store);
        buffer.close()
        response.write(pdf)
        
        FNMAE = FullName+'.pdf'
        # print('fs',FNMAE)
        if fs.exists(FNMAE):
            with fs.open(FNMAE) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename=FNMAE'
                # return "HELLO"
                return response
        else:
            return HttpResponseNotFound('The requested pdf was not found in our server.')
            
def sendMail(request,userId=None):
        userId = request.GET["userId"]
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT CONCAT(First_Name,' ',Last_Name) as FullName,noData from usData where  usData.id='{}'".format(userId))
            myresult = cursor.fetchall()
            for x in myresult:
                var = myresult[0]
                print('Result',x[0])
                
                FNMAE = x[0]+'.pdf'
                noData = x[1]
                if noData == 1:
                
                    s = smtplib.SMTP('gateway.greettech.com')
                    s.set_debuglevel(1)
                    msg = MIMEText("""No Data found for the Lead Name: """+x[0])
                    sender = 'bss@greettech.com'
                    # recipients = 'ravikiran@greettech.com,ravikiran6763@gmail.com'
                    recipients = 'jmaddux@franchampion.com,kumar@greettech.com,rkburnett@hotmail.com,atlq1@greettech.com,reena@greettech.com,sendil@greettech.com,at@greettech.com'
                    msg['Subject'] = "No Data Found"
                    msg['From'] = sender
                    msg['To'] = recipients
                    s.sendmail(sender, recipients.split(','), msg.as_string())
                    
                    template = loader.get_template('noData.html') # getting our template  
                    return HttpResponse(template.render())       # rendering the template in HttpResponse 
                    return render(request,'noData.html')
                else:
                    fs = FileSystemStorage()
                    print('fs',FNMAE)
                    if fs.exists(FNMAE):
                        with fs.open(FNMAE) as pdf:
                            response = HttpResponse(pdf, content_type='application/pdf')
                            response['Content-Disposition'] = 'filename=FNMAE'
                            
                            ##############################################################
                            html = """
                            
                            <br>
                            Please find the attached file for 
                            """+x[0]

                            # Creating message.
                            msg = MIMEMultipart('alternative')
                            msg['Subject'] = x[0]
                            # msg['From'] = "testmail@greettech.com"
                            msg['From'] = "bss@greettech.com"
                            # sender = "bss@greettech.com"
                            
                                                        
                            # msg['To'] = "ravikiran@greettech.com"
                            # msg["Cc"] = "kumar@greettech.com,pratish@greettech.com"
                             
                            msg['To'] = "rburnett@franchampion.com"
                            msg["Cc"] = "jmaddux@franchampion.com,kumar@greettech.com,rkburnett@hotmail.com,atlq1@greettech.com,reena@greettech.com,sendil@greettech.com,at@greettech.com"
                           
                                                        
                            # The MIME types for text/html
                            HTML_Contents = MIMEText(html, 'html')
                    
                            # Adding pptx file attachment
                            filename=FNMAE
                            fo=open(filename,'rb')
                            attach = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
                            # print('attach',attach)
                            
                            fo.close()
                            attach.add_header('Content-Disposition','attachment',filename=filename)

                            # Attachment and HTML to body message.
                            msg.attach(attach)
                            msg.attach(HTML_Contents)


                            # Your SMTP server information
                            s_information = smtplib.SMTP()
                            #You can also use SSL
                            # smtplib.SMTP_SSL([host[, port[, local_hostname[, keyfile[, certfile[, timeout]]]]]])
                            
                            s_information.connect('gateway.greettech.com')
                            
                            # s_information.connect('greettech.mail.pairserver.com','465')
                            # s_information.login('testmail@greettech.com','Sodo09090')
                            
                            # s_information.sendmail(msg['From'], msg['To'], msg.as_string())
                            
                            s_information.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
                            
                            # s_information.sendmail(sender, recipients, msg.as_string())
                            s_information.quit()
                            ##############################################################
                            
                            os.remove(FNMAE)
                            print("File Removed!")                        
                            return response
                    else:
                        # return HttpResponseNotFound('The requested pdf was not found in our server.')
                        template = loader.get_template('homePage.html') # getting our template  
                        return HttpResponse(template.render())       # rendering the template in HttpResponse 
                        return render(request,'homePage.html')

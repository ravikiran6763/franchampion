 
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

from datetime import date
import datetime
from reportlab.lib.styles import ParagraphStyle

from base64 import b64decode
import base64
from PIL import Image
from io import BytesIO

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

today = date.today()
mon = str(today.month)
day = str(today.day)
year = str(today.year)
d2 = mon+'/'+day+'/'+year[-2:]
# disclaimer = ""
# print(disclaimer)

import base64
import re

from PIL import Image
import cv2
# Take in base64 string and return cv image
def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

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
           
            city            =x[46]
                
            state            =x[47]
                
            cityState=x[46]+', '+x[47]
            
            university            =x[48]
            if university:
                univ=university.split(';')
            else:
                univ=''
             
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
            editCompleted =x[91]
            webSite =x[92]
            if not webSite:
                webSite ='NA'
            degreeType =x[93]
            estSavings =x[94]
            if not estSavings:
                estSavings ='NA'
            ####image data
            
            imageId            =x[95]
            person_image            =x[96]
            home_image            =x[97]
            name            =x[98]
            dateAndTime            =x[99]
            personImageFlag            =x[100]
            homeImageFlag            =x[101]
            # print(person_image)
           
            profileString = person_image.decode()
            if personImageFlag == 2:
                img = imread(io.BytesIO(base64.b64decode(profileString)))
                 # show image
                plt.figure()
                plt.imshow(img, cmap="gray")
                
                cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite("profileImage.jpg", cv2_img)
                plt.show()
            else:
                profileString = profileString[22:]

                # print(profileString)

                im = Image.open(BytesIO(base64.b64decode(profileString)))
                im.save('profileImage.jpg', 'PNG')
           
            houseString = home_image.decode()
            if homeImageFlag == 2:
                # reconstruct image as an numpy array
                img1 = imread(io.BytesIO(base64.b64decode(houseString)))

                # show image
                plt.figure()
                plt.imshow(img1, cmap="gray")
                
                cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
                cv2.imwrite("houseImage.jpg", cv2_img1)
                plt.show()
            else:
                houseString = houseString[22:]
                
                im1 = Image.open(BytesIO(base64.b64decode(houseString)))
                im1.save('houseImage.jpg', 'PNG')
                
        
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
         
         
         
         #######################################Tepmlate1#######################################
        
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
        
        # print('personImageFlag',personImageFlag)
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
            
        
        if JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA': 
            # nameHeight=2
            nameHeight=0
            # pdf.line(lineMargin1*cm,(27.4)*cm,lineMargin2*cm,(27.4)*cm)
        else:
            nameHeight=0
        
        
        pdf.drawCentredString((noImageMargin/2)*cm,(28.8-nameHeight)*cm,FullName.upper());
        # pdf.setDash([2,2,2,2],0)
        pdf.line(lineMargin1*cm,(28.6-nameHeight)*cm,lineMargin2*cm,(28.6-nameHeight)*cm)
        # pdf.setDash([0,0,0,0],0)
        pdf.setFont('Vera', 14);


        if len(Job_Desc) >=90:
                jobFont=9
        else:
                jobFont=14
                
        ##################################JOBS DISPLAY #############################   
       
        
        if JOB2 =='NA' and comp2 != 'NA':
            job2Height=0.5
        else:
            job2Height=0
            jobsHeight=0
        
        
        
        ##################################JOBS DISPLAY #############################            
          
        if personImageFlag == 2:
            # print('skipp')
            
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
        
        
        if personImageFlag == 2:
            shiftSaving = 4
        else:
            shiftSaving = 0
        if Addr == 1:
            print('homeValu1',homeValu1)
            print('homeEqu1',homeEqu1)
            if homeValu1 == '$0' and homeEqu1 == '$0': 
                if estSavings !='NA':
                    pdf.drawImage('/home/pdfImages/personHome.png',(4.5)*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                    pdf.setFillColorRGB(0,0,0)
                    pdf.drawImage('/home/pdfImages/savingsIcon.png', (0.25+shiftSaving)*cm, 27.6*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingRight.png', (1.25+shiftSaving)*cm, 27.7*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingsLeft.png',(9+shiftSaving)*cm, 27.7*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBI', 11);
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString((1.5+shiftSaving)*cm,27.9*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawString((9.5+shiftSaving)*cm,27.9*cm,estSavings);
                    pdf.setFillColorRGB(0,0,0)
                    
                    pdf.drawImage('/home/pdfImages/personHome.png',4.5*cm,(26.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(19.75)*cm,10.5*cm,7*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(19.7)*cm,10.5*cm,7*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (19.75)*cm, 10.5*cm, 7*cm, 4, stroke=1, fill=0);
                else:
                    pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(26.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',2*cm,(19.75)*cm,10.5*cm,7*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(19.7)*cm,10.5*cm,7*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (19.75)*cm, 10.5*cm, 7*cm, 4, stroke=1, fill=0);
               
                pdf.setFont('VeraBd', 9);
                
                pdf.drawCentredString(6.5*cm,(18.25)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',5.25*cm,(18.8)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',5.25*cm,(18.8)*cm,2.75*cm,0.8*cm,preserveAspectRatio=False);
                
            else:
            
                if estSavings !='NA':
                    pdf.drawImage('/home/pdfImages/personHome.png',(4.5)*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                    pdf.setFillColorRGB(0,0,0)
                    pdf.drawImage('/home/pdfImages/savingsIcon.png', (0.25+shiftSaving)*cm, 27.6*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingRight.png', (1.25+shiftSaving)*cm, 27.7*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingsLeft.png',(9+shiftSaving)*cm, 27.7*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBI', 11);
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString((1.5+shiftSaving)*cm,27.9*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawString((9.5+shiftSaving)*cm,27.9*cm,estSavings);
                    pdf.setFillColorRGB(0,0,0)
                    
                    pdf.drawImage('/home/pdfImages/personHome.png',4.5*cm,(26.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(21.75)*cm,10.5*cm,5*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(21.7)*cm,10.5*cm,5*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (21.75)*cm, 10.5*cm, 5*cm, 4, stroke=1, fill=0);
                else:
                    pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(27.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',2*cm,(21.75)*cm,7.5*cm,6*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(21.7)*cm,10.5*cm,6*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (21.75)*cm, 10.5*cm, 6*cm, 4, stroke=1, fill=0);
               
                pdf.setFont('VeraBd', 9);
                
                pdf.drawCentredString(6.5*cm,(20.25)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',5.25*cm,(20.8)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',5.25*cm,(20.8)*cm,2.75*cm,0.8*cm,preserveAspectRatio=False);
                
                
                if homeEqu1 == '$0':
                    shiftHomeVal=3.25
                    eqFontSize=12
                else:
                    shiftHomeVal=0
                    eqFontSize=8 
                    # pdf.drawImage('/home/pdfImages/dot.png',(1+shiftHomeVal)*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                if homeValu1 !='$0' and homeEqu1 == '$0':
                    pdf.setFont('VeraBd', eqFontSize);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2)*cm,"ESTIMATED HOME VALUE");
                    pdf.setFont('VeraBd', eqFontSize);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(18.6)*cm,homeValu1);

                    
                
                if homeEqu1 != '$0':
                    pdf.setFont('VeraBd', 8);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2)*cm,"ESTIMATED HOME VALUE");
                    pdf.setFont('VeraBd', 8);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(18.6)*cm,homeValu1);
                    pdf.setLineWidth(0.5);
                    pdf.line(6.25*cm,(19.5)*cm,6.25*cm,(18.65)*cm)
                    # pdf.drawImage('/home/pdfImages/dot.png',7.20*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(9.375*cm,(19.2)*cm,"ESTIMATED HOME EQUITY");
                    pdf.setFont('VeraBd', 8);
                    pdf.drawCentredString(9.375*cm,(18.65)*cm,homeEqu1);
            
        else:
            
            if spouse_name != 'NA':    
                if estSavings !='NA':
                    
                    pdf.drawImage('/home/pdfImages/personHome.png',4*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                    pdf.setFillColorRGB(0,0,0)
                    pdf.drawImage('/home/pdfImages/savingsIcon.png', (0.25+shiftSaving)*cm, 27.6*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingRight.png', (1.25+shiftSaving)*cm, 27.7*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingsLeft.png',(9+shiftSaving)*cm, 27.7*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBI', 11);
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString((1.5+shiftSaving)*cm,27.9*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawString((9.5+shiftSaving)*cm,27.9*cm,estSavings);
                    pdf.setFillColorRGB(0,0,0)
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',2*cm,(23.3)*cm,8*cm,3.6*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',2*cm,(23.3)*cm,8*cm,3.6*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(2*cm, (23.3)*cm, 8*cm, 3.6*cm, 4, stroke=1, fill=0);
                else:
                
                    pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(27.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',2*cm,(23.25)*cm,9*cm,4.5*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',2*cm,(23.25)*cm,9*cm,4.5*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(2*cm, (23.25)*cm, 9*cm, 4.5*cm, 4, stroke=1, fill=0);
               
                    pdf.setFont('VeraBd', 9);
                    
                    
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',1.5*cm,(22.5)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',1.5*cm,(22.5)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                    
                if Address != 'NA':
                    pdf.setFont('Vera', 8);
                    
                    pdf.drawString(1.5*cm,(22)*cm,"1.");
                    pdf.setFont('Vera', 8);
                    
                    pdf.drawString(2*cm,(22)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                    
                    if homeEqu1 != '$0':
                        
                        pdf.drawString(2*cm,(21.6)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(21.6)*cm,homeEqu1);
                        pdf.setFont('Vera', 8);
                    if homeEqu1 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    
                    if homeValu1 != '$0':
                        
                        pdf.drawString(2*cm,(21.2+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(21.2+homeHeight+Equiheight)*cm,homeValu1);
                        pdf.setFont('Vera', 8);
                    
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(21)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                
                if Address2 != 'NA':
                    pdf.setFont('Vera', 8);
                    
                    pdf.drawString(1.5*cm,(20.6)*cm,"2.");
                    pdf.setFont('Vera', 8);
                    
                    pdf.drawString(2*cm,(20.6)*cm,Address2+', '+city2+', '+state2.title()+' '+pincode2);
                    
                    if homeEqu2 != '$0':
                        
                        pdf.drawString(2*cm,(20.2)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(20.2)*cm,homeEqu2);
                        pdf.setFont('Vera', 8);
                    if homeEqu2 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu2 != '$0':
                        
                        pdf.drawString(2*cm,(19.8+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(19.8+homeHeight+Equiheight)*cm,homeValu2);
                        pdf.setFont('Vera', 8);
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(19.6)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                if Address3 != 'NA':
                        pdf.setFont('Vera', 8);
                        
                        pdf.drawString(1.5*cm,(19.2)*cm,"3.");
                        pdf.setFont('Vera', 8);
                        pdf.drawString(2*cm,(19.2)*cm,Address3+', '+city3+', '+state3.title()+' '+pincode3);
                        
                        if homeEqu3 != '$0':
                       
                            pdf.drawString(2*cm,(18.8)*cm,"ESTIMATED HOME EQUITY: ");
                            pdf.setFont('VeraBd', 8);
                            pdf.drawString(6*cm,(18.8)*cm,homeEqu3);
                            
                            pdf.setFont('Vera', 8);
                        if homeEqu3 == '$0':
                            Equiheight = 0.35;
                        else:
                            Equiheight = 0;
                        if homeValu3 != '$0':
                            
                            pdf.drawString(2*cm,(18.4+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                            pdf.setFont('VeraBd', 8);
                            pdf.drawString(6*cm,(18.4+homeHeight+Equiheight)*cm,homeValu3);
                            pdf.setFont('Vera', 8);
            else:
                print('spouse_name:::',spouse_name)
                if estSavings !='NA':
                
                    pdf.drawImage('/home/pdfImages/personHome.png',4.5*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                    pdf.setFillColorRGB(0,0,0)
                    pdf.drawImage('/home/pdfImages/savingsIcon.png', (0.25+shiftSaving)*cm, 27.6*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingRight.png', (1.25+shiftSaving)*cm, 27.7*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingsLeft.png',(9+shiftSaving)*cm, 27.7*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBI', 11);
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString((1.5+shiftSaving)*cm,27.9*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawString((9.5+shiftSaving)*cm,27.9*cm,estSavings);
                    pdf.setFillColorRGB(0,0,0)
                    
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(20.3)*cm,10.5*cm,6.6*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(20.3)*cm,10.5*cm,6.6*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (20.3)*cm, 10.5*cm, 6.6*cm, 4, stroke=1, fill=0);
                else:
                
                    pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(27.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(21.25)*cm,10.5*cm,6.5*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(21.25)*cm,10.5*cm,6.5*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (21.25)*cm, 10.5*cm, 6.5*cm, 4, stroke=1, fill=0);
               
                pdf.setFont('VeraBd', 9);
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',1.5*cm,(19.5)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',1.5*cm,(19.5)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                
                if Address != 'NA':
                        pdf.setFont('Vera', 9);
                        
                        pdf.drawString(1.5*cm,(19)*cm,"1.");
                        pdf.setFont('Vera', 9);
                        
                        pdf.drawString(2*cm,(19)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                        
                        if homeEqu1 != '$0':
                            
                            pdf.drawString(2*cm,(18.6)*cm,"ESTIMATED HOME EQUITY: ");
                            pdf.setFont('VeraBd', 9);
                            pdf.drawString(6.5*cm,(18.6)*cm,homeEqu1);
                            pdf.setFont('Vera', 9);
                        if homeEqu1 == '$0':
                            Equiheight = 0.35;
                        else:
                            Equiheight = 0;
                        
                        if homeValu1 != '$0':
                            
                            pdf.drawString(2*cm,(18.2+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE: ");
                            pdf.setFont('VeraBd', 9);
                            pdf.drawString(6.5*cm,(18.2+homeHeight+Equiheight)*cm,homeValu1);
                            pdf.setFont('Vera', 9);
                        
                        pdf.setFillColorRGB(0,0,1)
                        pdf.drawString(2.6*cm,(18)*cm,'_______________________________')
                        pdf.setFillColorRGB(0,0,0)
                
                if Address2 != 'NA':
                        pdf.setFont('Vera', 9);
                        
                        pdf.drawString(1.5*cm,(17.6)*cm,"2.");
                        pdf.setFont('Vera', 9);
                        
                        pdf.drawString(2*cm,(17.6)*cm,Address2+', '+city2+', '+state2.title()+' '+pincode2);
                        
                        if homeEqu2 != '$0':
                            
                            pdf.drawString(2*cm,(17.2)*cm,"ESTIMATED HOME EQUITY: ");
                            pdf.setFont('VeraBd', 9);
                            pdf.drawString(6.5*cm,(17.2)*cm,homeEqu2);
                            pdf.setFont('Vera', 9);
                        if homeEqu2 == '$0':
                            Equiheight = 0.35;
                        else:
                            Equiheight = 0;
                        if homeValu2 != '$0':
                            
                            pdf.drawString(2*cm,(16.8+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                            pdf.setFont('VeraBd', 9);
                            pdf.drawString(6.5*cm,(16.8+homeHeight+Equiheight)*cm,homeValu2);
                            pdf.setFont('Vera', 9);
                        pdf.setFillColorRGB(0,0,1)
                        pdf.drawString(2.6*cm,(16.6)*cm,'_______________________________')
                        pdf.setFillColorRGB(0,0,0)
                if Address3 != 'NA':
                    pdf.setFont('Vera', 9);
                    
                    pdf.drawString(1.5*cm,(16.2+homeHeight+Equiheight)*cm,"3.");
                    pdf.setFont('Vera', 9);
                    pdf.drawString(2*cm,(16.2+homeHeight+Equiheight)*cm,Address3+', '+city3+', '+state3.title()+' '+pincode3);
                    
                    if homeEqu3 != '$0':
                   
                        pdf.drawString(2*cm,(15.8)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(15.8)*cm,homeEqu3);
                        
                        pdf.setFont('Vera', 9);
                    if homeEqu3 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu3 != '$0':
                        
                        pdf.drawString(2*cm,(15.4+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(15.4+homeHeight+Equiheight)*cm,homeValu3);
                        pdf.setFont('Vera', 9);
       
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
            # vehicleHeight=2
            vehicleHeight=0
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
        
      ##################################################LEFT 2nd HALF ##############################################
        
        if spouse_name != 'NA' :
            if relationStatus != 'NA' : 
                pdf.setFillColorRGB(1,0,0.2)
                pdf.setFont('Vera', 12);
                pdf.drawString(7*cm,(14.7+qualiHeight)*cm,'['+relationStatus+']');
                pdf.setFillColorRGB(0,0,00)
            pdf.drawImage('/home/pdfImages/family.png',0.75*cm,(14.5+qualiHeight)*cm,9.5*cm,0.65*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/business.png',1.5*cm,(13.25+qualiHeight)*cm,0.5*cm,1*cm,preserveAspectRatio=False, mask='auto');
         
            pdf.setFont('VeraBd', 12);
            if Spouse_Age == 'NA':
                pdf.drawString(2.3*cm,(13.55+qualiHeight)*cm,spouse_name);
            else:
                pdf.drawString(2.3*cm,(13.8+qualiHeight)*cm,spouse_name);
            
            if Spouse_Age != 'NA':
                pdf.setFont('Vera', 9);
                pdf.drawString(2.3*cm,(13.3+qualiHeight)*cm,Spouse_Age);
            
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
                    if estSavings !='NA': 
                        pdf.drawImage('/home/pdfImages/salaryNew.png', 1.5*cm, (10.2+qualiHeight+spEduHt)*cm, width=9.8*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                        pdf.setFont('VeraBd', 11);
                        
                        pdf.drawString(2*cm,(10.4+qualiHeight+spEduHt)*cm,"ESTIMATED YEARLY SALARY:  ")
                        pdf.setFillColorRGB(255,0,0)
                        pdf.drawString(8.5*cm,(10.4+qualiHeight+spEduHt)*cm,Dep_Salary);
                    else:
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
            if spBank1 != 'NA' and spBank1 != 'None':
                    
                    pdf.setFont('Vera', 12);
                    pdf.drawImage('/home/pdfImages/spouseBank.png',1.5*cm,(7.35+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(2.2*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'POSSIBLE BANKRUPTCIES');
                    pdf.drawImage('/home/pdfImages/checked.png',8*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(8.9*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1);
                    # pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
                    
                    pdf.setFont('Vera', 9);      
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year    Filing Status');
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year');
                    
                    # pdf.drawImage('/home/pdfImages/arrow_blue.png',1.75*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    # pdf.drawString(2.25*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1)
                    
                    # if spBankDet1 != 'NA':
                        # pdf.drawString(3.35*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBankDet1)
       
   
        ############################# About Family ################################
         
         
        ###########################VEHICLES DETAILS#################################
            if spBank1 == 'NA' and spBankDet1 == 'NA':
                spBankHt = 1.5
            else: 
                spBankHt = 0.65
            spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
            # spouseSpacing = 0;
            
            if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
            else:
            
                if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
                pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
            
        else:
            if spBank1 == 'NA' and spBankDet1 == 'NA':
                spBankHt = 1.5
            else: 
                spBankHt = 0.65
            # spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
            spouseSpacing = 0;
            spouseHeight = 7;
            
            if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
            else:
            
                if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
                pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
            
        pdf.drawImage('/home/pdfImages/Disclaimer.png',0.06*cm,(0.05)*cm,21*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
    
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
        
        # webSite = "https://www.doctorquick.com/"
        # webSite = "NA"
        
        if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
            socialHght = 6
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 3.5
            
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
            
            
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        
        
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 1.25
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 1.25
        
            
        else:
            socialHght = 0
        
        
        rightSpacing = socialHght-1.2
        # print('rightSpacing',rightSpacing)
        pdf.setFillColorRGB(255,255,255)
        
        if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
            
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
            
            raw_addr2 = Per_LinkedIn
            address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
            address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
            ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
           
            f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(ld_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            gmail_url = []
            
            raw_addr3 = per_Email
            address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
            address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
            gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

            f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
            f.addFromList(gmail_url,pdf)
            
            
            
            pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.75*cm,13*cm,Per_Tel)
                            
            pdf.drawImage('/home/pdfImages/link.png',13.5*cm,11.45*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            website = []
            raw_addr4 = webSite
            address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
            address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
            website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
            
            f = Frame(14.5*cm, 10.8*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(website,pdf)
    
    
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA' or webSite != 'NA': 
            print('website')
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            
            if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                 
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
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

            elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
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
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:32]+'<br/>'+raw_addr[33:64]+'<br/>'+raw_addr[65:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                
                f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
                                      
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr2 = per_Email
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
              
            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
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

            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
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
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
                
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
               
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                
                f = Frame(14.5*cm, 14.3*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and webSite == 'NA':
            
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
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
             
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
             
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
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                
                
                
                pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
                    
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 12*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                print('Per_facebook',Per_facebook)
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                                    
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
                
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                                    
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
          
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.5*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
              

        
        # pdf.drawString(13.7*cm,(12.2)*cm,'________________________________________________') 
        
        contactHeight+=2.65 # comment it when hobbies are needed in the report
           
         ################### Removed as per client requirement dated on 24-01-2020 ########################
      
        ################### Criminal History,Bankruptcies,Evictions ##########################
        
        
        if corDate1 != 'NA' and corDate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');#Removed as per clients requirement dated on 24012020
            pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS ');
            if corDate1 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
                # print('len:',len(CHOdate1))
                pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
            if corDate2 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(10.78+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(10.78+rightSpacing)*cm,corDate2)
                pdf.drawString(15.5*cm,(10.78+rightSpacing)*cm,corpFile2)
        
            # extraHeight=2
        
        elif corDate1 != 'NA' and corDate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            
            # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');
            pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
            pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
        
        
        rightSpacing = 0
        if corDate1 == 'NA' and corDate2 == 'NA':
            corpHght = 2
        elif corDate1 != 'NA' and corDate2 == 'NA':
            corpHght = 0.6
            
        else:
            corpHght = 0.5
        
        rightSpacing = socialHght + corpHght-2
        
        pdf.setFillColorRGB(255,255,255)
        pdf.setFont('Vera', 11);
        pdf.drawString(13.75*cm,(10.5+rightSpacing)*cm,'____________________________________')
        
        pdf.drawString(13.8*cm,(9.7+rightSpacing)*cm,'POSSIBLE JUDGMENTS');
        if judments !='No':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            
        pdf.drawString(13.8*cm,(9+rightSpacing)*cm,'POSSIBLE EVICTIONS');
        if EVFdate1 != 'NA' or EVFdate2 != 'NA':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(19.8*cm,(9+rightSpacing)*cm,EVFdate1)
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
        
        if BRFdate1 != 'NA' and BRFdate1 != 'None' or BRFdate2 != 'NA':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(19.8*cm,(8.35+rightSpacing)*cm,BRFdate1)
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.drawString(13.75*cm,(8.1+rightSpacing)*cm,'____________________________________')        
        if len(licences) == 0:
            licenLen=2
        else:
            licenLen=0
        
        if len(licences) == 0 and profLicence != 'NA': 
            rightSpacing += 4.5
        else:
            rightSpacing += 3
            
        if len(licences) == 0 and profLicence == 'NA':
            pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
            pdf.drawString(14.3*cm,(3.65+rightSpacing)*cm,'No Licenses')
        
        else:
                
            if len(licences) != 0:
                pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(3.7+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFont('Vera', 9)
                if licence1 !='NA':
                    pdf.drawString(14.25*cm,(3.7+rightSpacing)*cm,licence1)
                if licence2 !='NA':
                    pdf.drawString(14.25*cm,(3.2+rightSpacing)*cm,licence2)
                if licence3 !='NA':
                    pdf.drawString(14.25*cm,(2.7+rightSpacing)*cm,licence3)
            # print('len(licences)',len(licences))
            
            if len(licences) == 0:
                licenHt=0
            elif len(licences) == 1 or len(licences) == 2:   
                licenHt=1
            elif len(licences) == 3 or len(licences) == 4:   
                licenHt=0.5
            
            rightSpacing = rightSpacing+licenHt
            # print('rightSpacing5',rightSpacing)
            print('length:',licenHt)
            if profLicence != 'NA':
                if len(licences) == 0:
                    pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(2.6+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 12);
                    pdf.drawString(14.5*cm,(2.7+rightSpacing)*cm,'LICENSES');
                pdf.setFont('Vera', 9);
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(2.05+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(2.05+rightSpacing)*cm,"Professional Licenses:")
                profLic = []
                pdf.setFillColorRGB(0,0,0)
                raw_addr = profLicence.title()
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:450]+'<br/>'+raw_addr[450:600]+'<br/>'+raw_addr[600:]
                # address = '<link href="' + raw_addr + '">' + address + '</link>'
                profLic.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                
                f = Frame(14.1*cm, (-1.3+rightSpacing)*cm, 6.8*cm, 3.4*cm, showBoundary=0)
                f.addFromList(profLic,pdf)
        
        pdf.setFillColorRGB(255,255,255) 
        pdf.setFont('Vera', 8);
        pdf.drawString(19.8*cm,(0.9)*cm,d2)   
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
            
            city            =x[46]
                
            state            =x[47]
                
            cityState=x[46]+', '+x[47]
            
            university            =x[48]
            if university:
                univ=university.split(';')
            else:
                univ=''
            
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
            editCompleted  =x[91]
            webSite =x[92]
            if not webSite:
                webSite ='NA'
            degreeType =x[93]
            estSavings =x[94]
            if not estSavings:
                estSavings ='NA'
            ####image data
            
            imageId            =x[95]
            person_image            =x[96]
            home_image            =x[97]
            name            =x[98]
            dateAndTime            =x[99]
            personImageFlag            =x[100]
            homeImageFlag            =x[101]
            profileString = person_image.decode()
            if personImageFlag == 2:
                img = imread(io.BytesIO(base64.b64decode(profileString)))
                 # show image
                plt.figure()
                plt.imshow(img, cmap="gray")
                
                cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite("profileImage.jpg", cv2_img)
                plt.show()
            else:
                profileString = profileString[22:]

                # print(profileString)

                im = Image.open(BytesIO(base64.b64decode(profileString)))
                im.save('profileImage.jpg', 'PNG')
           
            houseString = home_image.decode()
            if homeImageFlag == 2:
                # reconstruct image as an numpy array
                img1 = imread(io.BytesIO(base64.b64decode(houseString)))

                # show image
                plt.figure()
                plt.imshow(img1, cmap="gray")
                
                cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
                cv2.imwrite("houseImage.jpg", cv2_img1)
                plt.show()
            else:
                houseString = houseString[22:]
                
                im1 = Image.open(BytesIO(base64.b64decode(houseString)))
                im1.save('houseImage.jpg', 'PNG')
        
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
            homeHeight=2
            # homeHeight=0
           
        else:
            homeHeight=0
        print('homeHeight',homeHeight)  
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
        
        # print('personImageFlag',personImageFlag)
        if personImageFlag == 2:
            noImageMargin = 22
            lineMargin1 = 5.5
            lineMargin2 = 16
            salImgMargin = 8.2
            estSal = 6.5
            estSalImgMargin = 5.8
            estSalVal = 13
            savingIcon = 4.3
            savingRight = 5.3
            savingTitle = 5.5
            savingLeft = 13
            savingVal = 13.6
        else:
           noImageMargin = 12.5
           lineMargin1 = 2
           lineMargin2 = 10.5
           salImgMargin = 3.3
           estSal = 2
           estSalImgMargin = 1.25
           estSalVal = 8.5
           savingIcon = 0.25
           savingRight = 1.1
           savingTitle = 1.3
           savingLeft = 8.8
           savingVal = 9.3
            
        
        if JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA': 
            # nameHeight=2
            nameHeight=0
            # pdf.line(lineMargin1*cm,(27.4)*cm,lineMargin2*cm,(27.4)*cm)
        else:
            nameHeight=0
        
        
        pdf.drawCentredString((noImageMargin/2)*cm,(28.8-nameHeight)*cm,FullName.upper());
        # pdf.setDash([2,2,2,2],0)
        pdf.line(lineMargin1*cm,(28.6-nameHeight)*cm,lineMargin2*cm,(28.6-nameHeight)*cm)
        # pdf.setDash([0,0,0,0],0)
        pdf.setFont('Vera', 14);


        if len(Job_Desc) >=90:
                jobFont=9
        else:
                jobFont=14
                
        ##################################JOBS DISPLAY #############################   
       
        
        if JOB2 =='NA' and comp2 != 'NA':
            job2Height=0.5
        else:
            job2Height=0
            jobsHeight=0
        print('JOB1:',JOB1)
        print('JOB2:',JOB2)
        print('comp1:',comp1)
        print('comp2:',comp2)
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
            print('sdsdsd')
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
        
        elif JOB1 != 'NA' and comp1 == 'NA' and JOB2 != 'NA' and comp2 != 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA':        
            print('qwqwq')
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
            # print('skipp')
            
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
                
            
        if estSavings !='NA':
            if Per_Salary != 'NA':
                pdf.drawImage('/home/pdfImages/salaryNew.png', estSalImgMargin*cm, (24.7)*cm, width=9.8*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.setFont('VeraBd', 11);
                pdf.drawString((estSal)*cm,(24.9)*cm,"ESTIMATED YEARLY SALARY:  ")
                pdf.setFillColorRGB(255,0,0)
                pdf.drawString(estSalVal*cm,(24.9)*cm,Per_Salary);
            
            estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
            pdf.setFillColorRGB(0,0,0)
            pdf.drawImage('/home/pdfImages/savingsIcon.png', savingIcon*cm, (23.85)*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.drawImage('/home/pdfImages/savingRight.png', savingRight*cm, (23.9)*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            # pdf.drawImage('/home/pdfImages/retirment.png', 1.1*cm, 23.9*cm, width=10.25*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.drawImage('/home/pdfImages/savingsLeft.png', savingLeft*cm, (23.9)*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            pdf.setFont('VeraBI', 11);
            pdf.setFillColorRGB(255,255,255)
            pdf.drawString(savingTitle*cm,(24.1)*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
            pdf.setFillColorRGB(255,0,0)
            pdf.drawString(savingVal*cm,(24.1)*cm,estSavings);
            # pdf.drawCentredString((noImageMargin/2)*cm,25*cm,"ESTIMATED YEARLY SALARY:  "+Per_Salary);
            # estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
            # pdf.drawCentredString((noImageMargin/2)*cm,24.4*cm,"ESTIMATED RETIREMENT SAVINGS:  "+estSavings);
        else:
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
        
        noSpouseHt = 4.5
        # noSpouseHt = noSpouseHt + homeHeight
        
        # homeHeight 2.5

        if Addr == 1:
            pdf.drawImage('/home/pdfImages/personHome.png',4.5*cm,(27.8-noSpouseHt)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
            
            if houseType =='Rented Apartment' or houseType =='Apartment':
                pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(21.75-noSpouseHt)*cm,10.75*cm,6*cm,preserveAspectRatio=False);
                # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
            else:
                pdf.drawImage('houseImage.jpg',1*cm,(21.7-noSpouseHt)*cm,10.75*cm,6*cm,preserveAspectRatio=False);
            
            pdf.roundRect(1*cm, (21.75-noSpouseHt)*cm, 10.75*cm, 6*cm, 4, stroke=1, fill=0);
           
            pdf.setFont('VeraBd', 9);
            
            pdf.drawCentredString(6.5*cm,(20.25-noSpouseHt)*cm,Address+', '+city+', '+state.title()+' '+pincode);
            
            
            # pdf.drawString(1.5*cm,(20.25)*cm,Address);
            # pdf.drawString(1.5*cm,(19.75)*cm,city+', '+state.title()+' '+pincode);
            
            
            # pdf.drawString(5.62*cm,(21.25)*cm,pincode);
            
            if houseType =='Rented Apartment' or houseType =='Rented': 
                pdf.drawImage('/home/pdfImages/rented.png',5.25*cm,(20.8-noSpouseHt)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
            if houseType =='For Sale':  
                pdf.drawImage('/home/pdfImages/sale.png',5.25*cm,(20.8-noSpouseHt)*cm,2.75*cm,0.8*cm,preserveAspectRatio=False);
            

            if homeEqu1 == '$0':
                shiftHomeVal=3.25
                eqFontSize=12
            else:
                shiftHomeVal=0
                eqFontSize=8 
                # pdf.drawImage('/home/pdfImages/dot.png',(1+shiftHomeVal)*cm,(19.2-noSpouseHt)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            if homeValu1 !='$0' and homeEqu1 == '$0':
                pdf.setFont('VeraBd', eqFontSize);
                pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2-noSpouseHt)*cm,"ESTIMATED HOME VALUE");
                pdf.setFont('VeraBd', eqFontSize);
                pdf.drawCentredString((3.+shiftHomeVal)*cm,(18.6-noSpouseHt)*cm,homeValu1);

            if homeEqu1 != '$0':
                pdf.setFont('VeraBd', 8);
                pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2-noSpouseHt)*cm,"ESTIMATED HOME VALUE");
                pdf.setFont('VeraBd', 8);
                pdf.drawCentredString((3.+shiftHomeVal)*cm,(18.6-noSpouseHt)*cm,homeValu1);
                pdf.setLineWidth(0.5);
                pdf.line(6.25*cm,(19.5-noSpouseHt)*cm,6.25*cm,(18.65-noSpouseHt)*cm)
                # pdf.drawImage('/home/pdfImages/dot.png',7.20*cm,(19.2-noSpouseHt)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawCentredString(9.375*cm,(19.2-noSpouseHt)*cm,"ESTIMATED HOME EQUITY");
                pdf.setFont('VeraBd', 8);
                pdf.drawCentredString(9.375*cm,(18.6-noSpouseHt)*cm,homeEqu1);
            
        
        else:
            print('len(edu)',len(edu))
            print('edu1',edu1)
            print('edu2',edu2)
            print('univ1',univ1)
            print('univ2',univ2)
           
            if edu1 == 'NA' and edu2 =='NA' and univ1 == 'NA' and univ2 == 'NA':
                homeHeight=0;
                print('increse size:',homeHeight)
                pdf.drawImage('/home/pdfImages/personHome.png',5*cm,(27.8-noSpouseHt)*cm,3.25*cm,0.5*cm,preserveAspectRatio=False);
                
                if houseType =='Rented Apartment' or houseType =='Apartment':
                    pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(20.75-noSpouseHt)*cm,10.5*cm,7*cm,preserveAspectRatio=False);
                   
                else:
                    pdf.drawImage('houseImage.jpg',1*cm,(20.75-noSpouseHt)*cm,10.5*cm,7*cm,preserveAspectRatio=False);
                
                pdf.roundRect(1*cm, (20.75-noSpouseHt)*cm, 10.5*cm, 7*cm, 4, stroke=1, fill=0);
               
                pdf.setFont('VeraBd', 9);
                
                
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',1.5*cm,(20-noSpouseHt)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',1.5*cm,(20-noSpouseHt)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                    
                if Address != 'NA':
                    pdf.setFont('Vera', 10);
                    
                    pdf.drawString(1.5*cm,(19.5-noSpouseHt+homeHeight)*cm,"1.");
                    pdf.drawString(2*cm,(19.5-noSpouseHt+homeHeight)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                   
                    if homeEqu1 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeEqu1 != '$0':
                        
                        pdf.drawString(2*cm,(19-noSpouseHt+homeHeight+Equiheight)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 10);
                        pdf.drawString(7*cm,(19-noSpouseHt+homeHeight+Equiheight)*cm,homeEqu1);
                        pdf.setFont('Vera', 10);
                    
                   
                    if homeValu1 != '$0':
                        
                        pdf.drawString(2*cm,(18.5-noSpouseHt+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE: ");
                        pdf.setFont('VeraBd', 10);
                        pdf.drawString(7*cm,(18.5-noSpouseHt+homeHeight+Equiheight)*cm,homeValu1);
                        pdf.setFont('Vera', 10);
                    
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(18.3-noSpouseHt+homeHeight+Equiheight)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                
                if Address2 != 'NA':
                    pdf.setFont('Vera', 10);
                     
                    pdf.drawString(1.5*cm,(17.8-noSpouseHt+homeHeight)*cm,"2.");
                    pdf.drawString(2*cm,(17.8-noSpouseHt+homeHeight)*cm,Address2+', '+city2+', '+state2.title()+' '+pincode2);
                    if homeEqu2 == '$0':
                        Equiheight2 = 0.35;
                    else:
                        Equiheight2 = 0;
                    if homeEqu2 != '$0':
                        
                        pdf.drawString(2*cm,(17.25-noSpouseHt+homeHeight+Equiheight2)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 10);
                        pdf.drawString(7*cm,(17.25-noSpouseHt+homeHeight+Equiheight2)*cm,homeEqu2);
                        pdf.setFont('Vera', 10);
                    
                    if homeValu2 != '$0':
                        
                        pdf.drawString(2*cm,(16.75-noSpouseHt+homeHeight+Equiheight2)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 10);
                        pdf.drawString(7*cm,(16.75-noSpouseHt+homeHeight+Equiheight2)*cm,homeValu2);
                        pdf.setFont('Vera', 10);
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(16.55-noSpouseHt+homeHeight+Equiheight2)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                
                if Address3 != 'NA':
                    pdf.setFont('Vera', 10);
                    if homeEqu3 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                        
                    pdf.drawString(1.5*cm,(15.7-noSpouseHt+homeHeight+Equiheight)*cm,"3.");
                    
                    pdf.drawString(2*cm,(15.7-noSpouseHt+homeHeight+Equiheight)*cm,Address3+', '+city3+', '+state3.title()+' '+pincode3);
                    
                    if homeEqu3 != '$0':
                    
                        pdf.drawString(2*cm,(15.2-noSpouseHt+homeHeight+Equiheight)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 10);
                        pdf.drawString(7*cm,(15.2-noSpouseHt+homeHeight+Equiheight)*cm,homeEqu3);
                        
                        pdf.setFont('Vera', 10);
                    
                    if homeValu3 != '$0':
                        
                        pdf.drawString(2*cm,(14.7-noSpouseHt+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 10);
                        pdf.drawString(7*cm,(17.7-noSpouseHt+homeHeight+Equiheight)*cm,homeValu3);
                        pdf.setFont('Vera', 10);
               
        
            else:
                pdf.drawImage('/home/pdfImages/personHome.png',5*cm,(27.8-noSpouseHt)*cm,3.25*cm,0.5*cm,preserveAspectRatio=False);
                
                if houseType =='Rented Apartment' or houseType =='Apartment':
                    pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(22.25-noSpouseHt)*cm,10.5*cm,5.5*cm,preserveAspectRatio=False);
                    
                else:
                    pdf.drawImage('houseImage.jpg',1*cm,(22.25-noSpouseHt)*cm,10.5*cm,5.5*cm,preserveAspectRatio=False);
                
                pdf.roundRect(1*cm, (22.25-noSpouseHt)*cm, 10.5*cm, 5.5*cm, 4, stroke=1, fill=0);
               
                pdf.setFont('VeraBd', 9);
                
                
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',1.5*cm,(21.5-noSpouseHt)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',1.5*cm,(21.5-noSpouseHt)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                    
                if Address != 'NA':
                    pdf.setFont('Vera', 9);
                    
                    pdf.drawString(1.5*cm,(21.1-noSpouseHt)*cm,"1.");
                    pdf.setFont('Vera', 9);
                    
                    pdf.drawString(2*cm,(21.1-noSpouseHt)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                   
                    if homeEqu1 != '$0':
                        
                        pdf.drawString(2*cm,(20.65-noSpouseHt)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(20.65-noSpouseHt)*cm,homeEqu1);
                        pdf.setFont('Vera', 9);
                    if homeEqu1 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                   
                    if homeValu1 != '$0':
                        
                        pdf.drawString(2*cm,(20.25-noSpouseHt)*cm,"ESTIMATED HOME VALUE: ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(20.25-noSpouseHt)*cm,homeValu1);
                        pdf.setFont('Vera', 9);
                    
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(20.15-noSpouseHt)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                
                if Address2 != 'NA':
                    pdf.setFont('Vera', 9);
                    
                    pdf.drawString(1.5*cm,(19.7-noSpouseHt)*cm,"2.");
                    pdf.setFont('Vera', 9);
                    
                    pdf.drawString(2*cm,(19.7-noSpouseHt)*cm,Address2+', '+city2+', '+state2.title()+' '+pincode2);
                    
                    if homeEqu2 != '$0':
                        
                        pdf.drawString(2*cm,(19.3-noSpouseHt)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(19.3-noSpouseHt)*cm,homeEqu2);
                        pdf.setFont('Vera', 9);
                    if homeEqu2 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu2 != '$0':
                        
                        pdf.drawString(2*cm,(18.9-noSpouseHt)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(18.9-noSpouseHt)*cm,homeValu2);
                        pdf.setFont('Vera', 9);
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(18.8-noSpouseHt)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                
                if Address3 != 'NA':
                    pdf.setFont('Vera', 8);
                    
                    pdf.drawString(1.5*cm,(18.4-noSpouseHt)*cm,"3.");
                    pdf.setFont('Vera', 9);
                    pdf.drawString(2*cm,(18.4-noSpouseHt)*cm,Address3+', '+city3+', '+state3.title()+' '+pincode3);
                    
                    if homeEqu3 != '$0':
                        pdf.drawString(2*cm,(17.95-noSpouseHt)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(17.95-noSpouseHt)*cm,homeEqu3);
                        
                        pdf.setFont('Vera', 9);
                    if homeEqu3 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu3 != '$0':
                        
                        pdf.drawString(2*cm,(17.55-noSpouseHt)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 9);
                        pdf.drawString(6.5*cm,(17.55-noSpouseHt)*cm,homeValu3);
                        pdf.setFont('Vera', 8);
               
       
        ####DIVORCED IMG
        
              # if Education != 'NA' or university != 'NA':
        temp2Extraht = 3.5
        # temp2Extraht = 0
        
        
        
        if len(edu) == 1 and len(univ) == 1:
            pdf.drawImage('/home/pdfImages/Education.png', 2.1*cm, (17+temp2Extraht)*cm, width=8.5*cm, height=0.75*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            if univ1 != 'NA':
            
                pdf.setFont('VeraBd', 8);
                pdf.setFillColorRGB(0.5,0.2,0.1)
                pdf.drawCentredString((12.5/2)*cm,(16.5+temp2Extraht)*cm,univ1.upper());
                pdf.setFillColorRGB(0,0,0)
            if edu1 != 'NA':
                pdf.drawCentredString((12.5/2)*cm,(16.05+temp2Extraht)*cm,edu1); 
                
        else:
            
            # pdf.drawImage('/home/pdfImages/Education1.png', 1.1*cm, (15)*cm, width=1.3*cm, height=3.5*cm, mask='auto',preserveAspectRatio=False, anchor='c')
            if univ1 != 'NA':
                pdf.drawImage('/home/pdfImages/Education.png', 2*cm, (8.5+temp2Extraht)*cm, width=8.5*cm, height=0.75*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.setFont('VeraBd', 8);
                pdf.setFillColorRGB(0.5,0.2,0.1)
                pdf.drawCentredString((12.5/2)*cm,(8+temp2Extraht)*cm,univ1.upper());
                pdf.setFillColorRGB(0,0,0)
                
            if edu1 != 'NA':
                pdf.drawImage('/home/pdfImages/Education.png', 2*cm, (8.5+temp2Extraht)*cm, width=8.5*cm, height=0.75*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.drawCentredString((12.5/2)*cm,(7.5+temp2Extraht)*cm,edu1);
                pdf.setFillColorRGB(0,5,1)
                pdf.drawCentredString(6.25*cm,(7.4+temp2Extraht)*cm,'_______________________________')
                pdf.setFillColorRGB(0,0,0)    
            
            if univ2 != 'NA':
            
                pdf.setFont('VeraBd', 8);
                pdf.setFillColorRGB(0.5,0.2,0.1)
                pdf.drawCentredString((12.5/2)*cm,(7+temp2Extraht)*cm,univ2.upper());
                pdf.setFillColorRGB(0,0,0)
                
                
            if edu2 != 'NA':
                if univ2 == 'NA':
                    uniHeight = 0.5;
                else:
                    uniHeight = 0;
                pdf.drawCentredString((12.5/2)*cm,(6.54+temp2Extraht)*cm,edu2);
               
                
           
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
            # vehicleHeight=2
            vehicleHeight=0
        else:
            vehicleHeight = 0
        spouseHeight = 0;
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
        
      ##################################################LEFT 2nd HALF ##############################################
       
         
         
        ###########################VEHICLES DETAILS#################################
            
            # spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
        spouseSpacing = 0;
        spBankHt = 0+temp2Extraht
        
        if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
        else:
        
            if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                pdf.setFont('VeraBd', 12);
                pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
            pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
        
        
        
        pdf.drawImage('/home/pdfImages/Disclaimer.png',0.06*cm,(0.05)*cm,21*cm,0.8*cm,preserveAspectRatio=False, mask='auto');	
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
        
        # webSite = "https://www.doctorquick.com/"
        # webSite = "NA"
        print('teplate 2')
        if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
            socialHght = 6
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 4.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 4.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 4.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 4.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 4.5
            
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 3.5
            
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 3.5
            
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 3.5
            
        
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5        
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        
        
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 1.25
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 1.25   
        else:
            socialHght = 0
        
        
        rightSpacing = socialHght-1.2
        # print('rightSpacing',rightSpacing)
        pdf.setFillColorRGB(255,255,255)
        
        if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
            
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
            
            raw_addr2 = Per_LinkedIn
            address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
            address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
            ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
           
            f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(ld_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            gmail_url = []
            
            raw_addr3 = per_Email
            address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
            address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
            gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

            f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
            f.addFromList(gmail_url,pdf)
            
            
            
            pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.75*cm,13*cm,Per_Tel)
                            
            pdf.drawImage('/home/pdfImages/link.png',13.5*cm,11.45*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            website = []
            raw_addr4 = webSite
            address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
            address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
            website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
            
            f = Frame(14.5*cm, 10.8*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(website,pdf)
    
    
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA' or webSite != 'NA': 
            print('website')
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            
            if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                 
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
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

            elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
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
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                
                f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
                print('This module')                     
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr2 = per_Email
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
              
            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
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

            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
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
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:28]+'<br/>'+raw_addr[28:58]+'<br/>'+raw_addr[58:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                              
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
               
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                
                f = Frame(14.5*cm, 14.3*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and webSite == 'NA':
            
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
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
             
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
             
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
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                
                
                
                pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
                    
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 12*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                print('Per_facebook',Per_facebook)
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                                    
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
                
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                                    
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
  
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.5*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
              

        
        # pdf.drawString(13.7*cm,(12.2)*cm,'________________________________________________') 
        
        contactHeight+=2.65 # comment it when hobbies are needed in the report
           
         ################### Removed as per client requirement dated on 24-01-2020 ########################
      
        ################### Criminal History,Bankruptcies,Evictions ##########################
        
        
        if corDate1 != 'NA' and corDate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');#Removed as per clients requirement dated on 24012020
            pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS ');
            if corDate1 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
                # print('len:',len(CHOdate1))
                pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
            if corDate2 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(10.78+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(10.78+rightSpacing)*cm,corDate2)
                pdf.drawString(15.5*cm,(10.78+rightSpacing)*cm,corpFile2)
        
            # extraHeight=2
        
        elif corDate1 != 'NA' and corDate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            
            # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');
            pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
            pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
        
        
        rightSpacing = 0
        if corDate1 == 'NA' and corDate2 == 'NA':
            corpHght = 2
        elif corDate1 != 'NA' and corDate2 == 'NA':
            corpHght = 0.8
            
        else:
            corpHght = 0.5
        
        rightSpacing = socialHght + corpHght-2
        
        pdf.setFillColorRGB(255,255,255)
        pdf.setFont('Vera', 11);
        pdf.drawString(13.75*cm,(10.5+rightSpacing)*cm,'____________________________________')
        
        pdf.drawString(13.8*cm,(9.7+rightSpacing)*cm,'POSSIBLE JUDGMENTS');
        if judments !='No':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            
        pdf.drawString(13.8*cm,(9+rightSpacing)*cm,'POSSIBLE EVICTIONS');
        if EVFdate1 != 'NA' or EVFdate2 != 'NA':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(19.8*cm,(9+rightSpacing)*cm,EVFdate1)
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
        
        if BRFdate1 != 'NA' and BRFdate1 != 'None' or BRFdate2 != 'NA':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(19.8*cm,(8.35+rightSpacing)*cm,BRFdate1)
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.drawString(13.75*cm,(8.1+rightSpacing)*cm,'____________________________________')        
        if len(licences) == 0:
            licenLen=2
        else:
            licenLen=0
        
        if len(licences) == 0 and profLicence != 'NA': 
            rightSpacing += 4.5
        else:
            rightSpacing += 3
        
        if len(licences) == 0 and profLicence == 'NA':
            pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
            pdf.drawString(14.3*cm,(3.65+rightSpacing)*cm,'No Licenses')
        
        else:
                
            if len(licences) != 0:
                pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(3.7+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFont('Vera', 9)
                if licence1 !='NA':
                    pdf.drawString(14.25*cm,(3.7+rightSpacing)*cm,licence1)
                if licence2 !='NA':
                    pdf.drawString(14.25*cm,(3.2+rightSpacing)*cm,licence2)
                if licence3 !='NA':
                    pdf.drawString(14.25*cm,(2.7+rightSpacing)*cm,licence3)
            # print('len(licences)',len(licences))
            
            if len(licences) == 0:
                licenHt=0
            elif len(licences) == 1 or len(licences) == 2:   
                licenHt=1
            elif len(licences) == 3 or len(licences) == 4:   
                licenHt=0.5
            
            rightSpacing = rightSpacing+licenHt
            # print('rightSpacing5',rightSpacing)
            print('length:',licenHt)
            if profLicence != 'NA':
                if len(licences) == 0:
                    pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(2.6+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 12);
                    pdf.drawString(14.5*cm,(2.7+rightSpacing)*cm,'LICENSES');
                pdf.setFont('Vera', 9);
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(2.05+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(2.05+rightSpacing)*cm,"Professional Licenses:")
                profLic = []
                pdf.setFillColorRGB(0,0,0)
                raw_addr = profLicence.title()
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:450]+'<br/>'+raw_addr[450:600]+'<br/>'+raw_addr[600:]
                # address = '<link href="' + raw_addr + '">' + address + '</link>'
                profLic.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                
                f = Frame(14.1*cm, (-1.3+rightSpacing)*cm, 6.8*cm, 3.4*cm, showBoundary=0)
                f.addFromList(profLic,pdf)
        
        pdf.setFillColorRGB(255,255,255) 
        pdf.setFont('Vera', 8);
        pdf.drawString(19.8*cm,(0.9)*cm,d2)   
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

def template3(request,userId=None):
   
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
            
            
            city            =x[46]
                
            state            =x[47]
               
            cityState=x[46]+', '+x[47]
            
            university            =x[48]
            if university:
                univ=university.split(';')
            else:
                univ=''
                
            
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
                
                
            else:
                homeEqu2='$0'
                
            
            
            Esti_Home_Equi3            =x[75]
            if Esti_Home_Equi3:
                Esti_Home_Equi3 = int(float(Esti_Home_Equi3))
                homeEqu3 = custom_format_currency(Esti_Home_Equi3, 'USD', locale='en_US')
                
                
            else:
                homeEqu3='$0'
               
                
            Address2            =x[76]
            if not Address2:
                Address2 = 'NA'
            Address3            =x[77]
            if not Address3:
                Address3 = 'NA'
            
            
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
            editCompleted =x[91]
            webSite =x[92]
            if not webSite:
                webSite ='NA'
            degreeType =x[93]
            estSavings =x[94]
            if not estSavings:
                estSavings ='NA'
            ####image data
            
            imageId            =x[95]
            person_image            =x[96]
            home_image            =x[97]
            name            =x[98]
            dateAndTime            =x[99]
            personImageFlag            =x[100]
            homeImageFlag            =x[101]
            profileString = person_image.decode()
            if personImageFlag == 2:
                img = imread(io.BytesIO(base64.b64decode(profileString)))
                 # show image
                plt.figure()
                plt.imshow(img, cmap="gray")
                
                cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite("profileImage.jpg", cv2_img)
                plt.show()
            else:
                profileString = profileString[22:]

                # print(profileString)

                im = Image.open(BytesIO(base64.b64decode(profileString)))
                im.save('profileImage.jpg', 'PNG')
           
            houseString = home_image.decode()
            if homeImageFlag == 2:
                # reconstruct image as an numpy array
                img1 = imread(io.BytesIO(base64.b64decode(houseString)))

                # show image
                plt.figure()
                plt.imshow(img1, cmap="gray")
                
                cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
                cv2.imwrite("houseImage.jpg", cv2_img1)
                plt.show()
            else:
                houseString = houseString[22:]
                
                im1 = Image.open(BytesIO(base64.b64decode(houseString)))
                im1.save('houseImage.jpg', 'PNG')
        
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
            
            buffer = BytesIO()
            
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
            
            # print('personImageFlag',personImageFlag)
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
                
            
            if JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA': 
                # nameHeight=2
                nameHeight=0
                # pdf.line(lineMargin1*cm,(27.4)*cm,lineMargin2*cm,(27.4)*cm)
            else:
                nameHeight=0
            
            
            pdf.drawCentredString((noImageMargin/2)*cm,(28.8-nameHeight)*cm,FullName.upper());
            # pdf.setDash([2,2,2,2],0)
            pdf.line(lineMargin1*cm,(28.6-nameHeight)*cm,lineMargin2*cm,(28.6-nameHeight)*cm)
            # pdf.setDash([0,0,0,0],0)
            pdf.setFont('Vera', 14);


            if len(Job_Desc) >=90:
                    jobFont=9
            else:
                    jobFont=14
                    
            ##################################JOBS DISPLAY #############################   
           
            
            if JOB2 =='NA' and comp2 != 'NA':
                job2Height=0.5
            else:
                job2Height=0
                jobsHeight=0
            
            
            
            ##################################JOBS DISPLAY #############################            
              
            if personImageFlag == 2:
                # print('skipp')
                
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
            if personImageFlag == 2:
                shiftSaving = 4
            else:
                shiftSaving = 0 
            if Addr == 1:
                if estSavings !='NA':
                    pdf.drawImage('/home/pdfImages/personHome.png',(4.5)*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                    pdf.setFillColorRGB(0,0,0)
                    pdf.drawImage('/home/pdfImages/savingsIcon.png', (0.25+shiftSaving)*cm, 27.6*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingRight.png', (1.25+shiftSaving)*cm, 27.7*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingsLeft.png',(9+shiftSaving)*cm, 27.7*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBI', 11);
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString((1.5+shiftSaving)*cm,27.9*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawString((9.5+shiftSaving)*cm,27.9*cm,estSavings);
                    pdf.setFillColorRGB(0,0,0)
                    
                    pdf.drawImage('/home/pdfImages/personHome.png',4.5*cm,(26.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(21.75)*cm,10.5*cm,5*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(21.7)*cm,10.5*cm,5*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (21.75)*cm, 10.5*cm, 5*cm, 4, stroke=1, fill=0);
                else:
                    pdf.drawImage('/home/pdfImages/personHome.png',4.5*cm,(27.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(21.75)*cm,10.5*cm,6*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',1*cm,(21.7)*cm,10.5*cm,6*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(1*cm, (21.75)*cm, 10.5*cm, 6*cm, 4, stroke=1, fill=0);
               
                pdf.setFont('VeraBd', 9);
                
                pdf.drawCentredString(6.5*cm,(20.25)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',5.25*cm,(20.8)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',5.25*cm,(20.8)*cm,2.75*cm,0.8*cm,preserveAspectRatio=False);
                
                
                if homeEqu1 == '$0':
                    shiftHomeVal=3.25
                    eqFontSize=12
                else:
                    shiftHomeVal=0
                    eqFontSize=8
                    # pdf.drawImage('/home/pdfImages/dot.png',(1+shiftHomeVal)*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                print('shiftHomeVal',shiftHomeVal)
                
                if homeValu1 !='$0' and homeEqu1 == '$0':
                    pdf.setFont('VeraBd', eqFontSize);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2)*cm,"ESTIMATED HOME VALUE");
                    pdf.setFont('VeraBd', eqFontSize);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(18.6)*cm,homeValu1);

                if homeEqu1 != '$0':
                    pdf.setFont('VeraBd', 8);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2)*cm,"ESTIMATED HOME VALUE");
                    pdf.setFont('VeraBd', 8);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(18.6)*cm,homeValu1);
                    pdf.setLineWidth(0.5);
                    pdf.line(6.25*cm,(19.5)*cm,6.25*cm,(18.65)*cm)
                    # pdf.drawImage('/home/pdfImages/dot.png',7.20*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(9.375*cm,(19.2)*cm,"ESTIMATED HOME EQUITY");
                    pdf.setFont('VeraBd', 8);
                    pdf.drawCentredString(9.375*cm,(18.6)*cm,homeEqu1);
                
            else:

                if estSavings !='NA':
                    
                    pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                    pdf.setFillColorRGB(0,0,0)
                    pdf.drawImage('/home/pdfImages/savingsIcon.png', (0.25+shiftSaving)*cm, 27.6*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingRight.png', (1.25+shiftSaving)*cm, 27.7*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.drawImage('/home/pdfImages/savingsLeft.png',(9+shiftSaving)*cm, 27.7*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBI', 11);
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString((1.5+shiftSaving)*cm,27.9*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawString((9.5+shiftSaving)*cm,27.9*cm,estSavings);
                    pdf.setFillColorRGB(0,0,0)
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',2.5*cm,(23.3)*cm,8*cm,3.6*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',2.5*cm,(23.3)*cm,8*cm,3.6*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(2.5*cm, (23.3)*cm, 8*cm, 3.6*cm, 4, stroke=1, fill=0);
                else:
                
                    pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(27.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    
                    if houseType =='Rented Apartment' or houseType =='Apartment':
                        pdf.drawImage('/home/pdfImages/rentedApt.png',2*cm,(23.25)*cm,9*cm,4.5*cm,preserveAspectRatio=False);
                        # pdf.drawImage('',5.7*cm,(22.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                    else:
                        pdf.drawImage('houseImage.jpg',2*cm,(23.25)*cm,9*cm,4.5*cm,preserveAspectRatio=False);
                    
                    pdf.roundRect(2*cm, (23.25)*cm, 9*cm, 4.5*cm, 4, stroke=1, fill=0);
               
                pdf.setFont('VeraBd', 9);
                
                
                if houseType =='Rented Apartment' or houseType =='Rented': 
                    pdf.drawImage('/home/pdfImages/rented.png',1.5*cm,(22.5)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                if houseType =='For Sale':  
                    pdf.drawImage('/home/pdfImages/sale.png',1.5*cm,(22.5)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
                    
                if Address != 'NA':
                    pdf.setFont('Vera', 8);
                    
                    ## pdf.drawString(5.62*cm,(22.25)*cm,Address1+', '+city1+', '+state1+' '+pin1);
                    pdf.drawString(1.5*cm,(22)*cm,"1.");
                    pdf.setFont('Vera', 8);
                    
                    pdf.drawString(2*cm,(22)*cm,Address+', '+city+', '+state.title()+' '+pincode);
                    # pdf.drawString(5.6*cm,(22.40)*cm,);
                    
                    # pdf.drawString(5.6*cm,(22.7)*cm,Address);
                    # pdf.drawString(5.6*cm,(22.40)*cm,city+', '+state.title()+' '+pincode);
                    
                    
                    if homeEqu1 != '$0':
                        
                        pdf.drawString(2*cm,(21.6)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(21.6)*cm,homeEqu1);
                        pdf.setFont('Vera', 8);
                    if homeEqu1 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    # pdf.drawCentredString(7.7*cm,(21.45)*cm,Esti_Home_Equi);
                    # print('homeValu1',homeValu1)
                    if homeValu1 != '$0':
                        
                        pdf.drawString(2*cm,(21.2+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(21.2+homeHeight+Equiheight)*cm,homeValu1);
                        pdf.setFont('Vera', 8);
                    
                    # pdf.drawCentredString(7.7*cm,(20.55)*cm,Home_Val);
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(21)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                    
                
                if Address2 != 'NA':
                    pdf.setFont('Vera', 8);
                    
                    ## pdf.drawString(5.62*cm,(22.25)*cm,Address1+', '+city1+', '+state1+' '+pin1);
                    pdf.drawString(1.5*cm,(20.6)*cm,"2.");
                    pdf.setFont('Vera', 8);
                    
                    pdf.drawString(2*cm,(20.6)*cm,Address2+', '+city2+', '+state2.title()+' '+pincode2);
                    # pdf.drawString(5.6*cm,(20.90)*cm,);
                    
                    # pdf.drawString(5.6*cm,(21.20)*cm,Address2);
                    # pdf.drawString(5.6*cm,(20.90)*cm,city2+', '+state2.title()+' '+pincode2);
                    
                    # if homeValu2 == '0' or homeValu2 != '$0':
                    if homeEqu2 != '$0':
                        
                        pdf.drawString(2*cm,(20.2)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(20.2)*cm,homeEqu2);
                        pdf.setFont('Vera', 8);
                    if homeEqu2 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu2 != '$0':
                        
                        pdf.drawString(2*cm,(19.8+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(19.8+homeHeight+Equiheight)*cm,homeValu2);
                        pdf.setFont('Vera', 8);
                    pdf.setFillColorRGB(0,0,1)
                    pdf.drawString(2.6*cm,(19.6)*cm,'_______________________________')
                    pdf.setFillColorRGB(0,0,0)
                if Address3 != 'NA':
                    pdf.setFont('Vera', 8);
                    
                    ##pdf.drawString(5.62*cm,(22.25)*cm,Address1+', '+city1+', '+state1+' '+pin1);
                    pdf.drawString(1.5*cm,(19.2)*cm,"3.");
                    pdf.setFont('Vera', 8);
                    pdf.drawString(2*cm,(19.2)*cm,Address3+', '+city3+', '+state3.title()+' '+pincode3);
                    # pdf.drawString(5.6*cm,(19.40)*cm,);
                    
                    
                    if homeEqu3 != '$0':
                    # if homeEqu3 != 0:
                        
                        pdf.drawString(2*cm,(18.8)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(18.8)*cm,homeEqu3);
                        
                        pdf.setFont('Vera', 8);
                    if homeEqu3 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu3 != '$0':
                        
                        pdf.drawString(2*cm,(18.4+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(6*cm,(18.4+homeHeight+Equiheight)*cm,homeValu3);
                        pdf.setFont('Vera', 8);

               
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
                vehicleHeight=0
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
            
          ##################################################LEFT 2nd HALF ##############################################
            
            if spouse_name != 'NA' :
                if relationStatus != 'NA' : 
                    pdf.setFillColorRGB(1,0,0.2)
                    pdf.setFont('Vera', 12);
                    pdf.drawString(7*cm,(14.7+qualiHeight)*cm,'['+relationStatus+']');
                    pdf.setFillColorRGB(0,0,00)
                pdf.drawImage('/home/pdfImages/family.png',0.75*cm,(14.5+qualiHeight)*cm,9.5*cm,0.65*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/business.png',1.5*cm,(13.25+qualiHeight)*cm,0.5*cm,1*cm,preserveAspectRatio=False, mask='auto');
             
                # pdf.setFont('VeraBd', 12);
                if Spouse_Age == 'NA':
                    pdf.drawString(2.3*cm,(13.55+qualiHeight)*cm,spouse_name);
                else:
                    pdf.drawString(2.3*cm,(13.8+qualiHeight)*cm,spouse_name);
                
                if Spouse_Age != 'NA':
                    pdf.setFont('Vera', 9);
                    pdf.drawString(2.3*cm,(13.3+qualiHeight)*cm,Spouse_Age);
                
                if spUni1 !="NA":
                    pdf.drawImage('/home/pdfImages/edu.png',1.25*cm,(12.3+qualiHeight)*cm,0.9*cm,0.7*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFillColorRGB(0.5,0.2,0.1)
                    if spedu1 != 'NA':
                        spUni1=spUni1+','
                        pdf.setFont('Vera', 9);
                        pdf.drawString(2.3*cm,(12.75+qualiHeight)*cm,spUni1.upper());
                    else:
                        pdf.setFont('Vera', 9);
                        pdf.drawString(2.3*cm,(12.55+qualiHeight)*cm,spUni1.upper());
                    pdf.setFillColorRGB(0,0,0)
                if spedu1 !="NA":
                    pdf.drawImage('/home/pdfImages/edu.png',1.25*cm,(12.3+qualiHeight)*cm,0.9*cm,0.7*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 9);
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
                        if estSavings !='NA': 
                            pdf.drawImage('/home/pdfImages/salaryNew.png', 1.5*cm, (10.2+qualiHeight+spEduHt)*cm, width=9.8*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                            pdf.setFont('VeraBd', 11);
                            pdf.setFillColorRGB(0,0,0)
                            pdf.drawString(2*cm,(10.4+qualiHeight+spEduHt)*cm,"ESTIMATED YEARLY SALARY:  ")
                            pdf.setFillColorRGB(255,0,0)
                            pdf.drawString(8.5*cm,(10.4+qualiHeight+spEduHt)*cm,Dep_Salary);
                        else:
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
                
                # if spBank1 != 'NA' and spBank1 != 'None' and spBank1 != 'None' and spBank1 != 'None' and spouseBankruptDate != 'NA':
                if spBank1 != 'NA' and spBank1 != 'None' and spBank1 != 'None' and spBank1 != 'None' :
                    
                    pdf.setFont('Vera', 12);
                    pdf.drawImage('/home/pdfImages/spouseBank.png',1.5*cm,(7.35+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(2.2*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'POSSIBLE BANKRUPTCIES');
                    pdf.drawImage('/home/pdfImages/checked.png',8*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(8.9*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1);
                    # pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
                    
                    pdf.setFont('Vera', 9);      
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year    Filing Status');
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year');
                    
                    # pdf.drawImage('/home/pdfImages/arrow_blue.png',1.75*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    # pdf.drawString(2.25*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1)
                    
                    # if spBankDet1 != 'NA':
                        # pdf.drawString(3.35*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBankDet1)
       
       
            ############################# About Family ################################
             
             
            ###########################VEHICLES DETAILS#################################
                if spBank1 == 'NA' and spBankDet1 == 'NA':
                    spBankHt = 1.5
                else: 
                    spBankHt = 0.6
                # spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
                spouseSpacing = 0;
                
                if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
                else:
                
                    if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                        pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                        # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                        pdf.setFont('VeraBd', 12);
                        pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                        pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
                    pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
                
            else:
                if spBank1 == 'NA' and spBankDet1 == 'NA':
                    spBankHt = 1.5
                else: 
                    spBankHt = 0
                spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
                # spouseSpacing = 0;
                
                if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
                else:
                
                    if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                        pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                        # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                        pdf.setFont('VeraBd', 12);
                        pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                        pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
                    pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
                
            
            pdf.drawImage('/home/pdfImages/Disclaimer.png',0.06*cm,(0.05)*cm,21*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
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
            
            # webSite = "https://www.doctorquick.com/"
            # webSite = "NA"
                
            if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                socialHght = 6
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 3.5
                
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 2.5
                
                
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 1.25
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 1.25
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 1.25
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 1.25
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 1.25
            
                
            else:
                socialHght = 0
            
            
            rightSpacing = socialHght-1.2
            # print('rightSpacing',rightSpacing)
            pdf.setFillColorRGB(255,255,255)
            
            if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                
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
                
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
               
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
                                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,11.45*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                
                f = Frame(14.5*cm, 10.8*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
        
        
            if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA' or webSite != 'NA': 
                print('website')
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    fb_url = []
                    raw_addr = Per_facebook
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(fb_url,pdf)
                elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr = Per_LinkedIn
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                     
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    
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

                elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    
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
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    
                    gmail_url = []
                    raw_addr = per_Email
                    address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                    address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                    
                    f = Frame(14.5*cm, 15.4*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
                
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
                                          
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr2 = per_Email
                    address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                    address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                    f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                  
                elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
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

                elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                    address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                    address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                    f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
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
                
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
                    
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
                   
                elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                    address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                    address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    
                    f = Frame(14.5*cm, 14.3*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
                
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and webSite == 'NA':
                
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
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                    f = Frame(14.5*cm, 14.2*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    

                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
                 
                elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
                 
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
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)

                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                
                elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                    
                    
                    
                    pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)

                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                
                elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    fb_url = []
                    raw_addr = Per_facebook
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(fb_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                    

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                        
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 12*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    fb_url = []
                    raw_addr = Per_facebook
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(fb_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                    
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    print('Per_facebook',Per_facebook)
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr = Per_LinkedIn
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                                        
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
                    
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr = Per_LinkedIn
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                                        
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                  
                elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr = per_Email
                    address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                    address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.5*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                  

            
            # pdf.drawString(13.7*cm,(12.2)*cm,'________________________________________________') 
            
            contactHeight+=2.65 # comment it when hobbies are needed in the report
               
             ################### Removed as per client requirement dated on 24-01-2020 ########################
          
            ################### Criminal History,Bankruptcies,Evictions ##########################
            
            
            if corDate1 != 'NA' and corDate2 != 'NA':
                pdf.setFont('Vera', 12);
                pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');#Removed as per clients requirement dated on 24012020
                pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
                pdf.setFont('Vera', 9);
                # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS ');
                if corDate1 !='NA':
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
                    # print('len:',len(CHOdate1))
                    pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
                if corDate2 !='NA':
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(10.78+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.25*cm,(10.78+rightSpacing)*cm,corDate2)
                    pdf.drawString(15.5*cm,(10.78+rightSpacing)*cm,corpFile2)
            
                # extraHeight=2
            
            elif corDate1 != 'NA' and corDate2 == 'NA':
                pdf.setFont('Vera', 12);
                pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                
                # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');
                pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
                pdf.setFont('Vera', 9);
                # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS');
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
                pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
            
            
            rightSpacing = 0
            if corDate1 == 'NA' and corDate2 == 'NA':
                corpHght = 2
            elif corDate1 != 'NA' and corDate2 == 'NA':
                corpHght = 0.8
                
            else:
                corpHght = 0.5
            
            rightSpacing = socialHght + corpHght-2
            
            pdf.setFillColorRGB(255,255,255)
            pdf.setFont('Vera', 11);
            pdf.drawString(13.75*cm,(10.5+rightSpacing)*cm,'____________________________________')
            
            pdf.drawString(13.8*cm,(9.7+rightSpacing)*cm,'POSSIBLE JUDGMENTS');
            if judments !='No':
                pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            else:
                pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                
            pdf.drawString(13.8*cm,(9+rightSpacing)*cm,'POSSIBLE EVICTIONS');
            if EVFdate1 != 'NA' or EVFdate2 != 'NA':
                pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(19.8*cm,(9+rightSpacing)*cm,EVFdate1)
            else:
                pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
            
            if BRFdate1 != 'NA' and BRFdate1 != 'None' or BRFdate2 != 'NA':
                pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(19.8*cm,(8.35+rightSpacing)*cm,BRFdate1)
            else:
                pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(13.75*cm,(8.1+rightSpacing)*cm,'____________________________________')       
            if len(licences) == 0:
                licenLen=2
            else:
                licenLen=0
                
            if len(licences) == 0 and profLicence != 'NA': 
                rightSpacing += 4.5
            else:
                rightSpacing += 3
                
            if len(licences) == 0 and profLicence == 'NA':
                pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
                pdf.drawString(14.3*cm,(3.65+rightSpacing)*cm,'No Licenses')
            
            else:
                
                if len(licences) != 0:
                    pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(3.7+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 9)
                    if licence1 !='NA':
                        pdf.drawString(14.25*cm,(3.7+rightSpacing)*cm,licence1)
                    if licence2 !='NA':
                        pdf.drawString(14.25*cm,(3.2+rightSpacing)*cm,licence2)
                    if licence3 !='NA':
                        pdf.drawString(14.25*cm,(2.7+rightSpacing)*cm,licence3)
                # print('len(licences)',len(licences))
                
                if len(licences) == 0:
                    licenHt=0
                elif len(licences) == 1 or len(licences) == 2:   
                    licenHt=1
                elif len(licences) == 3 or len(licences) == 4:   
                    licenHt=0.5
                
                rightSpacing = rightSpacing+licenHt
                # print('rightSpacing5',rightSpacing)
                print('length:',licenHt)
                if profLicence != 'NA':
                    if len(licences) == 0:
                        pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(2.6+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                        pdf.setFont('Vera', 12);
                        pdf.drawString(14.5*cm,(2.7+rightSpacing)*cm,'LICENSES');
                    pdf.setFont('Vera', 9);
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(2.05+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.25*cm,(2.05+rightSpacing)*cm,"Professional Licenses:")
                    profLic = []
                    pdf.setFillColorRGB(0,0,0)
                    raw_addr = profLicence.title()
                    address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:450]+'<br/>'+raw_addr[450:600]+'<br/>'+raw_addr[600:]
                    # address = '<link href="' + raw_addr + '">' + address + '</link>'
                    profLic.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    
                    f = Frame(14.1*cm, (-1.3+rightSpacing)*cm, 6.8*cm, 3.4*cm, showBoundary=0)
                    f.addFromList(profLic,pdf)
            
            pdf.setFillColorRGB(255,255,255) 
            pdf.setFont('Vera', 8);
            pdf.drawString(19.8*cm,(0.9)*cm,d2)   
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

def template4(request,userId=None):
   
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
           
            city            =x[46]
                
            state            =x[47]
                
            cityState=x[46]+', '+x[47]
            
            university            =x[48]
            if university:
                univ=university.split(';')
            else:
                univ=''
             
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
            editCompleted =x[91]
            webSite =x[92]
            if not webSite:
                webSite ='NA'
            degreeType =x[93]
            estSavings =x[94]
            if not estSavings:
                estSavings ='NA'
            ####image data
            
            imageId            =x[95]
            person_image            =x[96]
            home_image            =x[97]
            name            =x[98]
            dateAndTime            =x[99]
            personImageFlag            =x[100]
            homeImageFlag            =x[101]
            # print(person_image)
           
            profileString = person_image.decode()
            if personImageFlag == 2:
                img = imread(io.BytesIO(base64.b64decode(profileString)))
                 # show image
                plt.figure()
                plt.imshow(img, cmap="gray")
                
                cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite("profileImage.jpg", cv2_img)
                plt.show()
            else:
                profileString = profileString[22:]

                # print(profileString)

                im = Image.open(BytesIO(base64.b64decode(profileString)))
                im.save('profileImage.jpg', 'PNG')
           
            houseString = home_image.decode()
            if homeImageFlag == 2:
                # reconstruct image as an numpy array
                img1 = imread(io.BytesIO(base64.b64decode(houseString)))

                # show image
                plt.figure()
                plt.imshow(img1, cmap="gray")
                
                cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
                cv2.imwrite("houseImage.jpg", cv2_img1)
                plt.show()
            else:
                houseString = houseString[22:]
                
                im1 = Image.open(BytesIO(base64.b64decode(houseString)))
                im1.save('houseImage.jpg', 'PNG')
                
        
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
         
         
         
         #######################################Tepmlate1#######################################
        
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
        
        # print('personImageFlag',personImageFlag)
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
            
        
        if JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA': 
            # nameHeight=2
            nameHeight=0
            # pdf.line(lineMargin1*cm,(27.4)*cm,lineMargin2*cm,(27.4)*cm)
        else:
            nameHeight=0
        
        
        pdf.drawCentredString((noImageMargin/2)*cm,(28.8-nameHeight)*cm,FullName.upper());
        # pdf.setDash([2,2,2,2],0)
        pdf.line(lineMargin1*cm,(28.6-nameHeight)*cm,lineMargin2*cm,(28.6-nameHeight)*cm)
        # pdf.setDash([0,0,0,0],0)
        pdf.setFont('Vera', 14);


        if len(Job_Desc) >=90:
                jobFont=9
        else:
                jobFont=14
                
        ##################################JOBS DISPLAY #############################   
       
        
        if JOB2 =='NA' and comp2 != 'NA':
            job2Height=0.5
        else:
            job2Height=0
            jobsHeight=0
        
        
        
        ##################################JOBS DISPLAY #############################            
          
        if personImageFlag == 2:
            # print('skipp')
            
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
        
        
        if personImageFlag == 2:
            shiftSaving = 4
        else:
            shiftSaving = 0
        if Addr == 1:
            if estSavings !='NA':
                pdf.drawImage('/home/pdfImages/personHome.png',(4.5)*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                pdf.setFillColorRGB(0,0,0)
                pdf.drawImage('/home/pdfImages/savingsIcon.png', (0.25+shiftSaving)*cm, 27.6*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.drawImage('/home/pdfImages/savingRight.png', (1.25+shiftSaving)*cm, 27.7*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.drawImage('/home/pdfImages/savingsLeft.png',(9+shiftSaving)*cm, 27.7*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.setFont('VeraBI', 11);
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString((1.5+shiftSaving)*cm,27.9*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                pdf.setFillColorRGB(255,0,0)
                pdf.drawString((9.5+shiftSaving)*cm,27.9*cm,estSavings);
                pdf.setFillColorRGB(0,0,0)
                
                pdf.drawImage('/home/pdfImages/personHome.png',4.5*cm,(26.8)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                if houseType =='Rented Apartment' or houseType =='Apartment':
                    pdf.drawImage('/home/pdfImages/rentedApt.png',1*cm,(18.8)*cm,10.5*cm,8*cm,preserveAspectRatio=False);
                    print('dddd')
                else:
                    pdf.drawImage('houseImage.jpg',1*cm,(18.8)*cm,10.5*cm,8*cm,preserveAspectRatio=False);
                
                pdf.roundRect(1*cm, (18.8)*cm, 10.5*cm, 8*cm, 4, stroke=1, fill=0);
            else:
                pdf.drawImage('/home/pdfImages/personHome.png',4.7*cm,(26.9)*cm,4*cm,0.5*cm,preserveAspectRatio=False);
                if houseType =='Rented Apartment' or houseType =='Apartment':
                    pdf.drawImage('/home/pdfImages/rentedApt.png',2*cm,(18.8)*cm,10.5*cm,8*cm,preserveAspectRatio=False);
                    
                else:
                    pdf.drawImage('houseImage.jpg',1*cm,(18.8)*cm,10.5*cm,8*cm,preserveAspectRatio=False);
                
                pdf.roundRect(1*cm, (18.8)*cm, 10.5*cm, 8*cm, 4, stroke=1, fill=0);
           
            pdf.setFont('VeraBd', 9);
            
            pdf.drawCentredString(6.5*cm,(17.25)*cm,Address+', '+city+', '+state.title()+' '+pincode);
            
            if houseType =='Rented Apartment' or houseType =='Rented': 
                pdf.drawImage('/home/pdfImages/rented.png',5.25*cm,(17.8)*cm,2.75*cm,0.6*cm,preserveAspectRatio=False);
            if houseType =='For Sale':  
                pdf.drawImage('/home/pdfImages/sale.png',5.25*cm,(17.8)*cm,2.75*cm,0.8*cm,preserveAspectRatio=False);
            
            if homeEqu1 == '$0':
                shiftHomeVal=3.25
                eqFontSize=12
            else:
                shiftHomeVal=0
                eqFontSize=8 
                # pdf.drawImage('/home/pdfImages/dot.png',(1+shiftHomeVal)*cm,(16.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            if homeValu1 !='$0' and homeEqu1 == '$0':
                pdf.setFont('VeraBd', eqFontSize);
                pdf.drawCentredString((3.125+shiftHomeVal)*cm,(16.3)*cm,"ESTIMATED HOME VALUE");
                pdf.setFont('VeraBd', eqFontSize);
                pdf.drawCentredString((3.125+shiftHomeVal)*cm,(15.7)*cm,homeValu1);

                
            
            if homeEqu1 != '$0':
                pdf.setFont('VeraBd', 8);
                pdf.drawCentredString((3.125+shiftHomeVal)*cm,(16.2)*cm,"ESTIMATED HOME VALUE");
                pdf.setFont('VeraBd', 8);
                pdf.drawCentredString((3.125+shiftHomeVal)*cm,(15.7)*cm,homeValu1);
                pdf.setLineWidth(0.5);
                pdf.line(6.25*cm,(16.5)*cm,6.25*cm,(15.65)*cm)
                # pdf.drawImage('/home/pdfImages/dot.png',7.20*cm,(16.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawCentredString(9.375*cm,(16.2)*cm,"ESTIMATED HOME EQUITY");
                pdf.setFont('VeraBd', 8);
                pdf.drawCentredString(9.375*cm,(15.7)*cm,homeEqu1);
        
        ####DIVORCED IMG
        
        # pdf.drawImage('/home/pdfImages/divorce.png',2.55*cm,(10.4)*cm,3.8*cm,2*cm,preserveAspectRatio=False, mask='auto');    
        if spouse_name != 'NA' or  edu1 != 'NA' or univ1 != 'NA' or edu2 != 'NA' or univ2 != 'NA': 
            pdf.line(1.3*cm,(15.5)*cm,11.2*cm,(15.5)*cm)
        
        
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
               
           
         ############################# About Family ################################
        
        if edu1 == 'NA' and edu2 == 'NA' and univ1 == 'NA' and univ2 == 'NA':
            qualiHeight = 0
        else:
            qualiHeight = 0
        
        if spouse_name == 'NA' :
            spouseHeight= 8+qualiHeight;
        elif edu1 == 'NA' and edu2 == 'NA' and univ1 == 'NA' and univ2 == 'NA' and spouse_name != 'NA':
            spouseHeight= qualiHeight;
        else:
            spouseHeight= 0;
        
        if vehicle1 == 'NA' and vehicle2 == 'NA' and vehicle3 == 'NA' :
            # vehicleHeight=2
            vehicleHeight=0
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
        
      ##################################################LEFT 2nd HALF ##############################################
        
        if spouse_name != 'NA' :
            if relationStatus != 'NA' : 
                pdf.setFillColorRGB(1,0,0.2)
                pdf.setFont('Vera', 12);
                pdf.drawString(7*cm,(14.7+qualiHeight)*cm,'['+relationStatus+']');
                pdf.setFillColorRGB(0,0,00)
            pdf.drawImage('/home/pdfImages/family.png',0.75*cm,(14.5+qualiHeight)*cm,9.5*cm,0.65*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawImage('/home/pdfImages/business.png',1.5*cm,(13.25+qualiHeight)*cm,0.5*cm,1*cm,preserveAspectRatio=False, mask='auto');
         
            pdf.setFont('VeraBd', 12);
            if Spouse_Age == 'NA':
                pdf.drawString(2.3*cm,(13.55+qualiHeight)*cm,spouse_name);
            else:
                pdf.drawString(2.3*cm,(13.8+qualiHeight)*cm,spouse_name);
            
            if Spouse_Age != 'NA':
                pdf.setFont('Vera', 9);
                pdf.drawString(2.3*cm,(13.3+qualiHeight)*cm,Spouse_Age);
            
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
                    if estSavings !='NA': 
                        pdf.drawImage('/home/pdfImages/salaryNew.png', 1.5*cm, (10.2+qualiHeight+spEduHt)*cm, width=9.8*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                        pdf.setFont('VeraBd', 11);
                        
                        pdf.drawString(2*cm,(10.4+qualiHeight+spEduHt)*cm,"ESTIMATED YEARLY SALARY:  ")
                        pdf.setFillColorRGB(255,0,0)
                        pdf.drawString(8.5*cm,(10.4+qualiHeight+spEduHt)*cm,Dep_Salary);
                    else:
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
            if spBank1 != 'NA' and spBank1 != 'None':
                    
                    pdf.setFont('Vera', 12);
                    pdf.drawImage('/home/pdfImages/spouseBank.png',1.5*cm,(7.35+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(2.2*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'POSSIBLE BANKRUPTCIES');
                    pdf.drawImage('/home/pdfImages/checked.png',8*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(8.9*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1);
                    # pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
                    
                    pdf.setFont('Vera', 9);      
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year    Filing Status');
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year');
                    
                    # pdf.drawImage('/home/pdfImages/arrow_blue.png',1.75*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    # pdf.drawString(2.25*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1)
                    
                    # if spBankDet1 != 'NA':
                        # pdf.drawString(3.35*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBankDet1)
       
   
        ############################# About Family ################################
         
         
        ###########################VEHICLES DETAILS#################################
            if spBank1 == 'NA' and spBankDet1 == 'NA':
                spBankHt = 1.5
            else: 
                spBankHt = 0.65
            spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
            # spouseSpacing = 0;
            
            if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
            else:
            
                if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
                pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
            
        else:
            if spBank1 == 'NA' and spBankDet1 == 'NA':
                spBankHt = 1.5
            else: 
                spBankHt = 0.65
            # spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
            spouseSpacing = 0;
            spouseHeight = 6;
            
            if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
            else:
            
                if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
                pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
            
        pdf.drawImage('/home/pdfImages/Disclaimer.png',0.06*cm,(0.05)*cm,21*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
    
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
        
        # webSite = "https://www.doctorquick.com/"
        # webSite = "NA"
        
        if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
            socialHght = 6
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 3.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 3.5
            
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        
        elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 2.5
            
            
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 2.5
        
        
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
            socialHght = 1.25
        elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
            socialHght = 1.25
        elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
            socialHght = 1.25
        
            
        else:
            socialHght = 0
        
        
        rightSpacing = socialHght-1.2
        # print('rightSpacing',rightSpacing)
        pdf.setFillColorRGB(255,255,255)
        
        if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
            
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
            
            raw_addr2 = Per_LinkedIn
            address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
            address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
            ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
           
            f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(ld_url,pdf)
            
            pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            gmail_url = []
            
            raw_addr3 = per_Email
            address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
            address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
            gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

            f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
            f.addFromList(gmail_url,pdf)
            
            
            
            pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.75*cm,13*cm,Per_Tel)
                            
            pdf.drawImage('/home/pdfImages/link.png',13.5*cm,11.45*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
            website = []
            raw_addr4 = webSite
            address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
            address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
            website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
            
            f = Frame(14.5*cm, 10.8*cm, 6*cm, 1.8*cm, showBoundary=0)
            f.addFromList(website,pdf)
    
    
        if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA' or webSite != 'NA': 
            print('website')
            pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
            
            if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                 
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
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

            elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
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
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                
                f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
                                      
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr2 = per_Email
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
              
            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
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

            elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
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
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
                
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
               
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                
                f = Frame(14.5*cm, 14.3*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
            
            elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and webSite == 'NA':
            
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
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                

                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
             
            elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
             
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
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                
                
                
                pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)

                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
                

                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
                    
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 12*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                fb_url = []
                raw_addr = Per_facebook
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(fb_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                print('Per_facebook',Per_facebook)
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                                    
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
                
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                ld_url = []
                raw_addr = Per_LinkedIn
                address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                                    
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
            
              
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                raw_addr = per_Email
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                address = '<link href="' + raw_addr + '">' + address + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                f = Frame(14.5*cm, 15.5*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
              

        
        # pdf.drawString(13.7*cm,(12.2)*cm,'________________________________________________') 
        
        contactHeight+=2.65 # comment it when hobbies are needed in the report
           
         ################### Removed as per client requirement dated on 24-01-2020 ########################
      
        ################### Criminal History,Bankruptcies,Evictions ##########################
        
        
        if corDate1 != 'NA' and corDate2 != 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');#Removed as per clients requirement dated on 24012020
            pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS ');
            if corDate1 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
                # print('len:',len(CHOdate1))
                pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
            if corDate2 !='NA':
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(10.78+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(10.78+rightSpacing)*cm,corDate2)
                pdf.drawString(15.5*cm,(10.78+rightSpacing)*cm,corpFile2)
        
            # extraHeight=2
        
        elif corDate1 != 'NA' and corDate2 == 'NA':
            pdf.setFont('Vera', 12);
            pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
            
            # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');
            pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
            pdf.setFont('Vera', 9);
            # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS');
            pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
            
            pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
            pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
        
        
        rightSpacing = 0
        if corDate1 == 'NA' and corDate2 == 'NA':
            corpHght = 2
        elif corDate1 != 'NA' and corDate2 == 'NA':
            corpHght = 0.6
            
        else:
            corpHght = 0.5
        
        rightSpacing = socialHght + corpHght-2
        
        pdf.setFillColorRGB(255,255,255)
        pdf.setFont('Vera', 11);
        pdf.drawString(13.75*cm,(10.5+rightSpacing)*cm,'____________________________________')
        
        pdf.drawString(13.8*cm,(9.7+rightSpacing)*cm,'POSSIBLE JUDGMENTS');
        if judments !='No':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            
        pdf.drawString(13.8*cm,(9+rightSpacing)*cm,'POSSIBLE EVICTIONS');
        if EVFdate1 != 'NA' or EVFdate2 != 'NA':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(19.8*cm,(9+rightSpacing)*cm,EVFdate1)
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
        
        if BRFdate1 != 'NA' and BRFdate1 != 'None' or BRFdate2 != 'NA':
            pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(19.8*cm,(8.35+rightSpacing)*cm,BRFdate1)
        else:
            pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
        pdf.drawString(13.75*cm,(8.1+rightSpacing)*cm,'____________________________________')        
        if len(licences) == 0:
            licenLen=2
        else:
            licenLen=0
        
        if len(licences) == 0 and profLicence != 'NA': 
            rightSpacing += 4.5
        else:
            rightSpacing += 3
            
        if len(licences) == 0 and profLicence == 'NA':
            pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
            pdf.drawString(14.3*cm,(3.65+rightSpacing)*cm,'No Licenses')
        
        else:
                
            if len(licences) != 0:
                pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(3.7+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.setFont('Vera', 9)
                if licence1 !='NA':
                    pdf.drawString(14.25*cm,(3.7+rightSpacing)*cm,licence1)
                if licence2 !='NA':
                    pdf.drawString(14.25*cm,(3.2+rightSpacing)*cm,licence2)
                if licence3 !='NA':
                    pdf.drawString(14.25*cm,(2.7+rightSpacing)*cm,licence3)
            # print('len(licences)',len(licences))
            
            if len(licences) == 0:
                licenHt=0
            elif len(licences) == 1 or len(licences) == 2:   
                licenHt=1
            elif len(licences) == 3 or len(licences) == 4:   
                licenHt=0.5
            
            rightSpacing = rightSpacing+licenHt
            # print('rightSpacing5',rightSpacing)
            print('length:',licenHt)
            if profLicence != 'NA':
                if len(licences) == 0:
                    pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(2.6+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 12);
                    pdf.drawString(14.5*cm,(2.7+rightSpacing)*cm,'LICENSES');
                pdf.setFont('Vera', 9);
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(2.05+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.25*cm,(2.05+rightSpacing)*cm,"Professional Licenses:")
                profLic = []
                pdf.setFillColorRGB(0,0,0)
                raw_addr = profLicence.title()
                address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:450]+'<br/>'+raw_addr[450:600]+'<br/>'+raw_addr[600:]
                # address = '<link href="' + raw_addr + '">' + address + '</link>'
                profLic.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                
                f = Frame(14.1*cm, (-1.3+rightSpacing)*cm, 6.8*cm, 3.4*cm, showBoundary=0)
                f.addFromList(profLic,pdf)
        
        pdf.setFillColorRGB(255,255,255) 
        pdf.setFont('Vera', 8);
        pdf.drawString(19.8*cm,(0.9)*cm,d2)   
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
            editCompleted  =x[91]
            webSite =x[92]
            if not webSite:
                webSite ='NA'
            degreeType =x[93]
            estSavings =x[94]
            if not estSavings:
                estSavings ='NA'
            ####image data
            
            imageId            =x[95]
            person_image            =x[96]
            home_image            =x[97]
            name            =x[98]
            dateAndTime            =x[99]
            personImageFlag            =x[100]
            homeImageFlag            =x[101]
            profileString = person_image.decode()
            if personImageFlag == 2:
                img = imread(io.BytesIO(base64.b64decode(profileString)))
                 # show image
                plt.figure()
                plt.imshow(img, cmap="gray")
                
                cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite("profileImage.jpg", cv2_img)
                plt.show()
            else:
                profileString = profileString[22:]

                # print(profileString)

                im = Image.open(BytesIO(base64.b64decode(profileString)))
                im.save('profileImage.jpg', 'PNG')
           
            houseString = home_image.decode()
            if homeImageFlag == 2:
                # reconstruct image as an numpy array
                img1 = imread(io.BytesIO(base64.b64decode(houseString)))

                # show image
                plt.figure()
                plt.imshow(img1, cmap="gray")
                
                cv2_img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
                cv2.imwrite("houseImage.jpg", cv2_img1)
                plt.show()
            else:
                houseString = houseString[22:]
                
                im1 = Image.open(BytesIO(base64.b64decode(houseString)))
                im1.save('houseImage.jpg', 'PNG')
        
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
         
         
         
         ####################################### Decide Templates #######################################
         
         
         
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
            
            # print('personImageFlag',personImageFlag)
            if personImageFlag == 2:
                noImageMargin = 22
                lineMargin1 = 5.5
                lineMargin2 = 16
                salImgMargin = 8.2
                estSal = 6.5
                estSalImgMargin = 5.8
                estSalVal = 13
                savingIcon = 4.3
                savingRight = 5.3
                savingTitle = 5.5
                savingLeft = 13
                savingVal = 13.6
            else:
               noImageMargin = 12.5
               lineMargin1 = 2
               lineMargin2 = 10.5
               salImgMargin = 3.3
               estSal = 2
               estSalImgMargin = 1.25
               estSalVal = 8.5
               savingIcon = 0.25
               savingRight = 1.1
               savingTitle = 1.3
               savingLeft = 8.8
               savingVal = 9.3
                
            
            if JOB1 == 'NA' and comp1 == 'NA' and JOB2 == 'NA' and comp2 == 'NA' and prevJOB1 == 'NA' and prevJOB2 == 'NA' and prevComp1 == 'NA' and prevComp2 == 'NA': 
                # nameHeight=2
                nameHeight=0
                # pdf.line(lineMargin1*cm,(27.4)*cm,lineMargin2*cm,(27.4)*cm)
            else:
                nameHeight=0
            
            
            pdf.drawCentredString((noImageMargin/2)*cm,(28.8-nameHeight)*cm,FullName.upper());
            # pdf.setDash([2,2,2,2],0)
            pdf.line(lineMargin1*cm,(28.6-nameHeight)*cm,lineMargin2*cm,(28.6-nameHeight)*cm)
            # pdf.setDash([0,0,0,0],0)
            pdf.setFont('Vera', 14);


            if len(Job_Desc) >=90:
                    jobFont=9
            else:
                    jobFont=14
                    
            ##################################JOBS DISPLAY #############################   
           
            
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
                        pdf.drawCentredString((noImageMargin/2)*cm,26.2*cm,JOB2);
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
                # print('skipp')
                
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
                    
                
            if estSavings !='NA':
                if Per_Salary !='NA':
                    pdf.drawImage('/home/pdfImages/salaryNew.png', estSalImgMargin*cm, 24.7*cm, width=9.8*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                    pdf.setFont('VeraBd', 11);
                    pdf.drawString((estSal)*cm,24.9*cm,"ESTIMATED YEARLY SALARY:  ")
                    pdf.setFillColorRGB(255,0,0)
                    pdf.drawString(estSalVal*cm,24.9*cm,Per_Salary);
                
                estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                pdf.setFillColorRGB(0,0,0)
                pdf.drawImage('/home/pdfImages/savingsIcon.png', savingIcon*cm, 23.85*cm, width=0.8*cm, height=0.8*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.drawImage('/home/pdfImages/savingRight.png', savingRight*cm, 23.9*cm, width=8.5*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                # pdf.drawImage('/home/pdfImages/retirment.png', 1.1*cm, 23.9*cm, width=10.25*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.drawImage('/home/pdfImages/savingsLeft.png', savingLeft*cm, 23.9*cm, width=3*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                pdf.setFont('VeraBI', 11);
                pdf.setFillColorRGB(255,255,255)
                pdf.drawString(savingTitle*cm,24.1*cm,"ESTIMATED RETIREMENT SAVINGS:  ");
                pdf.setFillColorRGB(255,0,0)
                pdf.drawString(savingVal*cm,24.1*cm,estSavings);
                # pdf.drawCentredString((noImageMargin/2)*cm,25*cm,"ESTIMATED YEARLY SALARY:  "+Per_Salary);
                # estSavings = custom_format_currency(estSavings, 'USD', locale='en_US')
                # pdf.drawCentredString((noImageMargin/2)*cm,24.4*cm,"ESTIMATED RETIREMENT SAVINGS:  "+estSavings);
            else:       
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
                    
                if homeEqu1 == '$0':
                    shiftHomeVal=3.25
                    eqFontSize=12
                else:
                    shiftHomeVal=0
                    eqFontSize=8
                    # pdf.drawImage('/home/pdfImages/dot.png',(0.75+shiftHomeVal)*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                print('shiftHomeVal',shiftHomeVal)    
                    
                if homeValu1 !='$0' and homeEqu1 == '$0':
                    
                    pdf.setFont('VeraBd', eqFontSize);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2)*cm,"ESTIMATED HOME VALUE");
                    pdf.setFont('VeraBd', eqFontSize);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(18.6)*cm,homeValu1);

                if homeEqu1 != '$0':
                    pdf.setFont('VeraBd', 9);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(19.2)*cm,"ESTIMATED HOME VALUE");
                    pdf.setFont('VeraBd', 9);
                    pdf.drawCentredString((3.125+shiftHomeVal)*cm,(18.6)*cm,homeValu1);
                    
                    pdf.setLineWidth(0.5);
                    pdf.line(6.25*cm,(19.5)*cm,6.25*cm,(18.65)*cm)
                    # pdf.drawImage('/home/pdfImages/dot.png',7*cm,(19.2)*cm,0.2*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(9.375*cm,(19.2)*cm,"ESTIMATED HOME EQUITY");
                    pdf.setFont('VeraBd', 9);
                    pdf.drawCentredString(9.375*cm,(18.6)*cm,homeEqu1);
               
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
                        
                        pdf.drawString(5.6*cm,(22.03)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(9.6*cm,(22.03)*cm,homeEqu1);
                        pdf.setFont('Vera', 8);
                    if homeEqu1 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    # pdf.drawCentredString(7.7*cm,(21.45)*cm,Esti_Home_Equi);
                    # print('homeValu1',homeValu1)
                    if homeValu1 != '$0':
                        
                        pdf.drawString(5.6*cm,(21.63+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(9.4*cm,(21.63+homeHeight+Equiheight)*cm,homeValu1);
                        pdf.setFont('Vera', 8);
                    
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
                        
                        pdf.drawString(5.6*cm,(20.53)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(9.6*cm,(20.53)*cm,homeEqu2);
                        pdf.setFont('Vera', 8);
                    if homeEqu2 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu2 != '$0':
                        
                        pdf.drawString(5.6*cm,(20.13+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(9.4*cm,(20.13+homeHeight+Equiheight)*cm,homeValu2);
                        pdf.setFont('Vera', 8);
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
                        
                        pdf.drawString(5.6*cm,(19.03)*cm,"ESTIMATED HOME EQUITY: ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(9.6*cm,(19.03)*cm,homeEqu3);
                        
                        pdf.setFont('Vera', 8);
                    if homeEqu3 == '$0':
                        Equiheight = 0.35;
                    else:
                        Equiheight = 0;
                    if homeValu3 != '$0':
                        
                        pdf.drawString(5.6*cm,(18.63+homeHeight+Equiheight)*cm,"ESTIMATED HOME VALUE:  ");
                        pdf.setFont('VeraBd', 8);
                        pdf.drawString(9.4*cm,(18.63+homeHeight+Equiheight)*cm,homeValu3);
                        pdf.setFont('Vera', 8);
                
           
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
                # vehicleHeight=2
                vehicleHeight=0
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
            
          ##################################################LEFT 2nd HALF ##############################################
            
            if spouse_name != 'NA' :
                if relationStatus != 'NA' : 
                    pdf.setFillColorRGB(1,0,0.2)
                    pdf.setFont('Vera', 12);
                    pdf.drawString(7*cm,(14.7+qualiHeight)*cm,'['+relationStatus+']');
                    pdf.setFillColorRGB(0,0,00)
                pdf.drawImage('/home/pdfImages/family.png',0.75*cm,(14.5+qualiHeight)*cm,9.5*cm,0.65*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawImage('/home/pdfImages/business.png',1.5*cm,(13.25+qualiHeight)*cm,0.5*cm,1*cm,preserveAspectRatio=False, mask='auto');
             
                pdf.setFont('VeraBd', 12);
                if Spouse_Age == 'NA':
                    pdf.drawString(2.3*cm,(13.55+qualiHeight)*cm,spouse_name);
                else:
                    pdf.drawString(2.3*cm,(13.8+qualiHeight)*cm,spouse_name);
                
                if Spouse_Age != 'NA':
                    pdf.setFont('Vera', 9);
                    pdf.drawString(2.3*cm,(13.3+qualiHeight)*cm,Spouse_Age);
                
                if spUni1 !="NA":
                    pdf.drawImage('/home/pdfImages/edu.png',1.25*cm,(12.3+qualiHeight)*cm,0.9*cm,0.7*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFillColorRGB(0.5,0.2,0.1)
                    if spedu1 != 'NA':
                        spUni1=spUni1+','
                        pdf.setFont('Vera', 9);
                        pdf.drawString(2.3*cm,(12.75+qualiHeight)*cm,spUni1.upper());
                    else:
                        pdf.setFont('Vera', 9);
                        pdf.drawString(2.3*cm,(12.55+qualiHeight)*cm,spUni1.upper());
                    pdf.setFillColorRGB(0,0,0)
                if spedu1 !="NA":
                    pdf.drawImage('/home/pdfImages/edu.png',1.25*cm,(12.3+qualiHeight)*cm,0.9*cm,0.7*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 9);
                    pdf.drawString(2.3*cm,(12.35+qualiHeight)*cm,spedu1);
               
                
                if Dep_Designation != 'NA':
                    pdf.drawImage('/home/pdfImages/work.png',1.5*cm,(11.3+qualiHeight+spEduHt)*cm,0.6*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 10);
                    pdf.setFillColorRGB(0,0.5,0.5)
                    
                    if Dep_Employment != 'NA':
                        pdf.drawString(2.3*cm,(11.7+qualiHeight+spEduHt)*cm,Dep_Designation+',');
                    else:
                        pdf.drawString(2.3*cm,(11.5+qualiHeight+spEduHt)*cm,Dep_Designation);
                    
                    if estSavings !='NA': 
                        if Dep_Salary !='NA':
                            pdf.drawImage('/home/pdfImages/salaryNew.png', 1.5*cm, (10.2+qualiHeight+spEduHt)*cm, width=9.8*cm, height=0.7*cm, mask='auto',preserveAspectRatio=False, anchor='c')
                            pdf.setFont('VeraBd', 11);
                            pdf.drawString(2*cm,(10.4+qualiHeight+spEduHt)*cm,"ESTIMATED YEARLY SALARY:  ")
                            pdf.setFillColorRGB(255,0,0)
                            pdf.drawString(8.5*cm,(10.4+qualiHeight+spEduHt)*cm,Dep_Salary);
                    else:
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
                
                # if spBank1 != 'NA' and spBank1 != 'None' and spBank1 != 'None' and spBank1 != 'None' and spouseBankruptDate != 'NA':
                if spBank1 != 'NA' and spBank1 != 'None' and spBank1 != 'None' and spBank1 != 'None' :
                    
                    pdf.setFont('Vera', 12);
                    pdf.drawImage('/home/pdfImages/spouseBank.png',1.5*cm,(7.35+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.5*cm,0.5*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(2.2*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'POSSIBLE BANKRUPTCIES');
                    pdf.drawImage('/home/pdfImages/checked.png',8*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(8.9*cm,(7.4+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1);
                    # pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
                    
                    pdf.setFont('Vera', 9);      
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year    Filing Status');
                    # pdf.drawString(2.25*cm,(7.2+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,'Year');
                    
                    # pdf.drawImage('/home/pdfImages/arrow_blue.png',1.75*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    # pdf.drawString(2.25*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBank1)
                    
                    # if spBankDet1 != 'NA':
                        # pdf.drawString(3.35*cm,(6.8+qualiHeight+spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt)*cm,spBankDet1)
       
       
                ############################# About Family ################################
                 
                 
                ###########################VEHICLES DETAILS#################################
                if spBank1 == 'NA' and spBankDet1 == 'NA':
                    spBankHt = 1.5
                else: 
                    spBankHt = 0.5
                # spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
                spouseSpacing = 0;
               
                
                if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
                else:
                
                    if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                        pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                        # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                        pdf.setFont('VeraBd', 12);
                        pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                        pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                        pdf.setFont('Vera', 10);
                    if vehicle1 !='NA':
                        pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(4.95+spouseHeight+spBankHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                        pdf.drawString(2*cm,(4.95+spouseHeight+spBankHt)*cm,vehicle1);
                    if vehicle2 !='NA':
                        pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(4.25+spouseHeight+spBankHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                        pdf.drawString(2*cm,(4.25+spouseHeight+spBankHt)*cm,vehicle2);
                    
                    if vehicle3 !='NA':
                        pdf.drawImage('/home/pdfImages/arrow_blue.png',1.5*cm,(3.65+spouseHeight+spBankHt)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                        pdf.drawString(2*cm,(3.55+spouseHeight+spBankHt)*cm,vehicle3);
                
                
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
                vehicleHeight = 0.3
                if Input_Pop != 'NA' or Median_HouseHold_Val != 'NA' or medianHouseValue !='NA':
                    pdf.setFont('Vera', 12);
                    pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
                
            else:
                if spBank1 == 'NA' and spBankDet1 == 'NA':
                    spBankHt = 1.5
                else: 
                    spBankHt = 0
                spouseSpacing = spEduHt+spWorkHt+depSalHt+depFbHt+depLinkHt
                # spouseSpacing = 0;
                
                if vehicle1 =='NA' and vehicle2 =='NA' and vehicle3 =='NA':
                    print('NO VEHICLES')
                    pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                    pdf.setFont('VeraBd', 12);
                    pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
                    pdf.setFont('Vera', 10);
                    pdf.drawCentredString(4*cm,(5+spouseHeight+spBankHt)*cm,"No Vehicles");
                else:
                
                    if vehicle1 !='NA' or vehicle2 !='NA' or vehicle3 !='NA':
                        pdf.line(1.3*cm,(6+spouseHeight+spBankHt)*cm,11.2*cm,(6+spouseHeight+spBankHt)*cm)
                        # pdf.drawImage('/home/pdfImages/registered_vehicle.png',1.5*cm,(3.4)*cm,5.5*cm,0.4*cm,preserveAspectRatio=False);
                        pdf.setFont('VeraBd', 12);
                        pdf.drawImage('/home/pdfImages/Car.png',1.5*cm,(5.5+spouseHeight+spBankHt)*cm,0.5*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                        pdf.drawCentredString(4.85*cm,(5.55+spouseHeight+spBankHt)*cm,"REGISTERED Vehicle(s)");
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
                    pdf.roundRect(0.75*cm, (0.4+spouseHeight+vehicleHeight+spBankHt)*cm, 11.5*cm, 2.6*cm, 10, stroke=1, fill=0);
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
                
                pdf.drawCentredString(10.2*cm,(0.8+spouseHeight+vehicleHeight+spBankHt)*cm,medianHouseValue);
            
            pdf.drawImage('/home/pdfImages/Disclaimer.png',0.06*cm,(0.05)*cm,21*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            # f.addFromList(disclaim,pdf)
            
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
            
            # webSite = "https://www.doctorquick.com/"
            # webSite = "NA"
            
            if Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                socialHght = 6
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 4.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 4.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 4.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 4.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 4.5
                
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 3.5
                
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 3.5
                
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 3.5
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 3.5
                
            
            elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5        
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 2.5
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 2.5
            
            
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':   
                socialHght = 1.25
            elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 1.25
            elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 1.25
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':   
                socialHght = 1.25
            elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':   
                socialHght = 1.25   
            else:
                socialHght = 0
            
            
            rightSpacing = socialHght-1.2
            # print('rightSpacing',rightSpacing)
            pdf.setFillColorRGB(255,255,255)
            
            if Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                
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
                
                raw_addr2 = Per_LinkedIn
                address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
               
                f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(ld_url,pdf)
                
                pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                gmail_url = []
                
                raw_addr3 = per_Email
                address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                f.addFromList(gmail_url,pdf)
                
                
                
                pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.drawString(14.75*cm,13*cm,Per_Tel)
                                
                pdf.drawImage('/home/pdfImages/link.png',13.5*cm,11.45*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                website = []
                raw_addr4 = webSite
                address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                
                f = Frame(14.5*cm, 10.8*cm, 6*cm, 1.8*cm, showBoundary=0)
                f.addFromList(website,pdf)
        
        
            if Per_facebook != 'NA' or Per_LinkedIn != 'NA' or per_Email != 'NA' or Per_Tel != 'NA' or webSite != 'NA': 
                print('website')
                pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                
                if Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    fb_url = []
                    raw_addr = Per_facebook
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(fb_url,pdf)
                
                elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr = Per_LinkedIn
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                     
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    
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

                elif Per_LinkedIn != 'NA' and Per_facebook != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    
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
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                elif per_Email != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and Per_Tel == 'NA' and webSite == 'NA':
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    
                    gmail_url = []
                    raw_addr = per_Email
                    address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                    address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                                    
                    f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.6*cm,16.6*cm,Per_Tel)
                
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
                                          
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr2 = per_Email
                    address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                    address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                    f = Frame(14.5*cm, 15.4*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.6*cm,15.4*cm,Per_Tel)
                  
                elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
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

                elif Per_Tel == 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
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
                    address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                    address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))

                    f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and webSite == 'NA':
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
                
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
                    
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
                   
                elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and webSite == 'NA':
                    pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    fb_url = []
                    raw_addr = Per_facebook
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[56:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))

                    f = Frame(14.5*cm, 15.6*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(fb_url,pdf)

                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    # raw_addr2 = 'http://www.linked.com/Mimsy/hacks/adding-links-to-pdf/'
                    raw_addr2 = per_Email
                    address2 = raw_addr2[0:150]+'<br/>'+raw_addr2[150:300]+'<br/>'+raw_addr2[300:]
                    address2 = '<link href="mailto:' + raw_addr2 + '">' + address2 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    
                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.65*cm,14.25*cm,Per_Tel)
                
                elif Per_Tel != 'NA' and Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and webSite == 'NA':
                
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
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))

                    f = Frame(14.5*cm, 14.2*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    

                    pdf.setFillColorRGB(255,255,255)
                    pdf.drawString(14.7*cm,14.2*cm,Per_Tel)
                 
                elif Per_Tel != 'NA' and Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and webSite == 'NA':
                 
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
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite == 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)

                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                
                elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                    
                    
                    
                    pdf.drawImage(linkedinLogo,13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)

                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                
                elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    fb_url = []
                    raw_addr = Per_facebook
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(fb_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))

                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                    

                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,13*cm,Per_Tel)
                        
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email != 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr3 = per_Email
                    address3 = raw_addr3[0:150]+'<br/>'+raw_addr3[150:300]+'<br/>'+raw_addr3[300:]
                    address3 = '<link href="mailto:' + raw_addr3 + '">' + address3 + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address3+'</font>',styleN))
                    f = Frame(14.5*cm, 13*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,12.6*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 12*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook != 'NA' and Per_LinkedIn == 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(facebookLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    fb_url = []
                    raw_addr = Per_facebook
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    fb_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(fb_url,pdf)
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
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
                    raw_addr2 = Per_LinkedIn
                    address2 = raw_addr2[0:28]+'<br/>'+raw_addr2[28:58]+'<br/>'+raw_addr2[58:]
                    address2 = '<link href="' + raw_addr2 + '">' + address2 + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address2+'</font>',styleN))
                    f = Frame(14.5*cm, 14.3*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                    
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook == 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    print('Per_facebook',Per_facebook)
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr = Per_LinkedIn
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                                        
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook != 'NA' and Per_LinkedIn != 'NA' and per_Email == 'NA' and Per_Tel == 'NA' and webSite != 'NA':
                    
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage(linkedinLogo,13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    ld_url = []
                    raw_addr = Per_LinkedIn
                    address = raw_addr[0:25]+'<br/>'+raw_addr[25:56]+'<br/>'+raw_addr[57:]
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    ld_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.6*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(ld_url,pdf)
                                        
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                
                elif Per_facebook == 'NA' and Per_LinkedIn == 'NA' and per_Email != 'NA' and Per_Tel != 'NA' and webSite != 'NA':
                    
                    pdf.drawImage('/home/pdfImages/Contact_info.png',16.5*cm,17.55*cm,3.8*cm,1.5*cm,preserveAspectRatio=False, mask='auto' );
                    
                    pdf.drawImage('/home/pdfImages/Mail.png',13.5*cm,16.2*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    gmail_url = []
                    raw_addr = per_Email
                    address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:]
                    address = '<link href="mailto:' + raw_addr + '">' + address + '</link>'
                    address = '<link href="' + raw_addr + '">' + address + '</link>'
                    gmail_url.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    f = Frame(14.5*cm, 15.5*cm, 6.5*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(gmail_url,pdf)
                    
                    
                    pdf.drawImage('/home/pdfImages/Call_Icon.png',13.5*cm,15*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.75*cm,15.4*cm,Per_Tel)
                    
                    pdf.drawImage('/home/pdfImages/link.png',13.5*cm,13.8*cm,1*cm,1*cm,preserveAspectRatio=False, mask='auto');
                    website = []
                    raw_addr4 = webSite
                    address4 = raw_addr4[0:25]+'<br/>'+raw_addr4[25:56]+'<br/>'+raw_addr4[57:]
                    address4 = '<link href="' + raw_addr4 + '">' + address4 + '</link>'
                    website.append(Paragraph('<font color="white">'+address4+'</font>',styleN))
                    f = Frame(14.5*cm, 13.25*cm, 6*cm, 1.8*cm, showBoundary=0)
                    f.addFromList(website,pdf)
                  

            
            # pdf.drawString(13.7*cm,(12.2)*cm,'________________________________________________') 
            
            contactHeight+=2.65 # comment it when hobbies are needed in the report
               
             ################### Removed as per client requirement dated on 24-01-2020 ########################
          
            ################### Criminal History,Bankruptcies,Evictions ##########################
            
            
            if corDate1 != 'NA' and corDate2 != 'NA':
                pdf.setFont('Vera', 12);
                pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawImage('/home/pdfImages/Bullet.png',13.65*cm,(7)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');#Removed as per clients requirement dated on 24012020
                pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
                pdf.setFont('Vera', 9);
                # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS ');
                if corDate1 !='NA':
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    # pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(7.25)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
                    # print('len:',len(CHOdate1))
                    pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
                if corDate2 !='NA':
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(10.78+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.25*cm,(10.78+rightSpacing)*cm,corDate2)
                    pdf.drawString(15.5*cm,(10.78+rightSpacing)*cm,corpFile2)
            
                # extraHeight=2
            
            elif corDate1 != 'NA' and corDate2 == 'NA':
                pdf.setFont('Vera', 12);
                pdf.drawImage('/home/pdfImages/Filing.png',13.65*cm,(11.8+rightSpacing)*cm,0.6*cm,0.4*cm,preserveAspectRatio=False, mask='auto');
                
                # pdf.drawString(14.5*cm,(8.95)*cm,'CRIMINAL HISTORY');
                pdf.drawString(14.5*cm,(11.8+rightSpacing)*cm,'CORPORATE FILINGS');
                pdf.setFont('Vera', 9);
                # pdf.drawString(14.25*cm,(8.45)*cm,'CORPORATE FILINGS');
                pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(11.3+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                
                pdf.drawString(14.25*cm,(11.34+rightSpacing)*cm,corDate1)
                pdf.drawString(15.5*cm,(11.34+rightSpacing)*cm,corpFile1)
            
            
            rightSpacing = 0
            if corDate1 == 'NA' and corDate2 == 'NA':
                corpHght = 2
            elif corDate1 != 'NA' and corDate2 == 'NA':
                corpHght = 0.8
                
            else:
                corpHght = 0.5
            
            rightSpacing = socialHght + corpHght-2
            
            pdf.setFillColorRGB(255,255,255)
            pdf.setFont('Vera', 11);
            pdf.drawString(13.75*cm,(10.5+rightSpacing)*cm,'____________________________________')
            
            pdf.drawString(13.8*cm,(9.7+rightSpacing)*cm,'POSSIBLE JUDGMENTS');
            if judments !='No':
                pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            else:
                pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(9.5+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                
            pdf.drawString(13.8*cm,(9+rightSpacing)*cm,'POSSIBLE EVICTIONS');
            if EVFdate1 != 'NA'  or EVFdate2 != 'NA':
                pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(19.8*cm,(9+rightSpacing)*cm,EVFdate1)
            else:
                pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.8+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(13.8*cm,(8.3+rightSpacing)*cm,'POSSIBLE BANKRUPTCIES');
            
            if BRFdate1 != 'NA' and BRFdate1 != 'None' or BRFdate2 != 'NA':
                pdf.drawImage('/home/pdfImages/checked.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(19.8*cm,(8.35+rightSpacing)*cm,BRFdate1)
            else:
                pdf.drawImage('/home/pdfImages/blank.png',18.9*cm,(8.1+rightSpacing)*cm,0.8*cm,0.8*cm,preserveAspectRatio=False, mask='auto');
            pdf.drawString(13.75*cm,(8.1+rightSpacing)*cm,'____________________________________')       
            if len(licences) == 0:
                licenLen=2
            else:
                licenLen=0
            if len(licences) == 0 and profLicence != 'NA': 
                rightSpacing += 4.5
            else:
                rightSpacing += 3
                
            if len(licences) == 0 and profLicence == 'NA':
                pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
                pdf.drawString(14.3*cm,(3.65+rightSpacing)*cm,'No Licenses')
            
            else:
                
                if len(licences) != 0:
                    pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(4.1+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.5*cm,(4.2+rightSpacing)*cm,'LICENSES');
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(3.7+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.setFont('Vera', 9)
                    if licence1 !='NA':
                        pdf.drawString(14.25*cm,(3.7+rightSpacing)*cm,licence1)
                    if licence2 !='NA':
                        pdf.drawString(14.25*cm,(3.2+rightSpacing)*cm,licence2)
                    if licence3 !='NA':
                        pdf.drawString(14.25*cm,(2.7+rightSpacing)*cm,licence3)
                # print('len(licences)',len(licences))
                
                if len(licences) == 0:
                    licenHt=0
                elif len(licences) == 1 or len(licences) == 2:   
                    licenHt=1
                elif len(licences) == 3 or len(licences) == 4:   
                    licenHt=0.5
                
                rightSpacing = rightSpacing+licenHt
                # print('rightSpacing5',rightSpacing)
                print('length:',licenHt)
                if profLicence != 'NA':
                    if len(licences) == 0:
                        pdf.drawImage('/home/pdfImages/Licenses.png',13.65*cm,(2.6+rightSpacing)*cm,0.5*cm,0.45*cm,preserveAspectRatio=False, mask='auto');
                        pdf.setFont('Vera', 12);
                        pdf.drawString(14.5*cm,(2.7+rightSpacing)*cm,'LICENSES');
                    pdf.setFont('Vera', 9);
                    pdf.drawImage('/home/pdfImages/Bullet_2.png',13.75*cm,(2.05+rightSpacing)*cm,0.3*cm,0.2*cm,preserveAspectRatio=False, mask='auto');
                    pdf.drawString(14.25*cm,(2.05+rightSpacing)*cm,"Professional Licenses:")
                    profLic = []
                    pdf.setFillColorRGB(0,0,0)
                    raw_addr = profLicence.title()
                    address = raw_addr[0:150]+'<br/>'+raw_addr[150:300]+'<br/>'+raw_addr[300:450]+'<br/>'+raw_addr[450:600]+'<br/>'+raw_addr[600:]
                    # address = '<link href="' + raw_addr + '">' + address + '</link>'
                    profLic.append(Paragraph('<font color="white">'+address+'</font>',styleN))
                    
                    f = Frame(14.1*cm, (-1.3+rightSpacing)*cm, 6.8*cm, 3.4*cm, showBoundary=0)
                    f.addFromList(profLic,pdf)
            
            pdf.setFillColorRGB(255,255,255) 
            pdf.setFont('Vera', 8);
            pdf.drawString(19.8*cm,(0.9)*cm,d2)   
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
                    recipients = 'jmaddux@franchampion.com,kumar@greettech.com,rkburnett@hotmail.com,atlq1@greettech.com,reena@greettech.com,at@greettech.com'
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
                            msg["Cc"] = "jmaddux@franchampion.com,kumar@greettech.com,rkburnett@hotmail.com,atlq1@greettech.com,reena@greettech.com,at@greettech.com"
                           
                                                        
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

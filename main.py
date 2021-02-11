import requests
import os
import shutil
from fpdf import FPDF
numPage = input("Δώσε το εύρος των σελίδων:")
while int(numPage) < 0:#validity check
    print("Το εύρος των σελίδων δεν γίνεται να είναι αρνητικό.")
    numPage = input("Δώσε το εύρος των σελίδων:")
site = input("Διάλεξε ενα site:\n1.pubhtml5\n2.Αλλο\n")
while True:#choose between pubhtml5 or custom url
    if(site=="1" or site=="2"):
        break
    else:
        print("Έκανες λάθος δώσε το 1 η το 2")
        site = input("Διάλεξε μια ιστοσελίδα:\n1.pubhtml5\n2.Αλλο\n")
while True:
    try:
        URL = (input("Δώσε τον σύνδεσμο του βιβλίου(π.χ http://online.pubhtml5.com/mkyj/sswg/):\n")).strip()
        requests.get(URL)
        break
    except requests.exceptions.MissingSchema:#if the url doesn't include the http header
        URL= str("http://") + URL.strip()
        break
    except:
            print("Δεν έδωσες σωστό σύνδεσμο.")
outputPDF = input("Δώσε το όνομα του αρχείου που θες να έχει το βιβλίο:\n")
try:
    os.mkdir("Images")
except FileExistsError:
    shutil.rmtree("Images",ignore_errors=True)
    os.mkdir("Images")
print("Λήψη εικόνων...")
for i in range(1,(int(numPage)+1)):#start from page 1 up to 2
    print(str(i)+"/"+str(numPage)) #print loading process
    if(site=="1"):#if site is pub5html
        if(URL.endswith("/")): #if the url includes / at the end of itself
            updatedUrl = URL.strip()+ "files/large/" + str(i).strip() + ".jpg" #add the image location of pub5html
        else:
            updatedUrl = URL.strip() + "/files/large/" + str(i).strip() + ".jpg"
    else:#if the site is other(custom url)
        updatedUrl = URL.strip() + str(i).strip() + '.jpg'.strip()
    p = requests.get(updatedUrl)
    with open('Images/'.strip()+str(i).strip()+'.jpg'.strip(),'wb') as f:
        f.write(p.content)#download image
print("Ολοκληρώθηκε η λήψη εικόνων\nΔημιουργία αρχείου...")
pdf = FPDF()
#try:
for i in range(1,int(numPage)+1):
        pdf.add_page()#add blank pages to pdf file
        try:
            pdf.image('Images/'+str(i)+".jpg",0,0,215) #add the downloaded images to pdf file
        except RuntimeError:
            break
#except:
    #print("test")
pdf.output(str(outputPDF).strip() + '.pdf', "F")
shutil.rmtree("Images", ignore_errors=True)
print("Η λήψη του βιβλίου " + outputPDF +" ολοκληρώθηκε.")
#except FileExistsError:
#    answer = input("Το αρχειο με όνομα "+ "\""+ outputPDF + "\"" +" υπάρχει ήδη,αντικατάσταση;(Ναι/οχι)")
#   answered = False
#    while(answered==False):
#       if(answer=="Ναι" or answer=="ναι"):
#            os.remove(outputPDF.pdf)
#           pdf.output(str(outputPDF).strip()+'.pdf', "F")
#           answered=True
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import mysql.connector
import exportkeywords
import os, shutil
import sys
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait


allarguments = sys.argv
print(allarguments)

# folder = '/activity'
# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     except Exception as e:
#         print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        
if(allarguments[1]=="-l"):
#liveserver
    mydb = mysql.connector.connect(host = "livehostname", user = "username",passwd = "password",database = "version1")
    cur = mydb.cursor(buffered=True)
else:
#testserver
    mydb = mysql.connector.connect(host = "testhostname", user = "testmaster",passwd = "testpassword",database = "version1")
    cur = mydb.cursor(buffered=True)   
 
try:
   if(allarguments[2]=="-A"):
        cur.execute("select url as drname from  linkedinanalytics ")  
        myresult = cur.fetchall()
        doctorname=[item for t in myresult for item in t] 
except: 
    print("in the user")
    
try:
    if(allarguments[2]=="-D"):
        cur.execute("select replace(substring_index(url, '/', -2),'/','') from linkedinanalytics where doctorid="+str(allarguments[3]))  
        myresult = cur.fetchall()
        doctorname=[item for t in myresult for item in t]
except: 
    print("in the dr")     
    
try:
    if(allarguments[2]=="-U"):
        cur.execute("select replace(substring_index(url, '/', -2),'/','')  from linkedinanalytics where createdby="+str(allarguments[3]))  
        myresult = cur.fetchall()
        doctorname=[item for t in myresult for item in t]
except: 
    print("in the dr")  
      
chromedriver='C:\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

print(doctorname)


driver.get('https://www.linkedin.com/') 
time.sleep(5)

driver.find_element_by_xpath('/html/body/nav/a[3]').click()

username =driver.find_element_by_xpath('//*[@id="username"]')
password =driver.find_element_by_xpath('//*[@id="password"]')
time.sleep(1)
username.send_keys("kacharekishori91@gmail.com")
password.send_keys("password")
# logging in
driver.find_element_by_xpath("//*[@id='app__container']/main/div[2]/form/div[4]/button").click()
print(doctorname)

for listdrname in doctorname:
    print(listdrname)
    try:
        print(listdrname)
        url = 'https://www.linkedin.com/in/'+str(listdrname)+'/detail/recent-activity/'
        print(url)
        driver.get(url)
        # driver.execute_script("window.open('https://www.linkedin.com/in/"+str(listdrname)+"/detail/recent-activity/'), 'new_window'")

        # driver.execute_script("window.open('https://www.linkedin.com/in/"+listdrname+"'/detail/recent-activity/', 'new_window')")

        for i in range(0,5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        title = driver.find_elements_by_class_name('feed-shared-header__text-view')
        ptitle = driver.find_elements_by_class_name('feed-shared-actor__container-link')
        description =driver.find_elements_by_class_name('feed-shared-text')
        likes =driver.find_elements_by_class_name('social-details-social-counts__reactions-count')
        comments= driver.find_elements_by_class_name('v-align-middle')

        activity=[]
       
        def remove_html_tags(text):
                """Remove html tags from a string"""
                import re
                clean = re.compile('<.*?>')
                return re.sub(clean, '', text)

        for t,p,l,c,d in zip(title,ptitle,likes,comments,description):

                        tit = t.get_attribute("innerHTML")
                        tit =str(remove_html_tags(tit))
                        # print(tit)

                        postt =p.get_attribute("innerHTML")
                        postt =str(remove_html_tags(postt))
                        # print(postt)

                        like =l.get_attribute("innerHTML")
                        like =str(remove_html_tags(like))
                        # print(like)

                        comment =c.get_attribute("innerHTML")
                        comment =str(remove_html_tags(comment))
                        # print(comment)

                        desc =d.get_attribute("innerHTML")
                        desc =str(remove_html_tags(desc))
                        # print(desc)
                        
                        file1 = open("exportedlinkedin.txt", "a")  # append mode 
                        try:
                            file1.write(tit+postt+desc) 
                            file1.close()
                        except:
                            print("no data found")
                        y = {   "title":tit, 
                                "description": desc, 
                                "posttitle": postt,
                                "likes":like,
                                "comments":comment
                                }
                        activity.append(y)   
                        
        print(activity)  
        print(len(activity))  
        sql = "UPDATE linkedinanalytics SET D_activities=%s,merge_date=%s WHERE url like %s"
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        print(timestampStr) 
        cur.execute(sql, (json.dumps(activity),f"{timestampStr}",f"%{listdrname}%"))

        with open('activity/'+str(listdrname) +'.json', 'w') as f:
            json.dump(activity, f, indent=2)
    except:  
        print("Page Does not exist")
        pass
    
                
exportkeywords.exportcsv()

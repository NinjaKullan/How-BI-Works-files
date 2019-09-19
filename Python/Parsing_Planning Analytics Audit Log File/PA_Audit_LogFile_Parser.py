# -*- coding: utf-8 -*-
#importing all needed libraries

import re
import sqlite3
from datetime import datetime, timedelta
import os
import glob

# replace the below with file path where your TM1 logs are located. 
path = '<replace with your file path>'

# mention the path you want the DB to be created.
conn = sqlite3.connect('<replace with your path>\AuditParser.sqlite')
cur = conn.cursor()


# Do some setup, creating tables in the Database for loading data.
cur.executescript('''
DROP TABLE IF EXISTS UserLoginDetail;
DROP TABLE IF EXISTS UserLoginSummary;

CREATE TABLE UserLoginDetail (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    LoginType TEXT,
    LoginTime TEXT,
    LoginDate DATE,
    UserName   TEXT
);

CREATE TABLE UserLoginSummary (
    LoginType TEXT,
    LoginDate DATE,
    UserName   TEXT,
    LoginCount INT
);

CREATE TABLE UserLoginCount (
    LoginType TEXT,
    LoginDate DATE,
    UserCount   INT
);
        
''')

newlist = list()
mylines = [] 
userlogs=[]
userLoginDetail = []

'''
The lines we are intrested in the log file appear in the below format

"1113","ACME_AD_DOMIAN/John Doe","29.999.9.999","User 'ACME_AD_DOMIAN/John Doe' 
successfully logged in from address '29.999.9.999'

We go through the below steps to extract the User ID and their corresponding login time stamp information.
'''
# based on the above format we extract the below lines needed to identify user logins from the logfile.
lineStartsWith = re.compile('<Commit ts=')
lineContains = re.compile('successfully logged in from address')

'''
Since the information we extract will contain some unwanted prefix and suffix information, we will need to remove those inorder 
to get the user ID and timestamp. So the unwanted prefix and suffix information is loaded into a dictionary as keywords, so the keywords
can be extracted out and discarded. 
'''
unwantedKeywords =[ '<Commit ts="','client="ACME_AD_DOMIAN/','">']

for filename in glob.glob(os.path.join(path, "tm1auditstore*.log")):
    #The below line is to tell us which logfile the program is looping thru.I left it on for validation purpose 
    #,it can be disabled upon scheduling of the code.
    print('I am reading' , filename , 'Now' )
    with open (filename, "r") as myfile:
        for myline in myfile:                   # For each line in the file,
            if lineStartsWith.match(myline):
                prefix = myline
                #print(prefix)
            if lineContains.findall(myline):
                body = myline   
                #print(body)
                #message = prefix + body
                #print(message)
                
                # strip newline and add to list.  
                userlogs.append(prefix.replace('<Commit ts="','').replace('client="ACME_AD_DOMIAN/','').replace('">','').replace('\n',''))
                #mylines.append(message.replace('\n',''))    
                
#performing the below steps to get the sucessfull user login timestamp.
for items in userlogs:
    LoginType = 'Successfull'
    UserLoginTime , UserLoginName = items.split('" ', 1)
    LoginDate = datetime(year=int(UserLoginTime[0:4]), month=int(UserLoginTime[4:6]), day=int(UserLoginTime[6:8]))
    #print(UserLoginTime)
    #print(UserLoginName)

    # userLogin.append(loginInfo)
    #writing the user login information into SQLite database 
    cur.execute('''INSERT OR IGNORE INTO UserLoginDetail (LoginType,LoginTime,LoginDate, UserName)
            VALUES ( ?,?,?,? )''', ( LoginType,UserLoginTime,LoginDate,UserLoginName, ) )

#writing the summary information into UserLoginSummary table 
cur.execute('''
            INSERT INTO 
                UserLoginSummary
            SELECT 
                LoginType,
                LoginDate,
                UserName,
                Count(UserName) AS LoginCount 
            FROM
                UserLoginDetail
            GROUP BY
                LoginType,
                LoginDate,
                UserName
                ''')

#writing the summary information into UserLoginCount table 
cur.execute('''
            INSERT INTO 
                UserLoginCount
            SELECT 
                LoginType,
                LoginDate,
                Count(UserName) AS UserCount 
            FROM
                UserLoginSummary
            GROUP BY
                LoginType,
                LoginDate
                ''')

                
conn.commit()
              

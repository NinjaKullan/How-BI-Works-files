import re
import json
import os

#the below 3 line of code imports sending mail function from SendUserNotificationEmail.py file"
import sys
sys.path.append('replace_with_path_where_the_SendUserNotificationEmail_file_is_stored')
from SendUserNotificationEmail import sendSuccessEmailWithAttachment
from SendUserNotificationEmail import sendFailureEmailWithAttachment

#checking if the file exists, if it does then deleting it before running the program
if os.path.exists("replace_with_location_where_the_file_will_stored\findings_filename.txt"):
  os.remove("findings_filename.txt")
#else:
 # print("The file does not exist")

Commentfile = open("replace_with_location_where_the_file_will_stored\findings_filename.txt", "x")

# loads the transfromer error codes and descriptions as a json
#address = input('Enter location: ')
JsonSetName = open('replace_with_location_of_the_json_file\TransformerErrorCode.json')
#load the json into dictonary and appending the generic error codes into it as well.
ErrorCodes = dict(json.load(JsonSetName))
ErrorCodes["Error"] = "There was a error generated in the cube build"
ErrorCodes["error"] = "There was a error generated in the cube build"

# loading, opening and reading the log file
FileName = input('Enter location: ')
if len(FileName) < 1 : FileName="replace_with_location_of_the_Powerplay_log_file\log_filename.log"
FileData = open( FileName , 'r')
FileData2 = open( FileName , 'r')

#below listed keywords will be searched within the log file.
KeyWords = {"TOTAL TIME (CREATE CUBE),","Start cube update"}
#print(ErrorCodes)
#declaring a list for storing the error generated
ErrorCollection = list()

#checking if there where errors in the log.If yes,then loading all the errors into a Error Collection List.
for Line in FileData:
    LineByLine = Line.rstrip()
    for x in ErrorCodes:
        if  x in LineByLine:
            ErrorCollection.append(x)
            #print(x)

for NewLine in FileData2:
    LineInLog = NewLine.rstrip()
    #checking if there where errors in the log, if yes, then exiting the loop
    if len(ErrorCollection) > 0:
        #print('There where some errors generated')
        for xyz in ErrorCollection:
            #print( 'Error Code:', xyz , ' ' , ErrorCodes.get(xyz) )
            Commentfile.write( 'Error Code:'+ xyz + ' ' + ErrorCodes.get(xyz) +'\n' )
            Commentfile.write('https://www.ibm.com/support/knowledgecenter/en/SSEP7J_11.1.0/com.ibm.swg.ba.cognos.ug.cogtr.doc/t_'+ xyz.lower() +'.html'+'\n')
        break

    #capturing the cube build time.
    elif "TOTAL TIME " in LineInLog:
        #print(LineInLog)
        x = re.search( "TOTAL TIME \(CREATE CUBE\)\," , LineInLog )
        #print( x.end() )
        #print("The Total Cube Build ime " + LineInLog[x.end():79])
        Commentfile.write( "The Total Cube Build time " + LineInLog[x.end():79] +'\n' )

    #capturing start of the cube build time.
    elif "Start cube update" in LineInLog:
        #print(LineInLog)
        #print( "Cube build started at " + LineInLog[16:27] )
        Commentfile.write(  "Cube build started at " + LineInLog[16:27] +'\n' )

Commentfile.close()

#reading generated file to identify if the job was successful or not so proper email can be sent
readCommentFile = open( "replace_with_location_where_the_file_will_stored\findings_filename.txt" , 'r')
for lineinCommentFile in readCommentFile:
        commentFileLine = lineinCommentFile.rstrip()
        if "The Total Cube Build time" in commentFileLine:
            sendSuccessEmailWithAttachment('john.doe@acme.com','replace_with_location_where_the_file_will_stored\findings_filename.txt')   
            #print(commentFileLine)
            break
        elif "Error Code" in commentFileLine:
            sendFailureEmailWithAttachment('john.doe@acme.com','replace_with_location_where_the_file_will_stored\findings_filename.txt')
            #print(commentFileLine)
            break

# The send mail function is called here.
#sendEmailWithAttachment('hema.suryaprakasam@martinmarietta.com','C:\Projects\Python\Personal\CubeBuildSummaryLog.txt')

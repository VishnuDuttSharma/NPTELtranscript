import urllib2
from bs4 import BeautifulSoup
import csv
import math

ADDRESS = "http://textofvideo.nptel.iitm.ac.in/"
DESTINTION = "Download/"

class Branch:
    def __init__( self, branchName, link, numVideo, numDoc, numMP3):
        self.name       =   branchName
        self.link       =   link
        self.num_v      =   numVideo
        self.num_d      =   numDoc
        self.num_mp3    =   numMP3

    def getName(self):
        return self.name

    def getLink(self):
        return self.link

    def getNumVideo(self):
        return self.num_v

    def getNumDoc(self):
        return self.num_d

    def getNumMP3(self):
        return self.num_mp3

    def getDescription(self):
        return self.name

class Subject:
    def __init__(self, subjectName, link, facultyName, instituteName):
        self.name       =   subjectName
        self.link       =   link
        self.faculty    =   facultyName
        self.institute  =   instituteName

    def printDescription(self):
        print "Subject:\t",self.name
        print "Faculty:\t",self.faculty
        print "Institute:\t",self.institute

    def getDescription(self):
        #return self.name+'\t'+self.faculty+'\t'+self.institute
        return self.name+'\n     '+self.faculty+'\n     '+self.institute

def updateBranch( data,  fileName = 'Branch_List.csv'):

    myfile = open( fileName, 'wb')

    myfile.write( 'Branch' )
    myfile.write( ',' )
    myfile.write( 'Link' )
    myfile.write( ',' )
    myfile.write( 'Number of PDFs' )
    myfile.write( ',' )
    myfile.write( 'Number of Videos' )
    myfile.write( ',' )
    myfile.write( 'Number of MP3s' )
    myfile.write( '\n' )

    for item in data:
        myfile.write( item.getName() )
        myfile.write( ',' )
        myfile.write( item.getLink() )
        myfile.write( ',' )
        myfile.write( str(item.getNumDoc()) )
        myfile.write( ',' )
        myfile.write( str(item.getNumVideo()) )
        myfile.write( ',' )
        myfile.write( str(item.getNumMP3()) )
        myfile.write( '\n' )

    myfile.close()

def loadBranchList( fileName = 'Branch_List.csv' ):

    data = []
    with open( fileName, 'rb') as myfile:
        reader = csv.reader( myfile)
        header = reader.next()
        for row in reader:
            item = Branch( row[0], row[1], row[2], row[3], row[4])
            data.append( item )

    return data

def getBranchData( address = ADDRESS ):
    data = []

    response = urllib2.urlopen( address )
    soup = BeautifulSoup(response, 'html.parser')

    table = soup.find_all( 'td', attrs={'bgcolor':'#ebeaea'})
    for i in range(0, len(table)-5, 5):
        #print table[i+1].text,':',table[i + 2].text,':',table[i+3].text,':',table[i+4].text,':',str(address) + str((((table[i+1]).span).a)['href'])
        b1 = Subject( (table[i+1].text).strip(), str(ADDRESS) + str((((table[i+1]).span).a)['href']), int(table[i + 2].text), int(table[i + 3].text) )
        data.append(b1)
    # print data
    return data

def getSubjectData( address ):
    data = []

    response = urllib2.urlopen( address )
    soup = BeautifulSoup(response, 'html.parser')

    table = soup.find_all( 'td', attrs={'bgcolor':'#ebeaea'})
    for i in range(0, len(table), 7):
        # print table[i+1].text,':',table[i + 2].text,':',table[i+3].text,':'
        b1 = Subject( (table[i+1].text).strip(), str(ADDRESS) + str((((table[i+1]).span).a)['href']), table[i + 2].text, table[i + 3].text )
        data.append(b1)
    # print data
    return data

def updateSubject( branch_data ):

    for element in branch_data:
        subject_link =  element.link
        subject_list =  getSubjectData( subject_link )

        myfile = open( element.name +'.csv', 'wb')

        myfile.write( 'Course' )
        myfile.write( ',' )
        myfile.write( 'Link' )
        myfile.write( ',' )
        myfile.write( 'Faculty' )
        myfile.write( ',' )
        myfile.write( 'Institute' )
        myfile.write( '\n' )


        for subject in subject_list:
            if ',' in subject.name:
                subject.name = (subject.name).replace(',', ';')

            myfile.write( subject.name )
            myfile.write( ',' )
            myfile.write( subject.link )
            myfile.write( ',' )
            myfile.write( subject.faculty )
            myfile.write( ',' )
            myfile.write( subject.institute )
            myfile.write( '\n' )

        myfile.close()

def loadSubjectList( fileName ):
    data = []
    with open( fileName, 'rb') as myfile:
        reader = csv.reader( myfile)
        header = reader.next()
        for row in reader:
            if ';' in row[0]:
                row[0] = row[0].replace(';', ',')
            item = Subject( row[0], row[1], row[2], row[3])
            data.append( item )

    return data

def printList( data ):
    for i in range(0, len(data)):
        print " %2d. %s" % (i, data[i].getDescription())

def download_file(download_url, name):
    response = urllib2.urlopen(download_url)
    file = open( DESTINTION+name, 'wb')
    file.write(response.read())
    file.close()
    print "Completed ", name

def getLectures( address ):
    data = []

    # print address
    response = urllib2.urlopen( address )
    soup = BeautifulSoup(response, 'html.parser')

    table = soup.findAll( 'td', {'bgcolor': '#d4d4d4'})

    for i in range(8, len(table) - 8, 8):
        name = (((table[i+2].span).a).text)
        name = name.split('\r')[0]
        data.append( name[2:-1] )

    return data

def getTranscript( address ):
    data = []

    # print address
    response = urllib2.urlopen( address )

    courseID = address.split('=')[-1]

    soup = BeautifulSoup(response, 'html.parser')

    table = soup.findAll( 'td', {'class': 'style5' })[1]
    total = float((table.text).split(' ')[-1])

    pages = int(math.ceil( total/10 ))

    for i in range(1, pages+1):
        dataPart = getLectures( address+'&p='+str(i) )
        data = data + dataPart

    for i in range( 0, int(total)):
        fileName = data[i]+' [lec'+str(i+1)+'].pdf'
        fileName = fileName.replace('/', '-')
        download_file( ADDRESS+courseID+'/lec'+str(i+1)+'.pdf',  fileName)

def update( address = ADDRESS):
    branch_list = getBranchData( ADDRESS )
    updateBranch( branch_list )
    updateSubject( branch_list)

def __main__():

    update( ADDRESS )

    branch_list = loadBranchList()
    printList( branch_list )
    option1 = int( raw_input('>> Choose branch(number) from the above list: '))

    fileName = branch_list[ option1 ].name + '.csv'
    subject_list = loadSubjectList( fileName )
    printList( subject_list )
    option2 = int( raw_input('>> Choose subject(number) from the above list: '))

    getTranscript( subject_list[ option2 ].link )

__main__()

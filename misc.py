from psychopy import visual, event, core, gui
import os, random, socket, numpy, shutil
from instructs import *

# creates folder if it doesnt exist
#------------------------------------------------------------------------------
def checkdirectory(dir): 
    if not os.path.exists(dir):
        os.makedirs(dir)


# writes list to file
#------------------------------------------------------------------------------
def writefile(filename,data,delim):
    datafile=open(filename,'w')
    for line in data: #iterate over litems in data list
        currentline='\n' #start each line with a newline
        for j in line: #add each item onto the current line

            if isinstance(j, (list, tuple)): #check if item is a list
                for k in j:
                    currentline=currentline+str(k)+delim
            else:
                currentline=currentline+str(j)+delim
                
##        write current line
        datafile.write(currentline)
    datafile.close()  


# do a dialouge and return subject info 
#------------------------------------------------------------------------------
def getsubjectinfo(experimentname,conditions,datalocation):
    ss_info=[]
    pc=socket.gethostname()
    myDlg = gui.Dlg(title=experimentname)
    myDlg.addText('Subject Info')
    myDlg.addField('ID:', tip='or subject code')
    myDlg.addField('Condition:', random.choice(conditions),choices=conditions)
    myDlg.show()
    if not myDlg.OK:
        core.quit()
        
    subjectinfo = [str(i) for i in myDlg.data]
    
    if subjectinfo[0]=='':
        core.quit()
    else: 
        id=subjectinfo[0]
        condition=subjectinfo[1]
        subjectfile=datalocation+pc+'-'+experimentname+'-'+condition+'-'+id+'.csv'
        while os.path.exists(subjectfile) == True:
            subject_file=datalocation+pc+'-'+experimentname+'-'+condition+'-'+id+'.csv' + '_dupe'
        return [int(id),int(condition),subjectfile]


# copies the data file to a series of dropbox folders
#------------------------------------------------------------------------------  
def copy2db(file_name,experiment_name):
    copyfolders=[ #add your own!
        'C:\\Users\\klab\\Dropbox\\PSYCHOPY DATA\\'+experiment_name+'\\',
        'C:\\Users\\klab\\Dropbox\\garrett\\PSYCHOPY DATA\\'+experiment_name+'\\']

    for i in copyfolders:
        checkdirectory(i)
        shutil.copy(file_name,i)


# takes in 1 or 2-d lists of objects and draws them in the window
#------------------------------------------------------------------------------
def draw_all(win,objects):
    for i in objects:
        if isinstance(i, (list, tuple)):
            for j in i:
                j.draw()
        else:
            i.draw()
    win.flip()


# grab button presses
#------------------------------------------------------------------------------
def buttongui(cursor,timer,buttons,labels):
    #clear events
    timer.reset()
    cursor.clickReset()
    event.clearEvents() 
    
    #iterate until response
    while True:
        
        #quit if desired
        if 'q' in event.getKeys():
            print 'User Terminated'
            core.quit()
            
        #check to see if any stimulus has been clicked inside of
        for i in buttons:
            if cursor.isPressedIn(i):
                return [labels[buttons.index(i)],timer.getTime()]


def rating_trial(win, scale, trial_instructs, item_circles, item_text):

    # run until response is confirmed
    while scale.noResponse:
        # draw trial
        draw_all(win, [scale, trial_instructs, item_circles, item_text])
        # quit exp if needed
        if 'q' in event.getKeys():
            print 'User Terminated'
            core.quit()            
        #get response
        if scale.noResponse == False:
            scale_response = scale.getRating()
            scale_rt = scale.getRT()

            return [scale_response, scale_rt]


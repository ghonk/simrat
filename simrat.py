"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                                                           
                               ____                         ___            
              ,--,           ,'  , `.                     ,--.'|_          
            ,--.'|        ,-+-,.' _ |  __  ,-.            |  | :,'         
  .--.--.   |  |,      ,-+-. ;   , ||,' ,'/ /|            :  : ' :         
 /  /    '  `--'_     ,--.'|'   |  ||'  | |' | ,--.--.  .;__,'  /          
|  :  /`./  ,' ,'|   |   |  ,', |  |,|  |   ,'/       \ |  |   |           
|  :  ;_    '  | |   |   | /  | |--' '  :  / .--.  .-. |:__,'| :           
 \  \    `. |  | :   |   : |  | ,    |  | '   \__\/: . .  '  : |__         
  `----.   \'  : |__ |   : |  |/     ;  : |   ," .--.; |  |  | '.'|        
 /  /`--'  /|  | '.'||   | |`-'      |  , ;  /  /  ,.  |  ;  :    ;        
'--'.     / ;  :    ;|   ;/           ---'  ;  :   .'   \ |  ,   /         
  `--'---'  |  ,   / '---'                  |  ,     .-./  ---`-'          
             ---`-'                          `--`---'                      
                                                                           

This experiment presents participants with pairs of concepts and asks
for either a similarity rating or an association rating on a 
judgment line with no tick marks  

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""

__author__  = "g_honk"
__credits__ = "n_conaway"
__status__  = "in_dev"
__license__ = "GPL"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from psychopy  import visual, event, core
from socket    import gethostname
from time      import strftime
from os        import getcwd, listdir, path, system
from itertools import combinations
from misc      import *
from instructs import *
import numpy   as np	 
import random  as rnd
import sys

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Experiment Settings
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

experiment_name   = "sim_rat"
conditions        = [1, 2, 3, 4]
cond_labels       = ['tax_order1', 'tax_order2', 'the_order1', 'the_order2']
window_color      = [.46, .74, .96]
font_color        = [-1,-1,-1]
init_button_color = [.5, .5, .5]
text_font         = "Consolas"
text_size         = 24

# Get experiment information
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # Get subject information and materials
if sys.platform == 'darwin':
    checkdirectory(getcwd() + '/subjects/')

    # Get subject information
    [subject_number, condition, subject_file] = getsubjectinfo(
        experiment_name, conditions, getcwd() + '/subjects/')
    
    # Get materials list
    trial_materials = np.genfromtxt(
    	getcwd() + "/materials/stimuli.csv", delimiter = ",", 
        dtype = "str").astype(str)

    # Get demo picture
    demo_imgs = []
    for i in os.listdir(os.getcwd() + '/materials/img/'):
        demo_imgs.append(os.getcwd() + '/materials/img/' + i)


else:
    checkdirectory(getcwd() + '\\subjects\\')

    # Get subject information
    [subject_number,condition,subject_file] = getsubjectinfo(
        experiment_name,conditions,getcwd() + '\\subjects\\')

    # Get materials list
    trial_materials = np.genfromtxt(
        getcwd() + "\\materials\\stimuli.csv", delimiter = ",", 
        dtype = "str").astype(str)
    
    # Get demo picture
    demo_imgs = []
    for i in os.listdir(os.getcwd() + '\\materials\\img\\'):
        demo_imgs.append(os.getcwd() + '\\materials\\img\\' + i)


trial_materials = trial_materials.tolist()

item_key = ['BASE','TAXONOMIC','THEMATIC','UNRELATED','UNRELATED','UNRELATED']

# Set up interface
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Create window and set logging option
if gethostname() not in ['klab1','klab2','klab3']:
    win = visual.Window([1440,900],units='pix',color = window_color, fullscr=True, screen = 0)

else:
    win = visual.Window([1440,900],units='pix', color = window_color, fullscr = True)
    checkdirectory(getcwd() + '\\logfiles\\')
    log_file = getcwd() + '\\logfiles\\' + str(subject_number) + '-logfile.txt'
    while path.exists(log_file):
       log_file = log_file + '_dupe.txt'
    log_file = open(log_file, 'w')
    sys.stdout = log_file
    sys.stderr = log_file

# Define the mouse and timer
cursor = event.Mouse(visible = True, newPos = None, win = win)
timer = core.Clock()

# Get current date and time
current_time = strftime("%a, %d %b %Y %X")

# init first lines of subject data
subject_data = [[current_time], [subject_number]]

# Get instructions
instructions = visual.TextStim(win, text = '', wrapWidth = 900,
	color = font_color, font = text_font, height = text_size)
fix_cross = visual.TextStim(win, text = '+', color = font_color, 
	font = text_font, height = text_size, pos = [0,0])

# make visual scale interface

scale_labels    = [tax_labels, tax_labels, the_labels, the_labels][condition - 1]
scale_instructs = [scale_instructs_tax, scale_instructs_tax, 
    scale_instructs_the, scale_instructs_the][condition - 1] 

trial_scale = visual.RatingScale(win, pos = [0,-100], textColor = font_color, 
		lineColor = font_color, showValue = False, stretch = 1.75, precision = 100,
		acceptText = 'CONFIRM', acceptPreText = 'CLICK LINE', mouseOnly = True,
		low = 0, high = 100, labels = scale_labels, scale = scale_instructs,
        textSize = .80, textFont = text_font)

# item display
# item positions
item_pos = [[-100, 150], [100, 150]]
# item background
item_circles = [visual.Circle(win, radius = 85, fillColor = init_button_color,
		lineColor = font_color, lineWidth = 3.0, pos = item_pos[0]),
	visual.Circle(win, radius = 85, fillColor = init_button_color,
		lineColor = font_color, lineWidth = 3.0, pos = item_pos[1])]
# item text
item_text = [visual.TextStim(win, text = '', height = text_size,
			font = text_font, color = font_color, pos = item_pos[0]),
		visual.TextStim(win, text = '', height = text_size,
			font = text_font, color = font_color, pos = item_pos[1])] 


# Primary trial instructions
trial_ins = visual.TextStim(win, text = '', height = text_size + 4,
				wrapWidth = 900, font = text_font, color = font_color)
trial_ins.setPos([0, 305])
if condition <= 2:
    trial_ins.setText(trial_instructs_tax)
    demo_img = visual.ImageStim(win, image = demo_imgs[0], pos = [0,0])
else:
    trial_ins.setText(trial_instructs_the)
    demo_img = visual.ImageStim(win, image = demo_imgs[1], pos = [0,0])
# trial demo



# Set condition specific variables
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
question_cond = ['tax', 'tax', 'the', 'the'][condition - 1]
item_cond     = [1, 2, 1, 2][condition - 1]
item_idx_list = [list([1,2] * 30)[0:59], list([2,1] * 30)[0:59]][item_cond - 1]

trial_list = []
for list_idx in range(0, 59):
        # append a base + tax/them set from trial set
        trial_list.append(list([[trial_materials[list_idx][0], # base item
            trial_materials[list_idx][item_idx_list[list_idx]]], # tax/the item
            ['', 'tax_item', 'the_item'][item_idx_list[list_idx]]])) # trial type label
        # append a random item set from trial set
        unr_choice = list(rnd.sample([3, 4, 5], 2))
        trial_list.append(list([[trial_materials[list_idx][unr_choice[0]], # unr item 1
            trial_materials[list_idx][unr_choice[1]]], #unr item 2
            'unr_item'])) # trial type label

# Start logging info
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print '\n SUBJECT INFORMATION:'
print ['        ID: ', subject_number]
print [' Condition: ', condition]
print ['  Question: ', question_cond]
print ['Item Order: ', item_cond]
print [' Data file: ', subject_file]
print ['  Run Time: ', current_time]
print '\n'
print ['----- Materials ------']
rnd.shuffle(trial_list)
for i in trial_list:
	print i

# Start experiment
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

instructions.setText(main_instructs)
instructions.draw()
win.flip()
core.wait(2)
event.waitKeys()

demo_img.draw()
instructions.setPos([0, -360])
instructions.setText('Press any key when you are ready to begin.')
instructions.draw()
win.flip()
core.wait(2)
event.waitKeys()

# # # DEMO SCREEN

# # # CONFIRM YOURE READY SCREEN

for trial in trial_list:
    # set trial stimuli/properties
    trial_items = list(rnd.sample(trial[0], 2)) 
    trial_scale.reset()
    item_text[0].setText(trial_items[0])
    item_text[1].setText(trial_items[1])
    
    fix_cross.draw()
    win.flip()
    core.wait(.5)

	# present items and rating scale and wait for response
    [trial_response, trial_rt] = rating_trial(win, trial_scale, trial_ins, 
        item_circles, item_text)

	# record data
    current_trial = [subject_number, cond_labels[condition - 1], question_cond,
        item_cond, (trial_list.index(trial) + 1), trial_items, trial[1], trial_rt, 
        trial_response]

    # write data
    subject_data.append(current_trial)
    writefile(subject_file, subject_data, ',')

    print ''
    print [' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ']
    print ['   Trial Number: ', trial_list.index(trial) + 1]
    print [' Trial Concepts: ', trial_items]
    print ['             RT: ', trial_rt]
    print ['       Response: ', trial_response]
    print [' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ']
    print ''

# Close experiment
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
instructions.setPos([0, 0])
instructions.setText(end_instructs)
instructions.draw()
win.flip()
event.waitKeys()

print '\nExperiment completed'
if gethostname() in ['klab1','klab2','klab3']:
    copy2db(subject_file, experiment_name)
    log_file.close()
    os.system("TASKKILL /F /IM pythonw.exe")


import pygame, sys
from datetime import datetime
import calendar
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import textwrap
import os.path
import ast
import time
from pprint import pprint

pygame.font.init()
font13r = pygame.font.Font("OpenSans-Regular.ttf", 13)
font13 = pygame.font.Font("OpenSans-SemiBold.ttf", 13)
font14 = pygame.font.Font("OpenSans-SemiBold.ttf", 14)
font16 = pygame.font.Font("OpenSans-Bold.ttf", 16)
font18 = pygame.font.Font("OpenSans-Bold.ttf", 18)
font24 = pygame.font.Font("OpenSans-SemiBold.ttf", 24)
font25 = pygame.font.Font(None, 25)
font26b = pygame.font.Font("OpenSans-Bold.ttf", 26)
font55b = pygame.font.Font("OpenSans-Bold.ttf", 55)

BLACK, WHITE, BLUE, GREEN, MAROON = (0,0,0), (255,255,255), (0,0,255), (0,128,0), (128,0,0) 
PURPLE, TEAL, FUCHSIA, LIME, OLIVE = (128,0,128), (0,128,128), (255,0,255), (0,255,0), (128,128,0) 
NAVYBLUE, RED, ORANGE, AQUA, TAN = (0,0,128), (255,0,0), (255,165,0), (0,255,255), (255,255,200)
COLOURS = [BLUE, GREEN, MAROON, PURPLE, TEAL, FUCHSIA, LIME, OLIVE, NAVYBLUE, RED, ORANGE, AQUA]

MONTH_STRINGS=["DECEMBER", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST",
            "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY"]
WEEK_STRINGS_LONG=["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
WEEK_STRINGS_SHORT=["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
DAY_NUMBERS=[" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9","10","11","12","13","14","15",
      "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

COORDS = {
    "LEFT_SMALL_CAL": {"x": 45, "y": 68, "w": 34, "h": 90, "offset": 34},
    "RIGHT_SMALL_CAL": {"x": 640, "y": 68, "w": 34, "h": 90, "offset": 34},
    "DAY_OF_WEEK_HEADING": {"x": 45, "y": 158, "w": 119, "h": 25, "offset": 119},
    "SMALL_CAL_HEADING": {"x": 45, "y": 43, "w": 238, "h": 25, "offset": 595},
    "MONTH_AND_YEAR": {"x": 283, "y": 43, "w": 357, "h": 115},
    "MAIN_BODY": {"x": 45, "y": 182, "w": 833, "h": 481},
    "FOR_LOOKS": {"x": 45, "y": 43, "w": 833, "h": 620},
    "ERROR_MESSAGE": {"x": 350, "y": 300, "w": 200, "h": 100},
    "LEFT_SM_CAL_TITLE": {"x": 45, "y": 39, "w": 238, "h": 25},
    "RIGHT_SM_CAL_TITLE": {"x": 640, "y": 39, "w": 238, "h": 25},
    "MAIN_COLUMN_TITLES": {"x1": 45, "x2": 119, "y": 150, "w": 119, "h": 25},   # first 2 give calculated x, then y, w, h
    "SMALL_COLUMN_TITLES": {"x1": 45, "x2": 595, "x3": 34, "y": 64, "w": 34, "h": 13},   # first 3 give calculated x, then y, w, h
    "DAY_NUMS_TEXT": {"x": 34, "y": 77, "w": 34, "h": 13},        # first 2 are used to calculate x and y, then w, h
    "CALC_X_AND_Y": {"x1": 45, "x2": 119, "y": 183},              # first 2 help calculate x value for day rectangle location, 3rd helps
                                                                  # calculate y value
    "TEXT_BOX_1": {"x": 114, "y": 673, "w": 33, "h": 25},
    "TEXT_BOX_2": {"x": 228, "y": 673, "w": 50, "h": 25},
    "TEXT_BOX_3": {"x": 515, "y": 673, "w": 360, "h": 24},
    "BUTTON_1": {"x": 850, "y": 0, "w": 40, "h": 40},
    "BUTTON_2": {"x": 800, "y": 0, "w": 40, "h": 40},
    "CURRENT_MONTH": {"x": 283, "y": 30, "w": 357, "h": 40},
    "CURRENT_YEAR": {"x": 283, "y": 93, "w": 357, "h": 35},
    "MONTH_TEXT_BOX": {"x": 34, "y": 667, "w": 80, "h": 25},
    "YEAR_TEXT_BOX": {"x": 150, "y": 667, "w": 100, "h": 25},
    "COMMENTS_TEXT_BOX": {"x": 402, "y": 667, "w": 110, "h": 25},
    "CIRCLE_FOR_LOOKS_1": {"x": 820, "y": 20, "radius": 20},      # x, y, radius
    "CIRCLE_FOR_LOOKS_2": {"x": 870, "y": 20, "radius": 20}
}

SMALL_RECT_SIZE = 30
SMALL_RECT_TEXT_Y = 27

ROW_OFFSET_4 = 120
ROW_OFFSET_5 = 96
ROW_OFFSET_6 = 80

DAYS_IN_MONTH1 = 28
DAYS_IN_MONTH2 = 30
DAYS_IN_MONTH3 = 31

WIDTH = 924
HEIGHT = 714

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Main Variables
class MV:
    year = datetime.now().year
    current_year = year
    current_month = datetime.now().month
    current_day = datetime.now().day
    month = current_month-1
    month_index = 0  # used to tell which day the cursor is on
    monthObj = []    # will hold 12 instances of MonthCls class
    personal_events = []    # will hold comments in tuple form as (m, d, "comment")

class MonthClass:
    def __init__(self, name):
        self.name = name
        self.stday = 0
        self.dysinmth = 0
        self.yoffset = 0
        self.days = []  # 28 to 31 DayClass class instances
        self.mthcomments = ["" for i in range(DAYS_IN_MONTH3)]  # daily comments in monthly calendar
                                                                # input from 3 text files

class Draw:
    @staticmethod
    def draw_rectangle(screen, x, y, w, h, width):
        pygame.draw.rect(screen, BLACK, (x, y, w, h), width)
    @staticmethod
    def draw_rectangles(screen, x, y, w, h, offset, qty):
        for i in range(qty):
            Draw.draw_rectangle(screen, x+i*offset, y, w, h, 1)
    @staticmethod
    def draw_text(screen, str, px, py, sx, sy, tuple, font):
        w, h = font.size(str)
        text = font.render(str, True, tuple)
        screen.blit(text, dest = (px+sx/2-w/2, py+sy/2-h/4))
    @staticmethod
    def draw_circles(screen):
        pygame.draw.circle(screen, BLACK, (COORDS["CIRCLE_FOR_LOOKS_1"]["x"], COORDS["CIRCLE_FOR_LOOKS_1"]["y"]),
                           COORDS["CIRCLE_FOR_LOOKS_1"]["radius"], 3)
        pygame.draw.circle(screen, BLACK, (COORDS["CIRCLE_FOR_LOOKS_2"]["x"], COORDS["CIRCLE_FOR_LOOKS_2"]["y"]),
                           COORDS["CIRCLE_FOR_LOOKS_2"]["radius"], 3)
    @staticmethod
    def draw_hiLite_rect(screen, x, y, w, h):
        pygame.draw.rect(screen, TAN, (x+1, y+1, w-2, h-2))

class DayClass:
    def __init__(self, month, dy):
        self.month = month
        self.dy = dy
        self.x = 0      # will be used as pos x on screen
        self.y = 0      # will be used as pos y on screen

# Do Stuff Monthly       
class DSM:        
    def initialize_month(yr):
        MV.monthObj = []      # start with empty month instance list        
        for i in range(12):
            MV.monthObj.append(MonthClass(MONTH_STRINGS[i+1]))   \
                  # create 12 instances of MonthClass each called monthObj[i]
            temp = calendar.monthrange(yr, i+1)
            MV.monthObj[i].stday = (temp[0]+1)%7            # calc start day for each Month
            MV.monthObj[i].dysinmth = temp[1]               # calc number of days in Month for each Month
            for j in range(temp[1]):
                MV.monthObj[i].days.append(DayClass(i+1,j+1))   \
                      # create 28 to 31 instances of Day class in each Month instance called monthObj[i].days[i]
        for i in range(12):
            MV.monthObj[i].yoffset = ROW_OFFSET_5                               # calc yoffsets for pleasing calendar rows
            if MV.monthObj[i].stday >=5 and MV.monthObj[i].dysinmth == DAYS_IN_MONTH3:    # happens about 3 times a year
                MV.monthObj[i].yoffset = ROW_OFFSET_6
            if MV.monthObj[i].stday == 6 and MV.monthObj[i].dysinmth >= DAYS_IN_MONTH2:
                MV.monthObj[i].yoffset = ROW_OFFSET_6
            if MV.monthObj[1].stday == 0 and MV.monthObj[1].dysinmth == DAYS_IN_MONTH1:    # happens about once in 10 years
                MV.monthObj[1].yoffset = ROW_OFFSET_4
        for i in range(12):
            ctr = MV.monthObj[i].stday
            for j in range (MV.monthObj[i].dysinmth):
                MV.monthObj[i].days[j].x = COORDS["CALC_X_AND_Y"]["x1"] + ctr%7 * COORDS["CALC_X_AND_Y"]["x2"]     # all days in year have x coordinate for display
                MV.monthObj[i].days[j].y = COORDS["CALC_X_AND_Y"]["y"] + ctr//7 * MV.monthObj[i].yoffset    # all days in year have y coordinate
                ctr += 1
        filename = "StaticHolidays.txt"    # load text file of holidays that do not change        
        DSM.load_monthly_comments(filename)
        filename = str(yr) + "FloatHolidays.txt"    # load text file of holidays that do change
        DSM.load_monthly_comments(filename)
        filename = "PersonalEvents.txt"    # load file of personal birthdays, anniversaries and misc. days of importance
        DSM.load_monthly_comments(filename)

    def load_monthly_comments(filename):
        Holidays = []
        try:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    file_content = f.read().strip()
                    Holidays = ast.literal_eval(file_content)   # evaluate file contents
                    if not isinstance(Holidays, list):          # make sure it is a list
                        DSM.display_error(screen, f"Error in  {filename}.  Content is not a list structure")
                    for item in Holidays:
                        if not (isinstance(item, tuple) and len(item) == 3):    # make sure it has 3-element tuples only
                            DSM.display_error(screen, f"Error in  {filename}.  List elements must be 3-element tuples")
                    for holiday in Holidays:
                        if holiday[0]<1 or holiday[0]>12:
                            DSM.display_error(screen, f"Error in  {filename}.  One of the months is not from 1 - 12")
                        if holiday[1]<1 or holiday[1]>31:
                            DSM.display_error(screen, f"Error in  {filename}.  One of the days is not from 1 - 31")
                        if holiday[2]=="":
                            DSM.display_error(screen, f"Error in  {filename}.  One of the strings is NULL")
                        if MV.monthObj[holiday[0]-1].mthcomments[holiday[1]-1] == "":
                            MV.monthObj[holiday[0]-1].mthcomments[holiday[1]-1] = holiday[2]    # if there already is a comment
                        else:                                                                   # concatenate them with 4 spaces in between
                            MV.monthObj[holiday[0]-1].mthcomments[holiday[1]-1] += "    " + holiday[2]
        except(SyntaxError, ValueError) as e:
            DSM.display_error(screen, f"Error in  {filename}.  Check for missing [], (), quotation marks or commas")
        # read PersonalEvents.txt file if present to put list in MV.personal_events
        if os.path.isfile("PersonalEvents.txt"):
            with open("PersonalEvents.txt", "r") as f:
                file_content = f.read()
            MV.personal_events = ast.literal_eval(file_content)
                    
    def display_error(screen,  error_message):
        screen.fill(WHITE)
        pygame.display.set_caption("Monthly Calendar")
        Draw.draw_text(screen, error_message, COORDS["ERROR_MESSAGE"]["x"], COORDS["ERROR_MESSAGE"]["y"], COORDS["ERROR_MESSAGE"]["w"],
                       COORDS["ERROR_MESSAGE"]["h"], RED, font25)
        pygame.display.update()
        time.sleep(6)
        exit(1) # exit to repair bad file
               
    def do_all_rectangles(screen):
        Draw.draw_rectangles(screen, COORDS["LEFT_SMALL_CAL"]["x"], COORDS["LEFT_SMALL_CAL"]["y"], COORDS["LEFT_SMALL_CAL"]["w"],
                             COORDS["LEFT_SMALL_CAL"]["h"], COORDS["LEFT_SMALL_CAL"]["offset"], 7)     # left side small calendar rectangles
        Draw.draw_rectangles(screen, COORDS["RIGHT_SMALL_CAL"]["x"], COORDS["RIGHT_SMALL_CAL"]["y"], COORDS["RIGHT_SMALL_CAL"]["w"],
                             COORDS["RIGHT_SMALL_CAL"]["h"], COORDS["RIGHT_SMALL_CAL"]["offset"], 7)    # right side small calendar rectangles
        Draw.draw_rectangles(screen, COORDS["DAY_OF_WEEK_HEADING"]["x"], COORDS["DAY_OF_WEEK_HEADING"]["y"], COORDS["DAY_OF_WEEK_HEADING"]["w"],
                             COORDS["DAY_OF_WEEK_HEADING"]["h"], COORDS["DAY_OF_WEEK_HEADING"]["offset"], 7)   # day of week headings
        Draw.draw_rectangles(screen, COORDS["SMALL_CAL_HEADING"]["x"], COORDS["SMALL_CAL_HEADING"]["y"], COORDS["SMALL_CAL_HEADING"]["w"],
                             COORDS["SMALL_CAL_HEADING"]["h"], COORDS["SMALL_CAL_HEADING"]["offset"], 2)   # small calendar headings
        Draw.draw_rectangle(screen, COORDS["MONTH_AND_YEAR"]["x"], COORDS["MONTH_AND_YEAR"]["y"], COORDS["MONTH_AND_YEAR"]["w"],
                             COORDS["MONTH_AND_YEAR"]["h"], 1)  # Month and year rectangle
        Draw.draw_rectangle(screen, COORDS["MAIN_BODY"]["x"], COORDS["MAIN_BODY"]["y"], COORDS["MAIN_BODY"]["w"], COORDS["MAIN_BODY"]["h"], 2)  # main body of calendar rectangle
        Draw.draw_rectangle(screen, COORDS["FOR_LOOKS"]["x"], COORDS["FOR_LOOKS"]["y"], COORDS["FOR_LOOKS"]["w"], COORDS["FOR_LOOKS"]["h"], 2)
        
    def do_all_texts(screen, mth, yr):      
        if MV.month==0:
            Draw.draw_text(screen, MONTH_STRINGS[mth] + "  " + str(yr-1), COORDS["LEFT_SM_CAL_TITLE"]["x"], COORDS["LEFT_SM_CAL_TITLE"]["y"],
                         COORDS["LEFT_SM_CAL_TITLE"]["w"], COORDS["LEFT_SM_CAL_TITLE"]["h"], BLACK, font14)
        else:    
            Draw.draw_text(screen, MONTH_STRINGS[mth] + "  " + str(yr), COORDS["LEFT_SM_CAL_TITLE"]["x"], COORDS["LEFT_SM_CAL_TITLE"]["y"],
                         COORDS["LEFT_SM_CAL_TITLE"]["w"], COORDS["LEFT_SM_CAL_TITLE"]["h"], BLACK, font14)
        if MV.month==11:
            Draw.draw_text(screen, MONTH_STRINGS[mth+2] + "  " + str(yr+1), COORDS["RIGHT_SM_CAL_TITLE"]["x"], COORDS["RIGHT_SM_CAL_TITLE"]["y"],
                         COORDS["RIGHT_SM_CAL_TITLE"]["w"], COORDS["RIGHT_SM_CAL_TITLE"]["h"], BLACK, font14)
        else:    
            Draw.draw_text(screen, MONTH_STRINGS[mth+2] + "  " + str(yr), COORDS["RIGHT_SM_CAL_TITLE"]["x"], COORDS["RIGHT_SM_CAL_TITLE"]["y"],
                         COORDS["RIGHT_SM_CAL_TITLE"]["w"], COORDS["RIGHT_SM_CAL_TITLE"]["h"], BLACK, font14)
        for i in range(7):
            Draw.draw_text(screen, WEEK_STRINGS_LONG[i], COORDS["MAIN_COLUMN_TITLES"]["x1"] + i * COORDS["MAIN_COLUMN_TITLES"]["x2"],
                         COORDS["MAIN_COLUMN_TITLES"]["y"], COORDS["MAIN_COLUMN_TITLES"]["w"], COORDS["MAIN_COLUMN_TITLES"]["h"], BLACK, font18)
        for i in range(2):
            for j in range(7):
                Draw.draw_text(screen, WEEK_STRINGS_SHORT[j], COORDS["SMALL_COLUMN_TITLES"]["x1"] + i * COORDS["SMALL_COLUMN_TITLES"]["x2"] + j * COORDS["SMALL_COLUMN_TITLES"]["x3"],
                             COORDS["SMALL_COLUMN_TITLES"]["y"], COORDS["SMALL_COLUMN_TITLES"]["w"], COORDS["SMALL_COLUMN_TITLES"]["h"], BLACK, font13)
        
    def do_small_calendar_month(screen, stday, dsinmo, x):    # draws small calendars of previous month and next month
        ctr=stday
        for i in range(dsinmo):
            Draw.draw_text(screen, DAY_NUMBERS[i], x+ctr%7*COORDS["DAY_NUMS_TEXT"]["x"], COORDS["DAY_NUMS_TEXT"]["y"]+ctr//7*12,
                         COORDS["DAY_NUMS_TEXT"]["w"], COORDS["DAY_NUMS_TEXT"]["h"], BLACK, font14)
            ctr+=1
            
    def do_small_calendar(screen, m):
        if MV.month == 0:
            temp = calendar.monthrange(MV.year-1, 12) # sets up December of previous year
            stdy = (temp[0]+1)%7
            dsinmo = DAYS_IN_MONTH3
        else:
            stdy = MV.monthObj[m-1].stday               # otherwise sets up previous month
            dsinmo = MV.monthObj[m-1].dysinmth
        DSM.do_small_calendar_month(screen, stdy, dsinmo, COORDS["LEFT_SMALL_CAL"]["x"])
        if MV.month == 11:
            temp = calendar.monthrange(MV.year+1, 1)  # sets up January of next year
            stdy = (temp[0]+1)%7
            dsinmo = DAYS_IN_MONTH3
        else:
            stdy = MV.monthObj[m+1].stday               # otherwise sets up next month
            dsinmo = MV.monthObj[m+1].dysinmth
        DSM.do_small_calendar_month(screen, stdy, dsinmo, COORDS["RIGHT_SMALL_CAL"]["x"])
         
    def month_text_boxes(screen):     # defines all text boxes and buttons
        def output_month():
            if(textbox1.getText()).isdigit():
                if(int(textbox1.getText())) >= 1 and (int(textbox1.getText())) <= 12:
                    MV.month = int(textbox1.getText()) - 1
            
        def output_year():
            if(textbox2.getText()).isdigit():
                if(int(textbox2.getText())) >= 1000:
                    MV.year = int(textbox2.getText())
                    DSM.year_changed(MV.year)
                    textbox2.setText(str(MV.year))

        def output_comments():
            MV.monthObj[MV.month].mthcomments[MV.month_index] = textbox3.getText()
            MV.personal_events.append((MV.month + 1, MV.month_index + 1, textbox3.getText()))
            DSM.save_personal_events()  # save personal_events to output file
            
        def go_ahead():
            MV.month += 1
            if MV.month == 12:
                MV.month = 0
                MV.year += 1
                DSM.year_changed(MV.year)
                textbox2.setText(str(MV.year))
            textbox1.setText(str(MV.month+1))              
        
        def go_back():
            MV.month -= 1
            if MV.month < 0:
                MV.month = 11
                MV.year -= 1
                DSM.year_changed(MV.year)
                textbox2.setText(str(MV.year))
            textbox1.setText(str(MV.month+1))

        global textbox1       
        textbox1 = TextBox(screen, COORDS["TEXT_BOX_1"]["x"], COORDS["TEXT_BOX_1"]["y"], COORDS["TEXT_BOX_1"]["w"],
                           COORDS["TEXT_BOX_1"]["h"], colour=(TAN),
                           font = font25, onSubmit=output_month, borderThickness=3)
        textbox1.setText(str(MV.month+1))
            
        global textbox2                            
        textbox2 = TextBox(screen, COORDS["TEXT_BOX_2"]["x"], COORDS["TEXT_BOX_2"]["y"], COORDS["TEXT_BOX_2"]["w"],
                           COORDS["TEXT_BOX_2"]["h"], colour=(TAN),
                           font = font25, onSubmit=output_year, borderThickness=3)
        textbox2.setText(str(MV.year))

        global textbox3
        textbox3 = TextBox(screen, COORDS["TEXT_BOX_3"]["x"], COORDS["TEXT_BOX_3"]["y"], COORDS["TEXT_BOX_3"]["w"],
                           COORDS["TEXT_BOX_3"]["h"], colour=(TAN),
                           font = font13, onSubmit=output_comments, borderThickness=3)

        global button1
        button1 = Button(screen, COORDS["BUTTON_1"]["x"], COORDS["BUTTON_1"]["y"], COORDS["BUTTON_1"]["w"],
                           COORDS["BUTTON_1"]["h"], text = '+', font=font26b, margin=10,
                           inactiveColour=(255, 255, 200), hoverColour=(255, 100, 255),
                           pressedColour=(0, 200, 20), radius=20, onClick=lambda: go_ahead())
            
        global button2
        button2 = Button(screen, COORDS["BUTTON_2"]["x"], COORDS["BUTTON_2"]["y"], COORDS["BUTTON_2"]["w"],
                           COORDS["BUTTON_2"]["h"], text = '-', font=font26b, margin=10,
                           inactiveColour=(255, 255, 200), hoverColour=(255, 100, 255),
                           pressedColour=(0, 200, 20), radius=20, onClick=lambda: go_back())
             
    def year_changed(yr):
        # when year changes, we must calculate new number of days and start date for each month
        DSM.initialize_month(yr)

    def save_personal_events():
        with open("PersonalEvents.txt", "w") as f:
            import io
            output = io.StringIO()
            pprint(MV.personal_events, stream = output)
            f.write(output.getvalue())

def main():
    DSM.initialize_month(MV.year)
    DSM.month_text_boxes(screen)
    show_text_boxes = True
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:            # up arrow toggles showing of text boxes
                    show_text_boxes = not show_text_boxes
                if event.key == pygame.K_DOWN:          # down arrow saves screenshot as png file
                    pygame.image.save(screen, datetime.now().strftime("MonthlyCalendar-%m-%d-%y-%H-%M-%S")+".png")
                if event.key == pygame.K_DELETE:  # delete key removes comment highlighted by cursor
                    if MV.personal_events != []:
                        month_to_find = MV.month + 1
                        day_to_find = MV.month_index + 1
                        target = next((item for item in MV.personal_events
                            if item[0] == month_to_find and item[1] == day_to_find), None)
                        if target:
                            MV.personal_events.remove(target)   # remove comment from personal_events list
                            MV.monthObj[MV.month].mthcomments[MV.month_index] = ""  # clear comment from screen
                        DSM.save_personal_events()  # save personal_events to output
        screen.fill(WHITE)  # clear background
        pygame.display.set_caption("Monthly Calendar")      # draw scene
        Draw.draw_text(screen, MV.monthObj[MV.month].name, COORDS["CURRENT_MONTH"]["x"], COORDS["CURRENT_MONTH"]["y"],
                    COORDS["CURRENT_MONTH"]["w"], COORDS["CURRENT_MONTH"]["h"], COLOURS[MV.month], font55b)                                                 
        Draw.draw_text(screen, str(MV.year), COORDS["CURRENT_YEAR"]["x"], COORDS["CURRENT_YEAR"]["y"], COORDS["CURRENT_YEAR"]["w"],
                    COORDS["CURRENT_YEAR"]["h"], COLOURS[MV.month], font55b)
        DSM.do_all_rectangles(screen)
        DSM.do_all_texts(screen, MV.month, MV.year)
        DSM.do_small_calendar(screen, MV.month)
        if show_text_boxes: # for cleaner printout
            pygame_widgets.update(events)      # text boxes can be turned off with up arrow
            Draw.draw_text(screen, "MONTH:", COORDS["MONTH_TEXT_BOX"]["x"], COORDS["MONTH_TEXT_BOX"]["y"], COORDS["MONTH_TEXT_BOX"]["w"],
                    COORDS["MONTH_TEXT_BOX"]["h"], BLACK, font16)
            Draw.draw_text(screen, "YEAR:", COORDS["YEAR_TEXT_BOX"]["x"], COORDS["YEAR_TEXT_BOX"]["y"], COORDS["YEAR_TEXT_BOX"]["w"],
                    COORDS["YEAR_TEXT_BOX"]["h"], BLACK, font16)
            Draw.draw_text(screen, "COMMENTS:", COORDS["COMMENTS_TEXT_BOX"]["x"], COORDS["COMMENTS_TEXT_BOX"]["y"], 
                    COORDS["COMMENTS_TEXT_BOX"]["w"], COORDS["COMMENTS_TEXT_BOX"]["h"], BLACK, font16)
            Draw.draw_circles(screen)
        for i in range(MV.monthObj[MV.month].dysinmth):
            day = MV.monthObj[MV.month].days[i]
            if show_text_boxes: # for cleaner printout
                if MV.year == MV.current_year and MV.month == MV.current_month-1 and i == MV.current_day-1:
                    Draw.draw_hiLite_rect(screen, day.x, day.y, COORDS["DAY_OF_WEEK_HEADING"]["w"], MV.monthObj[MV.month].yoffset)  # highlight current day
            Draw.draw_rectangle(screen, COORDS["LEFT_SMALL_CAL"]["x"], COORDS["MAIN_BODY"]["y"] + 1, MV.monthObj[MV.month].stday * COORDS["DAY_OF_WEEK_HEADING"]["w"], MV.monthObj[MV.month].yoffset, 1)  \
                # cleans up left side of top row
            Draw.draw_rectangle(screen, day.x, day.y,
                          COORDS["DAY_OF_WEEK_HEADING"]["w"], MV.monthObj[MV.month].yoffset, 1)   # big rectangle
            temp = pygame.mouse.get_pos()
            temp2 = MV.monthObj[MV.month].yoffset
            if temp[0] > day.x and temp[0] < day.x + COORDS["DAY_OF_WEEK_HEADING"]["w"] and temp[1] > day.y and \
            temp[1] < day.y + temp2:
                Draw.draw_hiLite_rect(screen, day.x, day.y, COORDS["DAY_OF_WEEK_HEADING"]["w"], MV.monthObj[MV.month].yoffset)
                # highlight day mouse cursor is on
                MV.month_index = i  # tells which day is selected
            Draw.draw_rectangle(screen, day.x, day.y, SMALL_RECT_SIZE, SMALL_RECT_SIZE, 1)    # small rectangle
            Draw.draw_text(screen, DAY_NUMBERS[i], day.x, day.y-9, SMALL_RECT_SIZE, SMALL_RECT_TEXT_Y, BLACK, font24)   # number in small rectangle
            value = MV.monthObj[MV.month].mthcomments[i]       # if there is a comment in the mthcomments list, then wordwrap it
            if value != '':
                wrapper = textwrap.TextWrapper(width = 14)
                word_list=wrapper.wrap(text=value)
                ctr2 = 0
                for line in word_list:
                    Draw.draw_text(screen, line, day.x, 7 + day.y+(ctr2*13),COORDS["DAY_OF_WEEK_HEADING"]["w"], COORDS["TEXT_BOX_2"]["w"]+5, BLACK, font13r) # display it to screen
                    ctr2 += 1                             # one line at a time
            temp = MV.monthObj[MV.month].dysinmth-1
            Draw.draw_rectangle(screen, MV.monthObj[MV.month].days[temp].x+COORDS["DAY_OF_WEEK_HEADING"]["w"], MV.monthObj[MV.month].days[temp].y,
                          (6-(MV.monthObj[MV.month].days[temp].x-COORDS["LEFT_SMALL_CAL"]["x"])//COORDS["DAY_OF_WEEK_HEADING"]["w"])*COORDS["DAY_OF_WEEK_HEADING"]["w"], MV.monthObj[MV.month].yoffset, 1)
                           # above cleans up right side of bottom row     
        pygame.display.update()

if __name__ == '__main__':
    main()


           
       
    





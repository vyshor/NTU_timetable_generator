# NTU Timetable Generator

## TL;DR

Download the easy-to-use timetable generator below:

2018/2019 Sem 1: [Updated as of 31/05/2018](http://www.mediafire.com/file/yv6w9yz3y3g9tek/20182019Sem1.zip)

### Information on each file

    UITimetableScheduler - Folder | Codes for the user-friendly version

    scrape_every_class_schedule.py | Scrape every class schedule online and store in allscheduledict.p
    extract_table.py | Scrape the class schedule based on given html
    compile_duplicates.py | Compile the duplicates (with same course, day, timing) and store in compiledscheduledict.p
    prepareddatabase.py | Compile all the class schedule into database in table format
    newtimetablescheduler.py | Generate all possible timetables by checking for clash

    allscheduledict.p | All the raw table information
    compiledscheduledict.p | Compile duplicates from allscheduledict.p
    database.p | Convert into pandas table formats from compiledscheduledict.p

    chromedriver.exe | Webdriver used to scrape information off the website

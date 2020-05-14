# NTU Timetable Generator

## TL;DR

Download the easy-to-use timetable generator below:

2018/2019 Sem 1: [Updated as of 31/05/2018](http://www.mediafire.com/file/yv6w9yz3y3g9tek/20182019Sem1.zip)

2018/2019 Sem 2: [Updated as of 17/11/2018](http://www.mediafire.com/file/9dc76oc38aapn1y/20182019Sem2.zip)

2019/2020 Sem 1: [Updated as of 19/05/2019](http://www.mediafire.com/file/63o6nsie170ruft/20192020Sem1.zip)

2020/2021 Sem 1: [Updated as of 14/05/2020](https://www.mediafire.com/file/kkjnme5zx1g6hh7/20202021Sem1.zip/file)

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

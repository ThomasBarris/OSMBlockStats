# -*- coding: utf-8 -*-
# encoding: utf-8

import requests
from lxml import html               # lib for getting the websites
import pandas as pd                 # for Pandas dataframes and such things
from datetime import datetime       # for parsing and formatting dates
from time import sleep              # let's wait between requests
import numpy as np                  # for timedelta


# what is the highest number of user blocks i.e. www.openstreetmap.org/user_blocks/xyz
max_block_number = 10

# Dataframe columns
columns = ["block_no", "user", "blocked_by", "block_created", "block_ends", "block_text",
           "user_since", "user_no_changesets"]

# list to store the scraped input
list = [[]]

# base urls for users and user blocks
block_base_url = "https://www.openstreetmap.org/user_blocks/"
user_base_url  = "https://www.openstreetmap.org/user/"


# boolean function to test for NaN
def isNaN(num):
    return num != num


# find nth occurrence of the needle in the haystack
def findnth(haystack, needle, n):
    n = n - 1
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

# ##################################################Main Loop#############################################


# iterate from 2 (number 1 was a test user block) to the max number of blocks
for x in range(2, max_block_number+1):
    print(x)

    # building the url to fetch block number x
    block_url = str(block_base_url + str(x))

    # getting content
    pageContent = requests.get(block_url)
    pageContent.encoding = 'utf-8'
    tree = html.fromstring(pageContent.text, 'UTF-8')

    # parsing html from the individual user block page to the elements we need
    blocked_user = tree.xpath('//*[@id="content"]/div[1]/div/h1/a[1]/text()')
    blocked_by   = tree.xpath('//*[@id="content"]/div[1]/div/h1/a[2]/text()')

    # hope this catches empty pages that might be there ...there are some gaps
    if blocked_user == []:
        continue

    # block creation date
    block_created = tree.xpath('/html/body/div[1]/div[2]/div/p[1]/span/@title')

    # if the block was manually released, the "date created" information does not exist there
    # but somewhere else
    try:
        str(block_created[0][0])
        #
    except:
        block_created = tree.xpath('//*[@id="content"]/div[2]/div/p[2]/span/@title')

    # cut after the 3rd space i.e. keep only the date and remove the text and time after the 3rd space
    # if date starts with " 9 December" rather than "09 Dec..." or "9 December"... in case of a single digit date
    # with space in front we need to find the 4rd instead of the third space, which marks the end of the date
    if str(block_created[0][0]) == " ":
        block_start_date = str(block_created[0][:(findnth(str(block_created[0]), " ", 4))])
    else:
        block_start_date = str(block_created[0][:(findnth(str(block_created[0]), " ", 3))])
    # convert to a datetime object
    block_start_date = datetime.strptime(str(block_start_date), '%d %B %Y')

    # get block end date
    block_ends = tree.xpath('/html/body/div[1]/div[2]/div/p[2]/span/@title')

    # in case of zero day block exist no end date, catch the exception and set end date = start date
    try:
        # will cause an exception in case of a zero day block (empty)
        str(block_ends[0])
        # cut after the 3rd space (or 4th as outlined above) i.e. keep only the date
        if str(block_ends[0][0]) == " ":
            block_end_date = str(block_ends[0][:(findnth(str(block_ends[0]), " ", 4))])
        else:
            block_end_date = str(block_ends[0][:(findnth(str(block_ends[0]), " ", 3))])
        # convert to a datetime object
        block_end_date = datetime.strptime(str(block_end_date), '%d %B %Y')
    except:
        block_end_date = block_start_date

    # get the text from the user block
    block_text = tree.xpath('/html/body/div[1]/div[2]/div/div/p/text()')

    # maybe the block text is empty like https://www.openstreetmap.org/user_blocks/200
    try:
        str(block_text[0])
    except:
        block_text = ["0"]

    # ToDo The text can consist of a text array, convert it to a string

    # creating the url for the user profile page to get some more info
    user_url = str(user_base_url + (blocked_user[0]))
    print(str(blocked_user[0]))

    # get the content of the user page
    UserpageContent = requests.get(user_url)
    user_tree = html.fromstring(UserpageContent.text)

    # parsing html from the individual user profile page to the get elements we need i.e. user since and no. changesets
    # extracting the user register date from free text element
    user_since = user_tree.xpath('/html/body/div[1]/div[1]/div/div/div[1]/p/small/text()')

    # get the date out of the long string
    try:
        # try to access information that should be there....in case it isn't, the user is probably deleted
        str(user_since[0][25:])
        # cut the date from the text
        user_since[0] = user_since[0][25:]
        user_since[0] = user_since[0][0:user_since[0].find('  ')]
        user_since[0] = user_since[0].splitlines()[0]
        # convert to a datetime object
        user_since_date = datetime.strptime(str(user_since[0]), '%B %d, %Y')

        # getting the number of changesets the user has now
        user_changeset = user_tree.xpath('/html/body/div[1]/div[1]/div/div/div[1]/ul/li[1]/span/text()')
        # delete the comma ('000 delimiter) and convert to Integer
        user_changeset_count = int(str(user_changeset[0]).replace(",", ""))
    except:
        # if no user profile exist, set register date to 01.01.2001 and changesets to 0
        user_since_date = datetime.strptime(str("January 01, 2001"), '%B %d, %Y')
        user_changeset_count = 0

    #  adding all to the list with the results
    list.append([int(x), str(blocked_user[0]), str(blocked_by[0]), block_start_date, block_end_date,
                 block_text[0], user_since_date, user_changeset_count])

    # wait a bit between requests
    sleep(0.25)


# creating Pandas Dataframe with the result list and delete empty values
block_list = pd.DataFrame(list, columns=columns)
block_list = block_list[isNaN(block_list["block_no"]) == False]


# calc age of a blocked account as of block date
block_list['block_created'] = pd.to_datetime(block_list['block_created'])
block_list['user_since']    = pd.to_datetime(block_list['user_since'])
block_list['account_age_at_block_years'] = (block_list['block_created'] - block_list['user_since'])\
                                           / np.timedelta64(1, 'Y')


# calc the length of punishment
block_list['block_ends'] = pd.to_datetime(block_list['block_ends'])
block_list['block_length_month'] = (block_list['block_ends'] - block_list['block_created'])\
                                   / np.timedelta64(1, 'M')

print(block_list.describe())

# write it to an Excel File
writer = pd.ExcelWriter(u"C:\\Users\.................\\output.xlsx",
                        engine='xlsxwriter', date_format='dd mmm yyyy')

block_list.to_excel(writer, 'Sheet1')
writer.save()

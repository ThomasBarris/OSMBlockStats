import pandas as pd
import time
# import vincent
import numpy as np


import datetime    # for parsing and formating dates

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.transforms

# ************************************* Things to know *************************************************
# for annualising the data...when was it pulled...don't forget to change footnotes/text when you edit this data
most_recent_month = 5
most_recent_year = 2018
# what do you consider as "senior" mapper in years
senior_user_age = 0.5
# deleted users are with 0 changesets and register date 01.01.2001 in the data, i.e. treated like older mapper

# read in the excel file
df_raw = pd.read_excel(u"C:\\Users\\toba0\OneDrive\\Dokumente\\OpenStreetMap\\Projekte\\UserBlockCounter\\output1.xlsx",date_format='dd mmm yyyy')

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


# df_raw['user_since'] = pd.to_datetime(df_raw['user_since'],errors='coerce')

# error at scraping with the calculation of the block duration...wrong formula as per below in v1 of the scraper...recalc it
df_raw['block_length_month'] = (df_raw['block_ends'] - df_raw['block_created'])/ np.timedelta64(1, 'M')

# same with the account age at block date in years
df_raw['account_age_at_block_years'] = (df_raw['block_created'] - df_raw['user_since'])/ np.timedelta64(1, 'Y')

# ****************************************************************************************
# All Blocks by Year
# ****************************************************************************************

# Create a Pandas DataSeries with the block year as index and count the number of blocks in the year
ds_byyear = df_raw.groupby( df_raw['block_created'].dt.year)['block_no'].count()
# convert it to a DataFrame with the columns year and block_count
df_byyear = pd.DataFrame({'year': ds_byyear.index, 'block_count':ds_byyear.values})

# make two Plots at one page. This is number 1
plt.subplot(2,1,1)

# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(211)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
for y in range(0, 600, 200):
    plt.plot(range(2009, 2019), [y] * len(range(2009, 2019)), "--", lw=0.5, color="black", alpha=0.3)


# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

# add and format a chart title
plt.title('All users',fontname="Times New Roman",fontweight="bold", fontsize=20)

# plot the data (x,y,c=color)
plt.plot(df_byyear['year'], df_byyear['block_count'],color=tableau20[1])

# add a label to the y axis
plt.ylabel("User Blocks")

# ****************************************************************************************
# Median Block Duration by Year
# ****************************************************************************************

# create a DataSeries with the data we need, calc the mean by year and convert it to a Dataframe
ds_bylength =df_raw.groupby( df_raw['block_created'].dt.year)['block_length_month'].mean()
df_bylength = pd.DataFrame({'year': ds_bylength.index, 'block_length':ds_bylength.values})

# the chart will be together with the previous one
plt.subplot(2,1,2)

# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(212)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
for y in range(0, 30, 10):
    plt.plot(range(2009, 2019), [y] * len(range(2009, 2019)), "--", lw=0.5, color="black", alpha=0.3)


# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

# plot the chart and add axis labels
plt.plot(df_bylength['year'], df_bylength['block_length'], color=tableau20[3])
plt.xlabel("Year")
plt.ylabel("Median block length (month)")

# we may want to know how the data looks like
print (df_byyear)
print (df_bylength)

# show chart and close it afterwards
plt.show()
plt.close()


# ****************************************************************************************
# All Blocks by Year with 2018 annualized
# ****************************************************************************************

# we already did it for the not annualised chart
#ds_byyear =df_raw.groupby( df_raw['block_created'].dt.year)['block_no'].count()
#df_byyear = pd.DataFrame({'year': ds_byyear.index, 'block_count':ds_byyear.values})

# row 9 is 2018
latest_row = most_recent_year - 2009

# annualise the number of blocks in the most recent year
df_byyear.loc[latest_row]['block_count']= int(df_byyear.loc[latest_row]['block_count']/(most_recent_month+1)*12)

# make two Plots at one page. This is number 1
plt.subplot(2,1,1)

# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(211)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
for y in range(0, 600, 200):
    plt.plot(range(2009, 2019), [y] * len(range(2009, 2019)), "--", lw=0.5, color="black", alpha=0.3)


# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")


# format chart and add blocks per year
plt.title('All users',fontname="Times New Roman",fontweight="bold", fontsize=20)
plt.plot(df_byyear['year'], df_byyear['block_count'],color=tableau20[1])
plt.ylabel("User Blocks")

# add footnote
plt.figtext(0.09, 0.01, '2018 annualised i.e. /6*12', horizontalalignment='left', fontsize = 6)



# ****************************************************************************************
# Median Block Duration by Year
# ****************************************************************************************

# we already did it
#ds_bylength =df_raw.groupby( df_raw['block_created'].dt.year)['block_length_month'].mean()
#df_bylength = pd.DataFrame({'year': ds_bylength.index, 'block_length':ds_bylength.values})

# plot number 2 on this page
plt.subplot(2,1,2)

# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(212)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
for y in range(0, 30, 10):
    plt.plot(range(2009, 2019), [y] * len(range(2009, 2019)), "--", lw=0.5, color="black", alpha=0.3)


# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

# plot the chart and add axis labels
plt.plot(df_bylength['year'], df_bylength['block_length'], color=tableau20[3])
plt.xlabel("Year")
plt.ylabel("Median block length (month)")

# we may want to know how the data looks like
print (df_byyear)
print (df_bylength)

# show chart and close it afterwards
plt.show()
plt.close()

# ****************************************************************************************
# User blocks by year divided into senior or newbie users
# ****************************************************************************************

# add a bool column with is True when considered as senior user
df_raw['senior_user'] = df_raw['account_age_at_block_years'] > senior_user_age

# create two dataframes with user name and block created date
df_newbie =df_raw.loc[df_raw['senior_user'] == False, ['user','block_created']]
df_senior = df_raw.loc[df_raw['senior_user'] == True, ['user','block_created']]

# create two dataseries with the year and the number of block per year
ds_newbie_year = df_newbie.groupby( df_newbie['block_created'].dt.year)['block_created'].count()
ds_senior_year = df_senior.groupby( df_senior['block_created'].dt.year)['block_created'].count()

# create a dataframe with columns year and newbie blocks
df_bytype_year = pd.DataFrame({'year': ds_newbie_year.index, 'newbie_blocks':ds_newbie_year.values})
# add the senior dataseries
df_bytype_year['senior'] = ds_senior_year.values

# row 9 is 2018...already defined earlier
# latest_row = most_recent_year - 2009

# annualise the numbers of blocks (newbie and senior) in the most recent year
df_bytype_year.loc[latest_row]['newbie_blocks']= int(df_bytype_year.loc[latest_row]['newbie_blocks']/(most_recent_month+1)*12)
df_bytype_year.loc[latest_row]['senior']= int(df_bytype_year.loc[latest_row]['senior']/(most_recent_month+1)*12)


# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
for y in range(0, 400, 100):
    plt.plot(range(2009, 2019), [y] * len(range(2009, 2019)), "--", lw=0.5, color="black", alpha=0.3)


# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

# add title
plt.title('New Mappers vs Seniors (>6 months)',fontname="Times New Roman",fontweight="bold", fontsize=20 )

# plot new and senior blocks by year
plt.plot(df_bytype_year['year'], df_bytype_year['newbie_blocks'], color=tableau20[5])
plt.plot(df_bytype_year['year'], df_bytype_year['senior'], color=tableau20[7])          # y Axis

# label x-axis
plt.ylabel("User Blocks")

# add text labels at the right side (year 2018.2) next to last value df_bytype_year['newbie_blocks'].values[-1]
y_pos = df_bytype_year['newbie_blocks'].values[-1] - 0.2
plt.text(2018.2, y_pos, "New Mappers", fontsize=10, color=tableau20[5])
# again a label for senior mappers
y_pos = df_bytype_year['senior'].values[-1] - 0.2
plt.text(2018.2, y_pos, "Seniors", fontsize=10, color=tableau20[7])

# add footnote
plt.figtext(0.09, 0.01, '2018 annualised i.e. /6*12', horizontalalignment='left', fontsize = 6)

# print data together with the chart and close the chart
print (df_bytype_year)
plt.show()
plt.close()


# ****************************************************************************************
# User block duration by year divided into senior or newbie users
# ****************************************************************************************

# create two dataframes with user name and block duration
df_newbie_length = df_raw.loc[df_raw['senior_user'] == False,['block_created','block_length_month']]
df_senior_length = df_raw.loc[df_raw['senior_user'] == True, ['block_created','block_length_month']]

# create two dataseries with the year and the block duration per year
ds_newbie__length = df_newbie_length.groupby( df_newbie['block_created'].dt.year)['block_length_month'].mean()
ds_senior_length  = df_senior_length.groupby( df_senior['block_created'].dt.year)['block_length_month'].mean()

# create a dataframe with columns year and block duration
df_length_byyear = pd.DataFrame({'year': ds_newbie__length.index, 'block_length_month':ds_newbie__length.values})
# add senior values
df_length_byyear['senior'] = ds_senior_length.values


# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
for y in range(0, 40, 10):
    plt.plot(range(2009, 2019), [y] * len(range(2009, 2019)), "--", lw=0.5, color="black", alpha=0.3)


# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

# add chart title and the two data series for block duration (senior and newbie
plt.title('Mean Block Duration', fontname="Times New Roman",fontweight="bold", fontsize=20)
plt.plot(df_length_byyear['year'], df_length_byyear['block_length_month'], color=tableau20[9])
plt.plot(df_length_byyear['year'], df_length_byyear['senior'], color=tableau20[11])          # y Axis

# label y axis and add text labels at the right side next where the lines end
plt.ylabel("Block Duration")
y_pos = df_length_byyear['block_length_month'].values[-1] - 0.5
plt.text(2018.2, y_pos+2, "New Mappers", fontsize=10, color=tableau20[9])
y_pos = df_length_byyear['senior'].values[-1] - 0.5
plt.text(2018.2, y_pos-1, "Seniors", fontsize=10, color=tableau20[11])

# print dataframe together with the chart
print(df_length_byyear)
plt.show()
plt.close()


# ****************************************************************************************
# Average block duration and block count by DWG member by senior/newbie
# ****************************************************************************************

# create two dataframes with blocked by name and block duration
df_newbie_dwg       = df_raw.loc[df_raw['senior_user'] == False,['blocked_by','block_length_month']]
df_senior_dwg       = df_raw.loc[df_raw['senior_user'] == True, ['blocked_by','block_length_month']]

# create two dataseries with blocked by name and block duration average
ds_newbie_dwg       = df_newbie_dwg.groupby( df_newbie_dwg['blocked_by'])['block_length_month'].mean()
ds_senior_dwg       = df_senior_dwg.groupby( df_senior_dwg['blocked_by'])['block_length_month'].mean()

# create two dataseries with blocked by name and block count
ds_newbie_dwg_count = df_newbie_dwg.groupby( df_newbie_dwg['blocked_by'])['block_length_month'].count()
ds_senior_dwg_count = df_senior_dwg.groupby( df_senior_dwg['blocked_by'])['block_length_month'].count()

# create a dataframe and put it all together
df_dwg = pd.concat([ds_newbie_dwg,ds_senior_dwg, ds_newbie_dwg_count, ds_senior_dwg_count ], ignore_index=True, axis=1, sort=True )
# add descriptive column names
df_dwg.columns=["junior_length","senior_length", "junior_count", "senior_count"]

#rename row index OSMF Data Working Group to DWG as it is too long for the chart
df_dwg.rename(index={'OSMF Data Working Group':'DWG'}, inplace=True)

ax = plt.subplot(1,1,1)
# Remove the plot frame lines. They are unnecessary chartjunk.
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# add the chart data x-axis = dwg blocked by name, y-axis block duration  for seniors and newbiews ....
# ...and bubble size = junior/senior block count, assigning labels added later. The sneior buubles are on typ of juniors...
# ...there transparent alpha=...
plt.scatter(x=df_dwg.index, y=df_dwg["junior_length"], color=tableau20[0], s = df_dwg["junior_count"], label='New Mappers\n ')
plt.scatter(x=df_dwg.index, y=df_dwg["senior_length"], color=tableau20[18], s = df_dwg["senior_count"], label='Seniors', alpha = 0.7)

# format the chart area
ax.set_title("Strongest Judges by Mapper Type", fontname="Times New Roman",fontweight="bold", fontsize=20)
ax.grid(axis="y", color="grey")
ax.set_facecolor("white")
ax.legend(frameon=False)

# footnote
plt.figtext(0.09, 0.01, 'Bubble size represents number of blocks', horizontalalignment='left', fontsize = 6)

# y-axis label
plt.ylabel("Block Duration")

# turn x-axsis labels
plt.setp( ax.xaxis.get_majorticklabels(), rotation=-45, ha="left",rotation_mode="anchor" )

# print dataframe together with the chart
print(df_dwg)
plt.show()
plt.close()

# ****************************************************************************************
# Average block duration and block count by DWG member by senior/newbie
# ****************************************************************************************

# drop the outliers DWG and emacsen
df_dwg.drop(['DWG','emacsen'], inplace=True)

ax = plt.subplot(1,1,1)
# Remove the plot frame lines. They are unnecessary chartjunk.
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# add the chart data x-axis = dwg blocked by name, y-axis block duration  for seniors and newbiews ....
# ...and bubble size = junior/senior block count, assigning labels added later. The sneior buubles are on typ of juniors...
# ...there transparent alpha=
plt.scatter(x=df_dwg.index, y=df_dwg["junior_length"], color=tableau20[0], s = df_dwg["junior_count"], label='New Mappers\n ')
plt.scatter(x=df_dwg.index, y=df_dwg["senior_length"], color=tableau20[18], s = df_dwg["senior_count"], label='Seniors', alpha = 0.7)

# format the chart area
ax.set_title("Strongest Judges by Mapper Type", fontname="Times New Roman",fontweight="bold", fontsize=20)
ax.grid(axis="y", color="grey")
ax.set_facecolor("white")
ax.legend(frameon=False)

# footnote
plt.figtext(0.09, 0.01, 'Bubble size represents number of blocks\nex OSMF DWG account (avg 267 months for 6 junior blocks) and emacsen (101 months for 30x senior blocks)', horizontalalignment='left', fontsize = 6)

# y axis label and label turn by 45 degrees
plt.ylabel("Block Duration")
plt.setp( ax.xaxis.get_majorticklabels(), rotation=-45, ha="left",rotation_mode="anchor" )

# print data and chart
print(df_dwg)
plt.show()
plt.close()

# ****************************************************************************************
# Daily block activity
# ****************************************************************************************

# create a dataseries with the count of blocks by day and convert it to a dataframe
ds_activity = df_raw.groupby( df_raw['block_created'].dt.date)['block_created'].count()
df_activity = pd.DataFrame({'year': ds_activity.index, 'block_created':ds_activity.values})


# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# add chart title and print chart ...pretty easy
plt.title('Block Activity by Date',fontname="Times New Roman",fontweight="bold", fontsize=20 )
plt.plot(df_activity['year'],df_activity['block_created'],  color=tableau20[1])

# show data and chart
print(df_activity)
plt.show()
plt.close()


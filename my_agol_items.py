# -*- coding: utf-8 -*-
# Python script pulls AGOL user item info into a spreadsheet

# Enter your arcgis online account below:
my_agol_user = "place_your_agol_username_here"

print ('importing libraries')
from arcgis import GIS
from datetime import date
import pandas as pd
import os

# Log in via users credentials stored in ArcGIS Pro
print ('connecting to your ArcGIS Online account')
gis = GIS("pro", verify_cert=False)

if os.path.exists('my_agol_items.xlsx'):
  os.remove('my_agol_items.xlsx')

# Set up a search for your content, then extract owner, title, etc.
my_content = gis.content.search("owner:" + my_agol_user, max_items=4000)

print('gathering your item details')
my_data = []

for i in my_content:
  try:
    txt_owner = i['owner']
    txt_title = i['title']
    txt_type = i['type']
    item_size = i.size
    upd_yr = time.localtime(i.modified/1000)[0]
    upd_mo = time.localtime(i.modified/1000)[1]
    upd_dy = time.localtime(i.modified/1000)[2]
    update_date = date(upd_yr, upd_mo, upd_dy)    
    if txt_title is None and txt_type is not None:
      row_tuple = (txt_owner, '', txt_type, item_size, update_date)
    elif txt_title is not None and txt_type is None:
      row_tuple = (txt_owner, txt_title, '', item_size, update_date)
    elif txt_title is None and txt_type is None:
      row_tuple = (txt_owner, '', '', item_size, update_date)
    else:
      row_tuple = (txt_owner, txt_title, txt_type, item_size, update_date)
  except:
    row_tuple = (txt_owner, 'non ascii error', txt_type, item_size, update_date)
  my_data.append(row_tuple)

# bring items into a data frame, then export to Excel
df = pd.DataFrame(my_data, columns = ['owner', 'title', 'type', 'bytes', 'updated'])

writer = pd.ExcelWriter('my_agol_items.xlsx')

df.to_excel(writer, sheet_name='my_agol')

writer.save()

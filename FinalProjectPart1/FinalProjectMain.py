"""
Name: Samuel Barroso
ID: 1844307
"""

import csv

#nested dictionary
#each entry will include a dictionary for a specific item
#key values for each dictionary is the id for the item
#key values within each item are manufacturer, item_type, condition, price, and service_date
master_list = {}

#opens the first csv file and adds each item entry to master_list
with open('FinalProjectManufacturerListINPUT.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        id = row[0]
        master_list[id] = {"manufacturer": row[1], "item_type": row[2], "condition": row[3]}

#opens the remaining csv files and uses the update() function to include new values to master_list
with open('FinalProjectPriceListINPUT.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        id = row[0]
        master_list[id].update({"price": row[1]})
with open('FinalProjectServiceDatesListINPUT.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        id = row[0]
        master_list[id].update({"service_date": row[1]})

#takes the master_list and creates full_inventory
#full_inventory is sorted by manufacturing date
#I was unsure if we were allowed to use the sort() function, so I decided to sort it myself
full_invetory = master_list
new_list = []
for id in full_invetory:
    if len(new_list) == 0:
        temp_dict = full_invetory[id]
        temp_dict.update({"id": id})
        new_list.append(temp_dict)
    else:
        changed = False
        for i in range(len(new_list)):
            if new_list[i]["manufacturer"] > full_invetory[id]["manufacturer"]:
                temp_dict = full_invetory[id]
                temp_dict.update({"id": id})
                new_list.insert(i, temp_dict)
                changed = True
                break
        if not changed:
            temp_dict = full_invetory[id]
            temp_dict.update({"id": id})
            new_list.append(temp_dict)
full_invetory = new_list

#takes full_inventory and writes values to a new csv file
#rows are ordered by id, manufacturer, item_type, price, service_date, and condition
with open('FinalProjectFullInventory.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for item in full_invetory:
        ordered_array = []
        ordered_array.append(item['id'])
        ordered_array.append(item['manufacturer'])
        ordered_array.append(item['item_type'])
        ordered_array.append(item['price'])
        ordered_array.append(item['service_date'])
        ordered_array.append(item['condition'])
        writer.writerow(ordered_array)

#takes the master_list and creates item_type_inventory
#key values in item_type_inventory are all of the item types from master_list
item_type_inventory = {}
for id in master_list:
    item_type = master_list[id]["item_type"]
    try:
        item_type_inventory[item_type][id] = master_list[id]
    except:
        item_type_inventory[item_type] = {}
        item_type_inventory[item_type][id] = master_list[id]


#takes item_type_inventor and writes values to a new csv file
#rows are ordered by id, manufacturer, price, service_date, and condition
#writes each item type to it's own csv file
#all items are sorted by their item ID
for dict in item_type_inventory:
    file_name = "FinalProject" + dict.capitalize() + "Inventory.csv"
    with open(file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        item_list = []
        for id in item_type_inventory[dict]:
            item = item_type_inventory[dict][id]
            ordered_array = []
            ordered_array.append(item['id'])
            ordered_array.append(item['manufacturer'])
            ordered_array.append(item['price'])
            ordered_array.append(item['service_date'])
            ordered_array.append(item['condition'])
            item_list.append(ordered_array)
        new_list = []
        for char in item_list:
            if len(new_list) == 0:
                new_list.append(char)
            else:
                changed = False
                for i in range(len(new_list)):
                    if item_list[i][0] > char[0]:
                        new_list.insert(i, char)
                        changed = True
                        break
                if not changed:
                    new_list.append(char)
        item_list = new_list
        writer.writerows(item_list)

#auxilary function for comparing values by date
def time_greater_than(date1, date2):
    date1_arr = date1.split("/")
    date2_arr = date2.split("/")
    if int(date1_arr[2]) > int(date2_arr[2]):
        return True
    elif int(date1_arr[2]) == int(date2_arr[2]):
        if int(date1_arr[0]) > int(date2_arr[0]):
            return True
        elif int(date1_arr[0]) == int(date2_arr[0]):
            if int(date1_arr[1]) > int(date2_arr[1]):
                return True
    return False

#takes the master_list and creates past_date_inventory
#sorts past_date_inventory from oldest to most recent
past_date_inventory = []
for id in master_list:
    date = master_list[id]["service_date"]
    if len(past_date_inventory) == 0:
        past_date_inventory.append(master_list[id])
    else:
        changed = False
        for i in range(len(past_date_inventory)):
            date_temp = past_date_inventory[i]['service_date']
            if time_greater_than(date_temp, date):
                past_date_inventory.insert(i, master_list[id])
                changed = True
                break
        if not changed:
            past_date_inventory.append(master_list[id])

#takes the sorted past_date_inventory and removes all entries past todays date
today = "4/9/2023"
temp_dict = []
for item in past_date_inventory:
    date_temp = item['service_date']
    if time_greater_than(today, date_temp):
        temp_dict.append(item)
past_date_inventory = temp_dict

#takes past_date_inventory and writes values to a new csv file
#rows are ordered by id, manufacturer, item_type, price, service_date, and condition
with open('FinalProjectPastServiceDateInventory.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for item in past_date_inventory:
        ordered_array = []
        ordered_array.append(item['id'])
        ordered_array.append(item['manufacturer'])
        ordered_array.append(item['item_type'])
        ordered_array.append(item['price'])
        ordered_array.append(item['service_date'])
        ordered_array.append(item['condition'])
        writer.writerow(ordered_array)

#takes the master_list and creates damaged_invetory
#this removes all values that are not damaged
damaged_invetory = master_list
temp_dict = []
for id in damaged_invetory:
    if damaged_invetory[id]['condition'] == "damaged":
        temp_dict.append(damaged_invetory[id])
damaged_invetory = temp_dict

#sort damaged_inventory by price
temp_dict = []
for item in damaged_invetory:
    if len(temp_dict) == 0:
        temp_dict.append(item)
    else:
        changed = False
        for i in range(len(temp_dict)):
            if temp_dict[i] > item:
                new_list.insert(i, item)
                changed = True
                break
        if not changed:
            new_list.append(item)
damaged_invetory = temp_dict

#takes damaged_invetory and writes values to a new csv file
#rows are ordered by id, manufacturer, item_type, price,and service_date
with open('FinalProjectDamagedInventory.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for item in damaged_invetory:
        ordered_array = []
        ordered_array.append(item['id'])
        ordered_array.append(item['manufacturer'])
        ordered_array.append(item['item_type'])
        ordered_array.append(item['price'])
        ordered_array.append(item['service_date'])
        writer.writerow(ordered_array)


#this code will sort a list alphabetically
#this algorithm I created was used throughout the project
"""
old_list = [*insert filled list here*]
new_list = []
for char in old_list:
    if len(new_list) == 0:
        new_list.append(char)
    else:
        changed = False
        for i in range(len(new_list)):
            if new_list[i] > char:
                new_list.insert(i, char)
                changed = True
                break
        if not changed:
            new_list.append(char)
old_list = new_list
print(new_list)
"""
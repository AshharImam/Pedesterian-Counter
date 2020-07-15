# import os


# for x, y, z in os.walk("../people-counting-opencv/data"):

#     print(z)
dict_arr = ['02', '03', '04', '10', '11', '12', '12', '14', '15']
i = 0
currTimeArr = ['12', '15']
endTimeArr = ['15', '30']
for time in currTimeArr:
    if i == 0:
        for hr in range(int(time), int(endTimeArr[0])):
            finalHour = [key for key in dict_arr if (key.startswith(time))]
            if finalHour:
                print(finalHour[0])
                break
from flask import Flask, json, jsonify
import os.path
from datetime import date

app = Flask(__name__)


def req_json(*args):
    listOfDates = []
    if len(args) == 0:
        listOfDates.append(str(date.today().strftime("%Y-%m-%d")))
        print("here")
    elif len(args) == 1:
        listOfDates.append(args[0])
    elif len(args) == 2:
        # print(args[0], args[1])
        boo = []
        for x, y, z in os.walk("../people-counting-opencv/data"):
            for z in z:
                z = z.split('.')
                boo.append(z[0])

        # print(boo)
        if args[0] in boo and args[1] in boo:
            start = boo.index(args[0])
            end = boo.index(args[1]) if len(boo) == boo.index(
                args[1]) else (boo.index(args[1]) + 1)
            listOfDates = boo[start: end]
            print(listOfDates)
        # if args[0] in boo and args[1] in boo:
        #     listOfDates = boo[boo.index(args[0], boo.index(args[1]))]
        #     print(listOfDates, 'dassda')
    js = {}
    for _date in listOfDates:
        f = []
        if os.path.exists("./data/" + str(_date) + ".txt"):
            with open("./data/" + _date + ".txt") as a:
                for l in a:
                    n = l.rstrip('\n')
                    n = f.append(n.split(','))
                    # print(n)

                for line in f:
                    # print(line)
                    if line[0] in js:
                        js[line[0]] = {
                            "in": int(js[line[0]]["in"])+int(line[1]),
                            "out": int(js[line[0]]["out"])+int(line[2])
                        }
                    else:
                        js[line[0]] = {
                            "in": int(line[1]),
                            "out": int(line[2])

                        }
    return js


# def check():
#     print()
#     return args


def sumInOut(dict_arr):
    sumIn = 0
    sumOut = 0
    for key in dict_arr:
        sumIn += int(dict_arr[key]["in"])
        sumOut += int(dict_arr[key]["out"])
    return [sumIn, sumOut]

def nextTime(currTimeArr, endTimeArr, dict_arr):
    i = 0
    finalHour = 0
    for hr in range(int(currTimeArr[0]), int(endTimeArr[0])):
        finalHours = [key for key in dict_arr if (key.startswith(str(hr)))]
        if finalHours:
            
            return finalHours
    
    return False



def specific_time(dict_arr, timeTo, timeFrom):
    sumIn = 0
    sumout = 0
    timeTo = timeTo.split(':')
    timeFrom = timeFrom.split(':')
    print(timeTo, timeFrom)
    sTimeStr = timeTo[0]+':'+timeTo[1] if len(timeTo) > 1 else timeTo[0]
    sHrTime = [key for key in dict_arr if (key.startswith(sTimeStr))]
    if len(sHrTime) == 0:
        sHrTime = nextTime(timeTo, timeFrom, dict_arr)
             
    # print(sHrTime[0])
    eTimeStr = timeFrom[0]+':'+timeFrom[1] if len(timeFrom) > 1 else timeFrom[0]
    eHrTime = [key for key in dict_arr if (key.startswith(eTimeStr))]
    if len(eHrTime) == 0:
        eHrTime = nextTime(timeFrom, ['24'], dict_arr)
    js = {}
    # print(eTimeStr)
    # print(eHrTime[0])
    flag = False
    if sHrTime and eHrTime:
        for key, value in dict_arr.items():
            # print(value['in'])
            if key == sHrTime[0]:
                print("we hit hrer ")
                flag = True
            if key == eHrTime[0]:            
                break
            if flag == True:
                if key in js:
                    js[key] = {
                        "in": int(js[key]["in"])+int(value["in"]),
                        "out": int(js[key]["out"])+int(value["out"])
                        }
                else:
                    js[key] = {
                        "in": int(value["in"]),
                        "out": int(value["out"])

                            }
    else:
        return {}
    # print(js)
    # for time in dict_arr:

    return js
# all data


@app.route("/")
def home():
    dict_arr = req_json()
    return jsonify(dict_arr)

# total of todays


@ app.route("/data")
def data():
    dict_arr = req_json()
    sum_arr = sumInOut(dict_arr)
    return jsonify({
        "totalIn": sum_arr[0],
        "totalOut": sum_arr[1]
    })

# of a specific date


@ app.route("/date/<date>")
def dateWise(date):
    js = req_json(date)
    sum_arr = sumInOut(js)
    return jsonify({
        "totalIn": sum_arr[0],
        "totalOut": sum_arr[1]
    })

# from <date> To <date>


@ app.route("/date/<dateFrom>/<dateTo>")
def dateToFrom(dateFrom, dateTo):
    sum_arr = sumInOut(req_json(dateFrom, dateTo))
    return jsonify({
        "totalIn": sum_arr[0],
        "totalOut": sum_arr[1]
    })


@ app.route("/time/<date>/<timeTo>/<timeFrom>")
def timeOfSpecificDate(date, timeTo, timeFrom):
    dict_arr = req_json(date)
    js = specific_time(dict_arr, timeTo, timeFrom)
    sum_arr = sumInOut(js)
    return jsonify({
        "totalIn": sum_arr[0],
        "totalOut": sum_arr[1]
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)

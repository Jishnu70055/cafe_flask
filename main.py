from flask import Flask ,request
import pymongo


app = Flask(__name__)


myclient = pymongo.MongoClient("mongodb://13.233.190.38:27017/")
mydb = myclient['cafe']
customers = mydb["customers"]
tables = mydb['tables']
bookings = mydb['booking']


@app.route("/customeraccount" ,methods = ['POST'])
def customeraccount():
    request_payloads = request.json
    cus = request_payloads['customer']
    customers.insert_one({"_id":cus['name'] ,"mobile_no":cus['mobile_number'] })
    return "Added"


@app.route("/table" ,methods = ['POST'])
def table():
    request_payloads = request.json
    tab = request_payloads['table']
    tables.insert_one({"_id":tab['name'] ,"capacity":tab['capacity'] })
    return "Added table"


@app.route("/booking" ,methods = ['POST'])
def booking():
    request_payloads = request.json
    book = request_payloads['book']
    custom = customers.find({"_id":book['customer_name']})
    if custom:
        tabl = tables.find({"_id":book['table_name']})
        if tabl:
            for tab in tabl:
                for cus in custom:
                    booked_table = bookings.find({"table_id":book['table_name'],"date":book['date']})
                    # booked_table = bookings.find({"table_id":book['table_name']},{"date":book['date']},{"from_time":book['from_time']})
                    if booked_table:
                        for time in booked_table:
                            start_time = time['from_time']
                            end_time = time['end_time']
                            book_from_time = book['from_time']
                            book_to_time = book['end_time']
                            def is_between(time, time_range):
                                if time_range[1] < time_range[0]:
                                    return time >= time_range[0] or time <= time_range[1]
                                return time_range[0] <= time <= time_range[1]

                            from_time_check = is_between(book_from_time, (start_time, end_time))
                            to_time_check = is_between(book_to_time, (start_time, end_time))

                            if from_time_check == True:
                                return "The Time is Already Booked"
                            elif to_time_check == True:
                                return "The Time is Already Booked"
                            else:
                                bookings.insert_one({"customer_id":cus['_id'] ,"table_id":tab['_id'] ,"date":book['date'],"from_time":book['from_time'] ,"end_time":book['end_time'] })
                                # booking.insert_one({"customer_id":cus['_id'] ,"table_id":tab['_id'] ,"date":book['date'],"from_time":book['from_time' ,"end_time":book['end_time']] })
                                return "Booked Sucessfully"

                        

                            

                
                        

                    

        else:
            return "Not a Valid table"
                
    else:
        return "Not a valid Customer"


if __name__ == '__main__':
    app.run(debug=True ,port=5000)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, json, request
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGODB_URI", "mongodb://localhost:27017/myDatabase")
mongo = PyMongo(app)


@app.route('/')
def showEmployeelist():
    return render_template('list.html')


@app.route("/addEmployee", methods=['POST'])
def addEmployee():
    json_data = request.json['info']

    # check type of incoming data
    # data_check.check_types(json_data)

    employeeName = json_data['employee']
    jobtitle = json_data['job']
    basesalary = float(json_data['salary'])
    medicalinsurance = float(json_data['insurance_pay'])
    take_home_pay = float(json_data['real_pay'])

    mongo.db.Employees.insert_one({
            'employee': employeeName, 'job': jobtitle, 'salary': basesalary, 'insurance_pay': medicalinsurance, 'real_pay': take_home_pay
        })

    return jsonify(status='OK', message='inserted successfully')


@app.route('/getEmployee/<eid>', methods=['GET'])
def getEmployee(eid):
    employeeId = eid
    employee = mongo.db.Employees.find_one({'_id': ObjectId(employeeId)})
    employeeDetail = {
        'employee': employee['employee'],
        'job': employee['job'],
        'salary': employee['salary'],
        'insurance_pay': employee['insurance_pay'],
        'real_pay': employee['real_pay'],
        'id': str(employee['_id'])
    }

    return json.dumps(employeeDetail)



@app.route('/updateEmployee', methods=['PUT'])
def updateEmployee():
    employeeInfo = request.json['info']
    # data_check.check_types(employeeInfo)

    employeeId = employeeInfo['id']
    employeeName = employeeInfo['employee']
    jobtitle = employeeInfo['job']
    basesalary = float(employeeInfo['salary'])
    medicalinsurance = float(employeeInfo['insurance_pay'])
    take_home_pay = float(employeeInfo['real_pay'])

    mongo.db.Employees.update_one({'_id': ObjectId(employeeId)}, {
        '$set': {'employee': employeeName, 'job': jobtitle, 'salary': basesalary, 'insurance_pay': medicalinsurance, 'real_pay': take_home_pay}})
    return jsonify(status='OK', message='updated successfully')


@app.route("/getEmployeeList", methods=['GET'])
def getEmployeeList():
    employees = mongo.db.Employees.find()
    employeeList = []

    for employee in employees:
        employeeItem = {
            'employee': employee['employee'],
            'job': employee['job'],
            'salary': employee['salary'],
            'insurance_pay': employee['insurance_pay'],
            'real_pay': employee['real_pay'],
            'id': str(employee['_id'])
        }

        employeeList.append(employeeItem)

    return json.dumps(employeeList)

@app.route("/deleteEmployee", methods=['POST'])
def deleteEmployee():
    try:
        employeeId = request.json['id']
        mongo.db.Employees.remove({'_id': ObjectId(employeeId)})
        return jsonify(status='OK', message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


if __name__ == "__main__":
    app.run(debug=True)

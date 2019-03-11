from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, json, request
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGODB_URI", "mongodb://localhost:27017/myDatabase")
mongo = PyMongo(app)

@app.route("/addEmployee", methods=['POST'])
def addEmployee():
    try:
        json_data = request.json['info']
        employeeName = json_data['employee']
        jobtitle = json_data['job']
        basesalary = json_data['salary']
        medicalinsurance = json_data['insurance_pay']
        take_home_pay = json_data['real_pay']
        mongo.db.Employees.insert_one({
            'employee': employeeName, 'job': jobtitle, 'salary': basesalary, 'insurance_pay': medicalinsurance, 'real_pay': take_home_pay
        })
        return jsonify(status='OK', message='inserted successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/')
def showEmployeelist():
    return render_template('list.html')


@app.route('/getEmployee', methods=['POST'])
def getEmployee():
    try:
        employeeId = request.json['id']
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
    except Exception as e:
        return str(e)



@app.route('/updateEmployee', methods=['PUT'])
def updateEmployee():
    try:
        employeeInfo = request.json['info']
        employeeId = employeeInfo['id']
        employeeName = employeeInfo['employee']
        jobtitle = employeeInfo['job']
        basesalary = employeeInfo['salary']
        medicalinsurance = employeeInfo['insurance_pay']
        take_home_pay = employeeInfo['real_pay']

        mongo.db.Employees.update_one({'_id': ObjectId(employeeId)}, {
            '$set': {'employee': employeeName, 'job': jobtitle, 'salary': basesalary, 'insurance_pay': medicalinsurance, 'real_pay': take_home_pay}})
        return jsonify(status='OK', message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route("/getEmployeeList", methods=['GET'])
def getEmployeeList():
    try:
        employees = mongo.db.Employees.find()

        employeeList = []
        for employee in employees:
            print(employee)
            employeeItem = {
                'employee': employee['employee'],
                'job': employee['job'],
                'salary': employee['salary'],
                'insurance_pay': employee['insurance_pay'],
                'real_pay': employee['real_pay'],
                'id': str(employee['_id'])
            }
            employeeList.append(employeeItem)
    except Exception as e:
        return str(e)
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

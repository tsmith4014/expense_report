# app.py, this script, is the entry point of the application. It defines a Flask app that generates an Excel file based on the data submitted through a form, using a pre-defined template.  It works with the populate_excel.py script, which contains the logic for populating the template with data. The populate_excel.py script is imported in the app.py script. The app.py script has two routes: '/' renders a form for inputting data, and '/generate-excel' generates an Excel file based on the data submitted through the form and returns it as an attachment.
"""
This script defines a Flask app that generates an Excel file based on the data submitted through a form, using a pre-defined template.
The app has two routes: 
    - '/' renders a form for inputting data
    - '/generate-excel' generates an Excel file based on the data submitted through the form and returns it as an attachment.
"""
# app.py
from flask import Flask, render_template, request, send_file
from populate_excel import populate_template

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(error):
    # You can log the error here if you'd like to review it in your server logs
    print(f"An error occurred: {error}")  # Example of simple logging
    
    # Return the custom error page
    return render_template("error.html"), 500

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/', methods=['GET'])
def form():
    # Render a form for inputting data
    return render_template('index.html')

@app.route('/generate-excel', methods=['POST'])
def generate_excel():
    """
    Generates an Excel file based on the data submitted through a form, using a pre-defined template.

    Returns:
        The generated Excel file as an attachment.
    """
    # Get data from form
    data = {
        'school': request.form['school'],
        'period_ending': request.form['periodEnding'],
        'trip_purpose': request.form['tripPurpose'],
        'travel': request.form.get('travel'),
        'travel_start_date': request.form.get('travelStartDate'),
        'travel_end_date': request.form.get('travelEndDate'),
        'employee_department': request.form['employeeDepartment'],
        # Capture new mileage-related data
        'mileage': request.form.get('mileage'),  # Check if mileage checkbox is selected
        'mileage_date': request.form.get('mileageDate'),  # The date of the mileage
        'mileage_amount': request.form.get('mileageAmount'),  # The mileage amount
    
    }

    # Define paths
    template_path = 'expense_report.xlsx'
    output_path = 'output.xlsx'

    # Populate the template
    populate_template(data, template_path, output_path)

    # Send the populated Excel file to the user
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 
    
    # If you change this to False, you'll need to restart the app manually after each change but this needs to be False when you deploy the app to production or it will be accessible to anyone because debug mode is insecure and should never be used in production.  This is because it allows arbitrary code execution.  If an attacker can run arbitrary code on your machine, they can do anything they want to it.  The attacker can read any file on your machine, modify any file on your machine, and even execute arbitrary system commands.  This is why debug mode is insecure and should never be used in production.  It's only meant to be used in development.  To test this in the frontend console type: fetch('/generate-excel', {method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: 'school=University+of+California%2C+Berkeley&periodEnding=2020-12-31&tripPurpose=Business'}).then(response => response.blob()).then(blob => {const url = window.URL.createObjectURL(blob);const a = document.createElement('a');a.style.display = 'none';a.href = url;a.download = 'output.xlsx';document.body.appendChild(a);a.click();window.URL.revokeObjectURL(url);alert('your file has downloaded!');}).catch(() => alert('oh no!'));  An attacked can see files inside by typing in the console: fetch('/generate-excel', {method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: 'school=University+of+California%2C+Berkeley&periodEnding=2020-12-31&tripPurpose=Business'}).then(response => response.text()).then(text => console.log(text)).catch(() => alert('oh no!'));  To prevent this from happening, you need to set debug to False when you deploy the app to production.  This will prevent the attacker from being able to execute arbitrary code on your machine.  To deploy the app to production, you need to transfer it to a server and configure it to run in production mode.  This is a multi-step process that is beyond the scope of this course.  The general steps are:    1. Transfer your application to the Oracle Compute instance.  You can use SCP, Git, or any other method you prefer.    2. Install necessary software on the Oracle Compute instance.  This typically includes Python, pip, and your application's dependencies.    3. Configure the application for production.  This may include setting environment variables, configuring logging, etc.    4. Set up a WSGI server.  Gunicorn is a popular choice for serving Flask applications.    5. Configure a reverse proxy server.  Nginx is a popular choice for this.  You can find more information about deploying Flask applications here: https://flask.palletsprojects.com/en/1.1.x/deploying/



# Step 1: Transfer your application to the Oracle Compute instance
# You can use SCP, Git, or any other method you prefer

# Step 2: Install necessary software on the Oracle Compute instance
# This typically includes Python, pip, and your application's dependencies

# Step 3: Configure the application for production
# This may include setting environment variables, configuring logging, etc.

# Step 4: Set up a WSGI server
# Gunicorn is a popular choice for serving Flask applications

# Step 5: Configure a reverse proxy server
# Nginx is a popular choice for this


#from the oracle compute instance below, this was working:
# (venv) [opc@testinstance expense_report]$ cat app.py
# # app.py, this script, is the entry point of the application. It defines a Flask app that generates an Excel file based on the data submitted through a form, using a pre-defined template.  It works with the populate_excel.py script, which contains the logic for populating the template with data. The populate_excel.py script is imported in the app.py script. The app.py script has two routes: '/' renders a form for inputting data, and '/generate-excel' generates an Excel file based on the data submitted through the form and returns it as an attachment.
# """
# This script defines a Flask app that generates an Excel file based on the data submitted through a form, using a pre-defined template.
# The app has two routes: 
#     - '/' renders a form for inputting data
#     - '/generate-excel' generates an Excel file based on the data submitted through the form and returns it as an attachment.
# """
# from flask import Flask, render_template, request, send_file
# from populate_excel import populate_template

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def form():
#     # Render a form for inputting data
#     return render_template('index.html')

# @app.route('/generate-excel', methods=['POST'])
# def generate_excel():
#     """
#     Generates an Excel file based on the data submitted through a form, using a pre-defined template.

#     Returns:
#         The generated Excel file as an attachment.
#     """
#     # Get data from form
#     data = {
#         'school': request.form['school'],
#         'period_ending': request.form['periodEnding'],
#         'trip_purpose': request.form['tripPurpose']
#     }

#     # Define paths
#     template_path = 'expense_report.xlsx'
#     output_path = 'output.xlsx'

#     # Populate the template
#     populate_template(data, template_path, output_path)

#     # Send the populated Excel file to the user
#     return send_file(output_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
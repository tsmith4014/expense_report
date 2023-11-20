# app.py, this script, is the entry point of the application. It defines a Flask app that generates an Excel file based on the data submitted through a form, using a pre-defined template.  It works with the populate_excel.py script, which contains the logic for populating the template with data. The populate_excel.py script is imported in the app.py script. The app.py script has two routes: '/' renders a form for inputting data, and '/generate-excel' generates an Excel file based on the data submitted through the form and returns it as an attachment.
"""
This script defines a Flask app that generates an Excel file based on the data submitted through a form, using a pre-defined template.
The app has two routes: 
    - '/' renders a form for inputting data
    - '/generate-excel' generates an Excel file based on the data submitted through the form and returns it as an attachment.
"""
from flask import Flask, render_template, request, send_file
from populate_excel import populate_template

app = Flask(__name__)

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
        'trip_purpose': request.form['tripPurpose']
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
#populate_excel.py
# import openpyxl
# from openpyxl.styles import Alignment
# from openpyxl.drawing.image import Image
# from datetime import datetime, timedelta
# import os


# def populate_mileage(sheet, mileage_date_str, mileage_amount, period_ending):
#     """
#     Populates the Excel sheet with mileage information.
#     """
#     if not mileage_date_str or not mileage_amount:
#         return  # Skip if mileage data is incomplete

#     # Convert string dates to datetime objects
#     mileage_date = datetime.strptime(mileage_date_str, '%Y-%m-%d').date()
#     period_ending_date = datetime.strptime(period_ending, '%Y-%m-%d').date()

#     # Calculate the difference in days between the mileage date and the period ending date
#     day_difference = (period_ending_date - mileage_date).days

#     # Mileage should be entered in row 9 from column D to J (4 to 10) corresponding to Sunday (0) to Saturday (6)
#     if 0 <= day_difference <= 6:
#         column_index = 10 - day_difference  # D9 (column 4) for Sunday to J9 (column 10) for Saturday
#         sheet.cell(row=9, column=column_index).value = mileage_amount


# def populate_template(data, template_path, output_path):
#     """
#     Populates an Excel template with data and saves it to a new file.
#     Incorporates logic for handling travel dates to determine per diem fields.
#     Includes error handling for robustness.
#     """
#     try:
#         # Load the Excel template
#         wb = openpyxl.load_workbook(template_path)
#         sheet = wb.active

#         # Insert and resize the image
#         img_path = os.path.join(os.path.dirname(__file__), 'eahead.jpg')
#         img = Image(img_path)
#         img.width, img.height = img.width * 0.43, img.height * 0.60
#         sheet.add_image(img, 'A1')

#         # Common setup for cell alignment
#         center_aligned_text = Alignment(horizontal='center', wrapText=True)

#         # Populate cells with provided data
#         cells_to_populate = {
#             'B5': data['school'],
#             'H4': datetime.strptime(data['period_ending'], '%Y-%m-%d').date(),
#             'H5': data['trip_purpose'],
#             'B4': data['employee_department']  # Employee/Department
#         }

#         for cell_ref, value in cells_to_populate.items():
#             cell = sheet[cell_ref]
#             cell.alignment = center_aligned_text
#             cell.value = value

#         # Handling date names and values
#         populate_dates(sheet, data['period_ending'])

#         # Handling travel dates for per diem fields
#         if 'yes' == data.get('travel') and all(data.get(key) for key in ['travel_start_date', 'travel_end_date']):
#             populate_travel_dates(sheet, data['travel_start_date'], data['travel_end_date'])

#         # Handling mileage data
#         # Populate mileage if data is provided
#         if data.get('mileage') == 'on':  # Assuming the checkbox returns 'on' when checked
#             populate_mileage(sheet, data.get('mileage_date'), data.get('mileage_amount'), data['period_ending'])


#         # Save the populated template to a new file
#         wb.save(output_path)
#     except Exception as e:
#         # Log the error or handle it as needed
#         print(f"An error occurred while populating the template: {e}")
#         raise

# def populate_dates(sheet, period_ending):
#     """Populates static day names and dates."""
#     period_ending_date = datetime.strptime(period_ending, '%Y-%m-%d')
#     day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
#     for i, day_name in enumerate(day_names):
#         day_cell = sheet.cell(row=7, column=4+i)
#         day_cell.value = f"Date\n{day_name}"
#         day_cell.alignment = Alignment(horizontal='center', wrapText=True)

#     for i in range(6, -1, -1):
#         date_cell = sheet.cell(row=8, column=4+i)
#         date_cell.value = (period_ending_date - timedelta(days=6-i)).date()
#         date_cell.alignment = Alignment(horizontal='center', wrapText=True)

# def populate_travel_dates(sheet, travel_start_date_str, travel_end_date_str):
#     """Handles the logic for populating travel dates and per diem fields."""
#     travel_start_date = datetime.strptime(travel_start_date_str, '%Y-%m-%d')
#     travel_end_date = datetime.strptime(travel_end_date_str, '%Y-%m-%d')
    
#     for i in range(4, 11):  # Assuming date columns are D to J (4 to 10)
#         cell_date = sheet.cell(row=8, column=i).value
#         if cell_date and travel_start_date.date() <= cell_date <= travel_end_date.date():
#             if cell_date == travel_start_date.date():
#                 sheet.cell(row=21, column=i).value = 30.00  # Only dinner on start date
#             elif cell_date == travel_end_date.date():
#                 sheet.cell(row=19, column=i).value = 5.00  # Only breakfast on end date
#             else:
#                 sheet.cell(row=19, column=i).value = 5.00  # Breakfast
#                 sheet.cell(row=21, column=i).value = 30.00  # Dinner



# from working mergecenter image deployed live:
#import openpyxl
import openpyxl
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image
from datetime import datetime, timedelta
import os

def populate_template(data, template_path, output_path):
    """
    Populates an Excel template with data and saves it to a new file.
    Incorporates logic for handling travel dates to determine per diem fields.
    Includes error handling for robustness.
    """
    try:
        # Load the Excel template
        wb = openpyxl.load_workbook(template_path)
        sheet = wb.active

        # Insert and resize the image
        img_path = os.path.join(os.path.dirname(__file__), 'eahead.jpg')
        img = Image(img_path)
        img.width, img.height = img.width * 0.43, img.height * 0.60
        sheet.add_image(img, 'A1')

        # Common setup for cell alignment
        center_aligned_text = Alignment(horizontal='center', wrapText=True)

        # Populate cells with provided data
        cells_to_populate = {
            'B5': data['school'],
            'H4': datetime.strptime(data['period_ending'], '%Y-%m-%d').date(),
            'H5': data['trip_purpose'],
            'B4': data['employee_department']  # Employee/Department
        }

        for cell_ref, value in cells_to_populate.items():
            cell = sheet[cell_ref]
            cell.alignment = center_aligned_text
            cell.value = value

        # Handling date names and values
        populate_dates(sheet, data['period_ending'])

        # Handling travel dates for per diem fields
        if 'yes' == data.get('travel') and all(data.get(key) for key in ['travel_start_date', 'travel_end_date']):
            populate_travel_dates(sheet, data['travel_start_date'], data['travel_end_date'])

        # Save the populated template to a new file
        wb.save(output_path)
    except Exception as e:
        # Log the error or handle it as needed
        print(f"An error occurred while populating the template: {e}")
        raise

def populate_dates(sheet, period_ending):
    """Populates static day names and dates."""
    period_ending_date = datetime.strptime(period_ending, '%Y-%m-%d')
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for i, day_name in enumerate(day_names):
        day_cell = sheet.cell(row=7, column=4+i)
        day_cell.value = f"Date\n{day_name}"
        day_cell.alignment = Alignment(horizontal='center', wrapText=True)

    for i in range(6, -1, -1):
        date_cell = sheet.cell(row=8, column=4+i)
        date_cell.value = (period_ending_date - timedelta(days=6-i)).date()
        date_cell.alignment = Alignment(horizontal='center', wrapText=True)

def populate_travel_dates(sheet, travel_start_date_str, travel_end_date_str):
    """Handles the logic for populating travel dates and per diem fields."""
    travel_start_date = datetime.strptime(travel_start_date_str, '%Y-%m-%d')
    travel_end_date = datetime.strptime(travel_end_date_str, '%Y-%m-%d')
    
    for i in range(4, 11):  # Assuming date columns are D to J (4 to 10)
        cell_date = sheet.cell(row=8, column=i).value
        if cell_date and travel_start_date.date() <= cell_date <= travel_end_date.date():
            if cell_date == travel_start_date.date():
                sheet.cell(row=21, column=i).value = 30.00  # Only dinner on start date
            elif cell_date == travel_end_date.date():
                sheet.cell(row=19, column=i).value = 5.00  # Only breakfast on end date
            else:
                sheet.cell(row=19, column=i).value = 5.00  # Breakfast
                sheet.cell(row=21, column=i).value = 30.00  # Dinner
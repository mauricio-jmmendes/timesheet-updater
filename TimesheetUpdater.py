import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
import io

# Add your name
user_name = "Your_Name"

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

# Add your service account file
creds = ServiceAccountCredentials.from_json_keyfile_name('your-service-account-key-file.json', scope) # replace with your own JSON key file name

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open(f'2023_Calendar_January-December_PayPal_{user_name}') # replace with your own spreadsheet name if needed

# Get the first sheet of the Spreadsheet
worksheet = sheet.get_worksheet(0)

# Set the intended filling way ('WHOLE_WEEK' | 'CURRENT_DAY')
filling_method_flag = 'WHOLE_WEEK'

# The default working hours per day
default_working_hours = 8

# Get today's date
today = datetime.now()

# Format it like 'May 17, 2023'
date_str = today.strftime("%B %d, %Y")

# Find today's date cell
cell = worksheet.find(date_str)

# Define weekday offsets
weekday_offsets = {
    0: [0, 1, 2, 3, 4],  # Monday
    1: [-1, 0, 1, 2, 3],  # Tuesday
    2: [-2, -1, 0, 1, 2],  # Wednesday
    3: [-3, -2, -1, 0, 1],  # Thursday
    4: [-4, -3, -2, -1, 0],  # Friday
}

# Update the cell for the current day with default working hours
if filling_method_flag == 'CURRENT_DAY':
    print(f'Filling the TimeSheet for the current day ({date_str}) with {default_working_hours} hours. ')
    worksheet.update_cell(cell.row + 1, cell.col, default_working_hours)

# Update cells for the current week, with default working hours, according to today's weekday
elif filling_method_flag == 'WHOLE_WEEK':
    for offset in weekday_offsets[today.weekday()]:
        current_day = (today + timedelta(days=offset)).strftime("%B %d, %Y")
        print(f'Filling the TimeSheet for {current_day} with {default_working_hours} hours. ')
        worksheet.update_cell(cell.row + 1, cell.col + offset, default_working_hours)

# Save the modified Google Sheet to a local Excel file using googleapiclient
drive_service = build('drive', 'v3', credentials=creds)
file_id = sheet.id
request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Downloading... %d%%." % int(status.progress() * 100))

with open(f'2023_Calendar_January-December_PayPal_{user_name}.xlsx', 'wb') as f:
    f.write(fh.getvalue())

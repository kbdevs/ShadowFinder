print("Welcome to the local ShadowFinder script!")
print("This script will help you generate a shadow image based on the height of an object and the length of its shadow.")
print("This works best when the shadow angle is close to 90 degrees.")
print("Please provide the following information: \n")
object_height = int(input("How tall is the shadow?: "))  # Height of object in arbitrary units
shadow_length = int(input("How long is the shadow?: "))  # Length of shadow in arbitrary units

date = input("What is the date of the image? (ex. 2022-02-22): ")  # Date
time_type = input("What is the time type? (utc/local): ")  # Time type
time = input("What is the time of the image? (ex. hh:mm:ss 24hr time): ")  # Time
print("Please wait while data is calculated...")


# Create output files
output = f"./shadowfinder_{object_height}_{shadow_length}_{date}T{time}.png"
logfile = f"./shadowfinder_{object_height}_{shadow_length}_{date}T{time}.log"

# Imports
from shadowfinder.shadowfinder import ShadowFinder
import datetime
import os


if not os.path.isfile("timezone_grid.json"):
    os.system("wget https://raw.githubusercontent.com/bellingcat/ShadowFinder/main/timezone_grid.json >> {logfile} 2>&1")

datetime_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
datetime_time = datetime.datetime.strptime(time, "%H:%M:%S").time()

date_time = datetime.datetime.combine(datetime_date, datetime_time)  # Date and time of interest

finder = ShadowFinder()

# Check if timezone grid exists
try:
    finder.load_timezone_grid()
except FileNotFoundError:
    finder.generate_timezone_grid()
    finder.save_timezone_grid()

finder.set_details(object_height, shadow_length, date_time, time_format=time_type)
finder.find_shadows()
fig = finder.plot_shadows()
fig.savefig(output)

print(f"\n Done! Shadow image saved as {output}")
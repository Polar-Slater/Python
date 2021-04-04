#
# Example file for formatting time and date output
#

from datetime import datetime

def main():
  # Times and dates can be formatted using a set of predefined string
  # control codes 
  now = datetime.now()
  
  #### Date Formatting ####
  
  # %y/%Y - Year, %a/%A - weekday, %b/%B - month, %d - day of month ## lower case means short name (abbrv)
  print(now.strftime("The current year is: %Y"))
  print(now.strftime("%a, %d %B, %y"))

  # %c - locale's date and time, %x - locale's date, %X - locale's time
  print(now.strftime("%c \n %x \n %X"))

  #### Time Formatting ####
  
  # %I/%H - 12/24 Hour, %M - minute, %S - second, %p - locale's AM/PM
  print (now.strftime("Current time: %I:%M:%S %p")) # 12-Hour:Minute:Second:AM
  print (now.strftime("24-hour time: %H:%M")) # 24-Hour:Minute  

if __name__ == "__main__":
  main();

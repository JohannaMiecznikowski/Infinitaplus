#This script converts video timecode into seconds.
#TC exported from WLAN is in the hours:minutes:seconds.milliseconds format.
#The framerate is set to 25 f/s.
#This is the fourth version of this script.
#In v4, the conversion has been changed according to the format output by ELAN.
    
def timeconvert(h, m, s):
    """Converts video timecode into seconds.

    Works for the hours:minutes:seconds.milliseconds format.""" 
    total_seconds = 3600*h + 60*m + s
    return total_seconds
    
#Fetches input from user
#(an alternative method would be to retrieve TC from transcript text):
tc = input("Type timecode here:")

#Creates list of strings:
tc_list = tc.split(":")

#Converts the list items to numbers and assigns these to variables:
hours = int(tc_list[0])
minutes = int(tc_list[1])
seconds = float(tc_list[2])

#Calls timeconvert function:
total_seconds = timeconvert(hours, minutes, seconds)

#Outputs a statement for the user:
print("These are", total_seconds, "seconds.")

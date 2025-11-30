#Timecodes in transcripts at user-defined intervals

#This script is part of the "TIGRformat" package.
#The package supports a workflow in which "traditional transcripts" are exported from ELAN
#and processed automatically and manually in view of qualitative analysis.
#Refer to the package's readme file for more information.

#INPUT: 
#- "traditional transcript" file exported from ELAN with timecodes and without suppressing repeated speaker labels;
#- interval in seconds defined by the user.
#OUTPUT: a processed transcript file in which only the following timecodes are maintained:
#- beginning time of an ELAN segment;
#- not the beginning of overlapping speech;
#- at roughly the interval defined by the user.

#EXPLANATION:
#The script's specific goal is to yield transcripts
#- that are easily readable to the human eye, 
#- that allow to retrieve discourse in the corresponding video or audio recording.
#To achieve this goal, the script reduces the number of timecodes in the transcript.
#NOTA BENE: 
#Segment beginnings that are not in overlap usually correspond to transcribers' choices that respect word boundaries.
#In the data this script was developed for, in many cases a segment boundary has been created at the beginning of overlapping speech.
#In those cases, the segment may not respect word boundaries because overlap may start in the middle of a word.
#That's why the script ignores timecodes at the beginning of overlapping speech:
#This restriction has the effect of avoiding word-internal timecodes in the transcript.

#AUTHOR: Johanna Miecznikowski, Università della Svizzera italiana
#FUNDING: 
#- InfinIta project, grant no. 192771 of the Swiss National Science Foundation
#  (https://data.snf.ch/grants/grant/192771)
#- ShareTIGR - Sharing the TIGR corpus of spoken Italian: an ORD case study, 
#  project funded by USI Università della Svizzera italiana
#  (https://search.usi.ch/projects/3090)

#When using the script please mention author and funding institution in acknowledgements.
#CREATED: December 2023
#Bug fixed October 18, 2024: When there are pauses in the transcript that are longer than the
#timecode interval defined by the user, the script now updates the counter by assigning it the
#value in seconds of the first timecode after the pause. 
#Bug fixed May 3, 2025: list(dict.fromkeys()) is applied to the list of all line-initial 
#timecodes in order to eliminate any timecode duplicates.

def run_function():

    #Import the Regex module.
    import re

    #Function to check if preceding text line starts with overlap
    def check_overlap(t, t_line, text):
        """Checks if timecode refers to overlapping talk.

        In a traditional transcript text exported from ELAN with timecodes, 
        each segment is listed on a separate line and the corresponding timecode
        is placed in the immediately following line.
        This function checks if the text in the immediately preceding line
        starts with an overlap (square brackets)."""    

        t_position = t_line.index(t)
        index_current_line = text.index(t_line)
        preceding = text[index_current_line - 1]
        if preceding[t_position] == "[":
            return True
        else:
            return False

    #Function to convert tc exported from ELAN into seconds
    def timeconvert(tc):
        """Converts video timecode into seconds.

        Works for the hours:minutes:seconds.milliseconds format.""" 
        tc_list = tc.split(":")
        if tc_list:
            hours = int(tc_list[0])
            minutes = int(tc_list[1])
            seconds = float(tc_list[2])
            total_seconds = 3600*hours + 60*minutes + seconds
            return total_seconds
        else: 
            print("Hours, minutes and seconds have not been successfully retrieved from timecode.")

    #Instruct user
    print("This script extracts a list of timecodes from a transcript at intervals defined by the user.\n")

    #Open a transcript file containing timecodes.
    attempts = 0
    while attempts < 3:
        try:
            filename = input("Write the file path of a traditional transcript exported from ELAN: ")
            file = open(filename, "r", encoding="utf-8")
            input_successful = True
            break
        except:
            if attempts < 2:
                print("Problem with name or location of the file. Try again.")
                input_successful = False
                attempts += 1
            else:
                print("Problem with name or location of the file.")
                input_successful = False
                attempts += 1

    if input_successful == True:

        #Ask the user to define the timecode intervals.
        while True:
            try:
                print("\nAt which interval do you wish to print timecodes in your transcript?")
                interval = int(input("Write the desired number of seconds: "))
            except ValueError:
                print("You need to input a number. Try again.")
                continue
            else:
                break

        #Read the file as a sequence of lines and close it.
        content = file.readlines()
        file.close()

        #Start by creating an empty list for line-initial timecodes.
        #Find all timecodes at the beginning of a line.
        #Complete the list by inserting those line-initial timecodes that do not refer to overlapping talk.
        first_tc_list = []
        for line in content:
            first_tc = re.search(r"\d\d:\d\d:\d\d\.\d{3}", line)
            if first_tc:
                if check_overlap(first_tc.group(), line, content) == False:
                    first_tc_list.append(first_tc.group())
            else:
                continue

        #Transform the list of line-initial timecodes into a dictionary (maintaining 
        #the order of the items) and back to a list. Since dictionaries do not allow 
        #for duplicates, the effet is to eliminate any timecode duplicates. 
        first_tc_list = list(dict.fromkeys(first_tc_list))

        #Create an empty list to store timecodes at intervals defined by the user's input.
        #Insert the first timecode of the transcript into the list.
        interval_list = []        
        interval_list.append(first_tc_list[0])

        #Convert the first timecode of the transcript into seconds.
        #Declare that amount of seconds as the starting point for counting intervals.
        counter = timeconvert(first_tc_list[0])

        #Loop through the list of line-initial timecodes: convert each timecode in seconds
        #until you reach the first timecode that is greater than the initial counter + the interval defined by the user. 
        #Insert that timecode into the list of timecodes at intervals and either update the counter by adding the interval
        #or (when the timecode just added to the list occurs at a distance of more than two times the interval from the preceding timecode)
        #update the counter by assigning it the value of the timecode just added. 
        for tc in first_tc_list:
            conv_in_seconds = timeconvert(tc)
            if conv_in_seconds < counter + interval:
                continue
            else:
                interval_list.append(tc)
                if conv_in_seconds > counter + (2 * interval):
                    counter = conv_in_seconds
                else:
                    counter = counter + interval

        #Output the number of timecodes that should be maintained in the transcript.
        print("\nThis is how many timecodes will be left in the transcript:")
        print(len(interval_list))

        #Remove lines that contain timecode which is not in the interval list.
        for i in range(len(content)):
            first_tc = re.search(r"\d\d:\d\d:\d\d\.\d{3}", content[i])
            if not first_tc:
                continue
            else:
                for j in interval_list:
                    if first_tc.group() == j:
                        has_interval_timecode = True
                        break
                    else:
                        has_interval_timecode = False
                if has_interval_timecode == False:
                    content[i] = ""
                else:
                    continue

        #Determine number of spaces before text beginning
        for line in content:
            first_tc = re.search(r"\d\d:\d\d:\d\d\.\d{3}", line)
            if first_tc:
                spaces = line.index(first_tc.group())
                break
            else:
                continue

        #Remove ending time and add line-initial "--TIMECODE--" and store index of timecode lines in list.
        tc_lines = []
        for i in range(len(content)):
            first_tc = re.search(r"\d\d:\d\d:\d\d\.\d{3}", content[i])
            if first_tc:
                content[i] = "--TIMECODE--"+(" " * (spaces-12))+first_tc.group()+"\n"
                tc_lines.append(i)
            else:
                continue

        #Place a marker in transcript text corresponding to timecode.
        #N.B. When repeated speaker labels are not suppressed during export from ELAN,
        #each speaker label indicates the beginning of a segment. 
        #This property is used here to find the nearest segment beginning looping through lines
        #backwards from the line containing timecode.
        for i in tc_lines:
            for counter in range(1, 12):
                if len(content[i-counter]) >=1:
                    if (content[i-counter])[0] != " ":
                        string_1 = (content[i-counter])[:spaces]
                        string_2 = "((TC)) "
                        string_3 = (content[i-counter])[spaces:]
                        content[i-counter] = string_1+string_2+string_3
                        break
                else:
                    continue  

        #Shift up timecode lines if distant from timecode markers.
        for i in range(len(content)):
            if re.search("TC", content[i]):
                for line in content[(i+1):len(content)]:
                    if re.match("-", line):
                        store_c = line
                        store_i = content.index(line)
                        break
                if store_i == i+1:
                    continue
                else:
                    content[i] = content[i]+line
                    content[store_i] = ""
                    
        print("\nThese are the first 50 lines of the processed document:\n")
        for line in content[0:50]:
            print(line, end="")

        #Save file.
        save = filename[:-4]+"_tcfltrd.txt"
        with open(save, "x", encoding="utf-8") as f:   
            for line in content:
                f.write(line)
        print("\n---Timecode filtered and timecode marks inserted---")
        print("\nFile saved as", save)


        #Add statement about the timecode interval chosen at the end of the file.
        with open(save, "a", encoding="utf-8") as f:
            tc_metadata = "\nThis transcript contains indications of timecode at intervals of approximately "+str(interval)+" seconds.\n"
            f.write(tc_metadata)
    else:
        print("\nInput failed several times.")
        print("---Operation interrupted.---")

#Perform all operations
run_function()

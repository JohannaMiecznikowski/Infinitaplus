#Suppress repeated speaker labels in transcripts

#This script is part of the "TIGRformat" package.
#The package supports a workflow in which "traditional transcripts" are exported from ELAN
#and processed automatically and manually in view of qualitative analysis.
#Refer to the package's readme file for more information.

#INPUT:
#"traditional transcript" file exported from ELAN
#- without suppressing repeated speaker labels and
#- processed in a preceding step to filter timecode indications
#  and insert time-aligned timecode markers in the transcript text.
#OUTPUT:
#transcript file in which repeated speaker labels within the same etic turn are suppressed.
#This operation makes the transcript more readable to the human eye.
#See the EXPLANATION below for a definition of the notion of "etic turn".

#EXPLANATION:
#The preceding step in the workflow is the filtering of timecode, which uses transcripts exported from ELAN 
#in which each segment is placed on a separate line and preceded by a speaker label.
#ELAN's in-built function to suppress speaker labels is thus not applied
#and the present script takes over that function.
#In the transcripts on which the script is supposed to operate,
#- portions in the timeline that contain no segment appear as pauses
#  with a length calculated by ELAN, expressed in the format "(X.XX)", and are not preceded by any label;
#- each line containing timecode starts with "--TIMECODE--";
#- a timecode mark "((TC))" has been placed at sequence beginnings to which timecode indications refer.
#"Etic Turn" is here defined as a stretch of talk by the same speaker in a time interval during which no contribution 
#by another speaker is made according to the audio recording.
#In this phase of the workflow, pauses are attributed to the last person speaking.
#Turns defined according to this etic criterion approximate emic turns at talk in many cases,
#but should not be equated with the latter for several reasons
#(especially: back-channels, parallel conversations audible on the same recording, long pauses).
#N.B. The script uses  the first presence of a timecode mark "TC" in the transcript
#to calculate the position in the line where the transcribed discourse starts.
#It will therefore not work if no such timecode marks are present in the transcript.

#AUTHOR: Johanna Miecznikowski, Università della Svizzera italiana
#FUNDING: 
#- InfinIta project, grant no. 192771 of the Swiss National Science Foundation
#  (https://data.snf.ch/grants/grant/192771)
#- ShareTIGR - Sharing the TIGR corpus of spoken Italian: an ORD case study, 
#  project funded by USI Università della Svizzera italiana
#  (https://search.usi.ch/projects/3090)

#When using the script please mention author and funding institution in acknowledgements.
#CREATED: December 2023

def run_function():

    #Import the Regex module.
    import re

    #Open a transcript file.
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

        #Read the file as a list of lines and close it.
        content = file.readlines()
        file.close()

        #Determine the number of spaces before the discourse starts
        for line in content:
            timecode_mark = re.search("TC", line)
            if timecode_mark:
                spaces = line.index(timecode_mark.group()) - 2
                break
            else:
                continue

        #Suppress speaker labels repeated within etic turns
        for index in range(len(content)):
            if re.match(r"[A-Z]", content[index]):
                label = (content[index])[:spaces]
                for nextind in range((index + 1), len(content)):
                    if re.match(" ", content[nextind]):
                        continue
                    elif re.match("-", content[nextind]):
                        continue
                    else:
                        if re.match("[A-Z]", content[nextind]):
                            if re.match(label, content[nextind]):
                                string_1 = " " * spaces
                                string_2 = (content[nextind])[spaces:]
                                content[nextind] = string_1+string_2
                                continue
                            else:
                                break
            else:
                continue
          

        print("\nThese are the first 50 lines of the processed document:\n")
        for line in content[0:100]:
            print(line, end="")

        #Save file.
        save = filename[:-4]+"_nolbls.txt"
        with open(save, "x", encoding="utf-8") as f:   
            for line in content:
                f.write(line)
        print("\n---Repeated labels suppressed---")
        print("\nFile saved as", save)

    else:
        print("\nInput failed several times.")
        print("---Operation interrupted.---")
        
#Perform all operations
run_function()

#Correct the placement of pauses between speaker changes

#This script is part of the "TIGRformat" package.
#The package supports a workflow in which "traditional transcripts" are exported from ELAN
#and processed automatically and manually in view of qualitative analysis.
#Refer to the package's readme file for more information.

#It corrects pauses between speaker changes that have been placed at the beginning of a line,
#(the position reserved for speaker labels),
#moving them to the indented position of the transcribed discourse.
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
#CREATED: January 2024

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

        #Replace pauses between speaker changes erroneously placed at the line beginning
        for index in range(len(content)):
            if re.match(r"\(\d+\.\d+\)", content[index]):
                pausematch = re.match(r"\(\d+\.\d+\)", content[index])
                string1 = " " * (spaces - 1)
                string2 = pausematch.group()
                content[index] = string1+string2+"\n"
            else: 
                continue           

        #Save file.
        save = filename[:-4]+"_pausecorr.txt"
        with open(save, "x", encoding="utf-8") as f:   
            for line in content:
                f.write(line)
        print("\n---Position of isolated pauses corrected---")
        print("\nFile saved as", save)

    else:
        print("\nInput failed several times.")
        print("---Operation interrupted.---")
        
#Perform all operations
run_function()

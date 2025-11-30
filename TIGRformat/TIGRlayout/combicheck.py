#Check transcript for
#- square brackets in lines with timecode marks
#- undesired repeated speaker labels

#This script is part of the "TIGRformat" package.
#The package supports a workflow in which "traditional transcripts" are exported from ELAN
#and processed automatically and manually in view of qualitative analysis.
#Refer to the package's readme file for more information.

#INPUT:
#"traditional transcript" file exported from ELAN manipulated both automatically and manually.
#OUTPUT:
#- a list of lines containing repeated speaker labels;
#- a list of lines with timecode marks that contain square brackets
#- a list of lines with "-->" (pointing to reference points of AMBIENT_NOISES)


def run_function():
    """Executes all operations in the script."""
    
    #Import the Regex module.
    import re

    def replabels(content):
        """Finds undesired repeated speaker labels and signals them to the user.

            The function operates on the content of a file opened as a list of lines (file.readlines())."""

        print("\n")
        print("Repeated speaker Labels")
        print("=======================", "\n")

        for line in content:
            timecode_mark = re.search("TC", line)
            if timecode_mark:
                spaces = line.index(timecode_mark.group()) - 2
                break
            else:
                continue        
        
        for index in range(len(content)):
            if re.match(r"[A-Z]", content[index]):
                label = (content[index])[:spaces]
                for nextind in range((index + 1), len(content[index + 1:])):
                    if len(content[nextind]) >= 1:
                        if (content[nextind])[0] == " ":
                            continue
                        elif (content[nextind])[0] == "-":
                            continue
                        else:
                            if re.match("[A-Z]", content[nextind]):
                                if (content[nextind])[:spaces] == label:
                                    print("Check these lines:")
                                    print("line", index+1, ":", content[index], end="")
                                    print("line", nextind+1, ":", content[nextind])
                                    continue
                                else:
                                    break
                    else:
                        continue
            else:
                continue      

    def find_tc_and_brackets(content):
        """Finds lines that contain both timecode marks and square brackets.

            The function operates on the content of a file opened as a list of lines (file.readlines()).
            In an early step of the formatting procedure, a timecode mark ("((TC))") was inserted into the transcript
            a each point referred to by timecode stamps. That insertion shifted the following text forward.
            When square brackets (indicating overlapping speech( were present in that line,
            their automatic graphical alignment performed by ELAN was disturbed.
            In later phases of the formatting process, overlapping speech was rearranged manually and many
            disalignments probably have been recognized and corrected.
            The function checks for disalignments that have gone unnoticed.
            Any disalignment found must be corrected manually."""
         
        print("\n")
        print("Lines containing timecode marks followed by square brackets")
        print("===========================================================", "\n")

        for i in range(len(content)):
            if re.search("TC", content[i]):
                tc = re.search("TC", content[i])
                if re.search(r"\[", (content[i])[tc.end():]):
                    print("Check square brackets at lines", i-2, "to", i+2)                    
                    print(content[i-2], end="")
                    print(content[i-1], end="")
                    print(content[i], end="")
                    print(content[i+1], end="")
                    print(content[i+2], "\n")
                else:
                    continue
            else:
                continue

    def ambnoise_arrows(content):
        """Finds arrows pointing towards endings of ambient noises.

            The function operates on the content of a file opened as a list of lines (file.readlines()).
            In ELAN, noises have been transcribed using a separate tier.
            Longer noises overlapping speech have been transcribed as short segments
            at the beginning of the noise, in order not to cover segments empty of speech
            and to allow ELAN to properly recognize and calculate such empty segments as pauses.
            An arrow is placed in the segment pointing to the ending of the noise.
            When formatting the exported transcript, it should be moved to the line that immediately
            precedes the corresponding reference point in the transcript (usually indicated by a "*").
            The present function retrieves arrows, which then must then be moved manually."""
        
        print("\n")
        print("Pointers to endings of AMBIENT_NOISES")
        print("=====================================")

        #List indexes of lines that contain 
        for i in range(len(content)):
            if re.search("-->", content[i]):
                print("Check line", i+1,":", content[i], "and possible reference points in the following lines.")
            else:
                continue

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

    #Read the file as a list of lines and close it.
    if input_successful == True:
        content = file.readlines()
        file.close()
        #Call function defined earlier
        replabels(content)
        #Call function defined earlier
        find_tc_and_brackets(content)
        #Call function defined earlier
        ambnoise_arrows(content)
        print("\n---Combicheck performed.---")
    else:
        print("\nInput failed several times.")
        print("---Operation interrupted.---")

#Execute combicheck.
run_function()        

#Reformats "etic turns"

#This script is part of the "TIGRformat" package.
#The package supports a workflow in which "traditional transcripts" are exported from ELAN
#and processed automatically and manually in view of qualitative analysis.
#Refer to the package's readme file for more information.

#INPUT:
#"traditional transcript" file exported from ELAN processed in preceding steps 
#to filter timecode indications, insert timecode labels and suppress repeated speaker labels
#(see the package's readme file for details).
#OUTPUT:
#transcript file in which discourse segments produced by the same speaker and pauses calculated by ELAN 
#(except those precding a speaker change) are concatenated without line breaks, forming "etic turns",
#(see the package's readme file for a definition) and most lines are shortened to a maximum of 86 characters
#(the initial 80 characters of the ELAN export + 6 characters due to the insertion of timecode marks).

#EXPLANATION:
#Compact "etic turns" are easier to read and to annotate. That's why this script
#- concatenates segments produced by the same speaker (without line breaks);
#- concatenates in the same way pauses between such segments;
#- inserts line breaks after the last space before the length of 86 characters.
#N.B. Timecode lines are ignored.
#N.B. For the time being, the line break function has a maximum of four recursions written manually.
#It therefore can handle properly etic turns that are at most 4x80 characters long.
#Longer etic turns will exceed the length of 80 characters per line.

#AUTHOR: Johanna Miecznikowski, Università della Svizzera italiana
#FUNDING: 
#- InfinIta project, grant no. 192771 of the Swiss National Science Foundation
#  (https://data.snf.ch/grants/grant/192771)
#- ShareTIGR - Sharing the TIGR corpus of spoken Italian: an ORD case study, 
#  project funded by USI Università della Svizzera italiana
#  (https://search.usi.ch/projects/3090)


def run_function():
    
    #Import the Regex module.
    import re

    def concat_after_label(content):
        """Looks for text by the same speaker and concatenates it.

            The function operates on the content of a file opened as a list of lines (file.readlines()).
            It loops through all lines in the document and starts operations from lines that start with a speaker label (uppercase letter).
            It then checks the following lines and concatenates discourse and pauses by the same speaker,
            except for the last pause before speaker change.
            It stops at timecode lines. Discourse following a timecode must be concatenated using the concat_after_tc function."""
        
        for line in content:
            timecode_mark = re.search("TC", line)
            if timecode_mark:
                spaces = line.index(timecode_mark.group()) - 2
                break
            else:
                continue

        for index in range(len(content)):
            if re.match(r"[A-Z]", content[index]):
                for nextind in range((index + 1), len(content)):
        #Check the following lines.
        #When encountering a line without speaker label or timecode, consider concatenating it with preceding discourse.
                    if re.match(" ", content[nextind]):
        #Concatenate pauses if not followed by next speaker label.
                        if re.search(r"\(\d+\.\d+\)",(content[nextind])):
                            if re.match(r"[A-Z]", content[nextind+1]):
                                break
                            else:
                                text_nextind = (content[nextind])[spaces:]
                                text_index = (content[index])[:-1]
                                content[index] = text_index+" "+text_nextind
                                content[nextind] = ""
                                continue
        #Concatenate if the line does not contain either pause or sign of overlap.
                        else:
                            text_nextind = (content[nextind])[spaces:]
                            text_index = (content[index])[:-1]
                            content[index] = text_index+" "+text_nextind
                            content[nextind] = ""
                            continue
                    else:
                        break


    def concat_after_tc(content):

        """Looks for text by the same speaker following a line with timecode and concatenates it.

            The function operates on the content of a file opend as a list of lines (file.readlines()).
            It loops through all lines in the document and start operations from lines without speaker label or timecode stamp.
            When encountering such a line, it checks the following lines and concatenates discourse and pauses by the same speaker,
            except for the last pause before speaker change.
            It only concatenates lines without speaker labels and is suitable to concatenate discourse following a timecode line.
            It is complentary to the concat_after_label function."""

        for line in content:
            timecode_mark = re.search("TC", line)
            if timecode_mark:
                spaces = line.index(timecode_mark.group()) - 2
                break
            else:
                continue
            
        for line in content:
            timecode_mark = re.search("TC", line)
            if timecode_mark:
                spaces = line.index(timecode_mark.group()) - 2
                break
            else:
                continue

        #Loop through all lines in the document and start operations from lines that start without speaker label or timecode
        for index in range(len(content)):
            if re.match(" ", content[index]):
        #Check following lines
                for nextind in range((index + 1), len(content)):
        #When encountering line without speaker label or timecode, consider concatenating it with preceding discourse.
                    if re.match(" ", content[nextind]):
        #Concatenate pauses if not followed by next speaker label.
                        if re.search(r"\(\d+\.\d+\)",(content[nextind])):
                            if re.match(r"[A-Z]", content[nextind+1]):
                                break
                            else:
                                text_nextind = (content[nextind])[spaces:]
                                text_index = (content[index])[:-1]
                                content[index] = text_index+" "+text_nextind
                                content[nextind] = ""
                                continue
        #Concatenate if the line does not contain either pause or sign of overlap.
                        else:
                            text_nextind = (content[nextind])[spaces:]
                            text_index = (content[index])[:-1]
                            content[index] = text_index+" "+text_nextind
                            content[nextind] = ""
                            continue
                    else:
                        break

    def break_lines(text, ind):

        for line in content:
            timecode_mark = re.search("TC", line)
            if timecode_mark:
                spaces = line.index(timecode_mark.group()) - 2
                break
            else:
                continue
            
        for line in content:
            timecode_mark = re.search("TC", line)
            if timecode_mark:
                spaces = line.index(timecode_mark.group()) - 2
                break
            else:
                continue

        if len(text[ind]) > 86:
            maxline = (text[ind])[:86]
            boundary = maxline.rfind(" ")
            string_1 = (text[ind])[:boundary]
            string_2 = (text[ind])[boundary:]
            text[ind] = string_1+"\n"+" " * (spaces-1)+string_2
            if len(string_2) > 86-spaces:
                maxline_string_2 = string_2[:86-spaces]
                boundary_string_2 = maxline_string_2.rfind(" ")
                string_3 = string_2[:boundary_string_2]
                string_4 = string_2[boundary_string_2:]
                text[ind] = string_1+"\n"+" " * (spaces-1)+string_3+"\n"+" " * (spaces-1)+string_4
                if len(string_4) > 86-spaces:
                    maxline_string_4 = string_4[:86-spaces]
                    boundary_string_4 = maxline_string_4.rfind(" ")
                    string_5 = string_4[:boundary_string_4]
                    string_6 = string_4[boundary_string_4:]
                    text[ind] = string_1+"\n"+" " * (spaces-1)+string_3+"\n"+" " * (spaces-1)+string_5+"\n"+" " * (spaces-1)+string_6
                    if len(string_6) > 86-spaces:
                        maxline_string_6 = string_6[:86-spaces]
                        boundary_string_6 = maxline_string_6.rfind(" ")
                        string_7 = string_6[:boundary_string_6]
                        string_8 = string_6[boundary_string_6:]
                        text[ind] = string_1+"\n"+" " * (spaces-1)+string_3+"\n"+" " * (spaces-1)+string_5+"\n"+" " * (spaces-1)+string_7+"\n"+" " * (spaces-1)+string_8

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
        print("This file has ", len(content), " lines.")
        #Call function defined earlier
        concat_after_label(content)
        #Call function defined earlier
        concat_after_tc(content)
        #Break lines after max. 86 characters.
        for i in range(len(content)):
            if len(content[i]) > 86:
                break_lines(content, i)
        print("\nThese are the first 50 lines of the processed document:\n")
        for line in content[0:50]:
            print(line, end="")
        #Save file.
        save = filename[:-4]+"_concat.txt"
        with open(save, "x", encoding="utf-8") as f:   
            for line in content:
                f.write(line)
        print("\n---Text concatenated and linebreaks inserted after approx. 86 characters.---")
        print("\nFile saved as", save)
    else:
        print("\nInput failed several times.")
        print("---Operation interrupted.---")
        
#Execute all operations
run_function()

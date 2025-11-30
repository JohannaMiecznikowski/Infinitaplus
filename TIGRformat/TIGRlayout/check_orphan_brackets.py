#Check square brackets

#This script is part of the "TIGRformat" package.
#The package supports a workflow in which "traditional transcripts" are exported from ELAN
#and processed automatically and manually in view of qualitative analysis.
#Refer to the package's readme file for more information.

#INPUT:
#"traditional transcript" file exported from ELAN
#- without suppressing repeated speaker labels and
#- using ELAN's built-in function to graphicallz align overlapping speech at square brackets.
#OUTPUT:
#- Two lists of lines in which brackets are missing.

#EXPLANATION:
#Square brackets indicate overlap.
#Each square bracket needs to be to be opened and closed.
#Brackets have been inserted by transcribers, who may make errors.
#The script looks for orphan opening / closing brackets and lists the corresponding lines.
#The errors must then be fixed manually, both in the .txt transcript and in the ELAN source transcript.
#N.B. Differently from other TIGRformat modules, the file must be read as a string, not as a list of lines.


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
    """Executes all operations in the script."""
    
    #Import the Regex module.
    import re
    
    def checkbr(content):
        """Checks for orphan square brackets in a file read as a string (file.read()).

            Outputs two lists of lines. The first lists open square brackets that are not closed.
            The second lists closed square brackets that are not preceded by opening ones."""
        
        print("\n")

        #Find all opening square brackets.
        opening_br = re.finditer(r"\[", content)
    #Loop them through looking for the next square bracket of each and signal its line number
    #if it is a further opening bracket instead of the expected closing bracket.
        for br in opening_br:
            next_br = re.search(r"[\[\]]", content[br.end():])
            if next_br.group() == "]":
                continue
            else:
                number = br.string.count("\n", 0, br.start()) + 1
                print("\nOrphan opening bracket at line", number, end="")
                line_start = content.rfind("\n", 0, br.start())
                line_end = content.find("\n", br.end()) 
                print(content[line_start:line_end])
                

        print("\n")

        #Find all closing square brackets.
        closing_br = re.finditer(r"\]", content)
        #Loop them through looking for the last square bracket before each and signal its line number
        #if it is a closing bracket instead of the expected opening bracket.
        for br in closing_br:
            preceding_br = (re.findall(r"[\[\]]",content[:br.start()]) )[-1]
            if preceding_br == "[":
                continue
            else:
                number = br.string.count("\n", 0, br.start()) + 1
                print("\nOrphan closing bracket at line", number, end="")
                line_start = content.rfind("\n", 0, br.start())
                line_end = content.find("\n", br.end()) 
                print(content[line_start:line_end])

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

    #Read the file as one long string and close it.
    if input_successful == True:
        content = file.read()
        file.close()
        #Call checkbr function defined earlier
        checkbr(content)
        print("\n---Brackets checked.---")
    else:
        print("\nInput failed several times.")
        print("---Operation interrupted.---")

#Check document for orphan brackets.
run_function()


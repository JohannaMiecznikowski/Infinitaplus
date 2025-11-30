#Number lines in transcript

#This script is part of the "TIGRformat" package.
#The package supports a workflow in which "traditional transcripts" are exported from ELAN
#and processed automatically and manually in view of qualitative analysis.
#Refer to the package's readme file for more information.

#INPUT:
#"Traditional transcript" file exported from ELAN manipulated both automatically and manually
#OUTPUT:
#Document with line numbers.

#EXPLANATION:
#N.B. The ----Transcript---- title, if present, is supposed to be followed 
#by one blank line.

def run_function():

    import re

    def insert_line_numbers(content):
        """Inserts line numbers at the beginning of transcript lines.

        The document must be opened as a list of lines (file.readlines()).
        Works properly for documents with up to 9999 lines.""" 
        
        ln = 1
        for i in range(len(content)):
            if i in range(10):
                content[i] = str(ln)+(" "*4)+content[i]
                ln = ln + 1
            elif i in range(10, 100):    
                content[i] = str(ln)+(" "*3)+content[i]
                ln = ln + 1
            elif i in range(100, 1000):    
                content[i] = str(ln)+(" "*2)+content[i]
                ln = ln + 1
            elif i in range(1000, 10000):    
                content[i] = str(ln)+(" "*1)+content[i]
                ln = ln + 1
            else:
                print("Document longer than 9999 lines, process interrupted.")
                break

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

        #Redefine the content to be numbered as the transript section of the file only, 
        #for the case that there is both a metadata section and a transcript section.
        for line in content:
            if re.search("----Transcript----", line):
                tr_start = content.index(line) + 2
                has_transcript_title = True
                metadata_content = content[:tr_start]
                content = content[tr_start:len(content)]
                break
            else:
                has_transcript_title = False
                continue

        if has_transcript_title == False:
            print("\nTitle ----Transcript---- not found. All lines in the document have been numbered.")
        else:
            print("\n---Lines numbered---")
                
        #Number lines
        insert_line_numbers(content)
            
        #Save file.
        save = filename[:-4]+"_ln.txt"
        with open(save, "x", encoding="utf-8") as f:   
            if has_transcript_title == True:    
                for line in metadata_content:
                    f.write(line)
                for line in content:
                    f.write(line)
            else:
                for line in content:
                    f.write(line)
        print("File saved as", save)
       
    else:
        print("\nInput failed several times.")
        print("---Operation interrupted---")
        
#Perform all operations
run_function()

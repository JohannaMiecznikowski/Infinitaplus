This package contains scripts to support a workflow that prepares trancripts exported from ELAN for qualitative analysis.

Goal
====

The goal of the workflow is to produce transcripts for qualitative analysis
- that are easily readable for the human eye, which means that graphical layout is used to convey information and the text is as compact as possible;
- that correctly represent speech overlap;
- that do not maintain as graphical units any ELAN segments that have no theoretically justifiable boundaries;
- that can relatively easily be annotated by the annotation program Inception, which implies (a) compactness and (b) the possibility to go back and forth between the original transcript and the text version visualized in the brat editor that works best in Inception; 
- that contain a certain amount of references to timecode to allow navigating audio/video recordings while reading and annotating the transcript.

Steps
=====

Step 1: Export from ELAN
Export from ELAN in the "traditional transcript" format with the following options:
- include participant labels
- no suppression of repeated labels
- include time codes
- include silence duration indication, minimal silence duration: 100 ms; 2 digits after decimal
- use Jefferson style alignment for "["
- line length: 80 characters
- merge annotations on the same tier if the gap is less than 10 ms

Step 2: Fix orphan square brackets
- Check if the transcript contains orphan brackets;
- Insert missing brackets manually in the original ELAN document;
- Export document again from ELAN, check again and, if ok, replace first export.
Supporting script: TIGRformat.TIGRlayout.check_orphan_brackets

Step 3: Filter and format timecode
- Leave timecodes at a user-defined interval, delete the rest;
- In this process avoid timecodes that follow lines with square brackets in order to minimize the risk of having to deal with word-internal segment beginnings;
- Insert explicit timecode marks at the corresponding positions in the transcript;
- Where necessary, move timecode up to the line that immediately follows the timecode mark;
- Save document appending "_tcfltrd" to the document name.
Script that performs these operations: TIGRformat.TIGRtimecode.timecode_at_intervals

Step 5: Suppress undesired repeated speaker labels
- Suppress speaker labels of segments (printed one at a line by the ELAN export function) uttered by the same speaker as the immediately preceding segment;
- Save document appending "_nolbls" to the document name.
Script that performs these operations: TIGRformat.TIGRlayout.suppress_repeated_labels

Step 6: Reformat discourse produced by the same speaker ("etic turn")
- Concatenate ELAN segments produced by the same speaker without interventions by other speakers and re-break any long lines to shorten them to a maximum of 86 charaters;
- Save document automatically appending "_concat" to the document name.
N.B. "Etic turns" share the basic idea with "contributions" in TEI/ISO 20624:2016 transcripts, but tend to be longer. 
The reason is that they include all pauses followed by a continuation by the same speaker. 
In contrast, TEI/ISO 20624:2016 contributions include only pauses marked by the transcriber, while pauses resulting from gaps between ELAN segments are treated as contribution delimiters.
Script that performs these operations: TIGRformat.TIGRlayout.concatenate

Step 7: Check concatenated timecode marks
Manually check timecode marks. Try to optimize graphically, trading off two requirements: compactness and the preferential placement of timecode in the line that immediately follows the mark.
No supporting script. These operations must be done manually.

Step 8: Format overlapping speech
- Manually align overlapping speech in those cases in which the ELAN export does not yield satisfactory results (usually, when more than two speakers are involved).
- When doing this, avoid incomplete words at the end of a line.
- Manually delete speaker labels that become superfluous when several segments are concatenated in one line.
- Keep the ELAN document open in this stage to check overlaps.
- You might notice errors in the ELAN document that have gone unnoticed so far: correct these in ELAN and in the .txt document. Remember to frequently save: ELAN might shut down from time to time unexpectedly.
- Save document manually without changing name.
No supporting script. These operations are best done in a text editor (e.g. Notepad++).

Step 9: Check layout
- Check the document again for orphan square brackets.
- Check the document for repeated speaker labels.
- Check the document for lines containing timecode marks and square brackets (the insertion of timecode marks in step 3 caused misalignments of square brackets, not all of which might have been detected in step 7);
- Check the document for pointers to ending points of ABIENT_NOISES ("-->"); where necessary, move the arrow to the corresponding point of reference in the following lines of the transcript.
- Save document manually with new name: replace "_tcfltrd_nolbls_concat" by "_formatted";
- Move all intermediate documents to a subfolder and leave in place only the "_formatted" document.
Supporting scripts: TIGRformat.TIGRlayout.check_orphan_brackets, TIGRformat.layout.combicheck

Step 10 (optional): Number lines
If you need numbered lines for qualitative analysis:
- Insert line numbers at the beginning of each line;
- Save document automatically appending "_ln" to the document name.

Instructions for the use of the TIGRformat package
==================================================
In these instructions, double quotes (" ") are used to cite code that must be typed. The quotes themselves should not be typed. If quotes need to be typed, they are indicated by means of single quotes here.

1) Open the command prompt / terminal. In Windows: click on the Windows symbol and open the computer's start menu. Type "cmd" to find the command prompt; click to open.

2) To use the TIGRformat package, you should navigate to the folder that contains it. In the command line, the text that precedes the prompt sign is the path of the current directory. The uppercase letter at the beginning of the path indicates the drive you are on. Check if you are on the drive that contains the TIGRformat package. If not, type the uppercase letter of the correct drive, followed by a colon (e.g. "A:"), and hit "Enter". Type "cd" (command to define the current directory), a space and then the entire path of the directory containing the TIGRformat package (+"Enter": this is necessary in general to make the commands work and will not be repeated further in these instructions). Use the "cd" to navigate in the folder hierarchy: Type "cd SUBFOLDER" to go a subfolder of the current directory and "cd .." to go up to the current directory's parent folder.

3) Once you're in the folder that contains the TIGRformat package, instruct the command prompt to use the Python language, or "interpreter". To do that, type "python" or "py". The prompt sign will change now: by default, the prompt of the Python interpreter is ">>>". 
N.B. You might need to go back to the basic prompt at some point, e.g. to navigate to a different directory. Type "exit()" to leave the Python interpreter.

4) TIGRformat is a set of scripts in a structure of folders and subfolders, each of which contains an "__init__" file. The entire structure is called a "package". The TIGRformat scripts consist of two parts:
- A definition of one large function (which can contain subfunctions) named "run_function()", which is designed to perform all the operations needed;
- At the end of the script, a command that calls that function to actually execute the operations.

5) Import a script into the interpreter to use it. 
- When importing a script for the first time, it is executed and its definitions, including the definitions of the run_function(), are recognized by Python. To reuse a script after it has been imported, call its run_function() (the syntax is explained at point 6).
- When you import a new script B after having imported a preceding script A, Python will recognize the definitions of script B and stop recognizing those of script A.
- To return to script A after having imported script B, you have to import script A again. The script will not be executed this time (only the first import results in immedate execution); but re-importing it is necessary to make Python recognize its definitions, including its run_function().

6) There are different ways of formulating import commands and calling a script's run_function.

6a) First possibility: Use commands of the form "from (FOLDER.)SCRIPT import run_function". The precise structure of the command depends on where you are in the folder hierarchy (remember that you can navigate in folders as described at point 2). If the script is in the current directory, refer to it directly and type "from SCRIPT import run_function". If the script is in a subfolder of the current directory, use dotted foldername syntax to refer to it: "from SUBFOLDER.SCRIPT import run_function", "from SUBFOLDER.SUBSUBFOLDER.SCRIPT import run_function", etc.
Once imported in that way, you can re-use the script calling its run_function without any prefix: simply type "run_function()".

6b) Second possiblity: Use commands of the form "(from FOLDER) import SCRIPT". If the script is in the current directory, directly type "import SCRIPT". If it is in a subfolder, type "from SUBFOLDER import SCRIPT", "from SUBFOLDER.SUBSUBFOLDER import SCRIPT" etc. 
Once a script has been imported in that way, in order to call its run_function(), the script name must be used as a prefix": "SCRIPT.run_function()".

Beware: When importing the run_function in scenario 6a, you must mention it as a name, whitout any argument brackets ("run_function"). On the other hand, when calling the function to execute it, you need to put argument brackets ("run_function()" in scenario 6a, "SCRIPT.run_function()" in scenario 6b).

7) When you exit the Python interpreter ("exit()"), all imports are erased. As a consequence, when you enter the interpreter again, importing a script will execute it (remember that scripts are executed immediately when they are imported for the first time in an interpreter session). So to execute a script repeatedly, instead of using its run_function() as explained at the points 5 and 6, you can also exit the interpreter, re-enter it and import the script anew. This alternative is more costly in terms of the number of computations to be performed, but in the case of the TIGRformat package, the scripts are so small that you will most probably not notice any difference with regard to the procedure described at points 5 and 6.














import re, argparse

########################################## Function/Constant Definitions ###############################################


#read in height/width/filename from command line if provided
parser = argparse.ArgumentParser(description='Provide the wait @ signs if the previous dialogue contained :dwave: an it ended with / (ignore line feed)')
parser.add_argument('--script', default ='0.utf')
parser.add_argument('--linux_line_endings', action='store_true')

args = parser.parse_args()
print('Settings used:', args)

#set line ending mode (either force windows newlines, or use whatever is given
newlineMode=None
if args.linux_line_endings:
    newlineMode = ''

####################################### Script Setwindow argument modification #########################################

print("\n\n----------------")
print("Providing @ if necessary")
print("----------------")
lookForWait = False
ii = 0
with open(args.script, encoding='utf-8') as script:
    with open('waitsAdded-' + args.script, 'w', encoding='utf-8', newline=newlineMode) as outScript:
        for line in script:

            #lookForWait at first is False so just skip that part for a moment
            ##############################################################

            matchObject = re.match('^langen', line)
            #not interested in not langen lines
            if not matchObject:
                outScript.write(line)
                continue

            if lookForWait is True:

                matchObject = re.match('(^.+?)(:dwave)(.+)$', line)
                if matchObject:
                    #first dwave in the line is the one we interested in.
                    #checking if dwave is not being preceded by wait sign
                    #provide @ if there is no wait
                    betweenStartAndFirstDwave = matchObject.group(1)
                    if "@" not in betweenStartAndFirstDwave and "\\" not in betweenStartAndFirstDwave:
                        ii=ii+1
                        line = betweenStartAndFirstDwave + "@" + matchObject.group(2) + matchObject.group(3) + "\n"
                    lookForWait = False

                #line does not contain a dwave but it might have the wait sign
                elif "@" in line or "\\" in line:
                    lookForWait = False

            ##############################################################

            #search for a line which contains the 'langen' and check if it:
            # contains dwave
            # ends with ignore line feed sign (/) without click wait signs (@ or \) between last dwave and end of the line
            if lookForWait is False:
                matchObject = re.match('^.*dwave.*/$', line)
                if matchObject:
                    betweenLastDwaveAndEnd = re.split(r"wave .*?:", line)[-1]
                    if "@" not in betweenLastDwaveAndEnd and "\\" not in betweenLastDwaveAndEnd:
                    #if described line is found in the next iterations the other langen line will be searched for with other conditions
                        lookForWait = True

            outScript.write(line)

        print(str(ii))
        print('Finished, wrote to:', outScript.name)
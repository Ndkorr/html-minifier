#!python3
# a minification script (initially) for html and css that removes whitespace and comments
# My idea is to allow the program to accept a single file then check if its html or css (limitation of this script)
# Future plan for this is to make it a parser as well
# The idea of minification is to reduce file size of the html/css as small as possible by deleting whitespace and comments. This optimize file can now be used on production to decrease the loading time by loading a relatively small html/css file compared to unminified version


# used built in function for path and extension checking
import os, sys

# reused function I made on my zip compressor module
def progclose(userinput):
    """ Function to accept current user input, closes the program it match to x"""
        
    if userinput == 'x':
        return True

def specifypath():
    """ Function to let the users specify the path to read"""
    while True:
        try:
            print('\n===========================================================================')
            print('Specify file path to read: ')
            print('Press x to exit the program')
            specifyFolderToZip = input()
            print(specifyFolderToZip)
            ext = progclose(specifyFolderToZip)
            if ext == True:
                return True
            # print(os.path.isdir(specifyFolderToZip))
            # use os path join to use this program on windows - this is to handle users input path in a default format like C:\Users... etc the \ is an escape character which will ignore the letter next to it
            for i in specifyFolderToZip: # iteration on each single char of the specified string path
                if i == '\\': # once found replace all string with double backslash
                    specifyDir = specifyFolderToZip.replace(i, '\\\\')
                    break
                else: # accepts directory with / format such as linux and macos
                    specifyDir = specifyFolderToZip
                    break

            # remove "" in cases of copy file as path (ctrl + shift + c) etc
            if '"' in specifyFolderToZip or "'" in specifyFolderToZip:
                specifyFolderToZip = specifyFolderToZip.replace('"', '')
                specifyFolderToZip = specifyFolderToZip.replace("'", '')
                #print(specifyFolderToZip)

            checkDir = os.path.isdir(specifyFolderToZip)
            checkFileDir = os.path.isfile(specifyFolderToZip)
            # check if file basename extension is equal to html/css
            fileBasename = os.path.basename(specifyFolderToZip)
            getExtension = fileBasename.rfind('.')
            getBasename = fileBasename[getExtension:]
            if checkDir == True: # modify string to remove last / on linux or other system that use /
                print('Specified file path is not a file')
                continue
            elif checkFileDir == True and (getBasename == '.html' or getBasename == '.css'):
                chosenDir = specifyDir
                return chosenDir
            elif checkFileDir == True and (getBasename != '.html' or getBasename != '.css'):
                print('Specified file is not an html or css')
                continue 
            else:
                print('Specified Path is not a valid path!')
                continue
        except:
            print('Specified Path is not a valid path!')
            continue

# parse style - checks for inline css on the html code
def parseStyle(file):
    # I'll just copy it from the parseScript I made.
    # check the <style> check the first tag first
    if '<style' in file:
        leftStyle = file.find('<style')
    # if no style found then that means return immediately 
    else:
        return file
    # check the closing tag
    if '</style>' in file:
        rightStyle = file.find('</style>')
        rightStyle = rightStyle + 9

    else:
        # convert the string first to list so that we can identify where the script start tag line occurs
        findLineOfStyle = file.splitlines()
        for i in findLineOfStyle:
            if '<style' in i:
                findLine = findLineOfStyle.index(i)               
                break

        err = f'<style> tag were never closed. Check line {findLine + 1}'
        print(err)
        return 0

    # if both conditions were successful then its time to parse / minify the script into one line
    storeStyle = file[leftStyle:rightStyle]
    # we need to store the original script (unparsed) and the script (parsed) so that we can replace it later on
    origStyle = file[leftStyle:rightStyle]

    # break the strings into list
    storeStyleL = storeStyle.splitlines()
    # remove unnecessary new lines
    for i in storeStyleL:
        if i == '':
            storeStyleL.remove(i)

    # iterate on each list item to check for ' ' or whitespace at index 0
    for i in storeStyleL:
        # get the index of current iteration
        index = storeStyleL.index(i)
        # loop through the string until the first index is not equal to whitespace
        while True:
            if i[0] == ' ':
                i = i[1:]
                continue
            else:
                break
        # after breaking the while loop, overwrite the current i with the modified/unmodified string
        storeStyleL[index] = i

    # when the for loop ends we have now a list of script without the whitespace
    # we can append it now to a single string
    # overwrite first the storeScript to empty string
    storeStyle = ""
    for i in storeStyleL:
        storeStyle = storeStyle + i

    # now the storeScript contains one line <script> ... </script>
    # replace the original script with the modified script in the file
    file = file.replace(origStyle, storeStyle)
    # print(file) # debug
    return file

# parse svg - checks for the svg markup on the html code
def parseSvg(file):
    initialCursor = 0
    while True:
        # initialCursor = 0
        # print('Find svg: ', file[initialCursor:])
        # check the <svg> start tag
        if '<svg' in file[initialCursor:]:
            finder = file.index('<svg', initialCursor)
            leftSvg = finder # file.find('<svg')
            # print(leftSvg)
        else:
            return file
            break
        # check the closing </svg> tag
        if '</svg>' in file[initialCursor:]:
            rightSvg = file.find('</svg>', initialCursor)
            rightSvg = rightSvg + 6
            # print(rightSvg)
        else:
            # convert the string first to identify where the svg starts
            findLineOfSvg = file.splitlines()
            for i in findLineOfSvg:
                if '<svg' in i:
                    findLine = findLineOfSvg.index(i)
                    break
    
            err = f'<svg> tag were never closed. Check line {findLine + 1}'
            print(err)
            return 0
    
        # if both conditions were met then start storing the svg and original
        storeSvg = file[leftSvg:rightSvg]
        # print(storeSvg)
        origSvg = file[leftSvg:rightSvg]
        # print(storeSvg)
        
        while True:
            if '<!--' in storeSvg and '-->' in storeSvg:
                # find index of the first comment it will find
                # for the left start the find index is always correct since it will match the '<' first
                findLeftComment = storeSvg.find('<!--')
                # while on the right comment we need to add 2 on its index to set the cursor to '>' because the find will return the index of '-'
                findRightComment = storeSvg.find('-->')
                # add additional 1 because of how the slice works
                findRightComment = findRightComment + 3
                findComment = storeSvg[findLeftComment:findRightComment]
                # comments.append(findComment)
                # replace now the comment with empty string
                storeSvg = storeSvg.replace(findComment, '')
                # continue looping until 
                continue
            # no comments where found on the file
            else:
                break
        
        # store the svg string on a list
        storeSvgL = storeSvg.splitlines()
        # print(storeSvgL, len(storeSvgL))
        
        # find multi line declaration ex "T 20 20 \n T 20 20"
        # initialize an empty dict
        storeDicSvg = {}
        # declare righty as 0
        righty = 0
        lefty = 0
        leftyFind = 0
        for i in storeSvgL:
            # declare lefty as 0 on each iteration
            #print(storeSvgL.index(i))
            # specifically find the first single ", ', """ that means there is a multi string declaration well unlike on for example class="hello" the string contains both declaration ""
            # I change it to count so it specifically find 1 occurance of the quote on the current index
            if i.count('"') == 1 or i.count("'") == 1 or i.count('"""') == 1:
                # leftQuote will only satisfy if lefty == righty on first leftQuote find
                # lefty == leftQuote and therefore this if condition to find leftQuote will not satisfy leading to
                # the rightQuote condition since lefty always return to 0 on each iteration,
                # the if condition is satisfied on rightQuote since righty caught the first leftQuote
                # and it may now declare the rightQuote and reset the righty value which will now satisfy the leftQuote if condition to find the next quote
                if lefty == righty:
                    leftQuote = storeSvgL.index(i, leftyFind)
                    # store the first caught leftQuote on a variable
                    lefty = leftQuote
                    # print(f'Left Quote: {leftQuote}, {storeSvgL[leftQuote]}')
                    # print(i)
                    correctIndex = storeSvgL.index(storeSvgL[leftQuote], leftyFind) 
                    # print(correctIndex)
                    continue
                    # store lefty on righty to store the first quote
                    # righty = lefty
            # if last index then pass to second if statement to catch the error
            elif i == storeSvgL[-1]:
                storeSvgL = storeSvgL
            # return the svgL as is
            else:
                # continue until it finds a single quoted string 
                storeSvgL = storeSvgL
                continue
            
            # print(lefty)
            if (i.count('"') == 1 or i.count("'") == 1 or i.count('"""') == 1) and righty != storeSvgL.index(i):
                # print(storeSvgL.index(i))
                # found a bug / well not actually a bug but a limitation of the current if else condition. Apparently if we find the index of the current iteration and it has the same copy on the list it will find the first occurance because by default the .index start searching at index zero so we need to specifically tell .index to start searching to the last index or -1 if the quote is found
                righty = lefty
                rightQuote = storeSvgL.index(i, righty)
                # add 1 because we don't want to slice the end quote
                rightQuote = rightQuote + 1
                # return righty to 0 to match a new quote
                leftyFind = rightQuote
                righty = 0
                lefty = 0
                # print(f'Right Quote: at {rightQuote}')
    
                # I moved the list and dict declaration here since if both quote conditions were satisfied then its time to add/append it on the list then dict
                # if both conditions were satisfied
                # store the list where the opening and closing quote occurs 
                # I add 1 to leftQuote because we will store it on a dict where the leftQuote is the key so it should not be included on the list(value)
                storeUnaffectedList = storeSvgL[(leftQuote + 1):rightQuote]
                # print('List:')
                # print(storeUnaffectedList)
                # store in a dictionary so that when user declares more multi line quoted string on an svg
                # I changed it to leftquote because we need to remove the unaffectedlist and remember what index they are on the original list
                l = leftQuote
                r = rightQuote
                # print('lefty', l)
                # use the iteration value as the key where it iterates on the for loop given that both of the above conditions were true because it will never reach up to this point
                storeDicSvg.setdefault(correctIndex, storeUnaffectedList)
                # storeDicSvg.setdefault(r, storeUnaffectedList)
                # i += 1
                # print('dict')
                # print(storeDicSvg)
                # rightQuote = 0
                
            elif lefty == storeSvgL.index(i):
                continue
            # catch the last index so that it won't go to else. The idea is that the first leftQuote search all index for quote and will just continue iterating if no found until the last index where it goes here on the rightQuote condition
            # we need to catch that last index so that it won't go to else
            elif i == storeSvgL[-1]:
                storeSvgL = storeSvgL
            else:
                findQuote = file.splitlines()
                for i in findQuote:
                    if i.count('"') == 1 or i.count("'") == 1 or i.count('"""') == 1:
                        findQ = findQuote.index(i)
                        break
                findErr = findQuote.index(findQuote[findQ]) 
                err = f'multi line string were never closed properly. Check line {findErr + 1}'
                print(err)
                return 0
    
            # reset the UnaffectedList
            storeUnaffectedList = []
            
        # print(storeSvgL[454])
        # print(storeDicSvg)
        # remove unneccesary new lines \n
        
        for i in storeSvgL:
            if i == '':
                print('tete', i)
                storeSvgL.remove(i)
        # print('debug:', storeSvgL[0:15])
        
        # print(storeSvgL[454])
        # we need to update the storeDicSvg values to remove the
        
        # now we need to parse it on a single line with respect to multi line quote
        # make sure storeDicSvg contains an item/s
        if len(storeDicSvg) != 0:
            # remove unneccesary new lines \n
            for k, v in storeDicSvg.items():
                for i in v:
                    #print(v)
                    if i == '':
                        storeDicSvg[k].remove(v)
                        #print(f'Hey:\n{storeDicSvg}')
                    # remove whitespace and tab
                    index = v.index(i)
                    while True:
                        if i[0] == ' ' or i[0] == '\t':
                            i = i[1:]
                            #print(f'Hey:\n{i}')
                            continue
                        else:
                            break
                    
                    v[index] = i
                    #print(v)
            # print(storeDicSvg)
            # add a reference of leftQuote start before deleting the storeSvgL.
            leftStarters = {}
            for k, v in storeDicSvg.items():
                leftStarters.setdefault(k, storeSvgL[k])
    
            # print('left starters:', leftStarters, '\n')
            # i need to store the keys on a list in order to get its absolute position - well if we remove it on the original file then removing it from the list should have the same value
            lst = []
            for k in storeDicSvg.keys():
                lst.append(k)
            # print(lst, '\n')
            getStart = {}
            for k in storeDicSvg.keys():
                getStart.setdefault(k, storeSvgL[k])
            # print(getStart)
            # now we have the list of all the keys, we can now set the first index as the cursor
            cursor = lst[0]
            prevIndex = [] # contains the distance between the last 'last quote' and the next quote
            newStartingPointAfterDeletion = []
            difference = [] # contains the distance the current quote takes
            start = [] # contains reference of the quoteStart
            # final = difference - (prevIndex
            # print('cursor', cursor)
            # print('type', type(cursor))
            # print(leftStarters)
            # print('before deleting', storeDicSvg)
            # print('before deleting', storeSvgL)
            # if we delete items on the original storeSvgL that means if the first quote starts at 3 and ends at 8
            # and the len of storeSvgL is 20 that means the original if the second quote is originally at 10 and ends at 14
            # if we delete at first cursor set at 3 range 3 to 9 that means we minus it to storeSvgL so -6 the storeSvgL len is now 14
            # and the next partner (quote [start and end]) should also adjust accordingly that means 10 and 14 is now 4 and 8 which makes sense because the new index 3 value is previously index 9
            # print('orig len', len(storeSvgL))
            # print(storeSvgL)
            # return storeSvgL
            defaultLen = len(storeSvgL)
            for k, v in storeDicSvg.items():
                # cut / remove the UnaffectedList stored in StoreDicSvg
                # know the start and end on which we will remove the items on the original list
                # on our dict the items are: {quotestart: [values, values... quoteend]} and it was derived from original svgList so each key-value pair or specifically list value, won't contain the 
                # get the cursor from lst
                # print(k)
                # print('len', len(storeSvgL))
                # removed = defaultLen - len(storeSvgL)
                # newLen = defaultLen - removed
                
                prev = lst.index(k) # [4, 16, 20, 31]
                quoteStart = k # ex - 4
                quoteEnd = k + len(v) + 1 # ex - k = 4 + 10 == 14 then loop starts at 4 and ends at 14 but 14 will not be included so add 1 
                # nextIndex = lst[lst.index(k) + 1]
                # prevIndex.append(nextIndex - quoteEnd) # [6, 4 ...]
                start.append(quoteStart)
    
                final = getStart[k]
                index = storeSvgL.index(final)
                newStartingPointAfterDeletion.append(index)
                prevIndex.append(index - 1)
                # prevIndex.append(index - 1)
                # print(prevIndex)
                # newStartingPointAfterDeletion.append(prev)
                # print(quoteStart)
                # print(quoteEnd)
                # print(final in storeSvgL)
                # print(storeSvgL.index(final))
                for i in range(quoteStart, quoteEnd):
                    # print(i)
                    # print(quoteStart)
                    # Use the quote start as the cursor of index deletion
                    # print(storeSvgL[new])
                    storeSvgL.remove(storeSvgL[index])
                    # print(quoteStart)
                    # print(storeSvgL) # debug
                    # print('hey')
                
            # print(prevIndex, '\n', newStartingPointAfterDeletion)
            # print(storeSvgL[prevIndex[5]])
            # print(f'after: {storeDicSvg}')
            # print(f'after: {storeSvgL}')
    
            
            # after processing the dict we can now update it with a string instead of list. we will overwrite the key(quotestart):value(list) to key(quotestart):value(string) where the string is the one line of that multiline string
            # print('before', storeDicSvg, '\n')
            for k, v in storeDicSvg.items():
                #print('k val', k)
                # find the first quoted string
                firstQuote = leftStarters[k]
                # print(leftStarters[k])
                for i in v:
                    # print(v[-2])
                    if i == v[-2] or i == v[-1]:
                        firstQuote += i
                        # print('tite kaba')
                    else:
                        firstQuote += i + ' '
    
                storeDicSvg[k] = firstQuote
    
    
            afterIndex = []
            for i in prevIndex:
                # index = i + 2
                # print(index)
                afterIndex.append(storeSvgL[i + 1])
            # print(afterIndex)
                        
            add = 0
            for i in prevIndex:
                index = prevIndex.index(i)
                i += add
                add += 1
                prevIndex[index] = i
    
            
            for i in prevIndex:
                storeSvgL.insert(i + 1, 'Put here')
                
            # print(f'after: {storeDicSvg}\n')
            # print(f'LOOK HERE after: {storeSvgL}')
            # return storeSvgL
            # since we have the new dict value we need to plug it in on the original storeSvgL
            # lst = [1 2 3 4 5]
            # if we remove the 2 3 4 lst = [1 2] the 5 becomes 2
            # the original position of 2 3 4 is 2
            # therefore if we use .insert then the k of storeDicSvg is correct
            # print('svgL', storeSvgL)
            # print('before', storeSvgL, '\n')
            # storeSvgL.insert(cursor, storeDicSvg[cursor])
            # use a while loop trick setting the iteration i = 0 but in for loop of dictionary to access the items and the newPoint list item as it iterates
            # before inserting we need to add on newStartingPointAfterDeletion 0,1,2,3,4 on each item iteration this is because if we insert something on storesvgL the reference point is not the same so we need to add (+1)
            add = 0
            for i in newStartingPointAfterDeletion:
                index = newStartingPointAfterDeletion.index(i)
                i += add
                add += 1
                newStartingPointAfterDeletion[index] = i
    
            # confirm the location of put here by using prevIndex well if we have newStartingPoint then we can test if the 'Put here' is in correct position
            for i in prevIndex:
                if storeSvgL[i + 1] == 'Put here':
                    continue
                    # print('correct')
                else:
                    # print('wrong')
                    storeWrongValue = storeSvgL[i + 1]
                    # print(storeWrongValue)
                    findPutHere = storeSvgL.index('Put here', i) # find put here starting from i which is the previous index so it will always find the first put here 
                    # swap the wrong value with put here and the findPutHere to wrongValue
                    storeSvgL[i + 1] = 'Put here'
                    storeSvgL[findPutHere] = storeWrongValue
    
            # print('\n')
            indx = 0
            # print(afterIndex)
            # print('tite', afterIndex[indx])
            for i in prevIndex:
                # print(storeSvgL[i + 2])
                after = afterIndex[indx]
                # print(afterIndex)
                if storeSvgL[i + 2] == after:
                    # print('correct')
                    indx += 1
                    continue
                else:
                    # print('wrong')
                    storeWrongValue = storeSvgL[i + 2]
                    # print(afterIndex)
                    # print(storeSvgL.index(after))
                    findAfterValue = storeSvgL.index(after, i)
                    # swap the correct after value to wrong value
                    storeSvgL[i + 2] = after
                    storeSvgL[findAfterValue] = storeWrongValue
                    
                indx += 1
                
            # print(newStartingPointAfterDeletion)
            
            i = 0
            for k, v in storeDicSvg.items():
                # print(i)
                storeSvgL[storeSvgL.index('Put here')] = v
                i += 1
    
            # remove whitespace / tab \t
            for i in storeSvgL:
                # print('current:', i)
                index = storeSvgL.index(i)
                if i[0] == ' ' or i[0] == '\t':
                    while True:
                        # check if i string becomes empty, that means it is a whitespace 
                        if i == '':
                            # storeSvgL.remove(storeSvgL[index])
                            # print(i)
                            break
                        
                        if i[0] == ' ' or i[0] == '\t':
                            i = i[1:]
                            # print('current', i, 'at index: ', index)
                            continue
                        else:
                            break
                    storeSvgL[index] = i
                else:
                    continue
            
            # print('after', storeSvgL, '\n')
            # loop through each item on the storeSvgL and declare it on storeSvg
            # print(storeSvg)
            storeSvg = ""
            for i in storeSvgL:
                if i == storeSvgL[-1]:
                    storeSvg += i
                else:
                    storeSvg += i + ' '
            # print(len(file))
            # print(len(origSvg))
            lenOfString = len(storeSvg)
            # print(lenOfString)
            # print('after:', storeSvg)
        # add an else statement if no multi line string found on the svg element
        else:
            storeSvg = ""
            for i in storeSvgL:
                if i == storeSvgL[-1]:
                    storeSvg += i
                else:
                    storeSvg += i + ' '
        # print(storeSvgL)
    
        # finally, combine all list(storeSvgL) in a single string which we will then append on the original file
        file = file.replace(origSvg, storeSvg)
        # print(file)
        # b = [storeDicSvg, storeSvgL, file]
        initialCursor = finder + lenOfString # we add the first svg find + lenOfString which is the modified storeSvg that means that is the end of the svg
        # return file

    
# parse script - checks if the html contains an inline script element
def parseScript(file):
    # check the <script> check the first tag first
    if '<script>' in file:
        leftScript = file.find('<script>')
    # if no script found then that means return immediately 
    else:
        return file
    # check the closing tag
    if '</script>' in file:
        rightScript = file.find('</script>')
        rightScript = rightScript + 9

    else:
        # convert the string first to list so that we can identify where the script start tag line occurs
        findLineOfScript = file.splitlines()
        for i in findLineOfScript:
            if '<script>' in i:
                findLine = findLineOfScript.index(i)               
                break

        err = f'<script> tag were never closed. Check line {findLine + 1}'
        print(err)
        return 0

    # if both conditions were successful then its time to parse / minify the script into one line
    storeScript = file[leftScript:rightScript]
    # we need to store the original script (unparsed) and the script (parsed) so that we can replace it later on
    origScript = file[leftScript:rightScript]

    # break the strings into list
    storeScriptL = storeScript.splitlines()
    # remove unnecessary new lines
    for i in storeScriptL:
        if i == '':
            storeScriptL.remove(i)

    # iterate on each list item to check for ' ' or whitespace at index 0
    for i in storeScriptL:
        # get the index of current iteration
        index = storeScriptL.index(i)
        # loop through the string until the first index is not equal to whitespace
        while True:
            if i[0] == ' ':
                i = i[1:]
                continue
            else:
                break
        # after breaking the while loop, overwrite the current i with the modified/unmodified string
        storeScriptL[index] = i

    # when the for loop ends we have now a list of script without the whitespace
    # we can append it now to a single string
    # overwrite first the storeScript to empty string
    storeScript = ""
    for i in storeScriptL:
        storeScript = storeScript + i

    # now the storeScript contains one line <script> ... </script>
    # replace the original script with the modified script in the file
    file = file.replace(origScript, storeScript)
    # print(file) # debug
    return file


# main function - accepts specified path and an optional parameter to tell whether replace the file or save it on different file name
def parse(yourpath, savename="overwrite"):
    # remove "" in cases of copy file as path (ctrl + shift + c) etc
    if '"' in yourpath or "'" in yourpath:
        yourpath = yourpath.replace('"', '')
        yourpath = yourpath.replace("'", '')
    # change dir incase user wants to change the output file name
    getPathOnly = os.path.dirname(yourpath)
    os.chdir(getPathOnly)

    # read the file
    file = open(yourpath, 'r')
    fileRead = file.read()
    file.close()
    
    # tell the user to specify the output file name
    name = input('Output file name: (n to disregard)\n')
    if name.lower() != 'n':
        savename = name
        yourpath = savename
    
    # read inline styles
    checkParseStyle = parseStyle(fileRead)
    # this means that the script tag were never closed
    if checkParseStyle == 0:
        fixTheCode = 'Fix the code first before parsing'
        print(fixTheCode)
        return fixTheCode
    # if no errors then pass the parsedScript to fileRead
    else:
        fileRead = checkParseStyle
    
    # read inline script
    checkParseScript = parseScript(fileRead)
    # this means that the script tag were never closed
    if checkParseScript == 0:
        fixTheCode = 'Fix the code first before parsing'
        print(fixTheCode)
        return fixTheCode
    # if no errors then pass the parsedScript to fileRead
    else:
        fileRead = checkParseScript

    # read svg elements
    checkParseSvg = parseSvg(fileRead)
    # this means that the svg tag were never closed
    if checkParseSvg == 0:
        fixTheCode = 'Fix the code first before parsing'
        print(fixTheCode)
        return fixTheCode
    # if no errors then pass the parseSvg to fileRead
    else:
        fileRead = checkParseSvg

    # print(fileRead) # debug fileRead
    # remove whitespace first
    # debug container of comments
    
    comments = []
    while True:
        if '<!--' in fileRead and '-->' in fileRead:
            # find index of the first comment it will find
            # for the left start the find index is always correct since it will match the '<' first
            findLeftComment = fileRead.find('<!--')
            # while on the right comment we need to add 2 on its index to set the cursor to '>' because the find will return the index of '-'
            findRightComment = fileRead.find('-->')
            # add additional 1 because of how the slice works
            findRightComment = findRightComment + 3
            findComment = fileRead[findLeftComment:findRightComment]
            comments.append(findComment)
            # replace now the comment with empty string
            fileRead = fileRead.replace(findComment, '')
            # continue looping until 
            continue
        # no comments where found on the file
        else:
            break
    
    # print(fileRead)
    # print(comments)
     
    # print(fileRead) # debug fileRead
    # split the string and put on a list
    fileList = fileRead.splitlines()
    # print(fileList)
    # remove unneccesary newline
    for i in fileList:
        if i == '':
            fileList.remove(i)
    # remove tab and space
    
    for i in fileList:
        # get the index of current iteration
        index = fileList.index(i)
        # loop through the string until the first index is not equal to whitespace
        while True:
            if i == '':
                break
            else:
                if i[0] == ' ' or i[0] == '\t':
                    i = i[1:]
                    continue
                else:
                    break
        # after breaking the while loop, overwrite the current i with the modified/unmodified string
        fileList[index] = i
    
    # loop on each items to check the string for whitespace using startwith
    for i in fileList:
        # finds the < on the string. suppose: '    <div>' the \n is automatically removed when we use splitlines
        findLessThan = i.find('<')
        # find the index of the current iteration(i) this will be used as a cursor when '<' is not equal to 0 therefore there's a space before the '<'
        indexOfFileList = fileList.index(i)
        if findLessThan != 0:
            i = i[findLessThan:]
            # overwrite the fileList item
            fileList[indexOfFileList] = i
    
    # print(fileList) # debug fileList
    # run a loop on the modified list and store the final output on a string
    # init string variable (container)
    fileListOutput = ''
    for i in fileList:
        fileListOutput = fileListOutput + i
        
    # open the file as write mode
    filew = open(yourpath, 'w')
    filewWrite = filew.write(fileListOutput)
    filew.close()

yourpath = specifypath()
if yourpath == True:
    sys.exit()

parse(yourpath)

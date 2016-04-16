#This is my project for CS 3430
#I need to take each barcode, and parse through a fastq file with several hundred million reads and pull out the ones that start with those 14-15 bases.
#It would be good if I could allow one mismatch to account for sequencing error.

barcodes = {}

with open("Barcodes_Salvinia.csv", "r") as f:           #reading in the barcode file
    for line in f:
        barcodes[line.split(',')[1]] = line.split(',')[0]       #creating dictionary with barcodes as key and A1 as value

#print barcodes                                             #printing to check that it worked
#print barcodes.keys()

for i in barcodes:
    with open(barcodes[i] + '.fastq', 'w') as j:
        j.write(barcodes[i] + "\n")

identifier = ""
codeline = ""
plussign = ""
quality = ""
tempBCholder = ""
counter = 0
list = []
baddata = []
mismatchbool = None
finalcheck = None

with open("jenessa_10000.fastq", "r") as bigfile:

    for line in bigfile:

        if line[0] == '@':
            counter = 0
        if counter == 0:
            identifier = line
            counter += 1
        elif counter == 1:
            codeline = line
            counter += 1
        elif counter == 2:
            plussign = line
            counter += 1
        elif counter == 3:
            quality = line
            if tempBCholder != "X":

                with open (tempBCholder + ".fastq", "a") as writefile:
                    writefile.write(identifier + "\n")
                    writefile.write(codeline + "\n")
                    writefile.write(plussign + "\n")
                    writefile.write(quality + "\n")


        if line[0] == 'A' or line[0] == 'T' or line[0] == 'C' or line[0] == 'G' or line[0] == 'N':         #only the ones we "care" about
            temp = ""
            for index, char in enumerate(line):
                if finalcheck == True:
                    finalcheck = None
                    break
                temp += char
                #print temp
                if index > 12 or index < 16:        #because barcodes range from 14 to 16 bases
                    if temp.lower() in barcodes:
                        #print "yes"
                        tempBCholder = barcodes[temp.lower()]
                        if temp.lower() not in list:
                            list.append(temp.lower())
                            tempBCholder = barcodes[temp.lower()]
                            print tempBCholder
                            break
                if index == 15:
                    for index2, barcode in enumerate(barcodes):
                        if mismatchbool == True:
                            mismatchbool = None
                            break
                        count = 0
                        Ncount = 0
                        barcount = 0
                        for index3, barcodeIndexes in enumerate(barcode):
                            if temp.lower()[index3] == "n":
                                Ncount +=1
                            elif temp.lower()[index3] != barcode[index3]:
                                count +=1
                            else:
                                count +=0
                        if count <= 1 and Ncount < 2:
                            list.append(barcode)
                            tempBCholder = barcodes[barcode]
                            mistmatchbool = True
                            finalcheck = True
                            #print barcount
                            barcount +=1
                            break
                        if count == 2 and barcode not in baddata:
                           baddata.append(barcode)
                if index > 15:
                    tempBCholder = "X"
                    break
list2 = []                                      #just checking to see how many reads we got. 
doublecount = 0
for i in barcodes:
    with open(barcodes[i] + '.fastq', 'r') as read:
        for line in read:
            doublecount += 1
            list2.append(line)
            if line[0] == 'A' or line[0] == 'T' or line[0] == 'C' or line[0] == 'G' or line[0] == 'N':
                print line
print doublecount
print len(list2)/8
print len(list2)

#print baddata
#print len(baddata)
print "done"

#print len(list)

#print list









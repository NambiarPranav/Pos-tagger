import copy


# Importing the context
dictr={}
dicttag={}  #dicttag denotes the names of the tags along with the corresponding index number
f=open("tags","r")
lines=f.readlines()
j=41
ultatag={}  #opposite of dicttag,it maps index number to tag
for line in lines:
	line=line.split(" ")
	dicttag[str(line[0])]=int(line[1])
	ultatag[int(line[1])]=str(line[0])
prev="DT"






# Now we train the data on the train.txt dataset
f=open("train.txt","r")
lines=f.readlines()
prevtag="CC"
currtag="CC"
tagg=[]   # tagg maps the probability that a tag occurs given the previous tag
a=[]      # a maps the probability the tag occurs given the word (ps:this is never used)
for j in range(0,60):
	a.append(0)
for i in range(0,60):
	tagg.append(a)
j=41


# Populating the tag and a lists
for line in lines:
	line=line.split(" ")
	if (len(line)==3):
		prevtag=currtag
		if (dictr.get(str(line[0]),"None")=="None"):
			a=[]
			for i in range(0,60):
				a.append(0)
			if (dicttag.get(str(line[1]),"None")=="None"):
				dicttag[str(line[1])]=j
				ultatag[j]=str(line[1])
				j=j+1
			currtag=line[1]
			a[dicttag[str(line[1])]]+=1
			dictr[str(line[0])]=a
		else:
			a=dictr[str(line[0])]
			a[dicttag[str(line[1])]]+=1
			dictr[str(line[0])]=a
		tagg[dicttag[(currtag)]][dicttag[prevtag]]+=1


foreachtag=[]    #foreachtag maps the probability of the word given the tag

# Initializing the foreachtag list
for j in range(0,60):
	foreachtag.append({})


# Populating the foreachtag list
for line in lines:
	line=line.split(" ")
	if (len(line)==3):
		if (foreachtag[dicttag[str(line[1])]].get(str(line[0]),"None")=="None"):
			(foreachtag[dicttag[str(line[1])]])[str(line[0])]=1
		else:
			(foreachtag[dicttag[str(line[1])]])[str(line[0])]=(foreachtag[dicttag[str(line[1])]])[str(line[0])]+1



# Converting the frequencies of foreachtag to the corr. probabilities
i=0
for currtag in foreachtag:
	suma=0
	for su in currtag.values():
		suma=suma+su
	for key in currtag.keys():
		foreachtag[i][key]=foreachtag[i][key]/(suma*1.0)
	i=i+1


# Converting the frequencies of tagg to the corr. probabilities

i=0
for currtag in tagg:
	suma=0
	for su in currtag:
		suma=suma+su
	j=0
	for key in currtag:
		tagg[i][j]=tagg[i][j]/(suma*1.0)
		j=j+1
	i=i+1

f.close()






# Testing the data
f=open("test.txt","r")
lines=f.readlines()
prevtag=prestag="CC"
flg=0
ifno=0.00001
ifnotagg=0.000001

# Declaring values to be used

prevtagdict={} #stores the probability sequence of the previous word having its corresponding tag
nexttagdict={} #stores the probability sequence that given the previous tag sequence will we have the present sequence
correctans=[]  #stores the probability sequence given in the test.txt data
prevtagval=[]  #stores corr. prev tag values
nexttagval=[]  #stores current tag  seq. value
tagcamefrom=[] #stores which is the tag preceding the current max tag values
a=[]           # empty 0 value list
b=[]		   # empty "" list
count=-1
count1=0
count2=0


# Initialising the values

for j in range(0,60):
	a.append(0)
	b.append("")
prevtagval=nexttagval=a
tagcamefrom=b



# Start testing on the data

for line in lines:
	line=line.split(" ")
	if (len(line)==3):
		correctans.append(str(line[1]))
		currword=str(line[0])
		tagcamefrom=b
		if (flg==0):    # If it is the first word of the line
			flg=1
			prevtagval=nexttagval=a
			tagcamefrom=b
			for key in dicttag.keys():
				temp=[]
				temp.append(key)
				# Assign values corresponding to the probability of word given tag
				if ((foreachtag[dicttag[key]]).get(currword,"None")=="None"):
					nexttagdict[key]=temp                      
					nexttagval[dicttag[key]]=ifno
				else:
					nexttagdict[key]=temp
					nexttagval[dicttag[key]]=(foreachtag[dicttag[key]])[currword]
		else:          
			a=[]
			b=[]
			for kr in range(0,60):
				a.append(0)
				b.append("")
			prevtagdict=nexttagdict
			nexttagdict={}
			prevtagval=nexttagval
			nexttagval=a
			for k in prevtagdict.values():
				tg=k[-1]
				valtag=prevtagval[dicttag[tg]]
				for key in dicttag.keys():
					tagtotag=tagg[dicttag[key]][dicttag[tg]]
					if (tagtotag==0):
						tagtotag=ifnotagg
					if ((foreachtag[dicttag[key]]).get(currword,"None")=="None"):
						wordiftag=ifno
					else:
						wordiftag=foreachtag[dicttag[key]][currword]

					# If the probability of the new tag given tag is higher store it
					if (nexttagval[dicttag[key]]<valtag*tagtotag*wordiftag*1000):
						nexttagval[dicttag[key]]=valtag*tagtotag*wordiftag*1000
						tagcamefrom[dicttag[key]]=tg
			
			# Update the nexttagdict now we know max value for each tag sequence
			for k in prevtagdict.values():
				tg=k[-1]
				i=0
				for val in tagcamefrom:
					if (val==tg):
						nexttagdict[ultatag[i]]=copy.deepcopy(k)
						nexttagdict[ultatag[i]].append(ultatag[i])
					i=i+1
		# In order to prevent the values from going too low ,find max and divide all by max so atleast one value is 1 at the end
		maxval=0
		for i in nexttagval:
			if (i>maxval):
				maxval=i
		i=0
		for j in nexttagval:
			nexttagval[i]=nexttagval[i]/maxval
			i=i+1
	else:
		flg=0
		count=count+1
		bestseq=[]
		bestval=0
		i=0
		# Find best sequence of all
		for key in nexttagdict.keys():
			if (nexttagval[dicttag[key]]>bestval):
				bestval=nexttagval[dicttag[key]]
				bestseq=nexttagdict[key]
		i=0
		# Calculate the number of words tagged properly and the total number of words
		while (i<len(bestseq) and i<len(correctans)):
			if (bestseq[i]==correctans[i]):
				count1=count1+1
			count2=count2+1
			i=i+1
		correctans=[]
		nexttagdict={}
		nexttagval=[]
		print ("done"+str(count))

# Print the correctly classified values and the correctness
print ("count1 is "+str(count1))
print ("count2 is "+str(count2))
print ((count1/(count2*1.0))*100)




			


import numpy as np # for math calculations
import math
import nltk # for splitting words from text as tokens
from itertools import combinations # easy computation of combinations
import os # for system navigation

ignore_list = ["the","a","an"]
print("Do you want to omit words ",ignore_list," from the comparison?")
mode = str(input("(Type y for Yes or n for No)"))
if mode is "n":
	ignore_list = []
elif mode is not "y":
	print("Invalid input. Defaulting to yes.\n")

invalid = "Invalid input. Please enter a number greater than 1."
try:
	n = int(input("Please specify number of documents: "))
	if(n<2):
		print(invalid)
		quit()
except ValueError:
	print(invalid)
	quit()
print ("\nComparing " , str(n) , " documents...\n")


# Build word list for every file
h_dir = os.path.join(os.path.dirname(__file__),"files/")

text= ""
words=[[]]*n
files = [f for f in os.listdir(h_dir) if os.path.isfile(os.path.join(h_dir,f)) and ".txt" in f] # selects all contents of folder that are text files
files.sort() # sorts the list of files for a better user experience
for i in range(0,n):
	try:
		doc = open(os.path.join(h_dir,files[i]),"r")
	except IOError:
		print("Could not access all files.")
		quit()
	except IndexError:
		print("Could not access all files.")
		quit()
	for line in doc:
		text+=line
	words[i]=[w.lower() for w in nltk.word_tokenize(text) if w.isalpha() and w not in ignore_list] # splits line to words, makes them lowercase and takes only the ones that are not in the ignore_list 
	text="" # empties the text string before accessing the next document
	doc.close()

# Calculate for each pair their similarities
similarity = {}
for (i,j) in list(combinations(range(n),2)):
	vector = list(set(words[i] + words[j]))
	num_vec1=[0] * len(vector)
	num_vec2=[0] * len(vector)
	for x in range(len(vector)):
		num_vec1[x] = words[i].count(vector[x])
		num_vec2[x] = words[j].count(vector[x])
	similarity[i,j]=np.inner(num_vec1,num_vec2)/ (np.sqrt(np.inner(num_vec1,num_vec1)) * np.sqrt(np.inner(num_vec2,num_vec2)))
print ("Analysis complete.\n")

# Ask user for how many of the top similar they want to see
max_pairs = int(math.factorial(n)/(2 * math.factorial(n-2)))
try:
	k = int(input("How many of the most similar do you want to see? "))
	if k > max_pairs:
		print("Invalid input. Maximum number of pairs to show is",str(max_pairs),". Defaulting to 1")
		k=1
except ValueError:
	print("Invalid input. Defaulting to 1")
	k = 1
print ("\nShowing ", str(k) +" most similar documents:\n")

# Print the most similar docs
top=sorted(similarity.items(),key=lambda x:x[1],reverse=True)[:k]

for i in range(k):
	print("Pair: ", files[(top[i][0])[0]],",",files[(top[i][0])[1]] ," Similarity: ",top[i][1])


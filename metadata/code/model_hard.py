import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
import os
import json
from tqdm import tqdm
from itertools import chain, combinations

def main():
	#setting up data
	train_path = 'msd_genre_dataset.csv'
	train_df = pd.read_csv(train_path)
	print(train_df.head())

	#splitting dataset and adding labels
	metal_df = train_df[train_df['genre'] == 'metal']
	met_len = len(metal_df.index)
	met = [1]*met_len
	metal_df['label'] = met
	metal_df = metal_df.sample(434)

	classical_df = train_df[train_df['genre'] == 'classical']
	classical_len =len(classical_df.index)
	classical = [0]*classical_len
	classical_df['label'] = classical
	classical_df = classical_df.sample(434)

	rock_df = train_df[train_df['genre'] == 'classic pop and rock']
	rock_len =len(rock_df.index)
	rock = [2]*rock_len
	rock_df['label'] = rock
	rock_df = rock_df.sample(434)

	pop_df = train_df[train_df['genre'] == 'pop']
	pop_len =len(pop_df.index)
	pop = [3]*pop_len
	pop_df['label'] = pop
	pop_df = pop_df.sample(434)

	reggae_df = train_df[train_df['genre'] == 'soul and reggae']
	reggae_len =len(reggae_df.index)
	reggae = [4]*reggae_len
	reggae_df['label'] = reggae
	reggae_df = reggae_df.sample(434)

	country_df = train_df[train_df['genre'] == 'folk']
	country_len =len(country_df.index)
	country = [5]*country_len
	country_df['label'] = country
	country_df = country_df.sample(434)	

	hiphop_df = train_df[train_df['genre'] == 'hip-hop']
	hiphop_len =len(hiphop_df.index)
	hiphop= [6]*hiphop_len
	hiphop_df['label'] = hiphop

	jnb_df = train_df[train_df['genre'] == 'jazz and blues']
	jnb_len =len(jnb_df.index)
	jnb= [7]*jnb_len
	jnb_df['label'] = jnb
	jnb_df = jnb_df.sample(434)

	disco_df = train_df[train_df['genre'] == 'dance and electronica']
	disco_len =len(disco_df.index)
	disco= [8]*disco_len
	disco_df['label'] = disco
	disco_df = disco_df.sample(434)

	frames = [metal_df, classical_df, rock_df, pop_df, reggae_df, country_df, hiphop_df, jnb_df, disco_df]
	df = pd.concat(frames)


	print('-------------------------------------')
	print('-------------------------------------')
	print('-----------9 Genre Model-------------')
	print('-------------------------------------')
	print('-------------------------------------')
	print("Generating Model based on Artist Name")
	#Transform names to integers (bag of words)
	vectorizer = CountVectorizer().fit(df['artist_name'])

	#turn names into count vectors
	x = vectorizer.transform(df['artist_name'])

	y = df['label']

	xtrain, xtest, ytrain, ytest = train_test_split(x, y,test_size=0.2)

	# instantiate the model as clf(classifier) and train it
	clf = MultinomialNB()
	clf.fit(xtrain, ytrain)
	acc = clf.score(xtest,ytest)
	print("Artist Accuracy on MSD Dataset: ", acc)

	#Our data set
	test_df = build_dataset()
	xtest = vectorizer.transform(test_df['artist_name'])
	ytest = test_df['label']
	acc = clf.score(xtest,ytest)
	print("Artist Accuracy on our dataset: ", acc)

	print('-------------------------------------')

	print("Generating Model based on Song Title")


	#Transform names to integers (bag of words)
	vectorizer = CountVectorizer().fit(df['title'])

	#turn names into count vectors
	x = vectorizer.transform(df['title'])

	xtrain, xtest, ytrain, ytest = train_test_split(x, y,test_size=0.2)

	# instantiate the model as clf(classifier) and train it
	clf_title = MultinomialNB()
	clf_title.fit(xtrain, ytrain)
	acc = clf_title.score(xtest,ytest)
	print("Song Title Accuracy on MSD Dataset:", acc)

	xtest = vectorizer.transform(test_df['title'])
	ytest = test_df['label']
	acc = clf_title.score(xtest,ytest)
	print("Song Title Accuracy on our Dataset:", acc)
	print('-------------------------------------')

	##################################################################################################################################################

	features = ['tempo','time_signature','loudness','key','duration']

	print("Generating Model based on", features)
	all_features = chain.from_iterable(combinations(features,r) for r in range(1,len(features)+1)  )

	max_accuracys = []
	for feature_list in tqdm(all_features):
		feature = list(feature_list)

		#x = df[['tempo','time_signature','loudness','key','duration']]
		x = df[feature]
		y = df['label']

		xtrain, xtest, ytrain, ytest = train_test_split(x, y,test_size=0.2)

		max_acc = -1
		for k in range(3,250,5):
			knn = KNeighborsClassifier(n_neighbors=k)
			knn.fit(xtrain,ytrain)
			acc = knn.score(xtest,ytest)
			if acc > max_acc:
				max_acc = acc 
		max_accuracys.append((max_acc,feature))
	acc = [item[0] for item in max_accuracys]
	feat = [item[1] for item in max_accuracys]

	print("KNN Model based on ",features,"\nAccuracy on MSD dataset:",max(acc),"-- uses:",feat[acc.index( max(acc))])



def build_dataset():
	fileNames = ['results_classical.txt','results_country.txt','results_hiphop.txt','results_metal.txt','results_pop.txt','results_reggae.txt','results_rock.txt','results_jazz.txt','results_blues.txt','results_disco.txt']
	#fileNames = ['results_classical.txt','results_metal.txt'] #easy version

	data = []
	for file in fileNames:
		f = open(file,'r')
		label = file.split('.')
		label = label[0][8:]
		Met = 0
		if label == 'metal':
			Met = 1
		elif label == 'rock':
			Met = 2
		elif label == 'pop':
			Met = 3
		elif label == 'reggae':
			Met = 4
		elif label == 'country':
			Met = 5
		elif label == 'hiphop':
			Met = 6
		elif label == 'jazz' or label == 'blues':
			Met = 7
		elif label == 'disco':
			Met = 8
		line = f.readline()
		while(line):
			x = line.split(":")
			songData = x[2]
			songData = songData.strip('][').split(', ') 
			song = songData[0]
			#song.replace("'","")			
			artist = songData[1]
			artist = artist[1:-1]
			#artist.replace("'","")
			if ('-' in songData[0] and file != 'results_classical.txt'):
				x = songData[0].split('-')
				artist  = x[0]
				artist = artist[1:]
				song = x[1]
				song = song[:-1]
			else:
				song = song[1:-1]

			data.append([label,artist,song,Met])
			line = f.readline()

	data = pd.DataFrame(data, columns = ['genre', 'artist_name','title','label'])
	#print(data)
	return data


if __name__ == '__main__':
	main()

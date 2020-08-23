# song-classifier
Classifies song to its closest of ten genres based on .wav / .mp3 file inputs

check `slides.pptx` for an overview

![webapp_image](https://user-images.githubusercontent.com/33814854/90926823-de89fd80-e3c1-11ea-9d34-1f92e7b63ff2.png)

Scroll to the bottom of the page for Web App Setup and Use instructions.

## Motivation

The goal of this project was to create a machine learning model that could accurately predict the genre of a song based on the audio waveform of the song. The classification of songs into genres can be useful for recommendation systems, playlist generation and audio generation, used at large audio companies such as Spotify, Pandora or Tidal. 

![pic1](https://user-images.githubusercontent.com/33814854/90966739-30a34f80-e4a4-11ea-9ff5-4d2dd7e01853.png)


## Dataset

The dataset used is the <a href="http://marsyas.info/downloads/datasets.html">GZTAN dataset</a>, consisting of 100 30-second unnamed songs classified into ten different genres:

<ul>
  <li>Rock</li>
  <li>Blues</li>
  <li>Jazz</li>
  <li>Metal</li>
  <li>Reggae</li>
  <li>Disco</li>
  <li>Classical</li>
  <li>Country</li>
  <li>Pop</li>
  <li>Hip Hop</li>
</ul>

## Strategy

This team tried multiple strategies. The main strategy centralized around using the <a href="https://en.wikipedia.org/wiki/Mel-frequency_cepstrum">Mel Frequency Cepstral Coefficients</a> of small segments of each song as inputs of training data to a TensorFlow Neural Network. Additional strategies explored, include a <a href="https://en.wikipedia.org/wiki/Long_short-term_memory">Long short-term memory (LSTM)</a> recurrent neural network architecture, which is not discussed here, and a metadata model. 

## MFCC Segmentation Model

### Preprocessing

![gif1](https://user-images.githubusercontent.com/33814854/90966876-be336f00-e4a5-11ea-963d-011f9786c71b.gif)

The raw audio files are segmented into 0.2 second chunks. The Mel Frequency Cepstral Coefficients (MFCC) of the 0.2 second segments are generated and then used as inputs into a TensorFlow Neural Network whose layers were set up as described below. 

![pic2](https://user-images.githubusercontent.com/33814854/90966919-49146980-e4a6-11ea-9dd7-91cfd8fb2a7b.png)

### Training and Prediction

An 80/20 train/test split was used with 80/100 songs of each genre in the GZTAN dataset being used for training.

After training, each new song input is segmented and converted to MFCC to be fed into the network. The 0.2 second segments are classified according to the model, and then a majority approach is used to determine the final classification.

![pic3](https://user-images.githubusercontent.com/33814854/90967017-59791400-e4a7-11ea-9a93-d13f1b2dba86.png)

### Results

The final accuracy of the majority voting segmentation MFCC method was around 81% between all 10 genres.

![pic4](https://user-images.githubusercontent.com/33814854/90967066-018edd00-e4a8-11ea-8da0-610d45ee56ab.png)

The easiest models to classify were Jazz and Classical at over 93%, these genres tend to have the most distinct musical style.

![pic5](https://user-images.githubusercontent.com/33814854/90967067-018edd00-e4a8-11ea-9284-da5ca65485fa.png)

## Metadata Model

![gif2](https://user-images.githubusercontent.com/33814854/90967390-9abff280-e4ac-11ea-96d4-049d99587a4f.gif)

It was proposed that the artist name or song title, might be able to predict the genre of a song. Similar to how you can probably predict the genre of a song called 'Symphony No. 40 Molto allegro' to be Classical or a song from an artist with the name 'Slayer' to be Metal, this group hoped to explore whether any verifiable pattern in data existed. These pieces of data (Artist Name, Song Title, Year Released, Album Name, Label), which describe the audio data are considered 'metadata' in this project. 

The two metadata features considered in the project were Artist Name and Song Title.

### Naïve Bayes


**Training data**
Data from the <a href="http://millionsongdataset.com/blog/11-2-28-deriving-genre-dataset/">Million Songs Genre Dataset</a> was used as training data, genres were separated into their closest genre in the GZTAN Dataset as described below.

<ul>
  <li><strong>MSD Dataset -> GZTAN Dataset</strong></li>
  <li>Classic Pop and Rock -> Rock</li>
  <li>Jazz and Blues -> Blues </li>
  <li>Jazz and Blues -> Jazz</li>
  <li>Metal -> Metal</li>
  <li>Reggae -> Reggae</li>
  <li>Dance and Electronica -> Disco</li>
  <li>Classical -> Classical</li>
  <li>Folk -> Country</li>
  <li>Pop -> Pop</li>
  <li>Hip Hop -> Hip Hop</li>
</ul>

The songs from this dataset were used to see if any patterns could be generated to predict genre based on the metadata. 

**Testing data**
The GZTAN dataset was used as the test dataset. However, since the files in GZTAN were unnamed, a third party API was used to generate the song title and artist name. It is imporant to note that the third party API used to identify song metadata was unable to identify all songs for some genres like Hip Hop and Classical. 

**Preprocessing**
A Bag of Words approach was used in the Naive Bayes model to map names and song titles.

![pic6](https://user-images.githubusercontent.com/33814854/90967632-ff308100-e4af-11ea-8e06-1b3d247f6703.png)

The SKLearn Library "MultinomialNB" implementation of Naïve Bayes was then used on an 'easy' binary classification between two genres and a 'hard' dataset consisting of seven of the ten GZTAN genres (Metal, Classical, Rock, Pop, Reggae, Country, Hip-hop). Other genres were excluded because these seven genres were the genres that directly correlated between the training and testing datasets.

**Easy Results**

![pic7](https://user-images.githubusercontent.com/33814854/90967687-f8563e00-e4b0-11ea-99d2-6b06ee75a17c.png)

We saw mixed results, where the Song Title generally outperformed the Artist Name, however often performance was not much better than a coin-flip (and worse in some cases).

**Hard Results**

Between the seven genres (Metal, Classical, Rock, Pop, Reggae, Country, Hip-hop) the best result of this model was
<ul>
  <li>27% - Artist Name</li>
  <li>23.8% - Song Title</li>
</ul>
This result is better than random genre guessing, but not impressive.

The MSD Genre Dataset is heavily unbalanced however for each different genre (434 Hip Hop songs vs. 23895 Classic Pop and Rock). This might explain why accuracy was so volatile in the binary classification. Additionally, the GZTAN dataset only contained 100 audio samples, some of which were different 30-second sections of the same song.

### K-NN Model

**Dataset**

Because the Million Songs Genre Dataset considered other metadata features, such as tempo, time signature, loudness, key, and duration, another metadata analysis on these features was done using only the MSGD, using all 9 MSGD genres. 

**Preprocessing**
An 80/20 train/test split of only the MSGD was used. Because of the imbalance in genre, only 434 songs of each genre were selected (as that was the number of Hip Hop Songs in total).

**Binary Classification Results**
The highest classification accuracy based on these metadata features was 93.68% between Hip-Hop and Classical, and the features that resulted in the highest accuracy were time signature and loudness.
The lowest classification accuracy was 63.79% between Country and Rock, and the features that resulted in this accuracy were time signature and loudness.

**Nine Genre Classification Results**
The highest classification accuracy using all 9 of the MSGD genres (Metal, Classical, Classic Pop and Rock, Pop, Reggae, Folk, Hiphop, Dance and Electronica, Jazz and Blues) was 29.92% using the features tempo, loudness, and key.

In conclusion, while there may seem to be some sensible reasoning that the metadata like Artist Name and Song Title might give some insight into what genre a song may be, it is not as accurate as analyzing the audio itself. In the future, larger and more balanced datasets might yield better results.

Teammates: Daniel Dias, Phalguna Rupanagudi, Sukris Vong, Brett Watanabe

## Web App Setup and Use

<ol>
  <li>Go to the executable directory</li>
  <li>In conda (version 4.7.10), create an environment using environment_mac.yml or environment_win.yml, depending on your operating system</li>
  <li>Activate the environment and run: python app.py</li>
  <li>Visit the output address from the command line into a web browser</li>
  <li>Click “Choose File” to select a wav file</li>
  <li>Click submit to run the classifier</li>
  <li>Once the classifier is finished, the display on the right side of the screen will show the classification and the confidences as shown below.</li>
</ol>

![webapp_image](https://user-images.githubusercontent.com/33814854/90926823-de89fd80-e3c1-11ea-9d34-1f92e7b63ff2.png)

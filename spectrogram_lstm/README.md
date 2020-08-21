### Installing the LSTM model environment

Run `conda env create -f environment.yml` in the root folder containing the LSTM source code.

Then activate the new enviroment with `conda activate cs6220ProjectLstm`

### Running the LSTM code

Run `jupyter notebook` in the `src` folder

There is only 1 audio file in each category to train on out of the box and files must be placed into the `audio_files/genres/*` folders. The files must be named in the format `{genre}.{#####}.wav`.
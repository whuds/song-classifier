from pydub import AudioSegment
import os
import requests
import json
import glob
import time


'''
Uses API from: https://user.audiotag.info/ to generate song title and artist
album and year are questionable
'''

def main():
	folder = input("input folder name with wav files: ")
	
	foldername = 'C:\\Users\\Wyndham\\Desktop\\Fall2019\\CS6220\\project\\data\\' + folder
	api_url = 'https://audiotag.info/api'
	apikey = '25fdc6ca95beefef0d9223be11c3d2cb'; # generate and place here your unique API access key, the key must be 'active'

	tokens = [];
	songs = [];
	results = {};

	txtFileName= 'results_' + folder + '.txt'
	res_file = open(txtFileName,"w+", encoding="utf-8")


	for filename in glob.glob(os.path.join(foldername, '*.wav')):
		print('\n\n\n\n\n')
		print("File name: ",filename)

		payload = {'action': 'identify', 'apikey': apikey}
		result = requests.post(api_url,data=payload,files={'file': open(filename, 'rb')})
		#print(result.text)
		json_object = json.loads(result.text);
		if 'token' in json_object.keys():
			tokens.append(json_object["token"]);
			songs.append(filename)
		pretty_print = json.dumps(json_object, indent=4, sort_keys=True)
		print(pretty_print);
		print('---------------------------------------------------------------');

		result_object = json_object
		if result_object['success']==True and result_object['job_status']=='wait' :
			token = result_object['token'];
			n=1;
			job_status = 'wait';
			while n < 100 and job_status=='wait':
				time.sleep(0.5) ;
				print('request:%d'%(n));
				n+=1;
				payload = {'action': 'get_result', 'token':token, 'apikey': apikey}
				result = requests.post('https://audiotag.info/api',data=payload)
				#print(result.text);
				result_object = json.loads(result.text);
				print(result_object);
				if ('success' in result_object.keys()) and result_object['success']==True:
					job_status = result_object['result'];
					if 'data' in result_object.keys():
						track = result_object['data'][0]['tracks'][0]
						print('----------------------------------------')
						print(track)
						print('----------------------------------------')

						results[filename] = track
						res_file.write(filename + ':' + str(track) + '\n')
				else:
					break;
		else :
			print ('not success');
			break;

	res_file.close()

	print(results)

if __name__ == "__main__":
	main()
import requests
import time


authKey = '93b8d80c0fa64ae695eb1b3ce60fbc13'

headers = {
    'authorization' : authKey,
    'content-type'  : 'application/json'
}

uploadUrl      = 'https://api.assemblyai.com/v2/upload'
transcriptUrl  = 'https://api.assemblyai.com/v2/transcript'



def uploadMyFile(fileName):

    def _readMyFile(fn):

        chunkSize = 5242880

        with open(fn, 'rb') as fileStream:

            while True:
                data = fileStream.read(chunkSize)

                if not data:
                    break

                yield data
   

    response = requests.post(
        uploadUrl,
        headers= headers,
        data= _readMyFile(fileName)
    )

    json = response.json()

    return json['upload_url']


def startTranscription(aurl):

    response = requests.post(
        transcriptUrl,
        headers= headers,
        json= { 'audio_url' : aurl }
    )
    
    json = response.json()

    return json['id']


def getTranscription(tid):

    maxAttempts = 10
    timedout    = False

    while True:
        response = requests.get(
            f'{transcriptUrl}/{tid}', #transcriptUrl + '/' + tid,
            headers= headers
        )

        json = response.json()

        if json['status'] == 'completed':
            break

        maxAttempts -= 1
        timedout = maxAttempts <= 0

        if timedout:
            break

       
        time.sleep(3)

    return 'Timeout...' if timedout else json['text']



# step 1) Upload Audio File
audioUrl = uploadMyFile('Recording2.m4a')

# step 2) Start Transcription
transcriptionID = startTranscription(audioUrl)

# step 3) Get Transcription Text
text = getTranscription(transcriptionID)

print(f'Result: {text}')
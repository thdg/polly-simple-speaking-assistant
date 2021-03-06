#! *--coding: utf-8--*
import boto3
import simpleaudio as sa
import wave

try:
    from secrets import access_key_id, secret_access_key
except importError:
    print("Please make sure you create a secret file with aws keys")
    exit()

POLLY = boto3.Session(
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name='us-west-2').client('polly')


def get_audio(text):
    response = POLLY.synthesize_speech(VoiceId='Karl',
        OutputFormat='pcm',
        Text = text)
    return response

def save_file(response):
    fname = "tmp.mp3"
    with wave.open(fname, 'wb') as wav_file:
        wav_file.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wav_file.writeframes(response['AudioStream'].read())
    return fname

def play(fname):
    wave_obj = sa.WaveObject.from_wave_file(fname)
    play_obj = wave_obj.play()
    return play_obj

print("Hvað liggur þér á hjarta?")
po = None
while True:
    text = input(u"")
    r = get_audio(text)
    f = save_file(r)
    if po:
        po.wait_done()
    po = play(f)

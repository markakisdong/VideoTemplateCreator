# Import everything needed to edit video clips
from moviepy.video.tools.segmenting import findObjects
from PIL import Image
from moviepy.editor import *
from moviepy.audio import *
from moviepy.audio.fx.all import audio_fadeout
from moviepy.video.fx.fadeout import fadeout
from effx import *
from procads import *
import urllib, cStringIO
import pdb
import json
import glob

screensize = (640, 480)

def simpleTextClip(textToShow, fsize, posi, subc, funcpos):
    txtClip = TextClip(textToShow, color='white', fontsize=fsize)
    cvc = CompositeVideoClip([txtClip.set_pos(posi)], size=screensize)
    letters = findObjects(cvc) # a list of ImageClips
    # WE ANIMATE THE LETTERS
    txt_clip = CompositeVideoClip(ef_moveLetters(letters, funcpos), size=screensize).subclip(0, subc)
    return txt_clip

def tagclip(taglist):
    cliplist = []
    for i in taglist:
        cliplist.append(ImageClip(i, duration=1))

    return cliplist

def readAds(adsjson):
    # with open(adsjson, 'r') as f:
    #     ads_list = json.load(f)

    img_list = []
    for i in range(10):
        img = cStringIO.StringIO(urllib.urlopen(adsjson[i]['url']).read())
        img_dict = {'data': Image.open(img), 'tag': adsjson[i]['tag']}
        img_list.append(img_dict)

    return img_list

def intro(duration):
    # Get the basic transforming text
    txt_clip = simpleTextClip('Ads for you', 50, 'center', 4, ef_vortex)
    # The circle effect
    maskclip = VideoClip(ef_intro_circle, duration=duration) # 2 seconds

    return txt_clip, maskclip

def run(adsjson):
    #adsjson = 'datas.json'
    img_list = readAds(adsjson)
    pdb.set_trace()
    good_imgs = []
    for i in img_list:
        gi = pil_adprocess(i['data'])
        gi_dict = {'data': gi, 'tag': i['tag']}
        good_imgs.append(gi_dict)

    _INTRO_DURATION = 4
    _ADS_DURATION = 10
    _TEXT_DURATION = 14
    _END_DURATION = 4
    _DURATION = _INTRO_DURATION + _ADS_DURATION + _TEXT_DURATION + _END_DURATION

    # 1. Get the intro clip
    txt_clip, maskclip = intro(_INTRO_DURATION)
    # Compose clips
    intro_clip = CompositeVideoClip([maskclip, txt_clip])

    # 2. Get the ads clips
    tag0 = []
    tag1 = []
    tag2 = []
    tag3 = []
    for i in good_imgs:
        if i['tag'] == 0:
            tag0.append(np.array(i['data']))
        elif i['tag'] == 1:
            tag1.append(np.array(i['data']))
        elif i['tag'] == 2:
            tag2.append(np.array(i['data']))
        elif i['tag'] == 3:
            tag3.append(np.array(i['data']))

    tag0textclip = simpleTextClip('love me plz', 50, 'center', 3, ef_cascade)
    tag0clips = tagclip(tag0)
    tag1textclip = simpleTextClip('We got cheaper ones!', 50, 'center', 3.5, ef_vortex)
    tag1clips = tagclip(tag1)
    tag2textclip = simpleTextClip('ON A DISCOUNT', 50, 'center', 3.5, ef_arrive)
    tag2clips = tagclip(tag2)
    tag3textclip = simpleTextClip('Thank you for these', 50, 'center', 4, ef_vortex)
    tag3clips = tagclip(tag3)
    fulltagclips = [tag0textclip] + tag0clips + \
                   [tag1textclip] + tag1clips + \
                   [tag2textclip] + tag2clips + \
                   [tag3textclip] + tag3clips

    # Bye clip
    byeclip = fadeout(simpleTextClip('SEE YA', 50, 'center', _END_DURATION, ef_vortex), duration=_END_DURATION)
    concat_clip = [intro_clip] + fulltagclips + [byeclip]
    #pdb.set_trace()

    # concatenate all the clips
    final = concatenate_videoclips(concat_clip)
    # Read the fucking audio
    audio = audio_fadeout(AudioFileClip("sources/facebook.mp3").subclip(0, _DURATION), duration=4)
    final = final.set_audio(audio)
    # Write the result to a file (many options available !)
    final.write_videofile("holy.avi", fps=25, codec="mpeg4")

if __name__ == '__main__':
    main()

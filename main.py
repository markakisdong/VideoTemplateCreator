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
    # append the moviepy's ImageClip to a python list
    cliplist = []
    for i in taglist:
        cliplist.append(ImageClip(i, duration=1))

    return cliplist

def readAds(adsjson):
    # the adsjson looks like this:
    # { 'data': [
    #     {
    #       'url': 'https://....',
    #       'tag': 0
    #     },
    #     ...
    #     {
    #       'url': 'https://....',
    #       'tag': 1
    #     }
    #   ]
    # }
    img_list = []
    for i in range(10):
        img = cStringIO.StringIO(urllib.urlopen(adsjson[i]['url']).read())
        img_dict = {'data': Image.open(img), 'tag': adsjson[i]['tag']}
        img_list.append(img_dict)

    return img_list

def intro(duration):
    # Get the basic transforming text, check out simpleTextClip()
    txt_clip = simpleTextClip('Ads for you', 50, 'center', 4, ef_vortex)
    # The circle expanding effect.
    maskclip = VideoClip(ef_intro_circle, duration=duration) # 2 seconds

    return txt_clip, maskclip

def run(adsjson):
    # read the ads from the json file, which contains:
    # url: the link to the image
    # tag: the type of the ad
    #   type 0: the user did not click on it and buy from the ad
    #   type 1: the user did not click on it but buy the product of the ad
    #   type 2: the user clicked on it but did not buy the product of the ad
    #   type 3: the user clicked on it and did buy the product of the ad
    img_list = readAds(adsjson)

    # prepare the ads' image for our template video
    # the width, height of our video is 640, 480. Therefore, our image should
    # be 640, 480. We achieve this goal by pasting the original ad on a blank
    # background. After the process, the datas are well processed.
    good_imgs = []
    for i in img_list:
        gi = pil_adprocess(i['data'])
        gi_dict = {'data': gi, 'tag': i['tag']}
        good_imgs.append(gi_dict)

    # define the duration of each clip for the final clip sampling
    _INTRO_DURATION = 4
    _ADS_DURATION = 10
    _TEXT_DURATION = 15
    _END_DURATION = 4
    # full duration of our created video
    _DURATION = _INTRO_DURATION + _ADS_DURATION + _TEXT_DURATION + _END_DURATION

    # Time to create our own video
    # 1. Get the intro clip with some text effect, check out info()
    txt_clip, maskclip = intro(_INTRO_DURATION)
    # Compose clips
    intro_clip = CompositeVideoClip([maskclip, txt_clip])

    # 2. Get the ads clips. The ads clips are splitted into 4 groups mentioned
    # previously, based on the tag.
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

    # The first tag, tag0, is the type of ad that the user totally ignored.
    tag0textclip = simpleTextClip('love me plz', 50, 'center', 3, ef_cascade)
    tag0clips = tagclip(tag0)
    # Tag1 is the type of ad that the user access the product not from the ad,
    # but somewhere else.
    tag1textclip = simpleTextClip('We got cheaper ones!', 50, 'center', 3.5, ef_vortex)
    tag1clips = tagclip(tag1)
    # Tag2 is the type of ad that the user actually clicked on it, but never did
    # the purchase action.
    tag2textclip = simpleTextClip('87/100 Interested', 50, 'center', 4.5, ef_arrive)
    tag2clips = tagclip(tag2)
    # Tag3 is the type of ad that the user appreciate. GOOD FOR THEM.
    tag3textclip = simpleTextClip('Thank you for these', 50, 'center', 4, ef_vortex)
    tag3clips = tagclip(tag3)
    fulltagclips = [tag0textclip] + tag0clips + \
                   [tag1textclip] + tag1clips + \
                   [tag2textclip] + tag2clips + \
                   [tag3textclip] + tag3clips

    # Bye clip, a 'SEE YA' fade out text clip
    byeclip = fadeout(simpleTextClip('SEE YA', 50, 'center', _END_DURATION, ef_vortex), duration=_END_DURATION)
    concat_clip = [intro_clip] + fulltagclips + [byeclip]

    # concatenate all the clips
    final = concatenate_videoclips(concat_clip)
    # Read the audio and give the fade out duration
    audio = audio_fadeout(AudioFileClip("sources/facebook.mp3").subclip(0, _DURATION), duration=4)
    final = final.set_audio(audio)
    # Write the result to a file (many options available !)
    final.write_videofile("holy.mp4", fps=24, codec='libx264', audio_codec='aac',\
                            temp_audiofile='bgTMP.m4a', remove_temp=True)

if __name__ == '__main__':
    # if called from here, give our prepared json file
    with open('datas.json', 'r') as f:
        adsjson = json.load(f)
    run(adsjson)

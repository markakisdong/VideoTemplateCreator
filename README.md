## VideoTemplateCreator

A very easy video generator.<br>
Generate a Facebook-rewind-like video with given advertisement image from the JSON file.

This is an advertisement rewind video generator, the advertisements are split into 4 tags. Tag 0 means the advertisement was not seen by the user, the product/item was not purchased by the user either. Tag 1 means the advertisement was not seen by the user, but the user actually purchased the product/item the advertisement trying to show. Tag 2 means the advertisement was seen by the user, but the user did not pay further attention. Tag 3 means the advertisement was successfully merchandised to the user and made profit from the user.

### System Requirement:
Required system-wide packages: ```imagemagick, cairo (sudo apt install or brew install will do)```. Please refer to [moviepy download/install page](https://zulko.github.io/moviepy/install.html) for more information. Install other dependencies by:<br>
```bash
pip install -r req.txt
```

### How to run:
Simple python (with datas.json as input, change it in bottom of main.py):
```python
python main.py
```
or from other program:
```python
from VideoTemplateCreator.main import *
run(jsonfile)
```

### Input format:
Simple JSON:
```
[
  {
    'url': '#image_url_here',
    'tag': #tag_number
  },
  {
    'url': '#image_url_here',
    'tag': #tag_number
  },
  ...
]
```

### Output format:
A sample rewind video of the advertisement that was put by the advertisers that wants to suck your money. Take a look.<br>
(Parsed from datas.json. Download holy.mp4 with audio and high fps, below is a sample gif)

![A sample gif from datas.json](https://github.com/markakisdong/VideoTemplateCreator/blob/master/sample.gif)

### Acknowledgement:
Meichu Hackathon 2016 Tagtoo Team 4.

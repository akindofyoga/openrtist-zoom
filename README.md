# OpenRTiST webcam stream for GNU/Linux

```bash
sudo apt-get install v4l2loopback-utils
sudo modprobe v4l2loopback devices=2
python3 -m pip install requirements.txt
python3 main.py HOST STYLE
```

You can see a list of styles
[here](https://github.com/cmusatyalab/openrtist/tree/master/models).
The STYLE argument should be the name of a txt file in that directory, 
without the extension (such as `mosaic`).

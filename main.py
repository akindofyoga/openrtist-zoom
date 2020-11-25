import argparse

import cv2
import pyfakewebcam

from gabriel_client.opencv_adapter import OpencvAdapter
from gabriel_client.websocket_client import WebsocketClient

import openrtist_pb2


IMG_WIDTH = 480
IMG_HEIGHT = 360
PORT = 9099

SOURCE_NAME = 'openrtist'


def main():
    parser = argparse.ArgumentParser(description='OpenRTiST Webcam Client')
    parser.add_argument('host')
    parser.add_argument('style', nargs='?', default='mosaic')
    args = parser.parse_args()

    video_capture = cv2.VideoCapture(-1)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)

    # Use these in case IMG_WIDTH or IMG_HEIGHT are not supported
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fake_webcam = pyfakewebcam.FakeWebcam('/dev/video2', width, height)

    def preprocess(frame):
        return frame

    def produce_extras():
            extras = openrtist_pb2.Extras()
            extras.style = args.style
            return extras

    def consume_frame(frame, packed_extras):
        # extras = openrtist_pb2.Extras()
        # packed_extras.Unpack(extras)
        fake_webcam.schedule_frame(frame)

    opencv_adapter = OpencvAdapter(
            preprocess,
            produce_extras,
            consume_frame,
            video_capture,
            SOURCE_NAME)

    client = WebsocketClient(
        args.host, PORT, opencv_adapter.get_producer_wrappers(),
        opencv_adapter.consumer)
    client.launch()


if __name__ == '__main__':
    main()

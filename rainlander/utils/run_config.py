# encoding: utf-8
from google.protobuf import text_format
import sys
from crtrain.protos.pipeline_pb2 import TrainPipeLine
from crtrain.api import gui_run

def main():
    tep = TrainPipeLine()  # 训练pipeline

    # 解析文本形式的配置文件
    with open("workspace/config_tmp/train.config", "r") as fp:
        text_format.Merge(fp.read(), tep)

    gui_run(tep)

if __name__ == '__main__':
    main()

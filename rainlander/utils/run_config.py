# encoding: utf-8
import sys
import argparse

from google.protobuf import text_format
from crtrain.protos.pipeline_pb2 import TrainPipeLine
from crtrain.protos.pipeline_pb2 import EvalPipeLine
from crtrain.api import gui_run

def main():
    parser = argparse.ArgumentParser(description='Run with a configuration')
    parser.add_argument('-t',
            action = 'store',
            dest = 'task',
            help = 'task: "train" or "eval"',
            required = True)
    parser.add_argument('-i',
            action = 'store',
            dest = 'input',
            help = 'Input Configuration',
            required = True)
    args = parser.parse_args()

    if args.task == 'train':
        pipe = TrainPipeLine()  # 训练pipeline
    elif args.task == 'eval':
        pipe = EvalPipeLine()

    # 解析文本形式的配置文件
    with open(args.input, "r") as fp:
        text_format.Merge(fp.read(), pipe)

    gui_run(pipe)

if __name__ == '__main__':
    main()

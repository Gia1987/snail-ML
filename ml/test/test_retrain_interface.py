import os
import random
import path_helper

from retrain_interface import get_retrain_command, run_bash_command, get_classify_command

class MyOutput(object):
    def __init__(self):
        self.data = []

    def write(self, s):
        self.data.append(s)

    def __str__(self):
        return "".join(self.data)

def test_get_retrain_command_generates_command_string_properly():
    images_path = "test_dir"
    module_url = "test_url"
    model_path = "./model"
    model_name = "model_name"
    command_string = get_retrain_command(
    images_path, module_url, model_path, model_name)
    expected_return = ("python retrain.py \\" +
        "--image_dir test_dir \\" +
        "--tfhub_module test_url \\" +
        "--bottleneck_dir ./model/bottleneck \\" +
        "--output_graph ./model/model_name.pb \\" +
        "--output_labels ./model/model_name_labels.txt \\" +
        "--intermediate_output_graphs_dir ./model/intermediate_graph/ \\" +
        "--summaries_dir ./model/retrain_logs \\" +
        "--saved_model_dir ./model/exported_graph")
    assert(command_string) == expected_return

def test_run_bash_command_runs_command():
    filename = "testfile" + str(random.random())
    run_bash_command("touch " + filename)
    assert (filename in os.listdir('.')) == True
    run_bash_command("rm " + filename)

def test_get_classify_command_generates_command_string_properly():
    model_path = "./model"
    model_name = "model_name"
    img_dimensions = [224, 224]
    img_path = "image_path"
    command_string = get_classify_command(
    model_path, model_name, img_dimensions, img_path)
    expected_return = ("python label_image.py \\" +
        "--graph  ./model/model_name.pb \\" +
        "--labels ./model/model_name_labels.txt \\" +
        "--input_layer Placeholder \\" +
        "--output_layer final_result \\" +
        "--input_height 224 \\" +
        "--input_width 224 \\" +
        "--image image_path")
    assert(command_string) == expected_return

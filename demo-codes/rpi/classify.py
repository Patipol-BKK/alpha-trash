import tensorflow as tf
from time import sleep
from termcolor import colored

import os
import sys

# Parse arguments
args = sys.argv[1:]
path_to_retrained_labels = args[0]
path_to_retrained_graph = args[1]
path_to_testing_imgs_folder = args[2]

sess = tf.Session(config=tf.ConfigProto(
  intra_op_parallelism_threads=100))
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
def classify(name):
    print("Clasifying...")
    image_path = name
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()


    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile("path_to_retrained_labels")]
                       
    with tf.gfile.FastGFile("path_to_retrained_graph", 'rb') as f:
     
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]


        result = label_lines[predictions[0].argmax()]
        return result

if __name__ == "__main__":
    for filename in os.listdir(path_to_testing_imgs_folder):
        print("\n")
        print(filename,classify(os.path.join(path_to_testing_imgs_folder,filename)))
        print("\n")
        

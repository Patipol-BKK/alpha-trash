from time import sleep

import tensorflow as tf

import os



root_dir = os.path.join(os.getcwd(),'tf_files')

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

    

label_lines = [line.rstrip() for line 

    in tf.gfile.GFile(os.path.join(root_dir,'retrained_labels.txt'))]



with tf.gfile.FastGFile(os.path.join(root_dir,"retrained_graph.pb"), 'rb') as f:

    graph_def = tf.GraphDef()

    graph_def.ParseFromString(f.read())

    _ = tf.import_graph_def(graph_def, name='')



def classify():

    image_path = "image.jpeg"



    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    with tf.Session() as sess:



        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        # return: Tensor("final_result:0", shape=(?, 4), dtype=float32); stringname definiert in retrain.py, zeile 1064 



        predictions = sess.run(softmax_tensor, \

                 {'DecodeJpeg/contents:0': image_data})

        # gibt prediction values in array zuerueck:

        

        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        # sortierung; circle -> 0, plus -> 1, square -> 2, triangle -> 3; array return bsp [3 1 2 0] -> sortiert nach groesster uebereinstimmmung



        # output

        '''for node_id in top_k:

            human_string = label_lines[node_id]

            score = predictions[0][node_id]

            print('%s (score = %.5f)' % (human_string, score))'''
        if label_lines[predictions[0].argmax()] == "plastic":
            type_ = "Recycle"
            sub_type = "Plastic"
        elif label_lines[predictions[0].argmax()] == "metal":
            type_ = "Recycle"
            sub_type = "Metal"
        elif label_lines[predictions[0].argmax()] == "paper":
            type_ = "Recycle"
            sub_type = "Paper"
        elif label_lines[predictions[0].argmax()] == "organic":
            type_ = "Organic"
            sub_type = "main"
        elif label_lines[predictions[0].argmax()] == "danger":
            type_ = "Danger"
            sub_type = "main"
        else:
            type_ = "General"
            sub_type = "main"
        result = {"type":type_, "sub_type":sub_type, "score":predictions[0][predictions[0].argmax()]}

        return result


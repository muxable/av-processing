import av
import sys
import numpy as np
import PIL
import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file("model/pipeline.config")
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore('model/ckpt-7').expect_partial()

category_index = label_map_util.create_category_index_from_labelmap('model/label_map.pbtxt')

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def main():
    
    source = av.open("pipe:", format="avi", mode="r")
    source_v = source.streams.video[0]
    source_a = source.streams.audio[0]
    

    sink = av.open("pipe:", format="avi", mode="w")
    sink_v = sink.add_stream(template=source_v)
    sink_a = sink.add_stream(template=source_a)

    for packet in source.demux():
        if packet is None:
            continue
        for frame in packet.decode():
            index = frame.index
        
            if packet.stream.type == 'video':
                
                image_np = frame.to_ndarray()
                input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
                detections = detect_fn(input_tensor)

                num_detections = int(detections.pop('num_detections'))
                detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
                detections['num_detections'] = num_detections

                detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

                label_id_offset = 1
                image_np_with_detections = image_np.copy()

                viz_utils.visualize_boxes_and_labels_on_image_array(image_np_with_detections, detections['detection_boxes'],detections['detection_classes']+label_id_offset, detections['detection_scores'],category_index,use_normalized_coordinates=True,max_boxes_to_draw=5,min_score_thresh=.96,agnostic_mode=False)

                cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                  cv2.destroyAllWindows()
                  break
                packet.stream = sink_v
            else:
                packet.stream = sink_a

            sink.mux(packet)
    sink.close()

if __name__ == '__main__':
    main()
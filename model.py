# -*- coding: utf-8 -*-
"""Covid.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/131-qY8LQq0VqI3p4JF3qe-580niUcfZ3
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model

test_tfrecord = 'XRay_test.tfrecords'
img_size = 224
batch_size = 32


def build_test_tfrecord(test_filenames):  # Generate TFRecord of test set
    with tf.io.TFRecordWriter(test_tfrecord) as writer:
        image = open(test_filenames, 'rb').read()

        feature = {
            'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image])),
        }

        example = tf.train.Example(features=tf.train.Features(feature=feature))
        writer.write(example.SerializeToString())


def _parse_example(example_string):
    feature_description = {
        'image': tf.io.FixedLenFeature([], tf.string),
    }

    feature_dict = tf.io.parse_single_example(example_string, feature_description)
    feature_dict['image'] = tf.io.decode_png(feature_dict['image'], channels=3)
    feature_dict['image'] = tf.image.resize(feature_dict['image'], [img_size, img_size]) / 255.0
    return feature_dict['image']


def get_test_dataset(test_tfrecord):
    raw_test_dataset = tf.data.TFRecordDataset(test_tfrecord)
    test_dataset = raw_test_dataset.map(_parse_example)

    return test_dataset


def data_Preprocessing(test_dataset):
    test_dataset = test_dataset.batch(batch_size)
    test_dataset = test_dataset.prefetch(tf.data.experimental.AUTOTUNE)

    return test_dataset


def test(test_dataset):
    model = load_model('./mymodel.h5')
    predIdxs = model.predict(test_dataset)
    predIdxs = np.argmax(predIdxs, axis=1)
    return predIdxs


def runModel(imgPath):
    build_test_tfrecord(imgPath)

    test_dataset = get_test_dataset(test_tfrecord)
    test_dataset = data_Preprocessing(test_dataset)

    return getStrType(int(test(test_dataset)[0]))


def getStrType(resultInt):
    if resultInt == 0:
        return 'COVID'
    if resultInt == 1:
        return 'NORMAL'
    if resultInt == 2:
        return 'PNEUMONIA'
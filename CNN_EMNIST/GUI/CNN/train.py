# -*- coding: utf-8 -*-
#引入库函数
import os
from tensorflow.python.keras.utils.data_utils import get_file
import gzip
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers,models
import matplotlib.pyplot as plt


def load_localData():
    path = r'C:\Users\Charlie\Downloads\CNN_EMNIST\GUI\letters'
    files = ['emnist-letters-train-labels-idx1-ubyte.gz', 'emnist-letters-train-images-idx3-ubyte.gz',
             'emnist-letters-test-labels-idx1-ubyte.gz', 'emnist-letters-test-images-idx3-ubyte.gz']
    paths = []
    for fname in files:
        paths.append(get_file(fname, origin=None, cache_dir=path + fname, cache_subdir=path))
    with gzip.open(paths[0], 'rb') as lbpath:
        y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)
    with gzip.open(paths[1], 'rb') as imgpath:
        x_train = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28)
    with gzip.open(paths[2], 'rb') as lbpath:
        y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)
    with gzip.open(paths[3], 'rb') as imgpath:
        x_test = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(y_test), 28, 28)
    return x_train, y_train, x_test, y_test
train_images,train_labels,test_images,test_labels = load_localData()
#print(test_labels.shape)

#CNN 模型框架
class CNN(object):
    def __init__(self):
        model = models.Sequential()
        #第一层卷积
        model.add(layers.Conv2D(32,(5,5),activation = 'relu',input_shape=(28,28,1),strides=(1,1)))
        model.add(layers.MaxPooling2D((2,2),padding='valid'))
        #第二层卷积
        model.add(layers.Conv2D(64,(5,5),activation='relu', strides=1))
        model.add(layers.MaxPooling2D((2,2),padding='valid'))
        #第三层卷积
       # model.add(layers.Conv2D(32,(3,3),activation = 'relu'))
       # model.add(layers.MaxPooling2D((2, 2), padding='valid'))
        model.add(layers.Flatten())
        model.add(layers.Dropout(0.25))
        model.add(layers.Dense(1024,activation = 'relu'))
      #  model.add(layers.Dropout(0.25))
        model.add(layers.Dense(27,activation = 'softmax'))
        model.summary()
        self.model = model

class DataSource(object):
    def __init__(self):
 
        train_images,train_labels,test_images,test_labels = load_localData()
        train_images = train_images.reshape((124800,28,28,1))
        test_images = test_images.reshape((20800,28,28,1))
        #像素映射到 0 - 1 之间
        train_images,test_images = train_images/255.0,test_images/255.0

        self.train_images,self.train_labels = train_images , train_labels
        self.test_images,self.test_labels = test_images,test_labels

class Train:
    def __init__(self):
        self.cnn = CNN()
        self.data = DataSource()
        
    def train(self):
        check_path = './ckpt/cp-{epoch:04d}.ckpt'
        #period 每隔5epoch保存一次        
        save_model_cb = tf.keras.callbacks.ModelCheckpoint(check_path,save_weights_only = True ,verbose = 1,period = 5)
        
        self.cnn.model.compile(optimizer = 'adam',
                               loss = 'sparse_categorical_crossentropy',
                               metrics = ['accuracy'])
        self.cnn.model.fit(self.data.train_images,self.data.train_labels,epochs=5,callbacks=[save_model_cb])
        
        test = self.cnn.model.evaluate(self.data.test_images,self.data.test_labels,verbose = 0)
        print("准确率：%.4f,共测试了%d张图片" % (test[1],len(self.data.test_labels)))
        
if __name__ == "__main__":
    app = Train()
    app.train()
#cek versi tensorflow
import tensorflow as tf
print(tf.__version__)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
%matplotlib inline
import seaborn as sns

!wget --no-check-certificate \
https://github.com/fadillarizalul/capstone-dicoding-sbuah/raw/main/dataset/3-fruits.zip \
  -O fruit.zip
  
!unzip /content/fruit.zip

import os
 #lokasi direktori dasar
dir_base ='/content/3-fruits'
os.listdir(dir_base)
print(os.listdir(dir_base))

#hitung jumlah file per direktori
fresh_banana = len(os.listdir('/content/3-fruits/fresh banana'))
fresh_mango = len(os.listdir('/content/3-fruits/fresh mango')) 
fresh_orange = len(os.listdir('/content/3-fruits/fresh orange')) 
rotten_banana = len(os.listdir('/content/3-fruits/rotten banana'))
rotten_mango = len(os.listdir('/content/3-fruits/rotten mango'))
rotten_orange = len(os.listdir('/content/3-fruits/rotten orange'))

print("Amount of fresh banana images:", fresh_banana)
print("Amount of fresh mango images:", fresh_mango)
print("Amount of fresh orange images:", fresh_orange)
print("Amount of rotten banana images:", rotten_banana)
print("Amount of rotten mango images:", rotten_mango)
print("Amount of rotten orange images:", rotten_orange)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
 
train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=0.2,
                    width_shift_range=0.2,
                    height_shift_range=0.2, 
                    horizontal_flip=True,
                    shear_range = 0.2,
                    zoom_range=0.2,
                    fill_mode = 'wrap',
                    validation_split=0.2
                    )

train_generator = train_datagen.flow_from_directory(
        dir_base, # direktori data base
        target_size=(150, 100),  # mengubah resolusi seluruh gambar menjadi 150x100 piksel
        batch_size=4,
        color_mode='rgb',
        subset='training',
        # klasifikasi > 2 kelas maka menggunakan class_mode = 'categorical'
        class_mode="categorical"
        )
 
validation_generator = train_datagen.flow_from_directory(
        dir_base, # direktori data base
        target_size=(150, 100), # mengubah resolusi seluruh gambar menjadi 150x100 piksel
        batch_size=4,
        color_mode='rgb',
        subset='validation', 
        # klasifikasi > 2 kelas maka menggunakan class_mode = 'categorical'
        class_mode='categorical'
        )
from tensorflow.keras.applications import MobileNetV2
# get base models
base_model = MobileNetV2(
    input_shape=(150,150,3),
    include_top=False,
    weights='imagenet',
    classes=2,
)

# pre-trained model
from tensorflow.keras import layers,Sequential
from tensorflow.keras.models import Model

num_class = 6

#Adding custom layers
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
x = layers.Dense(1024, activation="relu")(x)
predictions = layers.Dense(num_class, activation="softmax")(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Model Architecture
from tensorflow.keras.layers import Input
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications import ResNet152V2

classes = 6

model = tf.keras.models.Sequential([
    MobileNetV2(include_top=False, weights='imagenet', classes=classes, input_tensor=Input(shape=(150, 150, 3))),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(6, activation='softmax')
])
model.layers[0].trainable = False
model.summary()

from tensorflow.keras.optimizers import RMSprop
# compile model dengan 'adam' optimizer loss function 'categorical_crossentropy' 
model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

#callback
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.95 and logs.get('val_accuracy')>0.95):
      print("\n akurasi telah mencapai >95%!")
      self.model.stop_training = True
callbacks = myCallback()

# latih model dengan model.fit 
history = model.fit(
      train_generator,
      steps_per_epoch=12,  # berapa batch yang akan dieksekusi pada setiap epoch
      epochs= 100, # tambahkan eposchs jika akurasi model belum optimal
      validation_data=validation_generator, # menampilkan akurasi pengujian data validasi
      validation_steps=5,  # berapa batch yang akan dieksekusi pada setiap epoch
      verbose=2,
      callbacks=[callbacks]
      )

import tensorflow as tf
from tensorflow import keras
from keras.datasets import fashion_mnist
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten
from keras.optimizers import SGD
import numpy as np
import sys
from keras.models import Model
from keras import backend as K
from tqdm import tqdm
from keras import Input
from tensorflow.keras import layers

np.set_printoptions(threshold=sys.maxsize)

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
X_train = X_train.reshape(X_train.shape[0],28,28,1)
X_test = X_test.reshape(X_test.shape[0],28,28,1)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# convert from integers to floats
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
# normalize to range 0-1
X_train = X_train / 255.0
X_test = X_test / 255.0

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))
# compile model
opt = SGD(lr=0.01, momentum=0.9)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

hist = model.fit(X_train, y_train, validation_split=0.3, epochs=1,shuffle=True)
accuracy = model.evaluate(X_test, y_test)
print("Accuracy: ",accuracy)
'''
probability = model.predict(X_test,verbose=1)


print("----------------Probability----------------------")
print(probability)
print("--------------------------------------------------")

layer_name = 'max_pooling2d'
intermediate_layer_model = Model(inputs=model.input,
                                outputs=model.get_layer(layer_name).output)
intermediate_output = intermediate_layer_model(X_test)
print("---------------------------Pooling layer feature vector---------------------------------")
print(intermediate_output)
print("----------------------------------------------------------------------------------------")
'''
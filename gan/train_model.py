import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))
    )
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import argparse
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import time
import datetime
import PIL

from gan.generative_network import make_generator_model
from gan.discriminative_network import make_discriminator_model
from util.program import Program
from util.progress_bar import ProgressBar
from util.args_util import str2bool
from util.image_utils import normalize

class TrainModel(Program):

    def run(self):
        super().run()
        query = args['query']
        BUFFER_SIZE = args['buffer_size']
        BATCH_SIZE = args['batch_size']
        LEARNING_RATE = args['learning_rate']
        EPOCHS = args['epochs']
        NOISE_DIM = args['noise_dim']
        NUM_EXAMPLES_TO_GENERATE = args['example_size']

        options = os.listdir('../data/loaded/' + query)
        ind = -1
        if len(options) == 1:
            ind = 0
        else:
            for i, option in enumerate(options):
                print('({}) {}'.format(i, option))
            ind = input('Enter your option index: ')
            while not ind.isdigit() or int(ind) < 0 or int(ind) >= len(options):
                ind = input('Please enter a valid option: ')
            ind = int(ind)
        loaded_file = '../data/loaded/' + query + '/' + options[ind]
        
        if not os.path.exists('../models/' + query):
            os.mkdir('../models/' + query)
        if not os.path.exists('../models/' + query + '/' + options[ind]):
            os.mkdir('../models/' + query + '/' + options[ind])
        if not os.path.exists('../generated/' + query):
            os.mkdir('../generated/' + query)
        if not os.path.exists('../generated/' + query + '/' + options[ind]):
            os.mkdir('../generated/' + query + '/' + options[ind])

        images = np.load(loaded_file).astype(np.float32)
        img_res = images.shape[1:4]
        
        dataset = tf.data.Dataset.from_tensor_slices(images).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)

        generator = make_generator_model(NOISE_DIM, img_res)
        discriminator = make_discriminator_model(img_res)

        cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

        def discriminator_loss(real_output, fake_output):
            real_loss = cross_entropy(tf.ones_like(real_output), real_output)
            fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
            total_loss = real_loss + fake_loss
            return total_loss

        def generator_loss(fake_output):
            return cross_entropy(tf.ones_like(fake_output), fake_output)

        generator_optimizer = tf.keras.optimizers.Adam(LEARNING_RATE)
        discriminator_optimizer = tf.keras.optimizers.Adam(LEARNING_RATE)

        seed = tf.random.normal([NUM_EXAMPLES_TO_GENERATE, NOISE_DIM])

        @tf.function
        def train_step(images):
            noise = tf.random.normal([BATCH_SIZE, NOISE_DIM])

            with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
                generated_images = generator(noise, training=True)
            
                real_output = discriminator(images, training=True)
                fake_output = discriminator(generated_images, training=True)

                gen_loss = generator_loss(fake_output)
                disc_loss = discriminator_loss(real_output, fake_output)

            gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
            gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

            generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
            discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

            return gen_loss, disc_loss

        def generate_and_save_images(model, epoch, test_input):
            predictions = model(test_input, training=False)

            fig = plt.figure(figsize=(4,4))

            for i in range(predictions.shape[0]):
                plt.subplot(4, 4, i+1)
                plt.imshow(normalize(predictions[i, :, :, 0], input_range=(-1, 1), output_range=(0, 255)), cmap='gray')
                plt.axis('off')

            plt.savefig('./generated/{}/{}/epoch_{:04d}.png'.format(query, options[ind], epoch))
            plt.close()

        def train(dataset, epochs, progress_bar_width=80, progress_char='+', empty_char='-'):

            for epoch in range(epochs):
                start = time.time()

                gen_loss = -1
                disc_loss = -1

                cur_time = time.time()
                i = 0
                l = BUFFER_SIZE // BATCH_SIZE

                for image_batch in dataset:
                    w = i * progress_bar_width // l
                    s = int(time.time() - cur_time)
                    print('[' + progress_char * w + empty_char * (progress_bar_width - w) + ']', i, '/', l, datetime.timedelta(seconds=s), end='\r')
                    gen_loss, disc_loss = train_step(image_batch)
                    i += 1
                
                generate_and_save_images(generator, epoch + 1, seed)

                print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start), ' ' * (progress_bar_width + 10))

                generate_and_save_images(generator, epochs, seed)

        train(dataset, EPOCHS) # TODO: fix TypeError: Value passed to parameter 'input' has DataType uint8 not in list of allowed values: float16, bfloat16, float32, float64, int32 by converting to int32 in load_data

        def display_image(epoch_no):
            return PIL.Image.open('./generated/{}/{}/epoch_{:04d}.png'.format(query, options[ind], epoch_no))
        
        display_image(EPOCHS)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-l', '--log', type=str2bool, default=True, help='Whether or not the program should log anything to the console')
    parser.add_argument('-q', '--query', type=str, default='sunset', help='The search query used to find the images')
    parser.add_argument('-bf', '--buffer-size', type=int, default=100000, help='The buffer size while we are slicing the dataset into chunks')
    parser.add_argument('-ba', '--batch-size', type=int, default=256, help='The batch size while training the model')
    parser.add_argument('-lr', '--learning-rate', type=float, default=1e-4, help='The learning rate to train with')
    parser.add_argument('-e', '--epochs', type=int, default=100, help='The number of epochs to train on')
    parser.add_argument('-n', '--noise-dim', type=int, default=300, help='The noise vector\' size (which is the input to the generator)')
    parser.add_argument('-ex', '--example-size', type=int, default=8, help='The number of generated examples to display')

    args = vars(parser.parse_args())

    TrainModel(args).run()
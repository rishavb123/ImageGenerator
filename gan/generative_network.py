import tensorflow as tf

def make_generator_model(noise_dim, output_shape):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(int(output_shape[0] / 8) * int(output_shape[1] / 8) * 256, use_bias=False, input_shape=(noise_dim,)))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())

    model.add(tf.keras.layers.Reshape((int(output_shape[0] / 8), int(output_shape[1] / 8), 256)))
    assert model.output_shape == (None, int(output_shape[0] / 8), int(output_shape[1] / 8), 256)

    model.add(tf.keras.layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    assert model.output_shape == (None, int(output_shape[0] / 8), int(output_shape[1] / 8), 128)
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())

    model.add(tf.keras.layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    assert model.output_shape == (None, int(output_shape[0] / 4), int(output_shape[1] / 4), 64)
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())

    model.add(tf.keras.layers.Conv2DTranspose(32, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    assert model.output_shape == (None, int(output_shape[0] / 2), int(output_shape[1] / 2), 32)
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.LeakyReLU())

    model.add(tf.keras.layers.Conv2DTranspose(3, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    assert model.output_shape == (None, output_shape[0], output_shape[1], 3)

    return model
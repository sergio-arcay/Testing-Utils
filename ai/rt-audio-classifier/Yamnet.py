from mediapipe.tasks import python
from mediapipe.tasks.python import audio
from mediapipe.tasks.python.components import containers
import numpy as np
import time


class Yamnet:
    """ Wrapper para el modelo de clasificación de audio Yamnet.
    """

    DEFAULT_SAMPLERATE = 16000
    DEFAULT_CHANNELS = 1
    DEFAULT_CHUNKSIZE = int(DEFAULT_SAMPLERATE / 1)

    def __init__(self, tflite_path, callback=None, min_valid_score=0.5):
        self.tflite_path = tflite_path
        self.classifier_options = audio.AudioClassifierOptions(
            base_options=python.BaseOptions(model_asset_path=self.tflite_path),
            running_mode=audio.RunningMode.AUDIO_STREAM,
            max_results=5,
            score_threshold=0.0,
            result_callback=callback or self.__default_callback
        )
        # Minimum classification score in a classifier result to be accepted
        self.classifier_min_valid_score = min_valid_score
        self.classifier = audio.AudioClassifier.create_from_options(self.classifier_options)

        self.buffer_size, self.sample_rate, self.num_channels = 15600, 16000, 1
        self.__audio_buffer = containers.AudioData(self.buffer_size, containers.AudioDataFormat(self.num_channels, self.sample_rate))

    def __default_callback(self, result: audio.AudioClassifierResult, timestamp: float):
        print([f"{category.category_name}: {category.score:.2f} ({type(category.score)})"
               for category in result.classifications[0].categories
               if category.score >= self.classifier_min_valid_score])

    def __preprocess_audio_from_ndarray(self, audio_data):
        audio_normalized = (np.float32(audio_data).flatten()).reshape(-1, 1)
        self.__audio_buffer.load_from_array(audio_normalized)
        return self.__audio_buffer

    def classify_async(self, audio_data):

        # Adapt the input audio data to the format required by the classifier
        if type(audio_data) is np.ndarray:
            audio_data = self.__preprocess_audio_from_ndarray(audio_data)

        if type(audio_data) is not containers.AudioData:
            raise TypeError(f"El tipo de dato de audio_data debe ser 'numpy.ndarray' o 'containers.AudioData', no '{type(audio_data)}'.")
        self.classifier.classify_async(audio_data, round(time.time() * 1000000))


if __name__ == "__main__":

    import sounddevice as sd

    try:

        def recording_chunk_callback(indata, frames, time, status):
            yamnet.classify_async(indata)


        def classifier_result_callback(result, timestamp):
            print([f"{category.category_name}: {category.score:.2f} ({type(category.score)})" for category in
                   result.classifications[0].categories])

        yamnet = Yamnet("yamnet.tflite", callback=classifier_result_callback)

        with sd.InputStream(callback=recording_chunk_callback, channels=Yamnet.DEFAULT_CHANNELS,
                            samplerate=Yamnet.DEFAULT_SAMPLERATE,
                            blocksize=Yamnet.DEFAULT_CHUNKSIZE, dtype="float32"):
            print("Grabando...")
            input("Presiona Enter para detener la grabación...\n\n")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        print("Grabación detenida.")
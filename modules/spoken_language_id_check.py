import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier

class SLIDCheck:
    def __init__(self, p_threshold=0.5):
        self.model = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")
        self.p_threshold = p_threshold

    def load_audio(self, audio_path):
        signal, sr = torchaudio.load(audio_path)
        chunk_size = 10 * sr
        num_chunks = signal.shape[1] // chunk_size

        signal_chunks = [signal[:, i * chunk_size: (i + 1) * chunk_size] for i in range(num_chunks)]
        remaining_chunk = signal[:, num_chunks * chunk_size :]
        signal_chunks.append(remaining_chunk)
        return signal_chunks

    def predict(self, audio_path):
        signal_chunks = self.load_audio(audio_path)
        predictions = [self.model.classify_batch(signal) for signal in signal_chunks]
        predictions = [[pred[3][0].split(':')[0], pred[1].exp().item()] for pred in predictions]
        return predictions

    def __call__(self, audio_path, language_id='hi'):
        predictions = self.predict(audio_path)
        print(predictions)
        probability = sum([p for lid, p in predictions if lid==language_id]) / len(predictions)
        counts_percentage = sum([1 for lid, p in predictions if lid==language_id]) / len(predictions) * 100

        assert counts_percentage >= 70, f"Language is not as expected for file {audio_path}"
        return probability


if __name__ == "__main__":
    pass

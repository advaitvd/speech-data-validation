import wave
import os

class AudioFileCheck:
    def __init__(self, sample_rate=16000, num_channels=[1, 2]):
        self.framerate_threshold = sample_rate
        self.num_channels_threshold = num_channels

    def __call__(self, file_path):
        params = self.readfile(file_path)
        self.wavfile_corruption_check(*params)
        framerate, num_channels = params[-1], params[-2]
        self.framerate_check(file_path, framerate)
        self.channels_check(file_path, num_channels)

    def readfile(self, file_path):
        try:
            with wave.open(file_path, "rb") as wf:
                num_frames = wf.getnframes()
                sample_width = wf.getsampwidth()
                num_channels = wf.getnchannels()
                framerate = wf.getframerate()
        except wave.Error as e:
            print(f"Wave Error for file {file_path}")
            raise e

        return file_path, num_frames, sample_width, num_channels, framerate

    def framerate_check(self, file_path, framerate):
        assert framerate >= self.framerate_threshold, f"Sample rate is not as expected for {file_path}"

    def channels_check(self, file_path, num_channels):
        assert num_channels in self.num_channels_threshold, f"Number of channels are not as expected {file_path}"

    def wavfile_corruption_check(self, file_path, num_frames, sample_width, num_channels, framerate):
        # Expected file size: header (44 bytes) + data size
        expected_size = 44 + (num_frames * num_channels * sample_width)
        actual_size = os.path.getsize(file_path)
        assert expected_size == actual_size, f"Expected file size does not match actual file size for file {file_path}"


if __name__=="__main__":
    pass

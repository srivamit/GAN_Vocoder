---
language: "en"
tags:
- Tacotron2
- speechbrain
- zero-shot
- multi-speaker-tts
license: "apache-2.0"
datasets:
- LibriTTS
metrics:
- mos
---
<iframe src="https://ghbtns.com/github-btn.html?user=speechbrain&repo=speechbrain&type=star&count=true&size=large&v=2" frameborder="0" scrolling="0" width="170" height="30" title="GitHub"></iframe>
<br/><br/>


# Text-to-Speech (TTS) with Zero-Shot Multi-Speaker Tacotron2 trained on LibriTTS

**Please Note**: The current model effectively captures speaker identities. Nevertheless, the synthesized speech quality exhibits some metallic characteristics and may include artifacts like overly long pauses.
We are actively working to enhancing the model and will release updates as soon as improvements are achieved. We warmly welcome contributions from the community to collaboratively make the model even better!

This repository provides all the necessary tools for Zero-Shot Multi-Speaker Text-to-Speech (TTS) with SpeechBrain using a variation of [Tacotron2](https://arxiv.org/abs/1712.05884), extended to incorporate speaker identity information when generating speech. It is pretrained on [LibriTTS](https://www.openslr.org/60/).

The pre-trained model takes as input a short text and a reference speech sample. The model output is a mel-spectrogram corresponding to the input text with the voice characteristics of the speaker from the reference speech. One can get the final waveform by applying a vocoder (e.g., HiFIGAN) on top of the generated mel-spectrogram.

### Install SpeechBrain

```
pip install speechbrain
```

Please notice that we encourage you to read our tutorials and learn more about
[SpeechBrain](https://speechbrain.github.io).

### Perform Text-to-Speech (TTS)

The following is an example of converting text-to-speech with the speaker voice characteristics extracted from reference speech.

**Note:** 
- The model generates speech at a rate of 22050 Hz, but it's important to note that the input signal, crucial for capturing speaker identities, must be sampled at 16kHz.

```python
import torchaudio
from speechbrain.inference.TTS import MSTacotron2
from speechbrain.inference.vocoders import HIFIGAN
# Intialize TTS (mstacotron2) and Vocoder (HiFIGAN)
ms_tacotron2 = MSTacotron2.from_hparams(source="speechbrain/tts-mstacotron2-libritts", savedir="pretrained_models/tts-mstacotron2-libritts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-libritts-22050Hz", savedir="pretrained_models/tts-hifigan-libritts-22050Hz")
# Required input
REFERENCE_SPEECH = "speech_sample.wav"
INPUT_TEXT = "Mary had a little lamb"
# Running the Zero-Shot Multi-Speaker Tacotron2 model to generate mel-spectrogram
mel_outputs, mel_lengths, alignments = ms_tacotron2.clone_voice(INPUT_TEXT, REFERENCE_SPEECH)
# Running Vocoder (spectrogram-to-waveform)
waveforms = hifi_gan.decode_batch(mel_outputs)
# Save the waverform
torchaudio.save("synthesized_sample.wav", waveforms.squeeze(1).cpu(), 22050)
```

If you want to generate a random voice, you can use the following:

```python
import torchaudio
from speechbrain.inference.TTS import MSTacotron2
from speechbrain.inference.vocoders import HIFIGAN
# Intialize TTS (mstacotron2) and Vocoder (HiFIGAN)
ms_tacotron2 = MSTacotron2.from_hparams(source="speechbrain/tts-mstacotron2-libritts", savedir="pretrained_models/tts-mstacotron2-libritts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-libritts-22050Hz", savedir="pretrained_models/tts-hifigan-libritts-22050Hz")
# Required input
INPUT_TEXT = "Mary had a little lamb"
# Running the Zero-Shot Multi-Speaker Tacotron2 model to generate mel-spectrogram
mel_outputs, mel_lengths, alignments = ms_tacotron2.generate_random_voice(INPUT_TEXT)
# Running Vocoder (spectrogram-to-waveform)
waveforms = hifi_gan.decode_batch(mel_outputs)
# Save the waverform
torchaudio.save("synthesized_sample.wav", waveforms.squeeze(1).cpu(), 22050)
```


If you want to generate multiple sentences in one-shot, you can do it this way:
Note: The model internally reorders the input texts in the decreasing order of their lengths.

```python
import torchaudio
from speechbrain.inference.TTS import MSTacotron2
from speechbrain.inference.vocoders import HIFIGAN
# Intialize TTS (mstacotron2) and Vocoder (HiFIGAN)
ms_tacotron2 = MSTacotron2.from_hparams(source="speechbrain/tts-mstacotron2-libritts", savedir="pretrained_models/tts-mstacotron2-libritts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-libritts-22050Hz", savedir="pretrained_models/tts-hifigan-libritts-22050Hz")
# Required input
REFERENCE_SPEECH = "speech_sample.wav"
INPUT_TEXT = ["Welcome to the demo", "Convert text to speech"]
# Running the Zero-Shot Multi-Speaker Tacotron2 model to generate mel-spectrogram
mel_outputs, mel_lengths, alignments = ms_tacotron2.clone_voice(INPUT_TEXT, REFERENCE_SPEECH)
# Running Vocoder (spectrogram-to-waveform)
waveforms = hifi_gan.decode_batch(mel_outputs)
# Save the waverforms
for i in range(len(waveforms)):
    synthesized_audio_path = f"synthesized_sample_{i}.wav"
    torchaudio.save(synthesized_audio_path, waveforms[i].squeeze(1).cpu(), 22050)
```

### Inference on GPU
To perform inference on the GPU, add  `run_opts={"device":"cuda"}`  when calling the `from_hparams` method.

### Training
The model was trained with SpeechBrain.
To train it from scratch follow these steps:
1. Clone SpeechBrain:
```bash
git clone https://github.com/speechbrain/speechbrain/
```
2. Install it:
```bash
cd speechbrain
pip install -r requirements.txt
pip install -e .
```
3. Run Training:
```bash
cd recipes/LibriTTS/TTS/mstacotron2/
python train.py hparams/train.yaml --data_folder=/path/to/libritts_data --device=cuda:0 --max_grad_norm=1.0
```
The training logs will be available here in the future.

### Limitations
The SpeechBrain team does not provide any warranty on the performance achieved by this model when used on other datasets.

# **About SpeechBrain**
- Website: https://speechbrain.github.io/
- Code: https://github.com/speechbrain/speechbrain/
- HuggingFace: https://huggingface.co/speechbrain/


# **Citing SpeechBrain**
Please, cite SpeechBrain if you use it for your research or business.

```bibtex
@misc{speechbrain,
  title={{SpeechBrain}: A General-Purpose Speech Toolkit},
  author={Mirco Ravanelli and Titouan Parcollet and Peter Plantinga and Aku Rouhe and Samuele Cornell and Loren Lugosch and Cem Subakan and Nauman Dawalatabad and Abdelwahab Heba and Jianyuan Zhong and Ju-Chieh Chou and Sung-Lin Yeh and Szu-Wei Fu and Chien-Feng Liao and Elena Rastorgueva and François Grondin and William Aris and Hwidong Na and Yan Gao and Renato De Mori and Yoshua Bengio},
  year={2021},
  eprint={2106.04624},
  archivePrefix={arXiv},
  primaryClass={eess.AS},
  note={arXiv:2106.04624}
}
```
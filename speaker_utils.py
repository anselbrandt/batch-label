import nemo.collections.asr as nemo_asr
import logging
import random
import os

logging.getLogger("nemo_logger").setLevel(logging.ERROR)

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(
    "nvidia/speakerverification_en_titanet_large"
)


def reference_likleyhood(reference, samples):
    results = 0
    for sample in samples:
        try:
            result = speaker_model.verify_speakers(reference, sample)
            results = results + result
        except:
            print(sample)
    return results / 10


def getSpeakers(wavFilePaths):
    return list(
        set(
            [
                os.path.basename(filepath).split("_")[4].replace(".wav", "")
                for filepath in wavFilePaths
            ]
        )
    )


def getSpeakerLabels(reference, wavFiles, hosts):
    primary, secondary = hosts
    speakers = getSpeakers(wavFiles)
    speakerNames = {}
    for speaker in speakers:
        speakerWavs = [file for file in wavFiles if speaker in file]
        randomized = random.sample(speakerWavs, len(speakerWavs))[:10]
        result = reference_likleyhood(reference, randomized)
        speakerName = primary if result > 0.5 else secondary
        speakerNames[speaker] = speakerName
    return speakerNames

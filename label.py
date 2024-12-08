import os
import logging

from utils import (
    getTranscriptFiles,
    srt_to_transcript,
    transcript_to_srt,
    getTextTranscript,
    labelTextTranscript,
)

from speaker_utils import getSpeakerLabels

isCleanAudio = True if os.path.isdir("clean_splitwavs") else False

ROOT = os.getcwd()
labeledDir = os.path.join(ROOT, "clean_labeled" if isCleanAudio else "labeled")
os.makedirs(labeledDir, exist_ok=True)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(os.path.join(labeledDir, "labels.txt")),
        stream_handler,
    ],
)

transcriptDir = os.path.join(ROOT, "clean_output" if isCleanAudio else "output")
wavsDir = os.path.join(ROOT, "clean_splitwavs" if isCleanAudio else "splitwavs")
showDirs = os.listdir(transcriptDir)

for dir in showDirs:
    os.makedirs(os.path.join(labeledDir, dir), exist_ok=True)

hosts = {
    "rotl": ("John", "Merlin"),
    "roadwork": ("John", "Dan"),
    "omnibus": ("John", "Ken"),
}
reference = os.path.join(ROOT, "john.wav")
transcriptFiles = getTranscriptFiles(transcriptDir)

for filepath, showname, filename in transcriptFiles:
    episode = filename.split("_-_")[0] if "_-_" in filename else filename.split(".")[0]
    showDir = os.path.join(wavsDir, showname, episode)
    wavFiles = [os.path.join(showDir, file) for file in os.listdir(showDir)]
    showhosts = hosts[showname]
    speakerLabels = getSpeakerLabels(reference, wavFiles, showhosts)
    logging.info(f"{showname}|{episode}|{",".join(list(speakerLabels.values()))}")
    textFilepath = filepath.replace(".srt", ".txt")
    textTranscript = getTextTranscript(textFilepath)
    labeledText = labelTextTranscript(textTranscript, speakerLabels)
    textOutpath = os.path.join(labeledDir, showname, filename.replace(".srt", ".txt"))
    t = open(textOutpath, "w")
    t.write("\n\n".join(labeledText))
    t.close
    transcript = srt_to_transcript(filepath)
    labeled = [
        (idx, start, end, speakerLabels[speaker], speech)
        for idx, start, end, speaker, speech in transcript
    ]
    srt = transcript_to_srt(labeled)
    outpath = os.path.join(labeledDir, showname, filename)
    f = open(outpath, "w")
    f.write(srt)
    f.close()

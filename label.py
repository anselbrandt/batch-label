import os

from utils import (
    getTranscriptFiles,
    srt_to_transcript,
    transcript_to_srt,
    getTextTranscript,
    labelTextTranscript,
)

from speaker_utils import getReferenceLabel, getSpeakerLabels

ROOT = os.getcwd()
transcriptDir = os.path.join(ROOT, "output")
wavsDir = os.path.join(ROOT, "splitwavs")
labeledDir = os.path.join(ROOT, "labeled")
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
    episode = filename.split("_-_")[0]
    showDir = os.path.join(wavsDir, showname, episode)
    wavFiles = [os.path.join(showDir, file) for file in os.listdir(showDir)]
    referenceLabel = getReferenceLabel(reference, wavFiles)
    inferredLabels = getSpeakerLabels(referenceLabel, hosts[showname])
    textFilepath = filepath.replace(".srt", ".txt")
    textTranscript = getTextTranscript(textFilepath)
    labeledText = labelTextTranscript(textTranscript, inferredLabels)
    textOutpath = os.path.join(labeledDir, showname, filename.replace(".srt", ".txt"))
    t = open(textOutpath, "w")
    t.write("\n\n".join(labeledText))
    t.close
    transcript = srt_to_transcript(filepath)
    labeled = [
        (idx, start, end, inferredLabels[speaker], speech)
        for idx, start, end, speaker, speech in transcript
    ]
    srt = transcript_to_srt(labeled)
    outpath = os.path.join(labeledDir, showname, filename)
    f = open(outpath, "w")
    f.write(srt)
    f.close()

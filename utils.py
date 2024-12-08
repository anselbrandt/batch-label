from datetime import timedelta
import os

ROOT = os.getcwd()


def getTranscriptFiles(transcriptDir):
    dirs = [
        (os.path.join(transcriptDir, dir), dir)
        for dir in sorted(os.listdir(transcriptDir))
        if ".DS_Store" not in dir
    ]

    files = [
        (os.path.join(dir, file), showname, file)
        for dir, showname in dirs
        for file in sorted(os.listdir(dir))
        if ".srt" in file
        if ".DS_Store" not in file
    ]
    return files


def timeToSeconds(time):
    hhmmss = time.split(",")[0]
    ms = time.split(",")[1]
    hh = hhmmss.split(":")[0]
    mm = hhmmss.split(":")[1]
    ss = hhmmss.split(":")[2]
    seconds = timedelta(
        hours=int(hh), minutes=int(mm), seconds=int(ss), milliseconds=int(ms)
    )
    return seconds.total_seconds()


def srt_to_transcript(filepath):
    srt = open(filepath, encoding="utf-8-sig").read().replace("\n\n", "\n").splitlines()
    grouped = [srt[i : i + 3] for i in range(0, len(srt), 3)]
    transcript = [
        (
            idx,
            timeToSeconds(times.split(" --> ")[0]),
            timeToSeconds(times.split(" --> ")[1]),
            speech.split(": ")[0],
            speech.split(": ")[1],
        )
        for idx, times, speech in grouped
        if timeToSeconds(times.split(" --> ")[1])
        > timeToSeconds(times.split(" --> ")[0])
    ]
    return transcript


def secondsToTime(seconds):
    result = timedelta(seconds=seconds)
    string = (
        str(timedelta(seconds=result.seconds))
        + ","
        + str(int(result.microseconds / 1000))
    )
    return string


def transcript_to_srt(transcript):
    lines = [
        f"{idx}\n{secondsToTime(start)} --> {secondsToTime(end)}\n{speaker}: {speech}"
        for idx, start, end, speaker, speech in transcript
    ]
    return "\n\n".join(lines)


def getTextTranscript(filepath):
    file = open(filepath, encoding="utf-8-sig").read().splitlines()

    lines = [line.rstrip() for line in file if line != ""]
    return lines


def labelTextTranscript(textTranscript, labels):
    labeled = []
    for line in textTranscript:
        speaker = line.split(":")[0]
        if not line.split(":")[1].isspace() and len(line.split(":")) > 1:
            labeled.append(line.replace(speaker, labels[speaker]))
    return labeled

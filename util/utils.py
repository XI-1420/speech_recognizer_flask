import math


def total_words(data):
    words = data.split()
    count = 0
    for word in words:
        if word != "." and word != ",":
            count = count + 1
    return count


def read_file(filename):
    try:
        file = open(filename, "rt")
        data = file.read()
        return data
    except FileNotFoundError:
        print(f"No file found with name {filename}")


def rate_speech_on_fluency(words_count, duration):

    avg_words = avg_spoken_words_count(duration)
    print("Average words spoken should be", str(avg_words))

    if avg_words <= 50:
        if abs(avg_words - words_count) <= 5:
            return 1
        elif words_count >= avg_words+25 or words_count <= avg_words-25:
            return 0
        elif words_count >= avg_words+15 or words_count <= avg_words-15:
            return 0.5
        elif words_count >= avg_words+10 or words_count <= avg_words-10:
            return 0.7
        else:
            return 0.8
    elif avg_words <= 100:
        if abs(avg_words-words_count) <= 10:
            return 1
        elif words_count >= avg_words+40 or words_count <= avg_words-40:
            return 0
        elif words_count >= avg_words+30 or words_count <= avg_words-30:
            return 0.5
        elif words_count >= avg_words+20 or words_count <= avg_words-20:
            return 0.7
        else:
            return 0.8
    else:
        if abs(avg_words-words_count) <= 15:
            return 1
        elif words_count >= avg_words+50 or words_count <= avg_words-50:
            return 0
        elif words_count >= avg_words+40 or words_count <= avg_words-40:
            return 0.5
        elif words_count >= avg_words+30 or words_count <= avg_words-30:
            return 0.7
        else:
            return 0.8


def avg_spoken_words_count(seconds):
    total_seconds = 60
    avg_words_per_minute = 150
    avg_spoken_words = total_seconds / seconds
    return math.floor(avg_words_per_minute / avg_spoken_words)

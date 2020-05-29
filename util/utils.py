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


def avg_spoken_words_count(seconds):
    total_seconds = 60
    avg_words_per_minute = 150
    avg_spoken_words = total_seconds / seconds
    return avg_words_per_minute / avg_spoken_words


def rate_speech_on_fluency(words_count):
    avg_words = 45
    if abs(avg_words - words_count) <= 5:
        return 1
    elif words_count >= 70 or words_count <= 30:
        return 0
    elif words_count >= 60 or words_count <= 35:
        return 0.5
    elif words_count >= 55 or words_count <= 40:
        return 0.7

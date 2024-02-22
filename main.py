import os
import json
import math
from lexer import Lexer


def read_files(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(directory + filename)
    return files


def print_top_n(tf_index: dict[str, dict[str, dict[str, int | float]]], n: int):
    top_words_files = {}
    for file_name, words in tf_index.items():
        top_n_words = sorted(words.items(), key=lambda x: x[1]["tf-idf"], reverse=True)[
            :n
        ]
        top_words_files[file_name] = {key: value for key, value in top_n_words}
    with open("top_words_files.json", "w") as json_file:
        json.dump(top_words_files, json_file, indent=4)


def main():
    directory = "./text-files/"
    files = read_files(directory)
    N: int = len(files)
    tf_index: dict[str, dict[str, dict[str, int | float]]] = {}
    # print(files)
    for file in files:
        file = open(file, "r")
        read: str = file.read()
        lexer: Lexer = Lexer(read)
        token: str | None = lexer.next_token()
        tf: dict[str, int] = {}
        max: int = 0

        while token is not None:
            if token in tf:
                tf[token] += 1
            else:
                tf[token] = 1

            if tf[token] > max:
                max = tf[token]

            token = lexer.next_token()

        stats = sorted(tf.items(), key=lambda x: x[1], reverse=True)
        tf_index[file.name] = {
            key: {"count": value, "tf": round(value / max, 4)} for key, value in stats
        }

    steps = 0
    for file_name, words in tf_index.items():
        for word, stats in words.items():
            occurences = 0
            for file in files:
                steps += 1
                if word in tf_index[file] and "df" in tf_index[file][word]:
                    occurences = tf_index[file][word]["df"]
                    break
                if word in tf_index[file]:
                    occurences += 1
            tf_index[file_name][word]["df"] = occurences
            tf_index[file_name][word]["idf"] = round(math.log(N / occurences), 4)
            tf_index[file_name][word]["tf-idf"] = round(
                tf_index[file_name][word]["tf"] * tf_index[file_name][word]["idf"], 4
            )

    with open("tf-idf.json", "w") as json_file:
        json.dump(tf_index, json_file, indent=4)

    print_top_n(tf_index, 10)


if __name__ == "__main__":
    main()

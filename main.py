# ------------------------
# LETTER FREQUENCY PROJECT
# ------------------------
# This project builds a report of the number of
# times each letter of the alphabet appears in each
# word from a list of the most commonly used words
# in the English language.

import csv
import logging
from collections import Counter
from string import ascii_lowercase

import pandas as pd

log = logging.getLogger("letter counts")
logging.basicConfig(level=logging.INFO)


def full_range(start, stop):
    return range(start, stop + 1)


def export_to_csv(dist):
    # exports the results to a csv file
    # dist is in the form:
    # {'a': [(0, 1), (1, 2), (2, 1)], 'b': [(0, 2), (1, 1), (3, 1)] etc..}

    if len(dist) == 0:
        log.warning("data missing or incomplete - nothing exported")
        return

    try:
        file_name = "results.csv"
        max_columns = 6 # assume no letter appears more than 6 times in a word
        with open(file_name, mode='w', newline='', encoding="utf-8")as f:
            export_writer = csv.writer(f, delimiter=',')

            # create header row
            header = ["character"]
            for n in full_range(0, max_columns):
                header.append("count" + str(n))
            export_writer.writerow(header)

            # output the values
            for key in dist:
                frequency = Frequency(dist[key])
                values = [key]
                for n in full_range(0, max_columns):
                    values.append(frequency.dict[n] if n in frequency.dict else 0)
                export_writer.writerow(values)

            log.info("export complete")
    except PermissionError:
        log.error("unable to create export file")


def convert(tuple_list):
    # converts a list of tuples to a dictionary
    di = dict(tuple_list)
    return di


class Frequency:
    # helper class to help process the list of tuples:
    # format: [(0,1),(1,2),(2,1)]
    def __init__(self, tuple_list):
        self.tuple_list = tuple_list
        self.dict = convert(tuple_list)


def get_letter_distribution(letter, word_list):
    # produce a list of the counts of the 'letter' in each word in the word_list
    # e.g [1,0,2,1] for the letter 'h' in ['hello','bye','healthy','hope]
    count_list = [str(w).count(letter) for w in word_list]

    # create a frequency distribution of those counts
    # e.g [(0,1),(1,2),(2,1)]
    dist = Counter(count_list)

    return dist


def get_words_from_file_as_list(filename, column_name):
    words_df = pd.read_csv(filename)
    return words_df[column_name].tolist()


def generate_report(filename, column_name):
    # main method which creates the report by loop through all
    # characters of the alphabet and counting how many times they
    # appear in each of the words in the 'filename' under 'column_name'

    dist = {}
    word_list = get_words_from_file_as_list(filename, column_name)
    if word_list:
        for character in ascii_lowercase:
            distribution = get_letter_distribution(character, word_list)
            dist[character] = sorted(distribution.items())

    export_to_csv(dist)


if __name__ == '__main__':
    generate_report("english_words.csv", "english_words")

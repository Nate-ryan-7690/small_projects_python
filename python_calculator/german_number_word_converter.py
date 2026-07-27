# Small conversion tool to parse the German text form of numbers and convert them into Integers 
import re 

#-----------------------------------------------------------------------------------------------------------------------------------
# Lookup Tables
#-----------------------------------------------------------------------------------------------------------------------------------
ones_teens = {"null": 0, "eins": 1,"ein": 1,"eine": 1, "zwei": 2, "drei": 3, "vier": 4, "fuenf": 5, "sechs": 6, 
              "sieben": 7, "acht": 8, "neun": 9, "elf": 11, "zwoelf": 12, "dreizehn": 13,
              "vierzehn": 14, "fuenfzehn": 15, "sechzehn": 16, "siebzehn": 17,
              "achtzehn": 18, "neunzehn": 19}

tens = {"zehn": 10, "zwanzig": 20, "dreissig": 30, "vierzig": 40, "fuenfzig": 50, 
        "sechzig": 60, "siebzig": 70, "achtzig": 80, "neunzig": 90}

big_units = {"hundert": 100, "tausend": 1000, "million": 1000000,"millionen": 1000000, "milliarde": 1000000000, "milliarden": 1000000000}

calc_int = {**ones_teens, **tens, **big_units}

BIG_UNIT_KEYWORDS = ("tausend", "million", "millionen", "milliarde", "milliarden")   

#----------------------------------------------------------------------------------------------------------------------------------
# Step 1: normalize raw text (umlauts, case) so it matches dict keys
#----------------------------------------------------------------------------------------------------------------------------------

def normalize(text: str):
    text = text.lower()
    text = (text.replace("ü","ue")
                .replace("ö","oe")
                .replace("ä","ae")
                .replace("ß","ss"))
    text = re.sub(r"[.,;:!?()\[\]{}\"']", " ", text)
    return text

#-----------------------------------------------------------------------------------------------------------------------------------
# Step 2: split normalized text into word-chunks on the German keywords
#-----------------------------------------------------------------------------------------------------------------------------------

def split_text(text: str):
    text_to_int = re.split(r"(milliarde(?:n)?|million(?:en)?|tausend|hundert|und)", text)
    text_to_int = [chunk.strip() for chunk in text_to_int]
    return text_to_int

#-----------------------------------------------------------------------------------------------------------------------------------
# Step 3: the whole pipeline as ONE reusable function - text in, int out
#-----------------------------------------------------------------------------------------------------------------------------------

def convert_to_int(text: str):
    text = normalize(text)

    sign = 1
    if text.startswith("minus "):
        sign = -1
        text = text.removeprefix("minus ").strip()

    words = split_text(text)

    total = 0
    pending = 0

    for word in words:
        if word == "und" or word == "":
            continue
        elif word == "hundert":
            if pending == 0:
                pending = 1
            pending = pending * calc_int[word]
        elif word in BIG_UNIT_KEYWORDS:
            if pending == 0:
                pending = 1
            pending = pending * calc_int[word]
            total += pending
            pending = 0
        else:
            pending += calc_int[word]
    total += pending
    return sign * total

#-----------------------------------------------------------------------------------------------------------------------------------
# Entry point: process a list of phrases if given, otherwise ask for a phrase
#-----------------------------------------------------------------------------------------------------------------------------------
#            
def main():    
    num_list = []
    int_list = []
    failed_positions_list = []
    if num_list:
        for i, phrase in enumerate(num_list):
            try:
                value = convert_to_int(str(phrase))
                # Print function left in to verify small number batches in testing: remove before large list conversions
                # print(f"{phrase!r} -> {value}")
                int_list.append(value)
            except KeyError:
                int_list.append("FAIL")
                failed_positions_list.append(i)
        if failed_positions_list:
            print(f"Unrecognized phrases at position(s): {failed_positions_list}")
    else:
        while True:
            text = input(str("Number in text:  "))
            try:
                value = convert_to_int(text)
                break
            except KeyError as e:
                print(f"{e} was not recognized as a valid German number word, please try again.")
        print(f"{text!r} -> {value}")
        int_list.append(value)
    return int_list

if __name__ == "__main__":
    int_list = main()
    print(int_list)
import config
import collections
import time
import datetime
import pyrebase
import math
import random

firebase = pyrebase.initialize_app(config.firebase_config)
    

def main():

    markov_chain = dict()
    markov_chain['~'] = []

    word_count = 0
    total_comments = 0

    print("Fetching comments from db")

    # get past week of comments
    db = firebase.database()
    dt = datetime.datetime.fromtimestamp(time.mktime(time.gmtime()))
    for i in range(1,8):
        new_dt = dt - datetime.timedelta(days=i)
        new_dt = "{}-{}-{}".format(new_dt.month, new_dt.day, new_dt.year)
        #fetch daily comments
        daily_comments = db.child("comments").child(new_dt).get().val()
        if daily_comments == None: 
            continue
        daily_comments = daily_comments.values()
        for comment in daily_comments:
            word_list = str(comment['body']).split(' ')
            total_comments += 1
            word_count += len(word_list)
            for index, word in enumerate(word_list):
                if index == 0:
                    markov_chain["~"].append(word)
                else:
                    if word_list[index-1] not in markov_chain:
                        markov_chain[word_list[index-1]] = [word]
                    else: 
                        markov_chain[word_list[index-1]].append(word)

    print("Collected {} unique words".format(len(markov_chain)))
    average_comment_length = math.ceil(word_count/total_comments)
    print("Average comment length {} words".format(average_comment_length))

    key = '~'
    comment_body = ""
    
    for i in range(0, average_comment_length):
        if key not in markov_chain:
            break
        next_key = random.choice(markov_chain[key])
        comment_body += " {}".format(next_key)
        key = next_key
    print("COMMENT: {}".format(comment_body))

if __name__ == "__main__":
    main()
from reddit_scrape import scrape
from btc_price import fetch_btc_data
from train_model import train, test
import shlex

def help():
    print("User Guide:")
    print("1. Scrape [subreddit-name]")
    print("--- Will scrape [subreddit-name] subreddit")
    print()
    print("2. Train [model-name]")
    print("--- Will train the A.I. with model [model-name]")
    print("--- There are 3 models:")
    print("--- ---1) A")
    print("--- ---2) B")
    print("--- ---3) C")
    print()
    print("3. Test \"[title]\" [upvote-num] [comment-num]")
    print("--- Will test the model with the given data and...")
    print("--- predict will bitcoin go up or down in the next hour")
    print()
    print("4. Quit")
    print("--- Will quit the program")
    print()
    return

def main():
    fetch_btc_data()
    print()
    print("Welcome to A.I. train station")
    print("Write \"help\" to view the guidelines")
    while(True):
        try:
            op = input(">> ")
        except EOFError:
            print("It is fun playing with you, goodbye\n")
            break

        opers = shlex.split(op)
        if(len(opers) == 0 or opers[0] == ""):
            continue

        if(opers[0].lower() == "help"):
            help()

        elif(opers[0].lower() == "scrape"):
            if(len(opers) < 2):
                print("Missing [subreddit-name] parameter\n")
            else:
                scrape(opers[1])
                print()

        elif(opers[0].lower() == "train"):
            if(len(opers) < 2):
                print("Missing [model-name] parameter\n")
            else:
                train(opers[1])
                print()

        elif(opers[0].lower() == "test"):
            if(len(opers) < 4):
                print("Missing parameters\n")
            else:
                if(opers[2].isdigit() or opers[3].isdigit()):
                    test(opers[1], opers[2], opers[3])
                else:
                    print("Upvotes and Comments must be numbers\n")
                print()
            
        elif(opers[0].lower() == "quit"):
            print("Thank you for your order\n")
            break
        else:
            print("I don't quite understand your command\n")
    return


if __name__ == "__main__":
    main()
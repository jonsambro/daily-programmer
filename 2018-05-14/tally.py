def main():
    input_string = input()
    players = {x.lower() for x in input_string}
    scores = [(i, input_string.count(i) - input_string.count(i.upper())) for i in players]
    scores.sort(key=lambda x: x[0])
    print(scores)


if __name__ == "__main__":
    main()

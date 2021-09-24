import os
def negative_file_generation():
    with open('negatives.txt', 'w') as file:
        for filename in os.listdir('negative'):
            file.write('negative/' + filename + '\n')



import os
import sys
import glob


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    else:
        dir_path = './'


    with open('Cookbook.tmp', 'w') as cookbook:
        g = glob.glob(dir_path + "/*.html")
        for file in g:
            with open(file, 'r') as recipe:
                lines = recipe.read()
                cookbook.write(lines)
                cookbook.write('<br>')
            recipe.close()
    cookbook.close()

    os.rename('Cookbook.tmp', 'Cookbook.html')


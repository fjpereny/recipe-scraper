

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

        cookbook.write("<h1>Cook Book Table of Contents</h1>")
        for file in g:
            recipe_name = file.split('/')[-1].split('.')[0]
            cookbook.write(f"<h2><a href=\"#{recipe_name}\" >{recipe_name}</a></h2>")

        cookbook.write("<br>")
        for file in g:
            with open(file, 'r') as recipe:
                recipe_name = file.split('/')[-1].split('.')[0]
                lines = recipe.read()
                cookbook.write(f'<div id=\"{recipe_name}\" >')
                cookbook.write(lines)
                cookbook.write('</div>')
                cookbook.write('<br>')
            recipe.close()
    cookbook.close()

    os.rename('Cookbook.tmp', 'Cookbook.html')


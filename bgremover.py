from rembg import remove
from PIL import Image
import sys


def remove_background(input_path, output_path):
    inp = Image.open(input_path)
    output = remove(inp)
    output.save(output_path)
    Image.open(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Missing required input file argument")
    else:
        input_path = sys.argv[1]
        output_path = ""
        if len(sys.argv) >= 3:
            output_path = sys.argv[2]
            if not output_path.upper().endswith('.PNG'):
                output_path = output_path + '.png'
        else:
            output_path = input_path[:input_path.rfind('.')] + '.png'

        remove_background(input_path, output_path)

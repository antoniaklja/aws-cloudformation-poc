import os
import jinja2
import base64
import zlib

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Render a jinja2 template')
    parser.add_argument('--user-data', '-u', type=argparse.FileType('r'), help='user-data file')
    parser.add_argument('--template', '-t', help='template file to render')
    parser.add_argument('--output', '-o', help='destination file to save')
    args = parser.parse_args()

    encoded_data = base64.b64encode(zlib.compress(args.user_data.read()))

    context = {
        'user_data': encoded_data,
    }

    result = render(args.template, context)

    file = open(args.output, "w")
    file.write(result)
    file.close()
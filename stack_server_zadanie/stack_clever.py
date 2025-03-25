import sys
import os.path
from numberstack import NumberStack
from jinja2 import Template,FileSystemLoader,Environment


env=Environment(loader=FileSystemLoader('.'),
    line_statement_prefix='%%',variable_start_string='<<',variable_end_string='>>')
t=env.get_template(sys.argv[1])

basename=os.path.basename(sys.argv[0])
filename,suffix=os.path.splitext(basename)
splitted_filename=filename.split('_')
del splitted_filename[0]
st=NumberStack([int(s) for s in splitted_filename],4)
sys.stdout.write(t.render(numberstack=st))




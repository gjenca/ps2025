import sys
from numberstack import NumberStack
from jinja2 import Template,FileSystemLoader,Environment

env=Environment(loader=FileSystemLoader('.'),
    line_statement_prefix='%%',variable_start_string='<<',variable_end_string='>>')
t=env.get_template(sys.argv[1])

st=NumberStack([],4)
sys.stdout.write(t.render(numberstack=st))




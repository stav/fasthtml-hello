from fasthtml.common import *

app,rt = fast_app(live=True)

@rt('/')
def get(): return Titled(
    "Hello World!",
    P('Greetings', id='stuff', hx_get="/change")
)

@rt('/change')
def get(): return P('Nice to be here!')

serve()

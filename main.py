from fasthtml.common import *

def render(todo):
    tid = f'todo-{todo.id}'
    toggle = A('Toggle', target_id=tid, hx_get=f'/toggle/{todo.id}')
    delete = A('Delete', target_id=tid, hx_delete=f'/{todo.id}', hx_swap='outerHTML')
    return Li(
        toggle, ' ', delete, ' ',
        todo.title + (' (done)' if todo.done else ''),
        id=tid,
    )

app,rt,todos,Todo = fast_app('todos.db', live=True, render=render,
                             id=int, title=str, done=bool, pk='id', 
                             )

def mk_input():
    return Input(id='title', placeholder='Add a new todo', 
                 hx_swap_oob='true')

@rt('/')
def get():
    frm = Form(
        Group(
            mk_input(), 
            Button('Add')
            ),
        hx_post='/', target_id='todo-list', hx_swap='beforeend',
        )
    return Titled("Todos",
                  Card(
                    Ol(*todos(), id='todo-list'),
                    header=frm
                  )
                 )

@rt('/')
def post(todo: Todo): # type: ignore
    return todos.insert(todo), mk_input()

@rt('/{tid}')
def delete(tid: int):
    todos.delete(tid)

@rt('/toggle/{tid}')
def get(tid: int):
    todo = todos[tid]
    todo.done = not todo.done
    return todos.update(todo)

serve()

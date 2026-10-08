from copy import deepcopy

def singleton(priority=0):
    return dict(n_states=1,n_actions=1,initial=0,menus=[[0]],
                rows=[[[[1]]],[[[1]]]], priorities=[[[priority]],[[priority]]])

def bernoulli(equal=False):
    rows=[[[['2/3','1/3'] for _ in range(2)] for _ in range(2)],
          [[['1/3','2/3'] for _ in range(2)] for _ in range(2)]]
    if equal: rows[1]=deepcopy(rows[0])
    return dict(n_states=2,n_actions=2,initial=0,menus=[[0,1],[0,1]],rows=rows,
                priorities=[[[2,1],[2,1]],[[1,2],[1,2]]])

def separator():
    return dict(n_states=2,n_actions=1,initial=0,menus=[[0],[0]],
                rows=[[[[0,1]],[[1,0]]],[[[1,0]],[[0,1]]]],
                priorities=[[[0],[1]],[[0],[1]]])

def recovery():
    # Under 0, state0 self-loops; a mode1 reveal reaches even absorbing state1.
    return dict(n_states=2,n_actions=1,initial=0,menus=[[0],[0]],
                rows=[[[[1,0]],[[0,1]]],[[[0,1]],[[0,1]]]],
                priorities=[[[0],[0]],[[1],[0]]])

def stale():
    active0=[0,'2/3','1/3']; active1=[0,'1/3','2/3']
    return dict(n_states=3,n_actions=2,initial=0,menus=[[0],[0,1],[0,1]],
                rows=[[[[0,1,0],[0,1,0]],[active0,active0],[active0,active0]],
                      [[[0,'2/3','1/3'],[0,'2/3','1/3']],[active1,active1],[active1,active1]]],
                priorities=[[[2,2],[2,1],[2,1]],[[2,2],[1,2],[1,2]]])

def route(source, component=None, steps=(), reveal=None):
    return dict(source=source,steps=steps,component=component,reveal=reveal)

def bernoulli_body():
    return dict(K=(),W=(0,1),D1=(),D=((0,0),(0,1),(1,0),(1,1)),
                known_components=(),uncertain_components=((((0,0),(1,0)),),(((0,1),(1,1)),)),
                known_routes=(),uncertain_routes=((route(0,0),route(1,0)),(route(0,0),route(1,0))))

def recovery_body():
    return dict(K=(1,),W=(0,),D1=((1,0),),D=((0,0),),
                known_components=(((1,0),),),uncertain_components=((((0,0),),),()),
                known_routes=(route(1,0),),uncertain_routes=((route(0,0),),(route(0,reveal=(0,1)),)))

def stale_body():
    return dict(K=(1,2),W=(0,1,2),D1=((1,1),(2,1)),D=((0,0),(1,0),(1,1),(2,0),(2,1)),
                known_components=(((1,1),(2,1)),),
                uncertain_components=((((1,0),(2,0)),),(((1,1),(2,1)),)),
                known_routes=(route(1,0),route(2,0)),
                uncertain_routes=tuple((route(0,0,((0,1),)),route(1,0),route(2,0)) for _ in (0,1)))

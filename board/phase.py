import pygame as pg;
from typing import Callable, Any;
import re;
from icecream import ic;

from ..utilities.reader import read_header, read_repeatability, read_input, read_output, resolve;
from .exception import FinalRepException;

class Phase:
    def __init__(self, 
            conditions: list[tuple[str, str|int]], 
            output: Callable,
            consumption_times: int, *,
            andifying: bool = True, 
            repeatable: bool = False):

        self.__conditions = conditions
        self.__andifying = andifying
        self.__output = output
        self.__consumption_times = consumption_times
        self.__CT = consumption_times
        self.__repeatable = repeatable
        self.__last_iteration = False 
        self.__active = False

    def __call__(self, *args, **kwargs):
        return self.__execute(*args, **kwargs)

    def __execute(self, *args, **kwargs) -> None|Any:
        if not self:
            self.__last_iteration = False
            return
        if (not self.__repeatable and self.__last_iteration):
            return
        self.__consumption_times -= 1
        # ic(self.__consumption_times)
        if self.__consumption_times < 0:
            self.__active = False
            raise FinalRepException(self)
        elif self.__consumption_times == 0:
            self.__last_iteration = True
            self.__output(*args, **kwargs)
            raise FinalRepException(self)

        self.__last_iteration = True
        return self.__output(*args, **kwargs)

    def init_phase(self):
        self.__consumption_times = self.__CT 

    def activate(self):
        self.__active = True

    @property
    def active(self):
        return self.__active

    def __bool__(self):
        res = False
        for input_type, _input in self.__conditions:
            if self.__andifying:
                if self.__check_input(
                    input_type, _input
                ):
                    res = True
                else: res = False; break;
            else:
                res = (res or self.
                __check_input(input_type, _input))
        return res

    @staticmethod
    def __check_input(input_type: str, _input: str|int):
        match input_type:
            case 'KEY':
                if isinstance(_input, int):
                    return pg.key.get_pressed()[_input]
                elif isinstance(_input, str):
                    return pg.key.get_pressed()[getattr(
                        pg, "K_"+_input.lower())]
            case 'MOUSE':
                if isinstance(_input, int):
                    return pg.mouse.get_pressed()[_input]
                elif isinstance(_input, str):
                    return pg.mouse.get_pressed()[
                        getattr(pg, "MOUSE"+_input)
                    ]
            case 'MOUSE_POS':
                if isinstance(_input, pg.Rect) or \
                    (isinstance(_input, tuple) and len(_input) == 4):
                    return pg.Rect(_input).collidepoint(pg.mouse.get_pos())
                else:
                    print(f"Invalid mouse position checker: {_input}")
                    return False
            case 'TIME':
                return pg.time.get_ticks() >= _input
            case 'TE_LESS_THAN':
                return pg.time.get_ticks() - _input < 0


    @classmethod
    def fromQueries(cls, *queries: str):
        """
        TODO:
            - implement the reader for the queries

        Queries are a list of strings that are used to create a phase.
        Each Query describe an effect of the phase or an event triggered by 
        a certain key pressed or a mouse click, or a mouse position.

        The format of a query: 
        for an immediate effect: 
            EFFECT {variables declaration} -> {effects on these variables};
            to declare a variable: {variable_name} : {variable_value} || BOARD.{attribute_name} || WINDOW.{attribute_name} || THIS.{attribute_name} || PIECE.{piece index}
            a variable declaration is ended by putting || symbol
            to declare an effect: use the python syntax to define operations on the variables declared to be applied at the beggining of the phase
        
        for an event triggered by a key pressed:
            KEY {key_code} && {varible declaration} -> {effects on these variables};
            {key_code} is either a number, or a key name, ensure that the key name is the same used by pygame library [pg.K_{key_name}]

        for an event triggered by a mouse click:
            MOUSE {mouse_button} && {varible declaration} && {condition on mouse position} -> {effects on these variables};
            {mouse_button} is either NONE, LEFT, MIDDLE, RIGHT; referring to the mouse button pressed
            {condition on mouse position} is a rect described by four coordinates: x, y, width, height to specify the region where the mouse can activate the effect
            to use an advanced function as a checker for the mouse you can use a method created in python
        
        for making a loop: 
            L[{variable declaration} (optional)]<{queries number}, {iterations number}, {loop variable name} (optional)>;
            it loops the next {queries number} queries, {iterations number} times, using {loop variable name} as a variable to iterate

        for making a conditional:
            C[{variable declaration} (optional)]<{queries number}, {condition}>;
            if the {condition} is true, the next {queries number} queries are executed, otherwise they are skipped
        """
        def parse_python_code(text: str) -> str:
            """Extract and execute Python code between <<>>."""
            def replace_code(match: re.Match) -> str:
                code = match.group(1)
                try:
                    return str(eval(code))
                except:
                    return code
            return re.sub(r'<<(.*?)>>', replace_code, text)

        def parse_variable_declaration(decl: str, board, window) -> dict:
            """Parse variable declarations and create variables."""
            if not decl.strip():
                return {}
            
            variables = {}
            declarations = decl.split('||')
            
            for decl in declarations:
                if not decl.strip():
                    continue
                    
                name, value = decl.split(':', 1)
                name = name.strip()
                value = value.strip()
                
                # Handle special object attributes
                if value.startswith('BOARD.'):
                    attr = value[6:]
                    variables[name] = getattr(board, attr)
                elif value.startswith('WINDOW.'):
                    attr = value[7:]
                    variables[name] = getattr(window, attr)
                elif value.startswith('THIS.'):
                    attr = value[5:]
                    variables[name] = getattr(cls, attr)
                elif value.startswith('PIECE.'):
                    idx = int(value[6:])
                    variables[name] = board.pieces[idx]
                else:
                    # Handle Python code execution
                    value = parse_python_code(value)
                    try:
                        variables[name] = eval(value)
                    except:
                        variables[name] = value
                        
            return variables

        def create_effect_function(query: str) -> Callable:
            """Create a callable function from a query."""
            query = query.strip()
            
            # Handle different query types
            if query.startswith('EFFECT'):
                # Parse EFFECT query
                parts = query[6:].split('->', 1)
                var_decl = parts[0].strip()
                effects = parts[1].strip().rstrip(';')
                
                def effect_func(board, window):
                    variables = parse_variable_declaration(var_decl, board, window)
                    # Execute effects with variables in scope
                    exec(effects, variables)
                    # Update object attributes if they were modified
                    for name, value in variables.items():
                        if name.startswith('BOARD.'):
                            setattr(board, name[6:], value)
                        elif name.startswith('WINDOW.'):
                            setattr(window, name[7:], value)
                        elif name.startswith('THIS.'):
                            setattr(cls, name[5:], value)
                        elif name.startswith('PIECE.'):
                            idx = int(name[6:])
                            board.pieces[idx] = value
                
                return effect_func
                
            elif query.startswith('KEY'):
                # Parse KEY query
                parts = query[3:].split('->', 1)
                key_part = parts[0].split('&&', 1)
                key_code = key_part[0].strip()
                var_decl = key_part[1].strip() if len(key_part) > 1 else ''
                effects = parts[1].strip().rstrip(';')
                
                def key_func(board, window):
                    variables = parse_variable_declaration(var_decl, board, window)
                    exec(effects, variables)
                    # Update object attributes
                    for name, value in variables.items():
                        if name.startswith('BOARD.'):
                            setattr(board, name[6:], value)
                        elif name.startswith('WINDOW.'):
                            setattr(window, name[7:], value)
                        elif name.startswith('THIS.'):
                            setattr(cls, name[5:], value)
                        elif name.startswith('PIECE.'):
                            idx = int(name[6:])
                            board.pieces[idx] = value
                
                return (getattr(pg, f'K_{key_code}'), key_func)
                
            elif query.startswith('MOUSE'):
                # Parse MOUSE query
                parts = query[5:].split('->', 1)
                mouse_part = parts[0].split('&&', 2)
                button = mouse_part[0].strip()
                var_decl = mouse_part[1].strip() if len(mouse_part) > 1 else ''
                condition = mouse_part[2].strip() if len(mouse_part) > 2 else ''
                effects = parts[1].strip().rstrip(';')
                
                def mouse_func(board, window):
                    if not pg.mouse.get_pressed()[getattr(pg, f'MOUSE_{button}')]:
                        return False
                        
                    if condition:
                        # Parse condition as rect or custom function
                        try:
                            rect = eval(condition)
                            if not isinstance(rect, pg.Rect):
                                rect = pg.Rect(*rect)
                            if not rect.collidepoint(pg.mouse.get_pos()):
                                return False
                        except:
                            if not eval(condition):
                                return False
                    
                    variables = parse_variable_declaration(var_decl, board, window)
                    exec(effects, variables)
                    # Update object attributes
                    for name, value in variables.items():
                        if name.startswith('BOARD.'):
                            setattr(board, name[6:], value)
                        elif name.startswith('WINDOW.'):
                            setattr(window, name[7:], value)
                        elif name.startswith('THIS.'):
                            setattr(cls, name[5:], value)
                        elif name.startswith('PIECE.'):
                            idx = int(name[6:])
                            board.pieces[idx] = value
                    return True
                
                return mouse_func
                
            elif query.startswith('L'):
                # Parse LOOP query
                parts = query[1:].split(']', 1)
                var_decl = parts[0].strip('[')
                loop_part = parts[1].strip('<>').split(',')
                queries_num = int(loop_part[0])
                iterations = int(loop_part[1])
                loop_var = loop_part[2].strip() if len(loop_part) > 2 else None
                
                def loop_func(board, window):
                    variables = parse_variable_declaration(var_decl, board, window)
                    for i in range(iterations):
                        if loop_var:
                            variables[loop_var] = i
                        for j in range(queries_num):
                            query_idx = queries.index(query) + j + 1
                            if query_idx < len(queries):
                                create_effect_function(queries[query_idx])(board, window)
                
                return loop_func
                
            elif query.startswith('C'):
                # Parse CONDITIONAL query
                parts = query[1:].split(']', 1)
                var_decl = parts[0].strip('[')
                cond_part = parts[1].strip('<>').split(',')
                queries_num = int(cond_part[0])
                condition = cond_part[1]
                
                def cond_func(board, window):
                    variables = parse_variable_declaration(var_decl, board, window)
                    if eval(condition, variables):
                        for j in range(queries_num):
                            query_idx = queries.index(query) + j + 1
                            if query_idx < len(queries):
                                create_effect_function(queries[query_idx])(board, window)
                
                return cond_func

        # Process all queries
        effects = []
        key_map = {}
        mouse_map = []
        
        for query in queries:
            func = create_effect_function(query)
            if isinstance(func, tuple):  # KEY query
                key_map[func[0]] = func[1]
            elif query.startswith('MOUSE'):
                mouse_map.append(func)
            else:
                effects.append(func)
        
        return cls(
            end_condition=lambda: True,  # Default end condition
            key_map=key_map,
            mouse_map=lambda mouse, *args, **kwargs: [
                effect(*args, **kwargs) 
                for effect in mouse_map 
                if effect(*args, **kwargs)
            ],
            *effects
        )

    @classmethod
    def null(cls):
        return cls([], lambda *a, **k: ..., 0, andifying=True)
    
    @classmethod
    def from_query(cls, query: str, window, board):
        """
        a query start with repeating times, an input type, followed by an input value, then an output operations where python code is used,
        like: 
        

        """
        if not resolve(query, board, window):
            return cls.null()
        time = read_header(query)
        rep = read_repeatability(query)
        conds, andifying = read_input(query)
        acts = read_output(query)

        return cls(conds, acts, time, andifying=andifying, repeatable=(rep.lower() == 't'))
        
    @staticmethod
    def from_file(file_name: str):
        with open(file_name, 'r') as f:
            L = []
            while (c:=f.readline()):
                phase_query = c + '\n'
                while not (line := f.readline()).startswith('----'):
                    phase_query += line 
                L.append(Phase.from_query(phase_query))
                



KEY_WORDS = {
    'UP': 'BOARD.UP',
    'DOWN': 'BOARD.DOWN',
    'RIGHT': 'BOARD.RIGHT',
    'LEFT': 'BOARD.LEFT',
    'PEACE[': 'BOARD.pieces[',
    # 'ENDX':'',
    'END': 'BOARD.end_phase()'
}




def read_header(query: str):
    try: return int(query.split()[0])
    except ValueError: return float('inf')

def resolve(query: str, board, window):
    """
    TODO
    start by resolving loops, 
    then special objects, 
    then conditions,
    """
    return True

def __get_inner(text: str, opening: str, closing: str):
    start_index: int = 0
    end_index: int = -1
    started: bool = False
    for i, _ in enumerate(text):
        if not started and text[i:i+len(opening)] == opening:
            started = True 
            start_index = i 
        elif started and text[i:i+len(closing)] == closing:
            started = False
            end_index = i 
            return start_index, end_index
    return start_index, end_index

def __get_indexes(text, name):
    indexes: list[int] = []
    for i, c in enumerate(text):
        if text[i:i+len(name)] == name:
            indexes.append(i)
    return indexes

def read_input(query: str):
    query = query.strip('\n ')
    first = query.split('->')[0]
    number = first.split()[0]
    input_query = first[len(number)+2:]
    anding = input_query.split('&&')
    oring = input_query.split('||')

    conditions = []
    andifying = False

    if len(anding) > 1:
        support = anding
        andifying = True        
    else:
        support = oring

    for inpc in support:
        inpc = inpc.strip()
        input_type, input_value = inpc.split()
        try: input_value = int(input_value)
        except ValueError: ...
        conditions.append((input_type, input_value))

    return conditions, andifying

def read_repeatability(query: str):
    try: 
        x = query.split()[1]
        assert x in ('f', 'F', 't', 'T')
        return x.lower()
    except Exception as e:
        print("eror:", e)
        return 't'

def read_output(query: str):
    try:
        query = query.split('->')[1].strip()
        # query = query.replace('\n', ';')
        for convention, real in KEY_WORDS.items():
            query = query.replace(convention, real)
        return lambda WINDOW, BOARD: exec(query)
    except:
        raise ValueError("Invalid output")
    



if __name__ == "__main__":
    query = """
3 
KEY k 
&&
L3{
MOUSE LOOP.index} || 
MOUSE_POS BOARD.peaces[LOOP.index] -> 
print('hello')
print('world')
"""
    # print(__get_inner(query, "{", "}"))
    # print(__get_indexes(query, "BOARD"))
    # print(query[17:34])


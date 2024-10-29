from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT,SDL_KEYUP,SDLK_LEFT



# 이벤트 체크 함수를 정의
# 상태 이벤트 라고 하는 e = (종류, 실제값) -> 튜플로 정의

def start_event(e):
    return e[0] == 'START'

def space_down(e):  # e가 space down인지 판단 -> True or False 리턴
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):  # e가 time out인지 판단
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT



class StateMachine:
    def __init__(self, obj):
        self.cur_state = None
        self.obj = obj # 어떤 객체를 위한 상태머신인지 알려줌. obj = boy.self
        # 상태 이벤트를 보관할 리스트.. 큐!
        self.event_q = [] # 상태 이벤트를

    def start(self, state):
        self.cur_state = state # 시작 상태를 받아서, 그걸 현재상태로 정의
        self.cur_state.enter(self.obj, ('START',0))
        print(f'Enter into {state}')
        pass
    def update(self):
        self.cur_state.do(self.obj) #idle.do()
        # 혹시 이벤트가 있나?
        if self.event_q: # list는 멤버가 존재하면 True
            e = self.event_q.pop(0)
            #self.add_event(e)
            # 이 시점에서 우리한테 주어진 정보는?
            # e
            # cur_state
            # 현재 상태와 현재 발생한 이벤트에 따라서
            # 다음 상태를 결정하는 방법은???
            # 상태 변환 테이블 이용.
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    print(f' Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj,e)
                    self.cur_state = next_state
                    print(f' Enter into {next_state}')
                    self.cur_state.enter(self.obj,e) #상태변환의 이유를 명확히 알려줘야함.. e추가
                    return # 제대로 이벤트에 대한 상태변환이.... 끝!

            # 이 시점으로 왔다는 것은, event에 따른 전환 실패!!
            print(f'        WARNING경고..: {e} not handled at state {self.cur_state} ')

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e):
        print(f'    DEBUG: add_event {e}')
        self.event_q.append(e)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass



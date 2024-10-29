from unittest.mock import right

from pico2d import load_image, get_time

from state_machine import StateMachine, time_out, space_down, right_down, right_up, left_down, left_up, start_event


# 상태를 클래스를 통해 정의
class Idle:
    @staticmethod #이게 있으면 객체를 찍어내는 용도가 x, 클래스 내 있는 함수를 그냥 그룹화? 시키는 개념
    def enter(boy,e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1

        boy.dir = 0 # 정지상태이다..
        boy.frame = 0
        # 현재 시각을 저장
        boy.start_time = get_time()
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))

        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

        pass

class Sleep:
    @staticmethod
    def enter(boy,e):
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:   # 오른쪽보다가 자는거..
            boy.image.clip_composite_draw(
                boy.frame*100,300,100,100,
                3.141592/2,
                '',# 좌우상하반전X
                boy.x -25,boy.y - 25,100,100)
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                -3.141592 / 2,
                '',  # 좌우상하반전X
                boy.x + 25, boy.y - 25, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
            boy.dir =1
            boy.action =1
        elif left_down(e) or right_up(e):
            boy.dir = -1
            boy.action = 0

        boy.frame =0


    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.x+=boy.dir*5
        boy.frame = (boy.frame +1) % 8
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame*100,boy.action*100,100,100,
            boy.x,boy.y
        )

class AutoRun:
    @staticmethod
    def enter(boy, e):
       pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):

        pass

    @staticmethod
    def draw(boy):
        pass
from state_machine import StateMachine, space_down


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 stateMachine 생성
        self.state_machine.start(Idle) # 초기상태가 idle
        self.state_machine.set_transitions(
            {
                # key = 현재상태, value = dictionary로..
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                # run 상태에서 어떤 이벤트가 들어와도 처리핮 않겠다.. 라는 의미
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}

            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : 입력 이벤트.. key, mouse 등
        # 우리가 state machne 전달해줄건 (, ) - > 이런식의 튜플구조
        self.state_machine.add_event(
            ('INPUT',event)
        )



    def draw(self):
        self.state_machine.draw()



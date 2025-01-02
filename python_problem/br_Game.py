'''
- 배스킨라빈스31 게임은 마지막 31을 부른 사람이 지는 게임으로, 아래의 규칙을 따른다.
    - 참여자들은 번갈아가며 1부터 31까지의 수를 순서대로 부른다.
    - 한번에 1~3개의 수를 부를 수 있다.
    - 예를 들어, playerA가 1,2,3을 부르면, playerB는 4 또는 4,5 또는 4,5,6를 부를 수 있다.
'''

'''
로직
1. 입력 필터링 후 저장 (1,2,3만 입력가능)
2. 입력된 수 만큼 num 증가시키고 playerA playerB 스위칭
3. 반복
4. 더한 숫자가 31이 되면 게임 종료
5. 최종 결과 출력
'''

import sys
import random

def brGame():
    num = 0
    current_player = 'playerA'
    
    print('===Player A VS Player B (A부터 시작합니다)===')

    while True:
        while True:
            user_input = input(f"{current_player} - - 부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : ")

            #입력이 비어있거나 정수로 변환이 불가능하면 예외처리
            if not user_input:
                print("정수를 입력하세요")
                continue
            try:
                call_count = int(user_input)
            except ValueError:
                print("정수를 입력하세요")
                continue
            
            #입력이 1, 2, 3이 아니면 예외처리
            if call_count not in [1,2,3]:
                print("1, 2, 3 중 하나를 입력하세요")
                continue
            
            #입력이 1, 2, 3이면 반복문 탈출
            break

        for i in range(call_count):
            num += 1
            print(f"{current_player} : {num}")
            if num == 31:
                if current_player == 'playerA':
                    print("playerB win!")
                else:
                    print("playerA win!")
                
                return
            
        if current_player == 'playerA':
            current_player = 'playerB'
        else:
            current_player = 'playerA'

def brGameComputer():
    num = 0
    current_player = 'computer'

    print('===Player VS Computer (Computer부터 시작합니다)===')

    while True:
        if current_player == "computer":
            call_count = random.randint(1,3)
            print(f"{current_player}가 {call_count}개의 숫자를 부릅니다.")

            for i in range(call_count):
                num += 1
                print(f"{current_player} : {num}")
                
                if num == 31:
                    print('player win!')
                    return
            
            current_player = 'player'

        else:
            while True:
                user_input = input("부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : ")

                if not user_input:
                    print("정수를 입력하세요")
                    continue
                try:
                    call_count = int(user_input)
                except ValueError:
                    print("정수를 입력하세요")
                    continue
                
                if call_count not in [1,2,3]:
                    print("1, 2, 3 중 하나를 입력하세요")
                    continue
                
                break
            
            for i in range(call_count):
                num += 1
                print(f"{current_player} : {num}")
                if num == 31:
                    print("computer win!")
                    return
            current_player = 'computer'



if __name__ == "__main__":
    #brGame()
    brGameComputer()
# Install the Python3 venv package if not already installed
sudo apt install python3-venv

# Create a new virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

이것을 확인하기 위해서 처리를 한다.한다. 

site: https://codingboycc.tistory.com/89

#configuration을 변경하기 위해서
    sudo raspi-config

#라즈베리 ip: hostname -I 
    192.168.1.23

#맥에서 라즈베리로 파일 전송
    - scp [옵션] [로컬 파일 경로] [사용자명]@[라즈베리 파이 IP 주소]:[원격 경로]

    -사용자명 : whoami
    
    -예제: scp example.txt pi@라즈베리파이IP:~/Documents

#2024-4-8 : OZS iot 실행 디렉토리
    - /home/kwon/Raspberry/Iot-2024_3_20/aws-iot-device-sdk-python-v2/OZS-20240404
    - ozsPubSub.sh
    - ozsPubSub.py 
    
2024-4-13 : 라즈베리파이 터미널 경로길이가 너무 길어서 줄여서 보는 방법은
    - nano ~/.~/.bashrc 또는 ~/.bash_profile
    - PS1="\u@\h:\W \$ "
    - .bashrc 파일의 PS1 을 수정하면 된다. 

2024-4-16: 소스 코드를 github에 업로드
    - .gitignore : 참조 사이트 : https://sunhyeokchoe.github.io/posts/Ignoring-Files/
    - 업로드 제외 파일 / 디렉토리 example_directory/  뒤에 / 가 있어야 한다. 

            # 확장자가 .a인 파일 무시
            *.a

            # 윗 라인에서 확장자가 .a인 파일은 무시하게 했지만 lib.a는 무시하지 않음
            !lib.a

            # 현재 디렉터리에 있는 TODO 파일은 무시하고 subdir/TODO 처럼
            # 하위 디렉터리에 있는 파일은 무시하지 않음
            /TODO

            # build/ 디렉터리에 있는 모든 파일 무시
            build/

            # doc/notes.txt 파일은 무시하고 doc/server/arch.txt 파일은 무시하지 않음
            doc/*.txt

            # doc 디렉터리 아래의 모든 .pdf 파일을 무시
            doc/**/*.pdf
    -ozsPubSub.sh 가 동작하기 위해서는 실제적으로 sdk를 install 해야한다. 그렇게 해야 환경이 세팅이 된다.
        . workspace/aws-iot ..../ README.md 를 참조해서 환경을 구축해야한다.
        
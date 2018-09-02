파이썬 한국어 번역
==========================

현재 혹은 가까운 미래의 안정판만을 번역하고, 현재는 3.7 입니다. 번역은 3.7 브랜치에 들어있고, master 브랜치에는 번역 작업을 보조하는 도구들이 들어있습니다.

번역팀에 문의가 있으신 분들은 https://www.flowdas.com/pages/python-docs-ko.html 를 참고 바랍니다.

교정을 위한 프리뷰 빌드하기
---------------------------------------

저장소를 fork 한 후에 git clone 하면 master 브랜치의 작업 사본이 만들어집니다. 이 디렉토리에서 다음과 같은 명령을 실행합니다.

::

    python3 -m venv venv
    venv/bin/python -m pip install -r requirements.txt
    ./build.py

이제 ``cpython/Doc/build/html/index.html`` 에 프리뷰 파일이 만들어집니다.

한편 ``cpython/locale/ko/LC_MESSAGES`` 디렉토리에는 여러분이 fork 한 저장소의 3.7 브랜치의 작업 사본이 만들어집니다.

이제 ``cpython/locale/ko/LC_MESSAGES`` 디렉토리의 파일들을 번역한 후에, ``./build.py`` 를 실행하면 프리뷰가 업데이트 됩니다.

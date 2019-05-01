파이썬 한국어 번역
==========================

현재 혹은 가까운 미래의 안정판만을 번역하고, 현재는 3.7입니다. 번역은 3.7 브랜치에 들어있고, master 브랜치에는 번역 작업을 보조하는 파일들이 들어있습니다.

번역팀에 문의가 있으신 분들은 https://www.flowdas.com/pages/python-docs-ko.html 를 참고 바랍니다.

교정을 위한 프리뷰 빌드하기
---------------------------------------

프리뷰를 빌드하려면 git 와 docker 가 설치되어 있어야 합니다.

먼저 저장소를 fork 한 후에, 작업 공간을 다음과 같은 절차로 준비합니다.

::

	python3.7 -m venv <work-dir>
	cd <work-dir>
	source bin/activate
	pip install python-docs-ko
	pdk init <your-python-docs-ko-fork>

이제 ``<work_dir>/python-docs-ko`` 디렉터리에 여러분의 fork가 git clone 되었습니다.
``*.po`` 파일을 번역합니다.

빌드는 다음과 같은 명령을 사용합니다::

	pdk build

   
이제 ``<work_dir>/html/index.html`` 를 브라우저로 열면 됩니다.

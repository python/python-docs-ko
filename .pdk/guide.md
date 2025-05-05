## 번역 시작하기

직접 번역으로 기여하고 싶으신 분들은 다음과 같은 기본 절차를 따르시기 바랍니다.

1. 저장소를 포크(fork)합니다.
2. 가장 높은 버전의 브랜치로 Codespaces 를 만듭니다.
3. 작업할 이슈를 선택합니다.
4. `.po` 파일을 번역하고, `pdk watch` 명령으로 결과를 확인합니다.
5. `pdk format` 으로 파일을 표준형식으로 변환한 후 커밋합니다.
6. PR 을 보낸 후에 리뷰어와 협의하여 최종 병합될 때까지 수정합니다. 

일감은 이슈에서 고르시면 됩니다.
모든 `.po` 파일을 개별 이슈로 등록해 두었습니다. 
이슈의 순서는 중요하지 않습니다. 
서로 일이 겹치지 않도록, 시작하실 때 이슈에 코멘트를 남겨주시면 좋습니다. 
아주 오래된 코멘트는 무시하시고 작업하셔도 됩니다. 

이 때 다음과 같은 사항을 유의하셔야 합니다.

- 최신 버전의 브랜치에서 작업하세요. 
  `master` 브랜치는 번역물이 들어가는 곳이 아닙니다.
- `.po` 파일의 일부만 번역하지 마시고 파일 전체를 번역한 후에 PR 주세요.
  일부 파일들은 꽤 큽니다. 마무리할 수 있을지 미리 확인해 보시고 시작해주세요. 
- 교정이 끝난 최종본을 PR 해 주세요. 띄어쓰기, 철자 검사는 필수입니다.
  `pdk watch` 할 때 없던 경고가 생기지 않도록 확인 바랍니다.
- 어떤 경우에도 `msgid` 는 변경하지 마시고, `msgstr` 부분만 변경해주세요.
- 마크업 (`` :ref:`...` ``,`*term*`,`` `... <...>`_ ``, ...) 뒤에 조사가 공백없이 연결되면 마크업으로 인식되지 않습니다.
  띄어쓰기 없이 마크업을 분리하려면 `\\`를 삽입해주세요.
- `:ref:...` 는 번역하지 말고 그냥 두세요.
- 만약 `` :ref:`mutable <typesseq-mutable>` `` 처럼 참조가 `<>`로 처리되어있다면, 나머지 부분은 번역하세요.
  `` :ref:`가변 <typesseq-mutable>` ``
- `:term:...` 은 파이썬 설명서의 "용어집"을 참조하여 번역어와 원문을 병기해야 합니다. 
  가령 `` :term:`asynchronous iterator` ``는 `` :term:`비동기 이터레이터 <asynchronous iterator>` `` 로 번역해야합니다.
- `:dfn:...` 역시 번역어와 원문을 병기합니다. 
  예를 들어, `` :dfn:`comprehension` `` 은 `` :dfn:`컴프리헨션 (comprehension)` `` 으로 번역합니다.
- "파이썬 자습서"는 "...입니다" 스타일인 반면, "파이썬 언어 레퍼런스"는 "...다" 스타일입니다. 
  "파이썬 언어 레퍼런스" 이외의 모든 문서는 "파이썬 자습서" 스타일을 유지해주세요.
- 가능하면 긴 `msgstr` 은 여러 줄 로 나눠주세요. 
  그래야 웹에서 리뷰할 때 편합니다. 
  줄 나누기 할 때 필요한 공백이 빠지지 않도록 조심하시고요.
- 드물긴 하지만 때로 원문에 오류가 있을 수도 있습니다. 
  특히 실제로 동작하지 않는 무의미한 마크업이 존재하기도 합니다. 
  이 경우 마크업을 제거하지 마시고 그대로 유지해주세요. 
  원문과 번역의 마크업이 일치하지 않으면 빌더가 불평합니다. 
  꼭 마음의 평화를 얻으셔야한다면 원문의 오류를 등록하시기 바랍니다. 
  (파이썬 설명서의 "버그 다루기"를 참조하세요.)
- 번역을 완료했지만 빌드해보면 일부 번역이 이루어지지 않은 상태로 표시되는 경우가 있습니다. 
  번역이 `fuzzy` 로 마킹되어 있는지 확인하십시오. 
  `fuzzy` 로 마킹하는 것은 번역이 불완전해서 검토가 필요하다는 뜻입니다. 
  때문에 빌드할 때 반영되지 않습니다. 
- `.po` 파일 끝에 `#~` 로 시작하는 주석들이 있을 수 있습니다.
  비정기적으로 원문의 변경 사항을 반영해서 `.po` 파일을 갱신하는데, 이 때 원문에서 사라진 것으로 판단되는 `msgid` 가 있으면, 이런식으로 남겨둡니다. 
  이미 번역했던 파일이면 예전의 번역을 남겨두려는 의도입니다. 
  변경된 부분을 찾아서 수정할 때 쓰라는 것이지요. 
  과거에 번역된 적이 없던 파일에 이런 부분이 있으면 삭제해도 무방합니다.

## 용어집

용어는 이미 번역된 파일들을 참고해서 일관성을 유지해 주시기 바랍니다.
완전하지는 않지만 자주 등장하는 것들을 적어보았습니다.
파이썬 설명서의 "용어집"에 등장하지 않는 용어들에 대한 번역어들입니다. 
로마자 표기법으로 소리나는대로 적는 경우도 포함시켰습니다. 
기여자들간의 협의에 의해 변경될 수 있습니다. 
변경 전까지는 가능하면 일관성을 유지해주세요. 
그래야 한꺼번에 바꾸기도 쉽습니다.

```
access: 액세스
algorithm: 알고리즘
alias: 에일리어스
angle brackets: 화살괄호
apostrophe: 작은따옴표
application: 응용 프로그램
architecture: 아키텍처
assign: 대입
associative array: 연관 배열
asterisk: 애스터리스크
backslash: 역 슬래시
body: 바디
barrier: 장벽
buffer: 버퍼
buffered: 버퍼드
built-in: 내장
byte-oriented datastream: 바이트지향 데이터스트림
bytes: 바이트열
bytes-like: 바이트열류
cache: 캐시
callable: 콜러블
callback: 콜백
caller: 호출자
calling convention: 호출 규약
canonical: 규범적
case: 케이스
chaining: 연쇄
clause: 절
clean-up: 뒷정리
code: 코드
code block: 코드 블록
codec: 코덱
collation: 콜레이션
collection: 컬렉션
command: 명령
computationally-intensive: 계산집약적
concrete class: 구상 클래스
construct: 구조물
constructor: 생성자
container: 컨테이너
control flow: 제어 흐름
cyclic garbage collector: 순환 가비지 수거기
curly braces: 중괄호
custom: 커스텀
data structure: 자료 구조
decimal: 십진 소수 # decimal 모듈과 관련될 때
dedent: 내어쓰기
deep copy: 깊은 사본
default: 기본
delimiter: 구분자
derived class: 파생 클래스
deserializing: 역 직렬화
destructor: 파괴자
digit: 디지트 # numeric character 와 구분할 때
directory: 디렉터리
dispatch: 디스패치
documentation: 설명서
dotted expression: 점표현식
enclosing: 둘러싼
encoding: 인코딩
environment variable: 환경 변수
error: 에러
escape: 이스케이프
evaluate: 값을 구하다
exception: 예외
exhaust: 소진하다
explicit: 명시적
export: 익스포트
expose: 드러내다
factory: 팩토리
floating point number: 실수
format specifier: 포맷 지정자
formatted string literal: 포맷 문자열 리터럴
frozenset: 불변 집합
fully qualified name: 완전히 정규화된 이름
glossary: 용어집
hashability: 해시 가능성
heterogeneous: 이질적
homogeneous: 등질적
identifier: 식별자
idiom: 이디엄
imaginary unit: 허수 단위
implicit: 묵시적
indent: 들여쓰기
index: 인덱스
inheritance: 상속
inline: 인라인
instance: 인스턴스
instruction: 명령어
interface: 인터페이스
interactive: 대화형
interpreter: 인터프리터
interrupt: 인터럽트
introspection: 인트로스펙션
iteration: 이터레이션
keyword argument: 키워드 인자
lexicographical: 사전식
linked list: 연결 리스트
literal: 리터럴
local: 지역
locale: 로케일
locale specific convention: 로케일 특정 방식
locking: 로킹
logging: 로깅
lookup: 조회
loop: 루프
machine code: 기계어
magic method: 매직 메서드
mechanism: 메커니즘
machinery: 절차
mode: 모드
module: 모듈
multi-processor: 다중 프로세서
multi-threaded: 다중스레드화
operating system: 운영 체제
operation: 연산
operator: 연산자
optional: 선택적, 생략 가능한
parallelism: 병렬성
parentheses: 괄호
parse tree: 파스 트리
parser: 파서
phase: 시기
placeholder: 자리 표시자
positional argument: 위치 인자
procedure: 프로시저
prompt: 프롬프트
property: 프로퍼티
queue: 큐
quotation mark: 따옴표
raw string: 날 문자열
redirection: 리디렉션
reference counting: 참조 횟수 추적
reference cycle: 참조 순환
resume: 재개
reverse iteration: 역 이터레이션
section: 섹션
serializing: 직렬화
set: 집합
shallow copy: 얕은 사본
shell: 셸
shift: 시프트
short-circuit: 단락-회로
side effect: 부작용
signature: 시그니처
socket: 소켓
source: 소스
square brackets: 대괄호
stack: 스택
step: 스텝
stream: 스트림
string: 문자열
subroutine: 서브루틴
subscript notation: 서브 스크립트 표기법
superclass: 슈퍼 클래스
suspend: 일시 중지
symlink: 심볼릭 링크
syntactic sugar: 편의 문법
syntax error: 문법 에러
third party: 제삼자
thread: 스레드
token: 토큰
truth value: 논리값
tutorial: 자습서
underlying resource: 하부 자원
virtual subclass: 가상 서브 클래스
wildcard: 와일드카드
Windows: 윈도우
```
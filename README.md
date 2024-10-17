# BackendNews

## 🔐 로그인 API

<aside>
**호출 URL:** /users/login      **호출 메서드:** POST

</aside>

**요청 헤더 (자동로그인 시):**

| 이름 | 형식 |
| --- | --- |
| refresh_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| email | str |
| password | str |

**응답:**

| 상태 코드 | 메시지 | 데이터 |
| --- | --- | --- |
| 201 | 로그인 성공 ✅ | access_token, refresh_token, nickname, email, phone_number |
| 404 | 로그인 실패 ❌ | null |
| 401 | auto_token 만료 ❌ | null |

<aside>
*💡 참고: refresh_token을 보낼 시 자동로그인 됩니다. refresh_token을 보내어도 email, password(공백) 데이터를 전송해야 합니다.*

</aside>

## 📕 회원가입 API

<aside>
**호출 URL:** /users/register      **호출 메서드:** POST

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| user_email | str |
| user_password | str |
| user_name | str |
| user_number | str |
| suer_nickname | str |
| user_age | int |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 회원가입 성공 ✅ | null |
| 404 | 회원가입 실패 ❌ | null |
| 418 | 아이디 중복 ❌ | null |
| 419 | 닉네임 중복 ❌ | null |

*참고: 나이를 안넣을시 0을 보내세요*

## 🔄 엑세스 토큰 재발급 API

<aside>
**호출 URL:** /users/reissue      **호출 메서드:** POST

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| refresh_token | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 엑세스토큰 발급 ✅ | access_token |
| 401 | id확인불가 ❌ | null |
| 401 | access_token만료 ❌ | null |

*참고:  차후 refresh_token 헤더에 요청할 수 있음*

## 📑 뉴스 목록 가져오는 API

<aside>
**호출 URL:/getNewsList/{keyword}/{page}/{itemCount}**      **호출 메서드:** GET

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| keyword | str |
| page | int |
| itemCount | int |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 뉴스 조회 성공 ✅ | data |
| 404 | 뉴스 조회 실패 ❌ | null |

*참고: keyword별 itemCount 만큼 조회 + 페이징 기능 추가*

- 응답 예시
    
    ```json
    **/news/getNewsList/normal/1/3**
    {
        "status": 200,
        "message": "뉴스 조회 성공",
        "data": {
            "total": 47,
            "news": [
                {
                    "article_id": 50,
                    "article_title": "태권도 기대주 박재원, 춘천 세계주니어선수권 남자 73㎏급 우승",
                    "article_url": "https://m.sports.naver.com/general/article/055/0001195191",
                    "article_content": "▲ 발차기 공격 성공하는 박재원(오른쪽)\n\n태권도 기대주 박재원(경북체고)이 춘천 2024 세계태권도연맹(WT) 세계주니어선수권대회 남자 73㎏급에서 금메달을 차지했습니다.\n\n박재원은 오늘 강원도 춘천 송암스포츠타운 에어돔에서 열린 결승전에서 이란의 알리아크바르 에브라히미를 라운드 점수 2대 1로 꺾고 우승했습니다.\n\n그는 1회전을 내줬으나 2회전을 큰 점수 차로 가져오며 승부를 원점으로 돌렸습니다.\n\n마지막 3회전에선 경기 막판 몸통, 머리 공격을 연거푸 성공하며 점수 차를 벌렸습니다.\n\n박재원은 \"외국 선수와 경기를 치른 건 처음\"이라며 \"마지막까지 최선을 다하자는 마음으로 집중한 것이 좋은 결과로 이어졌다\"고 소감을 밝혔습니다.\n\n여자 68㎏급에 출전한 임예림(효정고)은 하나 로우드바리(이란)와 결승에서 라운드 점수 0대 2로 패해 은메달을 획득했습니다.\n\n(사진=세계태권도연맹 제공, 연합뉴스)",
                    "article_image": null,
                    "article_createat": "2024-10-05"
                },
                {
                    "article_id": 49,
                    "article_title": "맨유 떠나길 잘했다!...&quot;생애 첫 국가대표 발탁, 우리 모두 행복하다&quot;",
                    "article_url": "https://m.sports.naver.com/wfootball/article/411/0000053154",
                    "article_content": "사진=게티이미지\n\n\n[포포투=이종관]\n\n막시 오예델레가 맨체스터 유나이티드를 떠나 뛰어난 활약을 펼치고 있다.\n\n2004년생, 폴란드 국적의 오예델레는 맨유 '성골 유스' 출신의 미드필더다. 지난 2022년에 1군 무대로 콜업된 그는 곧바로 잉글랜드 내셔널리그(5부 리그) 올트링엄 FC로 임대를 떠났고, 복귀 이후 프리미어리그2(2군 리그) 무대를 오가며 실전 경험을 쌓기 시작했다.\n\n그러나 동포지션의 쟁쟁한 경쟁자들을 뚫지 못했고 1군 데뷔는 미뤄지기 시작했다. 2023-24시즌 역시 대부분의 시간을 2군에서 보냈고 더 많은 출전 기회를 얻기 위해 내셔널리그 포레스트 그린 로버스 FC로 또다시 임대를 택했다.\n\n결국 올 시즌을 앞두고 맨유를 떠났다. 행선지는 폴란드 '명문' 레기아 바르샤바. 합류와 동시에 꾸준한 출전 기회를 얻은 그는 현재 3경기에 나서 안정적인 활약을 펼치고 있다.\n\n소속 팀에서의 활약을 바탕으로 커리어 첫 A 대표팀에도 선발됐다. 이에 곤살루 페이우 감독은 \"오예델레는 정말 믿을 수 없는 재능을 가지고 있다. 그는 국가대표팀에 발탁된 이후에도 전혀 들뜨거나 하지 않았다. 그의 발탁은 우리 모두의 노력의 결과다. 축구는 팀 스포츠기 때문이다. 우리 모두 그의 발탁 소식에 행복하다\"라며 극찬했다.",
                    "article_image": "https://imgnews.pstatic.net/image/411/2024/10/05/0000053154_001_20241005224312719.jpg?type=w647",
                    "article_createat": "2024-10-05"
                },
                {
                    "article_id": 48,
                    "article_title": "발차기 공격 성공하는 박재원",
                    "article_url": "https://m.sports.naver.com/general/article/001/0014965919",
                    "article_content": "(서울=연합뉴스) 태권도 기대주 박재원(경북체고)이 5일 강원도 춘천 송암스포츠타운 에어돔에서 열린 춘천 2024 세계태권도연맹(WT) 세계주니어선수권대회 남자 73㎏급 결승전에서 이란의 알리아크바르 에브라히미를 상대로 발차기 공격에 성공하고 있다. 2024.10.5 [세계태권도연맹 제공. 재배포 및 DB 금지]\n\nphoto@yna.co.kr",
                    "article_image": "https://imgnews.pstatic.net/image/001/2024/10/05/PYH2024100504830000700_P4_20241005224820936.jpg?type=w647",
                    "article_createat": "2024-10-05"
                }
            ]
        }
    }
    ```
    

## 🔎 뉴스 세부정보 가져오는 API

<aside>
**호출 URL:** /news/getNews/{news_id}      **호출 메서드:** GET

</aside>

**요청 헤더(비로그인시 해당없음):**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| news_id | int |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 뉴스 조회 성공 ✅ | news,
comments(본인 댓글일시 host값이 True) |
| 404 | 뉴스 조회 실패 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:  API 호출 시 조회수 1 증가(차후 다른 용도 사용시 검토)*

- 응답예시
    
    ```json
    /news/getNews/14
    {
        "status": 200,
        "message": "뉴스 조회 성공",
        "data": {
            "news": {
                "article_id": 14,
                "article_title": "[바이오게시판] 제이엘케이, 20% 무상증자 추진 등",
                "article_content": "제이엘케이./뉴스1\n\n\n\n        ■의료 인공지능(AI) 기업인 제이엘케이는 미국 진출에 앞선 사전 준비 작업으로 기존 10주당 2주의 신주를 배정하는 무상증자를 추진 중이라고 4일 밝혔다. 오는 16일까지 본주를 추가 매수하면 누구나 무상증자를 받을 수 있다. 무상증자의 신주배정 기준일은 18일, 무상증자 신주상장 예정일은 다음 달 6일이다. 제이엘케이는 미국 시장에서의 성공적인 안착을 목표로 하고 있으며, 지속적인 연구 개발과 사업 확장을 계획하고 있다.■엔지켐생명과학은 급성방사선증후군(ARS) 치료 후보물질 EC-18이 방사선 조사에 의한 위장관계 손상에 효능을 입증했다는 비임상 연구논문이 미국 방사선연구학회가 발간하는 SCI급 학술지인 ‘방사선 연구(Radiation Research)’에 게재됐다고 4일 밝혔다. 엔지켐생명과학은 연구결과를 바탕으로 미 식품의약국(FDA)의 규칙에 따라 위장관계 급성방사선증후군(GI-ARS)으로 확장한 임상 2상을 미국 국립알레르기·전염병연구소(NIAID), 피폭실험 위탁수행 전문기관 SRI와 함께 진행할 계획이다.■동국제약은 치질 치료제 치센 기존 모델인 전현무와 다양한 예능프로그램에 함께 출연하며 뇌섹남 케미를 보여준 배우 김지석을 새롭게 모델로 기용한 신규 TV 광고를 방송했다고 4일 밝혔다. 먹는 치질약 치센(캡슐)은 유럽에서 개발된 식물성 플라보노이드 구조인 디오스민(diosmin) 성분의 치질 치료제다. 이번 CF는 김지석이 말 못 할 고민 치질을 친한 형 전현무에게 털어놓고 조언을 얻는 설정으로 제작됐다.■바이오시밀러 제조업체인 프레스티지바이오파마는 오는 8~10일 이탈리아 밀라노에서 열리는 ‘2024 세계 제약·바이오 전시회(CPHI Worldwide 2024)’와 9~11일 일본 요코하마에서 열리는 ‘바이오 재팬(BIO Japan 2024)’에 참가한다고 4일 밝혔다. 프레스티지바이오파마는 CPHI Worldwide 2024에 올해 27평 규모의 단독 부스를 꾸린다. 바이오 재팬에는 이번에 처음 참가해 미국 생물보안법 대체 수요를 겨냥할 계획이다.■노을은 AI 기반 소프트웨어 의료기기 및 카트리지가 인도네시아 보건국으로부터 의료기기 시판허가를 획득했다고 4일 밝혔다. 노을의 혈액 분석 제품에 대한 아세안 국가 대상 첫 시판 허가이다. 노을은 혈액 분석과 말라리아 진단 보조용 소프트웨어 및 카트리지를 통해 글로벌 시장 공략에 속도를 낼 계획이다. 현재 노을은 동남아시아국가연합(ASEAN) 국가 중 인도네시아, 말레이시아, 필리핀 대상 시판 허가를 확보했으며, 태국, 베트남을 포함한 타 주요국 인증도 마무리 단계에 있다.■국가임상시험지원재단(KoNECT)은 보건복지부, 식품의약품안전처와 오는 29∼31일 서울 용산구 서울드래곤시티에서 ‘2024 KoNECT 국제 콘퍼런스’(KIC)를 개최한다고 4일 밝혔다. 아시아 최대 규모의 임상 시험 콘퍼런스로, 치매 치료제 ‘레켐비’를 개발한 일본 에자이와 비만 치료제 ‘마운자로’를 개발한 미국 제약사 일라이 릴리의 고위 인사가 기조 강연에 나선다. 이밖에 글로벌 규제 동향과 신약 개발 이슈를 다루는 다양한 강연과 제약·바이오 관련 학과 학생을 위한 채용박람회가 열린다.",
                "article_url": "https://n.news.naver.com/mnews/article/366/0001021883?sid=101",
                "article_views": 2,
                "article_createat": "2024-10-04",
                "article_like": 0,
                "article_image": "https://imgnews.pstatic.net/image/366/2024/10/04/0001021883_001_20241004170508798.jpg?type=w800",
                "article_scrap": 0,
                "article_summary": null
            },
            "comments": [
                {
                    "comment_id": 1,
                    "comment_content": "2",
                    "comment_createat": "2024-10-08",
                    "user_nickname": "test",
                    "user_id": 1,
                    "host": false // api호출 시 Bearer 토큰을 보내면 해당 사용자가 댓글의 주인일 때 true
                }
            ]
        }
    }
    ```
    

## 📜 조회수 순 뉴스 조회 API

<aside>
**호출 URL:** /news/highestViews      **호출 메서드:** GET

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 조회수 별 뉴스 조회 성공 ✅ | data |
| 404 | 오늘의 뉴스가 존재하지 않습니다. ❌ | null |
| 404 | 조회수 별 뉴스 조회 실패 ❌ | null |

*참고:  오늘 기준 조회수 높은 순으로 10개씩 조회*

## 💖뉴스 좋아요 API

<aside>
**호출 URL:** /news/like      **호출 메서드:** POST

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| article_id | int |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 좋아요 성공 ✅ | data(좋아요 수) |
| 201 | 좋아요 취소 성공 ✅ | data(좋아요 수) |
| 404 | 좋아요 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:  좋아요인 경우 취소됨 (토글형식)*

## 💓 좋아요한 뉴스 보여주는 API

<aside>
**호출 URL:** /news/likeNewsLists      **호출 메서드:** GET

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 뉴스 조회 성공 ✅ | data(좋아요 뉴스 리스트) |
| 404 | 뉴스 조회 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:*  

## 🧾 뉴스 스크랩 API

<aside>
**호출 URL:** /news/scrap      **호출 메서드:** POST

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| article_id | int |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 스크랩 성공 ✅ | data(스크랩 수) |
| 201 | 스크랩 취소 성공 ✅ | data(스크랩 수) |
| 404 | 스크랩 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:  스크랩한 경우 스크랩 취소*

## 📚 스크랩한 뉴스 보여주는 API

<aside>
**호출 URL:** /news/scrapNewsLists      **호출 메서드:** GET

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 뉴스 조회 성공 ✅ | data |
| 404 | 뉴스 조회 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:*  

## 📝 뉴스 댓글 작성 API

<aside>
**호출 URL:** /news/createComment      **호출 메서드:** POST

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| article_id | int |
| comment_content | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 댓글 작성 성공 ✅ | null |
| 403 | 댓글 작성 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:*  

## 🔃 뉴스 댓글 수정 API

<aside>
**호출 URL:** /news/changeComment      **호출 메서드:** POST

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| comment_id | int |
| comment_content | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 댓글 수정 성공 ✅ | null |
| 403 | 유저 정보 불일치 ❌ | null |
| 403 | 댓글 수정 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:*  

## 🚬 뉴스 댓글 삭제 API

<aside>
**호출 URL:** /news/deleteComment      **호출 메서드:** DELETE

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| comment_id | int |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 댓글 삭제 성공 ✅ | null |
| 403 | 유저 정보 불일치 ❌ | null |
| 403 | 댓글 삭제 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:*  

## 🔀 개인정보 변경 API

<aside>
**호출 URL:** /users/changeinfo      **호출 메서드:** PUT

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| status | int |
| data | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 개인정보 변경 성공 ✅ | null |
| 404 | 개인정보 변경 실패 ❌ | null |
| 401 | access_token만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:  status에 따라 변경 정보가 다릅니다 100은 닉네임 변경, 200은 전화번호 변경, 300은 비밀번호 변경입니다.*

## 🔑 자동로그인 토큰 발급 API

<aside>
**호출 URL:** /users/autologinToken      **호출 메서드:** POST

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | auto_token 발급 성공 ✅ | auto_token |
| 401 | access_token만료 ❌ | null |

*참고:*  

## 단일 뉴스 요약 API

<aside>
**호출 URL:** /summary/{article_id}      **호출 메서드:** GET

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| article_id | int |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 요약 성공 ✅ | data |
| 404 | 요약 실패 ❌ | null |

*참고:*  

## 키워드 별 추천 뉴스 요약 API

<aside>
**호출 URL:**/recommend/{keyword}      **호출 메서드:** GET

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| keyword | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 요약 성공 ✅ | data |
| 404 | 요약 실패 ❌ | null |

*참고:*  **키워드 별 3개씩 뉴스를 요약하여 반환**

## 뉴스 검색 API

<aside>
**호출 URL:**/search/{searchText}      **호출 메서드:** GET

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| keyword | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 검색 성공 ✅ | data |
| 404 | 검색 실패 ❌ | null |

*참고:*  **뉴스 제목과 본문 중에 포함된 검색어를 기준으로 10개 반환**

## 아이디 찾기 API

<aside>
**호출 URL:** /users/findID      **호출 메서드:** POST

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| user_name | str |
| user_number | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 아이디 찾기 성공 ✅ | email |
| 403 | 아이디 찾기 실패 ❌ | null |

*참고:*  

## 비밀번호 재설정 API

<aside>
**호출 URL:** /users/resetPassword      **호출 메서드:** POST

</aside>

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| user_email | str |
| user_name | str |
| user_number | str |
| new_password | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 비밀번호 변경 성공 ✅ | null |
| 403 | 비밀번호 변경 실패 ❌ | null |
| 418 | 대상 정보가 없습니다 ❌ | null |

*참고:*

## 프로필 이미지 조회 API

<aside>
**호출 URL:** /users/profileImage      **호출 메서드:** GET

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 200 | 이미지 조회 성공 ✅ | img_str |
| 403 | 이미지 조회 실패 ❌ | null |
| 401 | access_token 만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:  base64로 인코딩된 string 형태로 이미지를 보냅니다.*

## 프로필 이미지 수정 API

<aside>
**호출 URL:** /users/profileImageChange      **호출 메서드:** POST

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**요청 파라미터:**

| 이름 | 형식 |
| --- | --- |
| imagedata | formdata |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 이미지 수정 성공 ✅ | null |
| 403 | 이미지 수정 실패 ❌ | null |
| 401 | access_token 만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:  form-data 객체로 이미지전송 바랍니다.*

## 회원탈퇴 API

<aside>
**호출 URL:** /users/secession      **호출 메서드:** DELETE

</aside>

**요청 헤더:**

| 이름 | 형식 |
| --- | --- |
| access_token | str |

**응답:**

| status | message | data |
| --- | --- | --- |
| 201 | 회원탈퇴 성공 ✅ | null |
| 404 | 회원탈퇴 실패 ❌ | null |
| 401 | access_token 만료 ❌ | null |
| 404 | 유저 조회 실패 ❌ | null |

*참고:*
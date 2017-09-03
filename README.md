# 사내 도서관리 웹어플리케이션 구현
> 사내 도서관리 웹어플리케이션을 구현하며 Django를 학습합니다.

## 기능개요
- 도서 검색 및 DB 등록 (네이버 검색 API 활용)
- 도서 대여 및 연체관리
  - 대여 / 반납 기능
  - 연체시 email, slack을 통한 알림
- 구매 희망도서 신청
- Celery를 활용한 비동기 작업처리 및 백그라운드 작업 스케줄링
- 도서목록 csv 다운로드
- 유저간 쪽지 교환 기능

## 연습내용
> 구현 중 새롭게 알게된 것 유용하다고 생각한 부분들을 블로그에 정리합니다. 
 
- [네이버 검색 Open API를 이용하여 책 검색하기](https://wayhome25.github.io/python/2017/07/15/naver-search-api/)
- [slack을 활용한 신규도서, 반납도서 알림](https://wayhome25.github.io/django/2017/09/03/django-slack-bot/)
- BaseUserManager, AbstractBaseUser 상속을 통한 User 모델 확장
- [Coalesce를 사용하여 aggregate가 None을 반환하는 것을 방지하기](https://wayhome25.github.io/django/2017/09/02/django-queryset-aggregate-coalesce/)
- email을 활용한 인증방식 적용 (username > email)
- [imagekit 라이브러리를 활용한 이미지 처리](https://wayhome25.github.io/django/2017/05/11/image-thumbnail/)
- 개발환경 PostgreSQL 적용

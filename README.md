# 사내 도서관리 웹어플리케이션 구현
> 사내 도서관리 웹어플리케이션을 구현하며 Django를 학습합니다.

## 기능개요
- 도서 검색 및 DB 등록 (네이버 검색 API 활용)
- 도서 대여 및 연체관리
  - 대여 / 반납 기능
  - 연체시 email, slack을 통한 알림
- 구매 희망도서 신청

## 목표
- [Two Scoops of Django](https://www.twoscoopspress.com/products/two-scoops-of-django-1-11)에서 공부한 내용을 적용한다.
- OPEN API를 활용한다.
- [AskDjango 해커톤](https://nomade.kr/moim/askdjango-hackathon-2017/) 참여에 앞서서 원하는 기능 구현을 미리 연습해본다.   

## 연습내용
- [네이버 검색 API](https://developers.naver.com/docs/common/openapiguide/)
- BaseUserManager, AbstractBaseUser 상속을 통한 User 모델 확장
- email을 활용한 인증방식 적용 (username > email)
- [imagekit 라이브러리를 활용한 이미지 처리](https://wayhome25.github.io/django/2017/05/11/image-thumbnail/)
- 개발환경 PostgreSQL 적용

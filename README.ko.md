# 차량 판매 시각화와 기회 연구

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

사용자가 명시한 출력 언어를 따르고, 지정이 없으면 요청 언어를 따릅니다. 명령, 스킬 ID, JSON 키, 열거값, 단위와 원문 인용은 유지합니다. 번역과 원문을 구분하고 언어로 국가, 통화, 관할을 추정하지 않습니다. 전체 명세의 관련 자료를 읽고 기존 검증과 권한 조건을 적용합니다.

## 설치와 사용

저장소를 내려받거나 복제한 뒤 아래 스킬 디렉터리를 기존 references, scripts, assets 등과 함께 호스트의 스킬 디렉터리에 복사합니다. 이름과 SKILL.md는 유지합니다. 문서 언어만 바꾸는 경우 재설치할 필요가 없습니다. 설치 명령은 선택지이며 설치 또는 활성화 완료를 뜻하지 않습니다.

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## 차량 판매 시각화와 기회 연구

`vehicle-sales-opportunity`

자동차·오토바이·UTV·ATV·보트의 기존 수량 자료를 시각화하고 동기간 비교와 근거 기반 기회 조사를 설계합니다.

스킬 디렉터리: `skills/vehicle-sales-opportunity`

**구현 근거와 의존성**

허가된 자료·시장/달력 기간/지표/단위, Python 3.10+ 표준 라이브러리와 화면 검사용 브라우저. 핵심 오프라인은 계정/API가 없으며 검증은 제품·사용자·호환·원가 근거가 필요합니다.

**입력**

필수 월별 dataset JSON·대응 기준 월·새 출력 위치. 선택 임계값·브리프·근거. 결측·assetType·metricKind 유지, 연간/분기를 월별로 균등 분할하지 않습니다.

**출력**

dashboard.html, analysis.json, opportunities.json, report.md, qa.json 및 별도 research-review.md. 후보·산술 PASS는 수요·호환·ROI 입증이 아닙니다.

[실행 절차 · 제약과 중단 조건 · 요청 예시](skills/vehicle-sales-opportunity/references/i18n/ko.md)

> 다음 스킬을 사용하세요: `$vehicle-sales-opportunity` — 미국·캐나다·멕시코1~6월을 전년 동월과 비교하되 판매+30%를 액세서리 수요+30%로 보지 않습니다. 한국어로 답하고 근거, 미확인 사항과 작업 권한을 유지하세요.

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## 언어 지원과 검증

이 문서는 목적, 전제, 입출력, 절차, 예시와 제약을 다루는 한국어 운영 가이드이며 모든 참고 문서의 문장별 번역은 아닙니다. 상세 기술 자료, 과거 사례, 스크립트 오류, 예제 화면과 이미지는 원래 언어를 유지합니다. 요청 시 해당 언어로 설명할 수 있습니다. 구조, 링크와 핵심 제약을 확인했으나 각 언어 원어민 교정은 수행하지 않았습니다.

전달 전에 입력, 근거, 결측값, 출력 파일과 원래 완료 기준을 대조합니다. 실행하지 않은 단계는 미검증으로 표시하며 스크립트의 정상 종료를 업무 검증 성공으로 취급하지 않습니다.

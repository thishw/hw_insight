# 파이프라인 발행 검증 체크리스트

> 작성 배경: 2026-07-07 발행된 `content/posts/2026-07-07-fable-intelligence-retail-era.md`("지능의 소매 시대")는
> **엔진 synthesizer를 거치지 않은 손글**이라, Synapse의 #90(pubcore 경로)·#91(DB 영속화)·#92(synthesizer
> Sources v2 생성)가 이 발행 건으로는 실전 검증되지 않았다. 3b 카운터도 이 건으로는 미증가(0건 유지) —
> pubcore 경유 실발행이 아니므로. 다음 **진짜 파이프라인 발행**(synthesizer→pubcore 경유) 시 아래 4항목을
> 확인한다. 이 문서는 체크리스트일 뿐이며, 실제 파이프라인 발행 실행이나 DB 접근은 이 작업 범위에 포함하지 않는다.

## 검증 항목

1. **#92 Sources v2 생성**
   - synthesizer가 `<details class="sources">` 블록을 규약대로 생성했는가.
   - 형식 불일치 warning 로그 유무 확인: `grep -i "sources.*mismatch\|형식 불일치" <봇로그>`.
   - summary의 카운트 `(N)`이 실제 `<li>` 개수와 자동으로 일치하는가.

2. **#91 DB 영속화**
   - 발행 후 해당 레코드의 `published_url` / `published_at`이 실제 저장됐는가 (`flag_modified` 픽스의 첫 실검증).

3. **#90 경로/gate**
   - `gate_version` 기록 확인.
   - byte parity 확인 (기존 E2E는 byte-for-byte 일치했음).

4. **3b 카운터**
   - 무장애로 발행되면 **1건째**로 카운트 → Syndicator에 통지(건수·무장애 여부).
   - 3b 발동 조건 재확인: 무장애 발행 ≥5건 **AND** 2026-07-21 경과 시.

## 범위 안내

- 이 문서는 **체크리스트 문서화만** 수행한 결과물이다.
- 실제 파이프라인 발행 실행, DB 접근, Synapse 엔진/`src/output`/pubcore/PUBLISHING_CONTRACT/Syndicator 레포 변경은
  이 작업의 범위 밖이며 수행하지 않았다.

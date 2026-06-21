# hw_insight 빌드 검증 보고서

**작성일**: 2026-06-22  
**목적**: Hugo Module cross-account import 검증 및 로컬 빌드 확인

---

## 1. 환경

| 항목 | 버전 |
|------|------|
| Hugo | v0.163.3+extended darwin/arm64 |
| Go | go1.26.4 darwin/arm64 |
| OS | macOS (darwin/arm64) |

Hugo는 기존 설치(`Homebrew`). Go는 이번 작업 중 `brew install go`로 신규 설치.

---

## 2. 파일 트리

```
hw_insight/
├── .github/
│   └── workflows/
│       └── hugo.yaml          # GitHub Pages 워크플로 (Go setup 포함)
├── .gitignore                 # public/, resources/_gen/, .hugo_build.lock
├── README.md
├── content/
│   ├── _index.md              # 홈 페이지
│   └── posts/
│       ├── _index.md          # 포스트 목록
│       └── 2026-06-20-hello.md  # 샘플 글 (표+blockquote+mermaid)
├── go.mod                     # module github.com/This-HW/hw_insight
├── go.sum                     # 모듈 해시 (커밋 대상)
└── hugo.toml                  # 설정 (module import 포함)
```

레이아웃 파일 없음. 모두 `github.com/thishw/synapse-hugo-shared` Module에서 import.

---

## 3. hugo mod get 결과 (cross-account Module fetch)

```
go: downloading github.com/thishw/synapse-hugo-shared v0.0.0-20260621154912-1095233ee786
go: added github.com/thishw/synapse-hugo-shared v0.0.0-20260621154912-1095233ee786
hugo: collected modules in 1260 ms
```

**cross-account public import 성공** — `github.com/thishw` (공용 레포)를 `github.com/This-HW` 사이트에서 import.

---

## 4. 빌드 결과

```
hugo --gc --minify

Start building sites …
hugo v0.163.3+extended+withdeploy darwin/arm64

              │ KO
──────────────┼────
 Pages        │ 10
 Paginator    │  0
 Non-page     │  0
 Static       │  0
 Images       │  0
 Aliases      │  0
 Cleaned      │  0

Total in 34 ms
```

에러 없이 `public/` 생성 완료.

---

## 5. 검증 3종

검증 대상 파일: `public/posts/knowledge-system-first-principles/index.html`

### (a) Mermaid render hook

```bash
grep -c 'class=mermaid\|class="mermaid"' public/posts/.../index.html
# → 1  (PASS)
```

출력: `<pre class=mermaid>graph TD...` — 공통 Module의 `layouts/_markup/render-codeblock-mermaid.html` render hook이 적용됨.  
`<script type=module>` import mermaid from CDN 도 함께 삽입됨 (baseof.html의 `hasMermaid` 조건 통과).

> Note: `--minify` 옵션으로 빌드 시 HTML 속성 값에 따옴표가 제거됨(`class=mermaid`). grep 패턴을 양쪽 모두 검사해 통과.

### (b) Table

```bash
grep -c '<table' public/posts/.../index.html
# → 1  (PASS)
```

### (c) Blockquote

```bash
grep -c '<blockquote' public/posts/.../index.html
# → 1  (PASS)
```

**레이아웃을 공통 Module에서 가져왔는데도 3종 모두 정상 렌더 → cross-account import 검증 성공.**

---

## 6. go.mod / go.sum 내용 요약

**go.mod**
```
module github.com/This-HW/hw_insight

go 1.26.4

require github.com/thishw/synapse-hugo-shared v0.0.0-20260621154912-1095233ee786 // indirect
```

**go.sum** (2줄, 커밋 완료)
```
github.com/thishw/synapse-hugo-shared v0.0.0-20260621154912-1095233ee786 h1:RfD/6AdGt...
github.com/thishw/synapse-hugo-shared v0.0.0-20260621154912-1095233ee786/go.mod h1:Mhqc...
```

go.sum은 `.gitignore`에 포함하지 않았으며, 초기 커밋에 포함됨.

---

## 7. 참조 URL

- Hugo Modules 사용: https://gohugo.io/hugo-modules/use-modules/
- module imports 설정: https://gohugo.io/configuration/module/
- GitHub Pages 배포: https://gohugo.io/host-and-deploy/host-on-github-pages/
- setup-go Action: https://github.com/actions/setup-go

---

## 8. 초기 커밋

```
commit 312eb67
feat: initial hw_insight Hugo site with shared layout module

 9 files changed, 186 insertions(+)
```

**push는 하지 않았음.** 레포 생성 및 remote push는 상위 컨트롤러(This-HW 계정)가 처리.

---

## 9. 미결사항

| 항목 | 상태 | 메모 |
|------|------|------|
| GitHub Pages 활성화 | 미완 | This-HW 계정에서 레포 생성 후 Settings > Pages 설정 필요 |
| go-version CI 정합 | 확인 필요 | `go.mod`는 `go 1.26.4`, CI workflow는 `go-version: "1.22"` 지정 — 상위 호환이므로 동작하나 맞추는 것 권장 |
| `baseURL` placeholder | 정상 | GitHub Actions 워크플로가 `steps.pages.outputs.base_url`로 런타임 대체 |
| synapse-hugo-shared 버전 고정 | 확인 필요 | 현재 pseudo-version(commit hash) 고정. 공식 tag 배포 시 `go.mod`를 semver로 갱신 권장 |

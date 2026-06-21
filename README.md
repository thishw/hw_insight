# hw_insight

Synapse가 자동 발행하는 인사이트 블로그 사이트.

## 구조

- **콘텐츠**: `content/posts/` — Synapse 봇이 자동 push
- **레이아웃**: `github.com/thishw/synapse-hugo-shared` Hugo Module에서 import
- **배포**: GitHub Pages (`.github/workflows/hugo.yaml`)

## 레이아웃 모듈

레이아웃은 이 레포에 없다. `github.com/thishw/synapse-hugo-shared` public 모듈에서 Hugo Module import로 가져온다.
공통 레이아웃 변경은 해당 레포에서 관리한다.

## 로컬 빌드

```bash
# 의존성 fetch
hugo mod get github.com/thishw/synapse-hugo-shared

# 빌드
hugo --gc --minify

# 개발 서버
hugo server
```

## 워크플로

```
Synapse 봇 → content/posts/ push → GitHub Actions → GitHub Pages 배포
```

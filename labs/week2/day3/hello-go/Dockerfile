# 1단계: 빌드 전용 — Go 컴파일러가 든 큰 이미지
FROM golang:1.27 AS build
WORKDIR /src
COPY go.mod main.go ./
RUN CGO_ENABLED=0 go build -o /hello .

# 2단계: 실행 전용 — 아무것도 없는 빈 이미지에 결과물(실행 파일)만 복사
FROM scratch
COPY --from=build /hello /hello
EXPOSE 8080
USER 10001
CMD ["/hello"]

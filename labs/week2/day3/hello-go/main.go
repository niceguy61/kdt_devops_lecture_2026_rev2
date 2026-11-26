// 멀티 스테이지 빌드 맛보기용 아주 작은 웹 서버
package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	host, _ := os.Hostname()
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "안녕하세요! Go 컨테이너 %s 입니다\n", host)
	})
	fmt.Println("listening on :8080")
	http.ListenAndServe(":8080", nil)
}

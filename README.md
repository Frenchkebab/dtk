
```
rm -r dist
pyinstaller main.py 
cp -r result settings upload chromedriver.exe dist/main
cp -r dist/main /c/CLAIMX/mbk새버전
```

## 변경사항
- 모든 추가 파일들(업로드 등)은 UserFiles에 추가
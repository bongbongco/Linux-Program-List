#!/bin/bash

###########################################
##             user Function             ##
###########################################
function DirCro(){
#디렉터리 수집을 위한 LS-alR 명령어 함수 (R옵션 - 하위 디렉토리까지)
 local dir=$1
echo "###   Directory Crawling Start($dir)   ###"
echo "###   Directory Crawling Start($dir)   ###" >> "$FileName"
ls -alR "$dir" >> "$FileName"
echo "###   Directory Crawling END($dir)   ###" >> "$FileName"
echo "###   Directory Crawling End($dir)   ###"
}



###########################################
##                 Main                  ##
###########################################

echo $HOSTNAME #호스트명 출력

wasdirrun=0
adddirrun=0
defaultrun=1


defaultdir_arr=("/tmp" "/usr" "/opt")  #default 옵션 시 디렉토리 기본 수집 경로 설정

while getopts ":w:a:d:" opt; do   #명령줄 내 옵션 값 체크 및 추가된 수집 경로 설정
  case "$opt" in
    w)
      wasdir_arr=(${OPTARG//,/ })
      wasdirrun=1
      defaultrun=0
    ;;
    a)
     adddir_arr=(${OPTARG//,/ })
      adddirrun=1
      defaultrun=0
    ;;
    d)
      defaultrun=1
    ;;
    \?)
      echo "usage: ProgramList_vx.x.sh -w waspath -a addpath -d"
      echo "-w : 수집할 웹루트 디렉토리 콤마(,)로 구분"
      echo "-a : 추가 수집할 디렉토리 콤마(,)로 구분"
      echo "-d : 추가 및 웹 루트 수집 없이 실행 시 (/usr,/tmp)"
      echo " ex) ./ProgramList_vx.x.sh -d"
      echo " ex) ./ProgramList_vx.x.sh -w /tmp,/usr/was,/usr/local/tmocat/ -a /tmp,/etc"
      exit 1
    ;;
  esac
done

if [ "$1" = ""  ]; then  
      echo "usage: ProgramList_vx.x.sh -w waspath -a addpath -d"
      echo "-w : 수집할 웹루트 디렉토리 콤마(,)로 구분"
      echo "-a : 추가 수집할 디렉토리 콤마(,)로 구분"
      echo "-d : 추가 및 웹루트 수집 없이 실행 시(/usr,/tmp)"
      echo " ex) ./ProgramList_vx.x.sh -d"
      echo " ex) ./ProgramList_vx.x.sh -w /tmp,/usr/was,/usr/local/tmocat/ -a /tmp,/etc"
      exit 1 
fi


#IP 주소 저장
IP=$(hostname -I)

#IP 주소 내 공백 제거
IP=$(echo $IP | tr -d "s")

#파일 명 생성 호스트_아이피.txt
FileName=$HOSTNAME'_'"$IP".txt

echo "###   Process List start(ps -ef)   ###"
echo "###   Process List Start(ps -ef)   ###" > "$FileName"
ps -ef >> "$FileName"
echo "###   Process List END   ###" >> "$FileName"
echo "###   Process List END   ###"

echo "###   RPM List Start(rpm -qa)   ###"
echo "###   RPM List Start(rpm -qa)   ###" >> "$FileName"
rpm -qa >> "$FileName"
echo "###   RPM List END   ###" >> "$FileName"
echo "###   RPM List END   ###"


if [ "$wasdirrun"  -eq 1 ];then  #wasdir(-w) 옵션 시 추가된 경로 설정
  input_arr+=("${wasdir_arr[@]}")
fi

if [ "$adddirrun" -eq 1 ]; then #adddir(-a) 옵션 시 추가된 경로 설정
  input_arr+=("${adddir_arr[@]}")   
fi

input_arr+=("${defaultdir_arr[@]}")  #default(-d) 옵션 시 설정 된 경로 설정

for value_arr in "${input_arr[@]}"; do   #추가 경로의 파일 및 디렉토리 정보 수집
  echo $value_arr
  DirCro $value_arr  #사용자 정의 함수 호출
done

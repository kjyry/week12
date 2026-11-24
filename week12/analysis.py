from pathlib import Path
import sys

import pandas as pd


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def 정제(df):
    """원본을 고치지 않고 데이터를 정제한다."""
    result = df.copy()

    print("진단표와 대조")
    print("단계                 예상 행 수  실제 행 수  대조")

    print(f"시작: {len(result)}행")

    result = result.dropna(subset=["점수"])  # 빈 점수 행을 삭제한다.
    expected = 108 if len(df) == 114 else None
    status = "일치" if expected is not None and len(result) == expected else (
        "대조 기준 없음" if expected is None else "불일치"
    )
    print(f"빈 칸 제거 후: {len(result)}행")
    print(f"  예상 108행 / 실제 {len(result)}행 / {status}" if expected is not None else f"  실제 {len(result)}행")

    result = result.drop_duplicates()  # 완전히 같은 중복 행을 하나만 남긴다.
    expected = 104 if len(df) == 114 else None
    status = "일치" if expected is not None and len(result) == expected else (
        "대조 기준 없음" if expected is None else "불일치"
    )
    print(f"중복 제거 후: {len(result)}행")
    print(f"  예상 104행 / 실제 {len(result)}행 / {status}" if expected is not None else f"  실제 {len(result)}행")

    result["반"] = result["반"].str.strip()  # 반의 앞뒤 공백을 제거한다.
    result["과목"] = result["과목"].str.strip()  # 과목의 앞뒤 공백을 제거한다.

    result["점수"] = pd.to_numeric(result["점수"], errors="coerce")
    result = result[result["점수"].between(0, 100)]  # 0~100 범위를 벗어난 행을 삭제한다.
    expected = 100 if len(df) == 114 else None
    status = "일치" if expected is not None and len(result) == expected else (
        "대조 기준 없음" if expected is None else "불일치"
    )
    print(f"범위 밖 제거 후: {len(result)}행")
    print(f"  예상 100행 / 실제 {len(result)}행 / {status}" if expected is not None else f"  실제 {len(result)}행")

    return result


def 반별평균(df):
    """반별 개수, 평균, 중앙값, 최댓값을 표로 출력하고 평균 딕셔너리를 반환한다."""
    통계표 = df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)
    통계표.columns = ["개수", "평균", "중앙값", "최댓값"]
    print(통계표)
    return 통계표["평균"].to_dict()


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    df = pd.read_csv(base_dir / "scores_2026.csv")

    정제_df = 정제(df)

    수학_df = 정제_df[정제_df["과목"] == "수학"]
    print(f"수학 행 수: {len(수학_df)}")

    일반_df = 정제_df[(정제_df["반"] == "1반") & (정제_df["점수"] >= 90)]
    print(f"1반 90점 이상 행 수: {len(일반_df)}")

    print("반별 점수 평균:")
    print(정제_df.groupby("반")["점수"].mean())

    print("과목·반별 점수 평균:")
    print(정제_df.groupby(["과목", "반"])["점수"].mean())

    반별평균(정제_df)
'''
# ① 필터링
정제된 df에서 과목이 '수학'인 행만 남기는 코드를 한 줄로 써라.
그리고 남은 행 수를 print 하라.
'''
수학_df = 정제_df[정제_df["과목"] == "수학"]
print(f"수학 행 수: {len(수학_df)}")

'''
② 그룹화
정제된 df를 '반'으로 묶어 점수 평균을 내는 코드를 써라.
그다음 '과목'과 '반' 두 기준으로 묶는 코드도 따로 써라.
'''
print("반별 점수 평균:")
print(정제_df.groupby("반")["점수"].mean())

print("과목·반별 점수 평균:")
print(정제_df.groupby(["과목", "반"])["점수"].mean())

'''
③ 통계
'반'으로 묶어 개수 · 평균 · 중앙값 · 최댓값을 한 표로 내는
코드를 써라. 소수 둘째 자리까지 반올림하라.
'''
print("반별 통계:")
print(정제_df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2))

'''
# ② 합계 일치 — 묶어도 총합은 변하지 않아야 합니다
df.groupby("반")["점수"].sum().sum()   # 7484.0
df["점수"].sum()                        # 7484.0    ← 같아야 합니다

df.groupby("반")["점수"].count().sum()  # 100
len(df)                                 # 100       ← 같아야 합니다
'''
반별점수합계 = 정제_df.groupby("반")["점수"].sum().sum()
전체점수합계 = 정제_df["점수"].sum()
assert 반별점수합계 == 전체점수합계
print(f"반별 점수 합계 합: {반별점수합계:.1f}")
print(f"전체 점수 합계: {전체점수합계:.1f}")

반별행수합계 = 정제_df.groupby("반")["점수"].count().sum()
전체행수 = len(정제_df)
assert 반별행수합계 == 전체행수
print(f"반별 행 수 합계: {반별행수합계}")
print(f"전체 행 수: {전체행수}")

'''
# ④ 스팟 체크 — 결과 표에서 한 칸을 골라 원본에서 직접 셉니다
df[(df["반"]=="1반") & (df["과목"]=="수학")]["점수"]
  → 여덟 개의 값이 나옵니다. 계산기로 더해서 8로 나눠 보세요.
  → groupby 결과의 60.0 과 같습니까?
'''
df_1반_수학 = 정제_df[(정제_df["반"] == "1반") & (정제_df["과목"] == "수학")]
print(f"1반 수학 점수: {df_1반_수학['점수'].tolist()}")

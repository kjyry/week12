from pathlib import Path

import pandas as pd

from analysis import 정제


base_dir = Path(__file__).resolve().parent
scores_df = pd.read_csv(base_dir / "scores_2026.csv")
mini_df = pd.read_csv(base_dir / "mini.csv")


def test_scores_정제_100행():
    assert len(정제(scores_df)) == 100


def test_반값은_1반과_2반만():
    정제_df = 정제(scores_df)
    assert set(정제_df["반"].unique()) == {"1반", "2반"}


def test_반별점수합계는_전체점수합계와같음():
    정제_df = 정제(scores_df)
    반별합계 = 정제_df.groupby("반")["점수"].sum().sum()
    assert 반별합계 == 정제_df["점수"].sum()


def test_mini_1반평균은_80():
    정제_df = 정제(mini_df)
    assert 정제_df.groupby("반")["점수"].mean()["1반"] == 80.0

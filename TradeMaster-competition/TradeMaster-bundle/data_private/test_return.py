import pandas as pd
import numpy as np

df_1 = pd.read_csv(
    "/home/sunshuo/qml/Competition/competition-examples/TradeMaster-competition/TradeMaster-bundle/data_public/test_input/test_input_1.csv",
    index_col=0)
df_1_next = pd.read_csv(
    "/home/sunshuo/qml/Competition/competition-examples/TradeMaster-competition/TradeMaster-bundle/data_private/next_test_input_1.csv",
    index_col=0)
df_2 = pd.read_csv(
    "/home/sunshuo/qml/Competition/competition-examples/TradeMaster-competition/TradeMaster-bundle/data_public/test_input/test_input_2.csv",
    index_col=0)
df_2_next = pd.read_csv(
    "/home/sunshuo/qml/Competition/competition-examples/TradeMaster-competition/TradeMaster-bundle/data_private/next_test_input_2.csv",
    index_col=0)

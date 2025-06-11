import os
import pandas as pd
import numpy as np

def baseline():
    path = input("データのフォルダパスを入力してください: ")
    path = path.strip('"')

    if (not os.path.exists(path)) or (not os.path.isdir(path)):
        print("フォルダが存在しません。最初に戻ります!!\n")
        return

    path_list = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if 'log' in filename:
                print(f"{filename}はログファイルとして認識されました。処理をスキップします")
                continue
            path_list.append(os.path.join(path, filename))


    for i, filepath in enumerate(path_list):
        df = pd.read_csv(filepath, comment='#', header=None, engine='python', encoding='cp932', sep=None)
        basedf = df[(1380 <= df[0]) & (df[0] <= 1420)]
        df[1] = df[1] - np.median(basedf[1])
        df.to_csv(os.path.splitext(filepath)[0] + '_baseline.txt', index=False, header=False)


if __name__ == "__main__":
    baseline()
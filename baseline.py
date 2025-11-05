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
        basedf = df[(1390 <= df[0]) & (df[0] <= 1430)]
        df[1] = df[1] - np.mean(basedf[1])
        df.to_csv(os.path.splitext(filepath)[0] + '_baseline.txt', index=False, header=False)

def ave_filter():
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
        df[1] = df[1].rolling(window=9, center=True).mean()
        df.dropna(inplace=True)
        df.to_csv(os.path.splitext(filepath)[0] + '_avefilter.txt', index=False, header=False)


if __name__ == "__main__":
    print("ベースライン補正を行う場合は「b」を入力してください/n"
          "移動平均フィルタをかける場合は「f」を入力してください")

    mode = input("モードを入力してください: ").strip().lower()
    if mode == 'b':
        baseline()
    elif mode == 'f':
        ave_filter()
    else:
        print("無効な入力です。プログラムを終了します。")

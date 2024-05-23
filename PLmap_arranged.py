import os
import numpy as np
from numpy.lib.function_base import meshgrid
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize

# 22/11/21 金田さんより
# 読み込むファイルがascかtxtか注意

Extension = '.txt' #拡張子txtかascか
start_wl = 500
end_wl = 840
interval = 10
bandwidth = interval
if_smoothing = True

# 各種設定（波長情報はおいおい自動化したい）
def get_parameter():
    global start_wl, end_wl, interval, bandwidth, if_smoothing
    print('励起波長範囲[nm](500 840など)：', end='')
    start_wl, end_wl = map(int, input().split(' '))
    print('励起波長測定間隔[nm]：', end='')
    interval = int(input())
    bandwidth = interval
    print('smoothing?(y/n)：', end='')
    ans = input()
    if ans == 'y':
        if_smoothing = True
    else:
        if_smoothing = False
    return 0

def read_asc():
    # 指定したフォルダ内のtxtファイル名のリストアップ
    # osによって区切り文字が違う
    if os.name == 'nt':
        slash = '\\'
    elif os.name == 'posix':
        slash = '/'
    print('フォルダのパスを入力してください：', end='')
    dir = input().strip('"') # windowsの「パスをコピー」ボタンでは""がついてきてしまうため
    asc_list = []
    for name in os.listdir(dir):
        if Extension in name:
            asc_list.append(name[:-4])

    # print('dir')
    # print(dir)
    # print('asc_list')
    # print(asc_list)

    # ascファイルの中身を読み込み，データの成型
    for i, name in enumerate(asc_list):
        # print('name')
        # print(name)
        # tmp_df = pd.read_csv(dir + slash + name + '.txt', index_col=0, header=None)
        # tmp_df = pd.read_csv(dir + slash + name + '.asc', sep='\t', index_col=0, header=None, usecols=[1,2]) #読み込み先のファイル形式，データ形式に合わせて変える
        tmp_df = pd.read_csv(dir + slash + name + Extension, index_col=0, header=None, encoding="shift-jis", skiprows=9)  # 読み込み先のファイル形式，データ形式に合わせて変える
        # tmp_df = tmp_df.drop(tmp_df.columns[[0]], axis=1)
        # print('tmp_df')
        # print(tmp_df)
        tmp_df.columns = [name]
        # print(tmp_df)
        if i == 0:
            df = tmp_df
        else:
            df = pd.merge(df, tmp_df, left_index=True, right_index=True)
    df.sort_index(axis=0, ascending=True, inplace=True)
    df.sort_index(axis=1, ascending=True, inplace=True)
    print(df)
    df_col = np.arange(start_wl, end_wl + interval, interval)
    print(df_col)
    # print(df.shape[1])
    # print(df_col.shape[0])
    if df.shape[1] != df_col.shape[0]: #励起波長の範囲・間隔が，データの個数と一致していないとエラー
        print('Error：励起波長の範囲と間隔が不適切です')
    df.columns = np.arange(start_wl, end_wl + interval, interval)
    df = df.T

    return df

# スムージング処理
def smooth(df):
    df_ret = df.copy()
    smoothed_wl = np.linspace(start_wl, end_wl, 512)
    for wl in smoothed_wl:
        if not wl in df.index:
            df_ret.loc[wl] = np.NaN
    df_ret.sort_index(axis=0, ascending=True, inplace=True)
    df_ret.interpolate(inplace=True)
    return df_ret

if __name__ == '__main__':
    # 描画用データの用意
    get_parameter()
    df = read_asc()
    if if_smoothing:
        df = smooth(df)
    x = df.columns
    y = df.index
    yticks = np.arange(start_wl, end_wl + interval, interval*2)
    X, Y = np.meshgrid(x, y)
    Z = df.values

    # グラフ描画
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, aspect='equal')
    # contour = ax.pcolormesh(X, Y, Z, cmap='rainbow', shading='auto', norm=Normalize(vmin=0, vmax=3000))
    contour = ax.pcolormesh(X, Y, Z, cmap='rainbow', shading='auto', norm=Normalize(vmin=250, vmax=2000)) #コンター図のカラーバー調整

    # カラーバー調整用
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    pp = fig.colorbar(contour, cax=cax, orientation='vertical')

    ax.set_yticks(yticks)
    ax.set_xlabel('Emission Wavelength [nm]')
    ax.set_ylabel('Excitation Wavelength [nm]')
    ax.grid()
    plt.show()

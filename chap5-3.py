import tkinter
# ウインドウ作成
root = tkinter.Tk()
root.title("棒グラフをソートして表示する")
# キャンバス配置
canvas = tkinter.Canvas(root, width=640, height=480)
canvas.create_rectangle(40, 40, 600, 440, fill="gray78")
canvas.pack()
# グラフ用変数
start_x = 60
start_y = 60
width_px = 5
height_px = 32
distance_px = 4
# リスト
list = [70, 15, 66, 21, 19, 97, 33, 44, 30, 2]
# disp = ""
# 繰り返し処理
for k in range(len(list) - 1, 0, -1):
    # print(str(10 - k) + "度目")
    for j in range(0, k):
        if list[j] > list[j+1]:
            temp = list[j]
            list[j] = list[j+1]
            list[j+1] = temp
        x = start_x
        y = start_y
        canvas.delete("graph")
        for i in list:
            canvas.create_rectangle(x, y, x + i * width_px, y + i * height_px, fill="blue", outline="blue", tag="graph")
            y = y + height_px + distance_px
            # disp = disp + str(i) + " "
        # print(disp)
        # disp = ""
root.mainloop()
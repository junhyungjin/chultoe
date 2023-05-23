import tkinter as tk
import datetime
from tkinter import messagebox
from tkinter import ttk

root = tk.Tk()
root.title("오늘도 화이링 💪")

time_label = tk.Label(root, text="")
time_label.grid(row=0, column=0, sticky='ew')

after_id = None
start_time = None
end_time = None

hour_combo = ttk.Combobox(root, width=5, values=[str(i) for i in range(7,17)])
hour_label = tk.Label(root, text="시")

minute_combo = ttk.Combobox(root, width=5, values=[str(i) for i in range(60)])
minute_label = tk.Label(root, text="분")

halfday_var = tk.BooleanVar(value=False)
halfday_checkbox = tk.Checkbutton(root, text="반차", variable=halfday_var)

def remaining_time():
    global end_time
    now = datetime.datetime.now()
    if now > end_time:
        overwork = now - end_time
        overwork_str = str(overwork).split('.')[0]
        return " 추가 근무 중 🫠" + overwork_str
    else:
        remaining = end_time - now
        remaining_str = str(remaining).split('.')[0]
        return " 탈출 남은 시간 🥹: " + remaining_str

def update_time():
    time_label.config(text=" 출근 시간: " + start_time.strftime("%Y-%m-%d %H:%M:%S") +
                             "\n 퇴근 시간: " + end_time.strftime("%Y-%m-%d %H:%M:%S") +
                             "\n " + remaining_time())
    if not end_time_reached:
        after_id = root.after(1000, update_time)
        #root.after(1000, update_time)

def start_work():
    global start_time, end_time, end_time_reached
    end_time_reached = False
    after_id = root.after(1000, update_time)

    if hour_combo.get() == '' or minute_combo.get() == '':
        start_time = datetime.datetime.now()
    else:
        hour = int(hour_combo.get())
        minute = int(minute_combo.get())
        start_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    if halfday_var.get():
        end_time = start_time + datetime.timedelta(hours=4)
        if end_time.hour > 13 and start_time.hour < 12:
            end_time += datetime.timedelta(hours=1)
    else:
        end_time = start_time + datetime.timedelta(hours=9)
    time_label.config(text="시작 시간: " + start_time.strftime("%Y-%m-%d %H:%M:%S") +
                             "\n종료 시간: " + end_time.strftime("%Y-%m-%d %H:%M:%S"))
    update_time()

def check_time():
    global end_time
    if end_time is not None:
        now = datetime.datetime.now()
        if (end_time - now).total_seconds() <= 600:
            messagebox.showinfo("알림", "종료 시간 10분 전입니다.")
            
def end_work():
    global end_time_reached, after_id
    end_time_reached = True
    # 이전에 등록한 root.after() 호출을 취소
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None
    messagebox.showinfo("탈 출!!! 🥳", " 수고했어 오늘도 👍 ")
        


start_button = tk.Button(root, text="근무 시작", command=start_work)
start_button.grid(row=4, column=0)

end_button = tk.Button(root, text="탈 출!!! 🥳", command=end_work)
end_button.grid(row=5, column=0)

hour_combo.grid(row=1, column=0)
hour_label.grid(row=1, column=0, sticky='e')
minute_combo.grid(row=2, column=0)
minute_label.grid(row=2, column=0, sticky='e')

halfday_checkbox.grid(row=3, column=0)

root.after(1000, check_time)
root.mainloop()

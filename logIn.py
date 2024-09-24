import tkinter as tk

win_login = tk.Tk()
win_login.title("User Login")
win_login.geometry('500x500')
win_login.configure(bg='#333333')




#WIDGET CREATION
lbl_login = tk.Label(win_login,text="Login",bg="#333333")
lbl_username = tk.Label(win_login,text="Username",bg="#333333")
ent_username = tk.Entry(win_login,)
lbl_password = tk.Label(win_login,text="Password")
ent_password = tk.Entry(win_login,show="*")
btn_login = tk.Button(win_login,text="Login",bg="#333333")

#PLACE THE WIDGETS ON SCREEN
lbl_login.grid(row = 0, column = 0, columnspan=2)
lbl_username.grid(row = 1, column = 0)
ent_username.grid(row =1, column = 1)
lbl_password.grid(row = 2, column = 0)
ent_password.grid(row = 2, column = 1)
btn_login.grid(row = 3, column = 0, columnspan=2)


win_login.mainloop()

#
#
#
#
#
#
#
#
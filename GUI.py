import tkinter 
import chatbot
from tkinter import *
root = tkinter.Tk()
def Ask():
    input = text_box.get("1.0",'end-1c').strip()
    text_box.delete("0.0",END)
    if input != "":
        ChatLog.config(state= NORMAL)
        ChatLog.insert(END, "Ti: " + input + '\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        rez = str(chatbot.message(input))
        ChatLog.insert(END, "Gimpi : " + rez + '\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)



root.geometry("800x970")
root.title("Pričaj sa gimnazijom")
root.resizable(width="False", height="False")
label = tkinter.Label(root, text="Pitaj gimnaziju", font = ('Arial',22))
label.pack(padx= 20, pady = 20)
ChatLog = Text(root, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)
scrollbar = Scrollbar(root, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set


text_box = tkinter.Text(root, font=('Arial',16))


btn = tkinter.Button(root, text="Pitaj me", font=('Arial',18) ,command= Ask)

scrollbar.place(x=373 * 2,y=6, height=386 * 2) 
ChatLog.place(x=6,y=6, height=386 * 2, width=370 * 2)
text_box.place(x=128, y=802 , height=90, width=265 * 2)
btn.place(x=6, y=802, height=90)


root.mainloop()

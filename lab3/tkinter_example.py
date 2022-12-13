import tkinter as tk

window = tk.Tk()

label = tk.Label(
    text="Привет, Tkinter!",
    fg="white",
    bg="black",
    width=20,
    height=10
)

label.pack()
window.mainloop()
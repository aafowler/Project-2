from gui2 import *



def main(): 
    master = tk.Tk()
    master.title('Poll')
    master.geometry('350x310')
    master.resizable(False, False)
    VotingApp(master)

    
    
    master.mainloop()


if __name__ == '__main__':
    main()

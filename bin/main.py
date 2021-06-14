# Default UI requirements
import tkinter as tk
import tkinter.font as tkf
from tkinter import ttk

# Model requirements
import re
import torch
import pandas as pd
from transformers import BertTokenizer
import torch.nn.functional as F


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.kamus_alay = self._load_dataset()
        self.w2i, self.i2w = {'positive': 1, 'negative': 0}, {1: 'Positive!', 0: 'Negative~'}
        self.tokenizer = BertTokenizer.from_pretrained('./lib/tokenizer/indobert-base-p1-v1')
        self.model = torch.load("./lib/model/model_v1_87_11.pkl", map_location='cpu')
        self.preprocessed_text = ""

        # Base Class
        self.title('AntiHate')
        self.geometry('900x650')
        self.iconbitmap('assets/jokris-toungue.ico')
        self.resizable(width=False, height=False)


        # Style sideload
        self.style = ttk.Style(self)
        self._load_themes()
        self.style.theme_use('azure')


        # Default style config
        self.header1 = tkf.Font(family="Comic Sans MS", size=24)
        self.header2 = tkf.Font(family="Comic Sans MS", size=12)
        self.subheader = tkf.Font(family="Comic Sans MS", size=10)
        basepad = (5,5,5,5)


        # First title section frame
        self.frame1 = ttk.Frame(self, padding=basepad)
        self.frame1.place(x=120, y=12)

        ttk.Label(self.frame1, text="\" AntiHate \"", font=self.header1, foreground="#343a40").pack()
        ttk.Label(self.frame1, text="Aplikasi pendeteksi ujaran kebencian dalam \nbahasa Indonesia berbasis artificial intelligence", 
            font=self.header2, justify=tk.CENTER, foreground="#334443").pack()


        # Second row section frame
        self.frame2 = ttk.Labelframe(self, padding=basepad, text="Input Your Text:")
        self.frame2.place(x=33, y=120)

        self.entry = ttk.Entry(self.frame2, width=70)
        self.entry.pack(padx=10, pady=10)

        self.btn = ttk.Button(self.frame2, text='Apply Preprocessing', command=self._preprocess).pack(padx=10, pady=10)


        # Preprocess section frame
        self.frame3 = ttk.Labelframe(self, padding=basepad, text="Preprocessing")
        self.frame3.place(x=33, y=265)

        ttk.Label(self.frame3, text="After unecessary char removal:", 
            font=self.subheader, width=65, foreground="#343a40").pack()
        self.preprocessing_tb = tk.Text(self.frame3, height=3, width=65, font=self.subheader)
        self.preprocessing_tb.insert(tk.END, '-')
        self.preprocessing_tb.configure(state='disabled')
        self.preprocessing_tb.pack(pady=5)

        ttk.Label(self.frame3, text="After kamus alay cleanup:", 
            font=self.subheader, width=65, foreground="#343a40").pack()
        self.preprocessing_tb_2 = tk.Text(self.frame3, height=3, width=65, font=self.subheader)
        self.preprocessing_tb_2.insert(tk.END, '-')
        self.preprocessing_tb_2.configure(state='disabled')
        self.preprocessing_tb_2.pack(pady=5)
        
        ttk.Label(self.frame3, text="After emoticon byte removal:", 
            font=self.subheader, width=65, foreground="#343a40").pack()
        self.preprocessing_tb_3 = tk.Text(self.frame3, height=3, width=65, font=self.subheader)
        self.preprocessing_tb_3.insert(tk.END, '-')
        self.preprocessing_tb_3.configure(state='disabled')
        self.preprocessing_tb_3.pack(pady=5)
        self.btn1 = ttk.Button(self.frame3, text='Make Prediction', command=self._predict, state="disabled")
        self.btn1.pack(padx=10, pady=10)

        # Output Section frame
        self.frame4 = ttk.Labelframe(self, padding=basepad, text="Prediction Output")
        self.frame4.place(x=600, y=200)
        ttk.Label(self.frame4, text="Hate Speech:", font=self.header2, justify=tk.CENTER, foreground="#343a40", width=25).pack()
        self.labelPred = ttk.Label(self.frame4, text="None", font=self.header1, justify=tk.CENTER, foreground="#77acf1")
        self.labelPred.pack()
        ttk.Label(self.frame4, text="Confidence:", font=self.header2, justify=tk.CENTER, foreground="#343a40", width=25).pack()
        self.labelConf = ttk.Label(self.frame4, text="None", font=self.header1, justify=tk.CENTER, foreground="#77acf1")
        self.labelConf.pack()

        # Creds Label
        self.frame5 = ttk.Labelframe(self, padding=basepad, text="Credits")
        self.frame5.place(x=600, y=380)
        ttk.Label(self.frame5, text="Created By:", font=self.header2, justify=tk.CENTER, foreground="#343a40", width=25).pack()
        ttk.Label(self.frame5, text="2301860154 - Jonathan Kristanto", 
            font=self.subheader, foreground="#343a40").pack()
        ttk.Label(self.frame5, text="2301865741 - Edgard Jonathan P. P", 
            font=self.subheader, foreground="#343a40").pack()
        ttk.Label(self.frame5, text="2301859650 - Cornelius Tantius", 
            font=self.subheader, foreground="#343a40").pack()

    def _load_dataset(self):
        df = pd.read_csv('lib/dataset/alay_dict.csv', names = ['original', 'replacement'], encoding='latin-1')
        return dict(zip(df['original'], df['replacement']))
    def _load_themes(self):
        self.tk.call('source', 'lib/default/azure.tcl')
    
    # Preprocess steps
    def _remove_unecessary_char(self, text):
        text = text.replace("\n", " ")
        text = re.sub('\\+n', ' ', text)
        text = re.sub('\n'," ",text) # Remove every '\n'
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
        text = re.sub('\\+n', ' ', text)
        text = re.sub('\n'," ",text) # Remove every '\n'
        text = text.replace("\\", " ")
        text = re.sub(' n ', ' ', text)
        text = re.sub('  +', ' ', text) # Remove extra spaces
        return text
    def _normalize_alay(self, text):
        alay_dict_map = self.kamus_alay
        return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])
    def _remove_emoticon_byte(self, text):
        text = text.replace("\\", " ")
        text = re.sub('x..', ' ', text)
        text = re.sub(' n ', ' ', text)
        text = re.sub('\\+', ' ', text)
        text = re.sub('  +', ' ', text)
        return text

    def _preprocess(self):
        self.labelPred.configure(text="None")
        self.labelConf.configure(text="None")
        self.set_neuts()
        txt = self.entry.get()
        txt = self._remove_unecessary_char(txt)
        self.preprocessing_tb.configure(state="normal")
        self.preprocessing_tb.delete("1.0","end")
        self.preprocessing_tb.insert(tk.END, txt)
        self.preprocessing_tb.configure(state="disabled")
        txt = self._normalize_alay(txt)
        self.preprocessing_tb_2.configure(state="normal")
        self.preprocessing_tb_2.delete("1.0","end")
        self.preprocessing_tb_2.insert(tk.END, txt)
        self.preprocessing_tb_2.configure(state="disabled")
        txt = self._remove_emoticon_byte(txt)
        self.preprocessing_tb_3.configure(state="normal")
        self.preprocessing_tb_3.delete("1.0","end")
        self.preprocessing_tb_3.insert(tk.END, txt)
        self.preprocessing_tb_3.configure(state="disabled")
        self.btn1.configure(state="normal") 
        self.preprocessed_text = txt
    
    def _predict(self):
        txt = self.preprocessed_text
        self.preprocessed_text = ""
        self.btn1.configure(state="disabled")

        subwords = self.tokenizer.encode(txt)
        subwords = torch.LongTensor(subwords).view(1, -1).to(self.model.device)
        logits = self.model(subwords)[0]
        label = torch.topk(logits, k=1, dim=-1)[1].squeeze().item()
        
        pred_res = self.i2w[label]
        pred_conf = f'{F.softmax(logits, dim=-1).squeeze()[label] * 100:.3f}%'

        self.labelPred.configure(text=pred_res)
        self.labelConf.configure(text=pred_conf)
        if label == 0:
            self.set_green()
        else:
            self.set_red()
        return 1
    
    def set_red(self):
        self.labelPred.configure(foreground="#f54748")
        self.labelConf.configure(foreground="#f54748")
    def set_green(self):
        self.labelPred.configure(foreground="#01937c")
        self.labelConf.configure(foreground="#01937c")
    def set_neuts(self):
        self.labelPred.configure(foreground="#77acf1")
        self.labelConf.configure(foreground="#77acf1")

        


if __name__ == "__main__":
    app = App()
    app.mainloop()

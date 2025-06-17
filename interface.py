import tkinter as tk
from tkinter import ttk, messagebox
import sys
from datetime import datetime

sys.path.insert(0, "..")
from sistema_bancario import depositar, sacar, obter_saldo, obter_extrato, get_numero_saques, get_limite_saques

def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

class BancoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏦 Cash Bank")
        self.geometry("420x580")
        self.configure(bg="#1e272e")
        self.resizable(False, False)
        self.data_hoje = datetime.now().date()

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), foreground="#fff", background="#34ace0")
        self.style.map("TButton", background=[("active", "#227093")])
        self.style.configure("TEntry", padding=5)

        self.create_widgets()
        self.atualizar_saldo()

    def create_widgets(self):
        tk.Label(self, text="Cash Bank 🪙", font=("Segoe UI", 18, "bold"),
                 bg="#1e272e", fg="#f7f1e3").pack(pady=20)

        self.lbl_saldo = tk.Label(self, text="Saldo: R$ 0,00", font=("Segoe UI", 16, "bold"),
                                  bg="#1e272e", fg="#2ed573")
        self.lbl_saldo.pack(pady=10)

        frm = tk.Frame(self, bg="#1e272e")
        frm.pack(padx=20, pady=10)

        tk.Label(frm, text="Valor (apenas números):", font=("Segoe UI", 12), bg="#1e272e", fg="#f1f2f6").grid(row=0, column=0, pady=5, sticky="e")
        self.valor_entry = ttk.Entry(frm, width=25)
        self.valor_entry.grid(row=0, column=1, pady=5, padx=10)

        btn_frame = tk.Frame(self, bg="#1e272e")
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="💰 Depositar", command=self.on_depositar).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="🏧 Sacar", command=self.on_sacar).grid(row=0, column=1, padx=10)
        ttk.Button(self, text="📋 Ver Extrato", command=self.on_extrato).pack(pady=10)

        self.status_label = tk.Label(self, text="", font=("Segoe UI", 10), bg="#1e272e", fg="#d2dae2", wraplength=380, justify="center")
        self.status_label.pack(pady=10)

    def atualizar_saldo(self):
        self.lbl_saldo.config(text=f"Saldo: {formatar_valor(obter_saldo())}")

    def ler_valor(self):
        valor_digitado = self.valor_entry.get()
        if not valor_digitado.isdigit():
            self.status_label.config(text="❌ Digite apenas números, sem pontos ou vírgulas.")
            return None
        return float(valor_digitado)

    def on_depositar(self):
        v = self.ler_valor()
        if v is None:
            return

        ok, msg = depositar(v)
        if ok:
            self.atualizar_saldo()
            self.status_label.config(text=f"✅ {msg}")
        else:
            self.status_label.config(text=f"❌ {msg}")
        self.valor_entry.delete(0, tk.END)

    def on_sacar(self):
        v = self.ler_valor()
        if v is None:
            return

        numero_saques = get_numero_saques()
        limite_saques = get_limite_saques()

        if numero_saques >= limite_saques:
            self.status_label.config(text="❌ Número máximo de saques diários excedido.")
            return

        if v > 500:
            self.status_label.config(text="❌ Saques acima de R$ 500,00 não são permitidos pelo canal atual. Acesse o app ou vá até uma agência para ajustar seu limite.")
            return

        ok, msg = sacar(v)
        if ok:
            self.atualizar_saldo()
            self.status_label.config(text=f"✅ {msg}")
        else:
            self.status_label.config(text=f"❌ {msg}")
        self.valor_entry.delete(0, tk.END)

    def on_extrato(self):
        history = obter_extrato()
        if not history or len(history) == 0:
            messagebox.showinfo("Extrato", "Não foram realizadas movimentações.")
        else:
            linhas = []
            for linha in history:
                if "Depósito:" in linha or "Saque:" in linha:
                    try:
                        valor_str = linha.split("R$")[1].strip()
                        valor = float(valor_str)
                        label = "Depósito" if "Depósito" in linha else "Saque"
                        linhas.append(f"{label}: {formatar_valor(valor)}")
                    except:
                        linhas.append(linha)
            messagebox.showinfo("Extrato", "\n".join(linhas))

if __name__ == "__main__":
    app = BancoApp()
    app.mainloop()
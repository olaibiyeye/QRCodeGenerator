import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
from reportlab.pdfgen import canvas

# ---------- QR GENERATION FUNCTIONS ----------
def generate_qr(data, fill_color="black", back_color="white", size=10):
    """Generate a QR code with customization options."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    return qr.make_image(fill_color=fill_color, back_color=back_color)

def save_as_pdf(img, filename):
    """Export QR code directly as PDF."""
    img = img.convert("RGB")
    img.save("temp_qr.png")

    c = canvas.Canvas(filename)
    c.drawImage("temp_qr.png", 100, 500, width=200, height=200)
    c.save()

# ---------- GUI APPLICATION ----------
class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Tabs
        self.text_tab = ttk.Frame(self.notebook)
        self.wifi_tab = ttk.Frame(self.notebook)
        self.vcard_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.text_tab, text="Text / URL")
        self.notebook.add(self.wifi_tab, text="Wi-Fi")
        self.notebook.add(self.vcard_tab, text="vCard")

        # Customization options
        self.custom_frame = ttk.LabelFrame(root, text="Customization")
        self.custom_frame.pack(pady=10, fill="x")

        ttk.Label(self.custom_frame, text="Fill Color:").grid(row=0, column=0, padx=5, pady=5)
        self.fill_color = tk.Entry(self.custom_frame)
        self.fill_color.insert(0, "black")
        self.fill_color.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.custom_frame, text="Background Color:").grid(row=0, column=2, padx=5, pady=5)
        self.back_color = tk.Entry(self.custom_frame)
        self.back_color.insert(0, "white")
        self.back_color.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.custom_frame, text="Size:").grid(row=0, column=4, padx=5, pady=5)
        self.size = tk.Spinbox(self.custom_frame, from_=5, to=20, width=5)
        self.size.delete(0, "end")
        self.size.insert(0, "10")
        self.size.grid(row=0, column=5, padx=5, pady=5)

        # Preview frame
        self.preview_frame = ttk.LabelFrame(root, text="QR Preview")
        self.preview_frame.pack(pady=10)

        self.preview_label = tk.Label(self.preview_frame)
        self.preview_label.pack()

        # Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        ttk.Button(self.button_frame, text="Generate", command=self.generate).grid(row=0, column=0, padx=10)
        ttk.Button(self.button_frame, text="Save PNG", command=self.save_png).grid(row=0, column=1, padx=10)
        ttk.Button(self.button_frame, text="Save PDF", command=self.save_pdf).grid(row=0, column=2, padx=10)

        self.qr_img = None

        # Setup input forms
        self.setup_text_tab()
        self.setup_wifi_tab()
        self.setup_vcard_tab()

    # ------------------- Input Forms -------------------
    def setup_text_tab(self):
        ttk.Label(self.text_tab, text="Enter text or URL:").pack(pady=5)
        self.text_entry = tk.Entry(self.text_tab, width=40)
        self.text_entry.pack(pady=5)

    def setup_wifi_tab(self):
        ttk.Label(self.wifi_tab, text="SSID:").pack(pady=5)
        self.ssid_entry = tk.Entry(self.wifi_tab, width=30)
        self.ssid_entry.pack(pady=5)

        ttk.Label(self.wifi_tab, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.wifi_tab, width=30, show="*")
        self.password_entry.pack(pady=5)

        ttk.Label(self.wifi_tab, text="Encryption:").pack(pady=5)
        self.encryption = ttk.Combobox(self.wifi_tab, values=["WPA", "WEP", "nopass"])
        self.encryption.current(0)
        self.encryption.pack(pady=5)

    def setup_vcard_tab(self):
        ttk.Label(self.vcard_tab, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.vcard_tab, width=30)
        self.name_entry.pack(pady=5)

        ttk.Label(self.vcard_tab, text="Phone:").pack(pady=5)
        self.phone_entry = tk.Entry(self.vcard_tab, width=30)
        self.phone_entry.pack(pady=5)

        ttk.Label(self.vcard_tab, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.vcard_tab, width=30)
        self.email_entry.pack(pady=5)

    # ------------------- QR Code Generation -------------------
    def generate(self):
        tab = self.notebook.index(self.notebook.select())
        data = ""

        if tab == 0:  # Text/URL
            data = self.text_entry.get()
            if not data.strip():
                messagebox.showerror("Error", "Please enter text or a URL.")
                return

        elif tab == 1:  # Wi-Fi
            ssid = self.ssid_entry.get()
            password = self.password_entry.get()
            enc = self.encryption.get()
            if not ssid.strip():
                messagebox.showerror("Error", "Please enter SSID.")
                return
            data = f"WIFI:T:{enc};S:{ssid};P:{password};;"

        elif tab == 2:  # vCard
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            if not name.strip() or not phone.strip() or not email.strip():
                messagebox.showerror("Error", "Please fill in all vCard fields.")
                return
            data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"

        # Get customization values
        fill = self.fill_color.get()
        back = self.back_color.get()
        try:
            size = int(self.size.get())
        except ValueError:
            messagebox.showerror("Error", "Size must be a number.")
            return

        # Generate QR
        img = generate_qr(data, fill_color=fill, back_color=back, size=size)
        self.qr_img = img

        # Preview in GUI
        preview = img.resize((200, 200))
        self.tk_img = ImageTk.PhotoImage(preview)
        self.preview_label.config(image=self.tk_img)

    def save_png(self):
        if not self.qr_img:
            messagebox.showerror("Error", "Generate a QR code first.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            self.qr_img.save(filename)

    def save_pdf(self):
        if not self.qr_img:
            messagebox.showerror("Error", "Generate a QR code first.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            save_as_pdf(self.qr_img, filename)

# ---------- MAIN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()

import pytesseract  # Utilizzato per applicare OCR alle immagini e estrarre il testo
from PIL import Image  # Utilizzato per aprire e manipolare immagini (JPEG, PNG, ecc.)
from pdf2image import convert_from_path  # Utilizzato per convertire le pagine di un PDF in immagini
import re  # Utilizzato per lavorare con le espressioni regolari e catturare i dati dai testi estratti
import os  # Utilizzato per gestire le operazioni sul file system (come rimuovere file)
import pandas as pd  # Utilizzato per creare e gestire DataFrame per organizzare i dati estratti
from tkinter import Tk  # Utilizzato per nascondere la finestra principale di Tkinter
from tkinter.filedialog import askopenfilename  # Utilizzato per aprire una finestra di dialogo per selezionare un file PDF


# Funzione per estrarre il testo da un'immagine usando pytesseract
def extract_text_from_image(image_path):
    # Imposta il percorso di Tesseract manualmente se non è nel PATH
    img = Image.open(image_path)

    # Configura Tesseract con PSM 4
    custom_config = f'--psm 4'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

def formatta_valori(valore):
    if isinstance(valore, float):
        return f"{valore:.2f}".replace('.', ',')
    return valore

# Funzione per strutturare i dati estratti in colonne
def structure_extracted_data(extracted_text):
    data_processati = []  # Lista per i dati processati
    data_non_processati = []  # Lista per le righe non processate
    data_non_riconosciuti = []  # Lista per le righe con re errata
    processa_dati = False  # Flag per iniziare e fermare il processo di estrazione
    
    for page_text in extracted_text:
        lines = page_text.split("\n")
        for line in lines:
            line = line.strip()
            print(f"Riga estratta: {line}")  # Stampa per verificare cosa sta leggendo esattamente l'OCR

            # Inizia a processare dopo questa intestazione
            if ('Total (EUR)' in line or
                'Your reference' in line):
                processa_dati = True
                continue  # Salta questa riga, ma imposta il flag per iniziare a processare

            # Smetti di processare se trovi una di queste righe
            if ('Please note that third party payments' in line or
                'Pallet fee' in line or
                'Transport' in line):
                processa_dati = False
                continue  # Salta questa riga e smetti di processare le righe successive

            # Processa solo se il flag è True
            if processa_dati:

                pattern = re.compile(r'([\w\-]+)\s+.*?(\d+[,\.]?\d*)\s+liter\s+(\d+)\s+bottles?\s+(\d+[,\.]\d+)')

                # Esegui il regex per catturare Reference, Volume, Quantity, Price
                # match = re.match(r'([\w\-]+)\s+(.*?)\s+(\d+\.\d*\s+\w+)\s+(\d+\s+\w+)\s+(\d+\.\d+)', line)
                match = pattern.match(line)

                try:

                    # Estrarre i gruppi dal regex
                    anker_ref = match.group(1)  # Cattura l'Anker Ref
                    volume = match.group(2).replace(',', '.').strip()  # Converte la virgola in punto
                    quantity = match.group(3).strip()  # Quantità
                    price = float(match.group(4).replace(',', '.'))  # Prezzo per bottiglia
                    total = price * int(quantity)  # Calcola il totale
                    total_str = f"{total:.2f}".replace('.', ',')  # Converte il totale in stringa con virgola come separatore

                    # Determinare la descrizione per differenza
                    end_of_ref = match.end(1)
                    start_of_volume = match.start(2)
                    description = line[end_of_ref:start_of_volume].strip()
                    
                    # Aggiungi i dati processati alla lista
                    data_processati.append([anker_ref, description, volume, quantity, price, total_str])

                except Exception as e:
                    # In caso di errore (ad esempio, una riga spezzata), aggiungi ai non processati
                    print(f"Errore nella riga: {line}, errore: {e}")
                    data_non_riconosciuti.append(line)
            else:
                data_non_processati.append(line)

    return data_processati, data_non_processati, data_non_riconosciuti

# Funzione per selezionare il file PDF tramite dialog box
def select_pdf_file():
    Tk().withdraw()  # Nasconde la finestra principale di Tkinter
    pdf_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return pdf_path




#####################################################################################################################
# INIZIO CODICE MAIN METHOD #########################################################################################
#####################################################################################################################

# 1. Selezionare il PDF con una dialog box
pdf_path = select_pdf_file()  # Finestra di dialogo per selezionare il PDF

# Imposta il percorso di Poppler
poppler_path = r"C:\poppler\Library\bin"# Insert your output path here

# Imposta il percorso completo di Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\steph\AppData\Local\Programs\Tesseract-OCR\tesseract.exe" # Insert your output path here

if pdf_path:

    # Lista per memorizzare i percorsi delle immagini generate
    image_paths = []

    # 2. Convertire il PDF in immagini
    images = convert_from_path(pdf_path, poppler_path=poppler_path, dpi=450)

    # 3. Applicare l'OCR su ogni immagine
    extracted_text = []
    for i, image in enumerate(images):

        image_path = f'C:/Users/steph/Documents/images/immagine_{i+1}.png' # Insert your output path here
        image.save(image_path, 'PNG')
        # Aggiungi il percorso dell'immagine alla lista
        image_paths.append(image_path)
        # Apre l'immagine per usarla con Tesseract
        img = Image.open(image_path)

        # Estraggo il testo dalle immagini usando tesseract
        text = extract_text_from_image(image_path)

        # Aggiunge il testo alla lista creando una stringa unica
        extracted_text.append(text)

        # Chiudi l'immagine per rilasciare le risorse
        img.close()

    print(extracted_text)

    # 4. Strutturare i dati
    structured_data, unstructured_data, error_data = structure_extracted_data(extracted_text)

    # 5. Creare un DataFrame per organizzare i dati
    df = pd.DataFrame(structured_data, columns=["Anker Ref.", "Descrizione", "Volume", "Quantity", "Price", "Total"])

    # Applica la formattazione dei valori per Price e Total
    df['Price'] = df['Price'].apply(formatta_valori)
    df['Total'] = df['Total'].apply(formatta_valori)
    df['Volume'] = df['Volume'].apply(lambda v: v.replace('.', ','))  # Sostituisci i punti con virgole nei volumi

    # 6. Salvare i dati in un file CSV
    output_csv_path = r'C:\Users\steph\Desktop\test.csv'  # Insert your output path here
    df.to_csv(output_csv_path, index=False, sep=';')

    # 7. Salvare i dati non processati in un file TXT
    output_txt_path = r'C:\Users\steph\Desktop\dati_non_processati.txt'  # Insert your output path here
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for line in unstructured_data:
            f.write(line + '\n')

    # 8. Salvare i dati non riconosciuti in un file TXT
    output_txt_path = r'C:\Users\steph\Desktop\dati_non_riconosciuti.txt'  # Insert your output path here
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for line in error_data:
            f.write(line + '\n')

    # 9. Cancella le immagini create durante il processo
    for image_path in image_paths:
        try:
            os.remove(image_path)
            # print(f"Immagine cancellata: {image_path}")
        except OSError as e:
            print(f"Errore nella cancellazione dell'immagine {image_path}: {e}")

    print(f"I dati sono stati salvati in: {output_csv_path}")
    print()
else:
    print("Nessun file PDF selezionato.")
    print()
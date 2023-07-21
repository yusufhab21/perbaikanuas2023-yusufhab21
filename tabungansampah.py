from random import choices
from datetime import date
from json import load, dump
from os import path, getcwd, system
import json


def tambah_tabungan(idanggota, idsampah, kuantitas):
    with open(path.join(getcwd(), f"produksampah.json"), encoding="utf-8") as file:
        produk = load(file)
    
    while True:
        try:
            with open(path.join(getcwd(), f"tabungan{idanggota}.json"), encoding="utf-8") as file:
                history = load(file)
        except FileNotFoundError:
            ct = []
            history = []
            with open(path.join(getcwd(), f"tabungan{idanggota}.json"), "w") as file:
                dump(ct, file, indent= 4)


        if (idsampah, kuantitas) == (None, None):
            nota(idanggota)

            idsampah = input_pilihan("Pilih jenis sampah (Kode): ", ["1", "2", "3", "4"])

            while True:
                try:
                    kuantitas = float(input("Kuantitas sampah: "))
                    break
                except ValueError:
                    print("input yang anda masukkan tidak valid!")
        

        tanggal = date.today().strftime("%Y-%m-%d")
        while True:
            try:
                idtransaksi = generate_idtransaksi()
                assert idtransaksi not in [ ele["idtransaksi"] for ele in history ]
                break
            except AssertionError:
                continue
        
        nilaisatuan = produk[idsampah]["hargasatuan"]
        total = kuantitas * nilaisatuan
        saldo = total if len(history) == 0 else (history[-1]["saldo"] + total)

        transaksi = {
                "tanggal"       : tanggal,
                "idtransaksi"   : idtransaksi,
                "tipetransaksi" : "K",
                "sampah"        : idsampah,
                "kuantitas"     : kuantitas,
                "nilaisatuan"   : nilaisatuan,
                "total"         : total,
                "saldo"         : saldo
            }

        with open(path.join(getcwd(), f"tabungan{idanggota}.json"), "w") as file:
            history.append(transaksi)
            dump(history, file, indent= 4)
        
        print("Pencatatan transaksi tambah tabungan sampah berhasil.")

        input_2 = input_pilihan("Ada jenis sampah lain akan ditabung (Y/y=Ya, T/t=Tidak) ? : ", ["y", "Y", "T", "t"])
        
        if input_2 == "y" or input_2 == "Y":
            system("cls")
            idsampah, kuantitas = None, None
            continue
        elif input_2 == "t" or input_2 == "T": 
            break

        
def nominal(prompt:str, moneyparam:float):
    while True:
        try:
            amount = float(input(prompt))
            assert amount >= 0, "Uang tidak bisa bernilai negatif!"
            assert amount % 100 == 0, "Uang harus dalam kelipatan 100 rupiah!"
            assert amount < 10_000_000, "Uang terlalu besar!"
            assert moneyparam - amount >= 0, "saldo tidak cukup"
            break
        except ValueError:
            print("Masukkan nominal uang dengan benar")
        except AssertionError as er:
            print(er)
    return amount

def generate_idtransaksi():
    ls_num = "0123456789"
    return ''.join(choices(ls_num, k=7))

def get_saldo(idanggota):
    nota2(idanggota)
    
    while True:
        with open(path.join(getcwd(), f"tabungan{idanggota}.json"), encoding="utf-8") as file:
            history = load(file)
        
        saldo = history[-1]["saldo"]
        print(f"Saldo saat ini adalah           : Rp{saldo:,.2f}")
        
        tarik = nominal("Masukkan banyak uang ditarik    : ", saldo)
        saldo -= tarik
        print(f"Sisa saldo adalah               : Rp{saldo:,.2f}")
        
        tanggal = date.today().strftime("%Y-%m-%d")
        while True:
            try:
                idtransaksi = generate_idtransaksi()
                assert idtransaksi not in [ ele["idtransaksi"] for ele in history ]
                break
            except AssertionError:
                continue

        transaksi = {
                "tanggal"       : tanggal,
                "idtransaksi"   : idtransaksi,
                "tipetransaksi" : "D",
                "total"         : -tarik,
                "saldo"         : saldo
            }

        with open(path.join(getcwd(), f"tabungan{idanggota}.json"), "w") as file:
            history.append(transaksi)
            dump(history, file, indent= 4)

        print("Pencatatan transaksi tabungan sampah berhasil.")

        input2 = input_pilihan("Apakah anda ingin menarik saldo lagi? (Y/Y=Ya, T/t=Tidak) ? : ", ["y", "Y", "T", "t"])
        
        if input2 == "y" or input2 == "Y":
            system("cls")
            continue
        elif input2 == "t" or input2 == "T":
            break

def cari_harga(idsampah):
    with open("produksampah.json") as file:
        data = json.load(file)
        for item in data:
            if item["kode"] == idsampah:
                return item["hargaSatuan"]
    return 0       

def nota(idanggota):
    with open(path.join(getcwd(), "anggotas.json"), encoding="utf-8") as file:
        isi = load(file)
        data = isi[idanggota]
        
    print(f"""Penambahan Tabungan Sampah. 
Input ID Anggota : {idanggota} 
============================================= 
IDAnggota : {idanggota:<15} | Nama  : {data["nama"]} 
Telepon   : {data["telepon"]:<15} | Alamat: {data["alamat"]} 
============================================= 
--------------------------------------------- 
Kode    | Jenis Sampah  | Harga Satuan (Rp)     
--------------------------------------------- 
1       | Kardus        | 500      
2       | Botol plastic | 300 
3       | Logam besi    | 800 
4       | Tembaga       | 950 
---------------------------------------------""")
    
def nota2(idanggota):
    with open(path.join(getcwd(), "anggotas.json"), encoding="utf-8") as file:
        content = load(file)
        data = content[idanggota]
        
    print(f"""Penambahan Tabungan Sampah. 
Input ID Anggota : {idanggota} 
============================================= 
IDAnggota : {idanggota:<15} | Nama  : {data["nama"]} 
Telepon   : {data["telepon"]:<15} | Alamat: {data["alamat"]} 
=============================================""")

def tampilkan_tabungan(idanggota):
    nota2(idanggota)

    with open(path.join(getcwd(), f"tabungan{idanggota}.json"), encoding="utf-8") as file:
        history = load(file)

    tanggal = history[-1]["tanggal"]
    kode = history[-1]["idtransaksi"]
    jenis = history[-1]["tipetransaksi"]
    total = f'{history[-1]["total"]:,.2f}'
    saldo = f'{history[-1]["saldo"]:,.2f}'
    
    print(f"""Tanggal Transaksi Terakhir  : {tanggal} 
                Kode Transaksi Terakhir     : {kode} 
                Jenis Transaksi Terakhir    : {"Tabungan" if jenis == "K" else "Penarikan"}
                Nilai Transaksi Terakhir    : {total}
                Saldo Tabungan              : {saldo}""")
    
    input("Tekan enter untuk melanjutkan...")

def input_pilihan(prompt:str, ls_opt:list):
    while True:
        try:
            masuk = input(prompt)
            assert masuk.strip() in ls_opt, "Input tidak valid !"
            break
        except AssertionError as er:
            print(er)

    return masuk.strip()


def riwayat_tabungan(id_anggota):
    with open(path.join(getcwd(), f"tabungan{id_anggota}.json"), encoding="utf-8") as file:
        history = load(file)

    print("Riwayat Penambahan Tabungan atau Penarikan Tabungan:")
    print("=================================================")

    # Header penjurnalan
    print(f"{'Tanggal':<12} {'ID Transaksi':<15} {'Jenis Transaksi':<20} {'Penambahan':<12} {'Penarikan':<12} {'Saldo':<12}")
    print("-" * 80)

    saldo = 0
    for transaksi in history:
        tanggal = transaksi["tanggal"]
        idtransaksi = transaksi["idtransaksi"]
        tipetransaksi = transaksi["tipetransaksi"]
        total = transaksi["total"]

        jenis_transaksi = "Tabungan" if tipetransaksi == "K" else "Penarikan"
        if total >= 0:
            penambahan = f'Rp{abs(total):,.2f}'
            penarikan = ''
            saldo += total
        else:
            penambahan = ''
            penarikan = f'Rp{abs(total):,.2f}'
            saldo += total

        print(f"{tanggal:<12} {idtransaksi:<15} {jenis_transaksi:<20} {penambahan:<12} {penarikan:<12} Rp{saldo:,.2f}")

    input("Tekan enter untuk melanjutkan...")


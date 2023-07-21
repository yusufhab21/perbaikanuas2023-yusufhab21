import json
import random
import string
from datetime import date, datetime
import os
from os import path, getcwd, system
from json import load, dump


def tambah_anggota():
    nama = input("Masukkan nama anggota: ")
    alamat = input("Masukkan alamat anggota: ")
    telepon = input("Masukkan telepon anggota: ")
    
    id_anggota = generate_idanggota()
    
    file_path = os.path.join(os.path.dirname(__file__), 'anggotas.json')
    with open(file_path) as file:
        data_anggota = json.load(file)
    
    tanggal = date.today().strftime("%Y-%m-%d")
    
    anggota_baru = {
        "idanggota": id_anggota,
        "nama": nama,
        "alamat": alamat,
        "tanggal": tanggal,
        "telepon": telepon
    }
    
    data_anggota[id_anggota] = anggota_baru
    
    with open(file_path, 'w') as file:
        json.dump(data_anggota, file)
    
    print("Anggota baru telah ditambahkan:")
    print("ID Anggota:", id_anggota)
    print("Nama:", nama)
    print("Alamat:", alamat)
    print("Tanggal:", tanggal)
    print("Telepon:", telepon)

def generate_idanggota():
    file_path = os.path.join(os.path.dirname(__file__), 'anggotas.json')
    
    with open(file_path) as file:
        data_anggota = json.load(file)
    
    existing_ids = set(data_anggota.keys())
    new_id = ''.join(random.choices(string.digits, k=5))
    
    while new_id in existing_ids:
        new_id = ''.join(random.choices(string.digits, k=5))
    
    return new_id

def cari_anggota_by_id(id_anggota):
    file_path = os.path.join(os.path.dirname(__file__), 'anggotas.json')
    with open(file_path) as file:
        data_anggota = json.load(file)
    
    if id_anggota in data_anggota:
        return data_anggota[id_anggota]
    else:
        return {}

def tampilkan_anggota(anggota):
    if anggota:
        print("ID Anggota:", anggota['idanggota'])
        print("Nama:", anggota['nama'])
        print("Alamat:", anggota['alamat'])
        print("Telepon:", anggota['telepon'])
        print("Tanggal Daftar:", anggota['tanggal'])
    else:
        print("Tidak ada data anggota!")


def edit_anggota():
    while True:
        with open(path.join(getcwd(), "anggotas.json"), encoding="utf-8") as file:
            content = load(file)
        
        print("ketik ID anggota yang akan diedit : ")
        id_anggota = input()


        anggota = cari_anggota_by_id(id_anggota)
        
        if anggota == {}:
            print("Data anggota tidak ditemukan !")
            while True:
                try:
                    re_input = input("Cari lagi (Y/y = Ya, T/t = Tidak)?")
                    assert re_input.lower() in ["y", "t"], "Input tidak valid"
                    break
                except AssertionError as er:
                    print(er)
            
            if re_input.lower() == "y":
                system("cls")
            else:
                input("Tekan enter untuk kembali ke menu utama ")
                break
        else:
            id = anggota["idanggota"]
            nama = anggota["nama"]
            alamat = anggota["alamat"]
            telp = anggota["telepon"]
            
            nama_baru = input(f"Nama : {nama} -> ")
            if nama_baru.strip() != "":
                anggota["nama"] = nama_baru
                
            alamat_baru = input(f"Alamat : {alamat} -> ")
            if alamat_baru.strip() != "":
                anggota["alamat"] = alamat_baru
                
            telp_baru = input(f"Telepon : {telp} -> ")
            if telp_baru.strip() != "":
                anggota["telepon"] = f"+62{telp_baru}"
            
            content[id] = anggota
            
            with open("anggotas.json", "w") as file:
                dump(content, file, indent= 4)

            print("Data berhasil diubah")
            input("Tekan enter untuk melanjutkan ... ")
            break
    


def urut_tanggal():
    with open("anggotas.json", "r") as file:
        data = json.load(file)

        listId = list(data.keys())
        listId.sort(key=lambda x: datetime.strptime(data[x]['tanggal'], "%Y-%m-%d"))

        print("====================================")
        print("List Anggota Urut Berdasarkan Tanggal")
        print("====================================")
        for id in listId:
            anggota = data[id]
            print(f"Nama: {anggota['nama']}")
            print(f"Tanggal Bergabung: {anggota['tanggal']}")
            print("------------------------------")
        print("====================================")

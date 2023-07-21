import os
from anggota import tambah_anggota, cari_anggota_by_id, tampilkan_anggota, edit_anggota, urut_tanggal
from tabungansampah import tambah_tabungan, get_saldo, tampilkan_tabungan, riwayat_tabungan
from os import getcwd, listdir


def display_menu():
    print("** Program Pengelolaan Tabungan Sampah **")
    print("="*40)
    print("Pilih menu :")
    print("1. Pengelolaan Keanggotaan")
    print("    1a. Penambahan Data Anggota")
    print("    1b. Pencarian Data Anggota")
    print("    1c. Pengubahan Data Anggota")
    print("    1d. Tampilkan list Anggota secara berurutan") # tambahan perbaikan nilai (mengurutkan berdasarkan tanggal bergabung/daftar)
    print("2. Pengelolaan Tabungan Anggota")
    print("    2a. Penambahan Tabungan")
    print("    2b. Penarikan Tabungan")
    print("    2c. Menampilkan Data Tabungan")
    print("    2d. Pelaporan Transaksi") # tambahan perbaikan nilai (Pelaporan2 transaksi)
    print("3. Exit")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    try :
        clear_terminal()
        display_menu()
        
        pilihan = input("Masukkan pilihan Anda: ")
        
        if pilihan == '1a':
            clear_terminal()
            tambah_anggota()
            input("Tekan Enter untuk melanjutkan...")
        elif pilihan == '1b':
            clear_terminal()
            print("Pencarian data anggota.")
            id_anggota = input("Masukkan ID Anggota: ")
            hasil_pencarian = cari_anggota_by_id(id_anggota)
            clear_terminal()
            tampilkan_anggota(hasil_pencarian)
            input("Tekan Enter untuk melanjutkan...")
        elif pilihan == '1c':
            clear_terminal()
            edit_anggota()
        elif pilihan == '1d' :
            clear_terminal()
            urut_tanggal()
            input("Tekan Enter untuk melanjutkan...")
        elif pilihan == '2a':
            print("Penambahan Tabungan")
            id_anggota = input("Input ID Anggota: ")
            hasil_pencarian = cari_anggota_by_id(id_anggota)
            if hasil_pencarian == {}:
                print("ID yang anda input tidak valid")
                input("Tekan enter untuk melanjutkan ")
                continue
            
            print(f"""============================================= 
IDAnggota : {id_anggota:<15} | Nama  : {hasil_pencarian["nama"]} 
Telepon   : {hasil_pencarian["telepon"]:<15} | Alamat: {hasil_pencarian["alamat"]} 
============================================= 
--------------------------------------------- 
Kode    | Jenis Sampah  | Harga Satuan (Rp)     
--------------------------------------------- 
 1       | Kardus        |  500      
 2       | Botol plastic |  300 
 3       | Logam besi    |  800 
 4       | Tembaga       |  950
---------------------------------------------""")

            idsampah = input("Pilih jenis sampah (Kode): ")
            while True:
                try:
                    kuantitas = float(input("Kuantitas sampah: "))
                    break
                except ValueError:
                    print("input yang anda masukkan tidak valid!")
                    
            tambah_tabungan(id_anggota, idsampah, kuantitas)
        elif pilihan == '2b':
            print("Penarikan tabungan")
            id_anggota = input("Input ID Anggota: ")
            hasil_pencarian = cari_anggota_by_id(id_anggota)

            if hasil_pencarian == {}:
                print("ID tidak ditemukan !")
                input("Tekan enter untuk melanjutkan ")
                continue
                
            if f"tabungan{id_anggota}.json" not in listdir(getcwd()):
                print("Belum ada tabungan!")
                input("Tekan enter untuk melanjutkan ")
                continue

            get_saldo(id_anggota)
        elif pilihan == '2c':
                id_anggota = input("Masukkan ID Anggota : ")
                hasil_pencarian = cari_anggota_by_id(id_anggota)
                
                if hasil_pencarian == {}:
                    print("ID tidak ditemukan !")
                    input("Tekan enter untuk melanjutkan ")
                    continue
                
                if f"tabungan{id_anggota}.json" not in listdir(getcwd()):
                    print("Belum memiliki tabungan!")
                    input("Tekan enter untuk melanjutkan ")
                    continue

                tampilkan_tabungan(id_anggota)
        elif pilihan == '2d':
            id_anggota = input("Masukkan ID Anggota: ")
            hasil_pencarian = cari_anggota_by_id(id_anggota)
            
            if hasil_pencarian == {}:
                print("ID tidak ditemukan!")
                input("Tekan enter untuk melanjutkan ")
                continue

            riwayat_tabungan(id_anggota)

        elif pilihan == '3':
            exit()
        else :
            raise ValueError("Input yang anda masukkan tidak tersedia")
    except ValueError as e:
        print("\n===============================================================")
        print(f"{'Terjadi kesalahan input':^60}")
        print(f"{str(e):^60}")
        print("===============================================================")
        input("Tekan Enter untuk melanjutkan...")
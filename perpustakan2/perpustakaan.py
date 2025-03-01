"""
Sistem Manajemen Perpustakaan
Copyright (C) 2024 [andika aji nugroho]

Dibuat untuk mendukung pengelolaan buku, anggota, dan peminjaman di perpustakaan.

Lisensi:
Kode ini dilindungi oleh hak cipta. Anda bebas menggunakannya untuk kebutuhan pribadi, pendidikan, atau pengembangan internal.
Namun, dilarang memperjualbelikan kode ini tanpa izin dari pemilik hak cipta.

Dikembangkan oleh: [andika aji nugroho]
Email: [andkaji1927@gmail.com]
"""

import sqlite3
from datetime import datetime

# Membuat koneksi ke database SQLite
conn = sqlite3.connect("perpustakaan2.db")
cursor = conn.cursor()

# Membuat tabel Buku
cursor.execute('''
CREATE TABLE IF NOT EXISTS Buku (
    id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
    judul TEXT NOT NULL,
    penulis TEXT NOT NULL,
    tahun_terbit INTEGER NOT NULL CHECK(tahun_terbit > 0),
    stok INTEGER NOT NULL CHECK(stok >= 0)
)
''')

# Membuat tabel Anggota
cursor.execute('''
CREATE TABLE IF NOT EXISTS Anggota (
    id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    nomor_telepon INTEGER NOT NULL
)
''')

# Membuat tabel Peminjaman
cursor.execute('''
CREATE TABLE IF NOT EXISTS Peminjaman (
    id_peminjaman INTEGER PRIMARY KEY AUTOINCREMENT,
    id_buku INTEGER NOT NULL,
    id_anggota INTEGER NOT NULL,
    tanggal_pinjam DATE NOT NULL,
    tanggal_kembali DATE,
    FOREIGN KEY (id_buku) REFERENCES Buku (id_buku),
    FOREIGN KEY (id_anggota) REFERENCES Anggota (id_anggota)
)
''')

# Fungsi CRUD Buku
def kelola_buku(): 
    while True: 
        print("\n--- Kelola Buku ---")
        print("1. Tambah Buku")
        print("2. Lihat Buku")
        print("3. Ubah Buku")
        print("4. Hapus Buku")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            tambah_buku()
        elif pilihan == "2":
            lihat_buku()
        elif pilihan == "3":
            ubah_buku()
        elif pilihan == "4":
            hapus_buku()
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid!")

def tambah_buku(): 
    judul = input("Masukkan judul buku: ")
    penulis = input("Masukkan penulis buku: ")
    while True: 
        try:
            tahun_terbit = int(input("Masukkan tahun terbit: "))
            stok = int(input("Masukkan jumlah stok: "))
            if tahun_terbit > 0 and stok >= 0:
                break 
            else:
                print("Tahun terbit harus lebih besar dari 0 dan stok tidak boleh negatif.")
        except ValueError: 
            print("Input tidak valid. Masukkan angka yang sesuai.")
    cursor.execute("INSERT INTO Buku (judul, penulis, tahun_terbit, stok) VALUES (?, ?, ?, ?)", 
                   (judul, penulis, tahun_terbit, stok)) 
    conn.commit() 
    print("Buku berhasil ditambahkan!")

def lihat_buku(): 
    cursor.execute("SELECT * FROM Buku") 
    
    hasil = cursor.fetchall() 
    print("\n--- Daftar Buku ---")
    print(f"{'ID':<5} {'Judul':<30} {'Penulis':<20} {'Tahun':<10} {'Stok':<5}") 
    print("-" * 75)
    for buku in hasil:
        print(f"{buku[0]:<5} {buku[1]:<30} {buku[2]:<20} {buku[3]:<10} {buku[4]:<5}")

    if not hasil: 
        print("Tidak ada data buku.")

def ubah_buku(): 
    cursor.execute("SELECT * FROM Buku")
    hasil = cursor.fetchall()
    print("\n--- Daftar Buku ---")
    print(f"{'ID':<5} {'Judul':<30} {'Penulis':<20} {'Tahun':<10} {'Stok':<5}")
    print("-" * 75)
    for buku in hasil:
        print(f"{buku[0]:<5} {buku[1]:<30} {buku[2]:<20} {buku[3]:<10} {buku[4]:<5}")
    if not hasil:
        print("Tidak ada data buku.")
        return
    
    try:
        id_buku = int(input("Masukkan ID buku yang akan diubah: "))
        judul = input("Masukkan judul baru: ")
        penulis = input("Masukkan penulis baru: ")
        tahun_terbit = int(input("Masukkan tahun terbit baru: "))
        stok = int(input("Masukkan stok baru: "))
        cursor.execute("UPDATE Buku SET judul = ?, penulis = ?, tahun_terbit = ?, stok = ? WHERE id_buku = ?", 
                       (judul, penulis, tahun_terbit, stok, id_buku))
        conn.commit()
        print("Buku berhasil diubah!")
    except ValueError:
        print("Input tidak valid. Pastikan ID, tahun, dan stok berupa angka.")

def hapus_buku():  
    cursor.execute("SELECT * FROM Buku")
    hasil = cursor.fetchall()
    print("\n--- Daftar Buku ---")
    print(f"{'ID':<5} {'Judul':<30} {'Penulis':<20} {'Tahun':<10} {'Stok':<5}")
    print("-" * 75)
    for buku in hasil:
        print(f"{buku[0]:<5} {buku[1]:<30} {buku[2]:<20} {buku[3]:<10} {buku[4]:<5}")
    
    if not hasil:
        print("Tidak ada data buku.")
        return  

    try:
        id_buku = int(input("Masukkan ID buku yang akan dihapus: "))
        cursor.execute("SELECT * FROM Buku WHERE id_buku = ?", (id_buku,))
        buku = cursor.fetchone()

        if buku:  
            print("\nData Buku yang akan dihapus:")
            print(f"ID Buku: {buku[0]}")
            print(f"Judul Buku: {buku[1]}")
            print(f"Pengarang: {buku[2]}")
            print(f"Tahun Terbit: {buku[3]}")
            print(f"Jumlah Stok: {buku[4]}")
            konfirmasi = input("\nApakah Anda yakin ingin menghapus buku ini? (y/n): ")
            if konfirmasi.lower() == 'y':
                cursor.execute("DELETE FROM Buku WHERE id_buku = ?", (id_buku,))
                conn.commit()
                print("Buku berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("Buku dengan ID tersebut tidak ditemukan.")
    except ValueError:  
        print("Input tidak valid. Masukkan ID yang sesuai.")



# Fungsi CRUD Anggota
def kelola_anggota(): 
    while True: 
        print("\n--- Kelola Anggota ---")
        print("1. Tambah Anggota")
        print("2. Lihat Anggota")
        print("3. Ubah Anggota")
        print("4. Hapus Anggota")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            tambah_anggota()
        elif pilihan == "2":
            lihat_anggota()
        elif pilihan == "3":
            ubah_anggota()
        elif pilihan == "4":
            hapus_anggota()
        elif pilihan == "5": 
            break
        else: 
            print("Pilihan tidak valid!")

def tambah_anggota(): 
    nama = input("Masukkan nama anggota: ")
    while True:
        nomor_telepon = input("Masukkan nomor telepon anggota (hanya angka): ")
        if nomor_telepon.isdigit(): 
            break
        else:
            print("Nomor telepon hanya boleh berisi angka.")
    cursor.execute("INSERT INTO Anggota (nama, nomor_telepon) VALUES (?, ?)", 
                   (nama, nomor_telepon)) 
    conn.commit() 
    print("Anggota berhasil ditambahkan!")

def lihat_anggota(): 
    cursor.execute("SELECT * FROM Anggota") 
    hasil = cursor.fetchall() 
    print("\n--- Daftar Anggota ---")
    print(f"{'ID':<5} {'Nama':<25} {'Nomor Telepon':<15}") 
    print("-" * 50)
    for anggota in hasil:
        print(f"{anggota[0]:<5} {anggota[1]:<25} {anggota[2]:<15}") 
    if not hasil: 
        print("Tidak ada data anggota.")

def ubah_anggota():
    cursor.execute("SELECT * FROM Anggota")
    hasil = cursor.fetchall()
    print("\n--- Daftar Anggota ---")
    print(f"{'ID':<5} {'Nama':<25} {'Nomor Telepon':<15}")
    print("-" * 50)
    for anggota in hasil:
        print(f"{anggota[0]:<5} {anggota[1]:<25} {anggota[2]:<15}")
    if not hasil:
        print("Tidak ada data anggota.")
        return

    try:
        id_anggota = int(input("Masukkan ID anggota yang akan diubah: "))
        nama = input("Masukkan nama baru: ")
        while True:
            nomor_telepon = input("Masukkan nomor telepon baru (hanya angka): ")
            if nomor_telepon.isdigit():
                break
            else:
                print("Nomor telepon hanya boleh berisi angka.")
        cursor.execute("UPDATE Anggota SET nama = ?, nomor_telepon = ? WHERE id_anggota = ?", 
                       (nama, nomor_telepon, id_anggota))
        conn.commit()
        print("Anggota berhasil diubah!")
    except ValueError:
        print("Input tidak valid.")


def hapus_anggota():  
    cursor.execute("SELECT * FROM Anggota")
    hasil = cursor.fetchall()
    print("\n--- Daftar Anggota ---")
    print(f"{'ID':<5} {'Nama':<25} {'Nomor Telepon':<15}")
    print("-" * 50)
    for anggota in hasil:
        print(f"{anggota[0]:<5} {anggota[1]:<25} {anggota[2]:<15}")
    
    if not hasil:
        print("Tidak ada data anggota.")
        return  

    try:
        id_anggota = int(input("Masukkan ID anggota yang akan dihapus: "))
        cursor.execute("SELECT * FROM Anggota WHERE id_anggota = ?", (id_anggota,))
        anggota = cursor.fetchone()

        if anggota:  
            print("\nData Anggota yang akan dihapus:")
            print(f"ID Anggota: {anggota[0]}")
            print(f"Nama: {anggota[1]}")
            print(f"Nomor Telepon: {anggota[2]}")
            konfirmasi = input("\nApakah Anda yakin ingin menghapus anggota ini? (y/n): ")
            if konfirmasi.lower() == 'y':
                cursor.execute("DELETE FROM Anggota WHERE id_anggota = ?", (id_anggota,))
                conn.commit()
                print("Anggota berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("Anggota dengan ID tersebut tidak ditemukan.")
    except ValueError:  
        print("Input tidak valid. Masukkan ID yang sesuai.")


# Fungsi CRUD Peminjaman
def kelola_peminjaman(): 
    while True:
        print("\n--- Kelola Peminjaman ---")
        print("1. Tambah Peminjaman")
        print("2. Lihat Peminjaman")
        print("3. Ubah Peminjaman")
        print("4. Hapus Peminjaman")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            tambah_peminjaman()
        elif pilihan == "2":
            lihat_peminjaman()
        elif pilihan == "3":
            ubah_peminjaman()
        elif pilihan == "4":
            hapus_peminjaman()
        elif pilihan == "5": 
            break
        else: 
            print("Pilihan tidak valid!")

def tambah_peminjaman():  
    
    print("\n--- Daftar Buku ---")
    cursor.execute("SELECT id_buku, judul, stok FROM Buku")
    daftar_buku = cursor.fetchall()
    print(f"{'ID':<5} {'Judul':<30} {'Stok':<5}")
    print("-" * 45)
    for buku in daftar_buku:
        print(f"{buku[0]:<5} {buku[1]:<30} {buku[2]:<5}")
    if not daftar_buku:
        print("Tidak ada data buku. Tambahkan buku terlebih dahulu.")
        return
    
    print("\n--- Daftar Anggota ---")
    cursor.execute("SELECT id_anggota, nama FROM Anggota")
    daftar_anggota = cursor.fetchall()
    print(f"{'ID':<5} {'Nama':<30}")
    print("-" * 40)
    for anggota in daftar_anggota:
        print(f"{anggota[0]:<5} {anggota[1]:<30}")
    if not daftar_anggota:
        print("Tidak ada data anggota. Tambahkan anggota terlebih dahulu.")
        return

    try:
        id_buku = int(input("Masukkan ID buku: "))
        id_anggota = int(input("Masukkan ID anggota: "))
        tanggal_pinjam = input("Masukkan tanggal pinjam (YYYY-MM-DD): ")
        if not validate_date(tanggal_pinjam):
            print("Tanggal tidak valid. Format harus YYYY-MM-DD.")
            return

        
        cursor.execute("SELECT stok FROM Buku WHERE id_buku = ?", (id_buku,))
        result = cursor.fetchone()
        if result and result[0] > 0:

            cursor.execute("INSERT INTO Peminjaman (id_buku, id_anggota, tanggal_pinjam) VALUES (?, ?, ?)",
                           (id_buku, id_anggota, tanggal_pinjam))
            
            cursor.execute("UPDATE Buku SET stok = stok - 1 WHERE id_buku = ?", (id_buku,))
            conn.commit()
            print("Peminjaman berhasil ditambahkan!")
        else:
            print("Stok buku habis atau ID buku tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.")


def lihat_peminjaman(): 
    cursor.execute('''
    SELECT Peminjaman.id_peminjaman, Buku.judul, Anggota.nama, Peminjaman.tanggal_pinjam, Peminjaman.tanggal_kembali
    FROM Peminjaman
    JOIN Buku ON Peminjaman.id_buku = Buku.id_buku
    JOIN Anggota ON Peminjaman.id_anggota = Anggota.id_anggota
    ''') 
    hasil = cursor.fetchall() 
    print("\n--- Daftar Peminjaman ---")
    print(f"{'ID':<5} {'Buku':<30} {'Anggota':<20} {'Tanggal Pinjam':<15} {'Tanggal Kembali':<15}") # untuk menampilkan header tabel
    print("-" * 85)
    for peminjaman in hasil: 
        kembali = peminjaman[4] if peminjaman[4] else "Belum kembali"
        print(f"{peminjaman[0]:<5} {peminjaman[1]:<30} {peminjaman[2]:<20} {peminjaman[3]:<15} {kembali:<15}") # untuk menampilkan data peminjaman
    if not hasil: 
        print("Tidak ada data peminjaman.")

def ubah_peminjaman():
    cursor.execute('''
    SELECT Peminjaman.id_peminjaman, Buku.judul, Anggota.nama, Peminjaman.tanggal_pinjam, Peminjaman.tanggal_kembali
    FROM Peminjaman
    JOIN Buku ON Peminjaman.id_buku = Buku.id_buku
    JOIN Anggota ON Peminjaman.id_anggota = Anggota.id_anggota
    ''') 
    hasil = cursor.fetchall() 
    print("\n--- Daftar Peminjaman ---") 
    print(f"{'ID':<5} {'Buku':<30} {'Anggota':<20} {'Tanggal Pinjam':<15} {'Tanggal Kembali':<15}") 
    print("-" * 85) 
    for peminjaman in hasil: 
        kembali = peminjaman[4] if peminjaman[4] else "Belum kembali" 
        print(f"{peminjaman[0]:<5} {peminjaman[1]:<30} {peminjaman[2]:<20} {peminjaman[3]:<15} {kembali:<15}") 
    if not hasil: 
        print("Tidak ada data peminjaman.")
        return

    try:
        id_peminjaman = int(input("Masukkan ID peminjaman yang akan diubah: "))
        tanggal_kembali = input("Masukkan tanggal kembali (YYYY-MM-DD): ")
        if not validate_date(tanggal_kembali):
            print("Tanggal tidak valid. Format harus YYYY-MM-DD.")
            return
        cursor.execute("UPDATE Peminjaman SET tanggal_kembali = ? WHERE id_peminjaman = ?", 
                       (tanggal_kembali, id_peminjaman))
        cursor.execute('''
        UPDATE Buku SET stok = stok + 1 
        WHERE id_buku = (SELECT id_buku FROM Peminjaman WHERE id_peminjaman = ?) 
        ''', (id_peminjaman,))
        conn.commit()
        print("Peminjaman berhasil diubah!")
    except ValueError:
        print("Input tidak valid.")


def hapus_peminjaman():
    
    cursor.execute(''' 
    SELECT Peminjaman.id_peminjaman, Buku.judul, Anggota.nama, Peminjaman.tanggal_pinjam, Peminjaman.tanggal_kembali
    FROM Peminjaman
    JOIN Buku ON Peminjaman.id_buku = Buku.id_buku
    JOIN Anggota ON Peminjaman.id_anggota = Anggota.id_anggota
    ''')
    hasil = cursor.fetchall()
    print("\n--- Daftar Peminjaman ---")
    print(f"{'ID':<5} {'Buku':<30} {'Anggota':<20} {'Tanggal Pinjam':<15} {'Tanggal Kembali':<15}")
    print("-" * 85)
    for peminjaman in hasil:
        kembali = peminjaman[4] if peminjaman[4] else "Belum kembali"
        print(f"{peminjaman[0]:<5} {peminjaman[1]:<30} {peminjaman[2]:<20} {peminjaman[3]:<15} {kembali:<15}")
    if not hasil:
        print("Tidak ada data peminjaman.")
        return  

    
    try:
        id_peminjaman = int(input("Masukkan ID peminjaman yang akan dihapus: "))
        cursor.execute("SELECT id_peminjaman FROM Peminjaman WHERE id_peminjaman = ?", (id_peminjaman,))
        data = cursor.fetchone()
        if data:
            konfirmasi = input("\nApakah Anda yakin ingin menghapus peminjaman ini? (y/n): ")
            if konfirmasi.lower() == 'y':
                cursor.execute("DELETE FROM Peminjaman WHERE id_peminjaman = ?", (id_peminjaman,))
                conn.commit()
                print("Peminjaman berhasil dihapus!")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("Peminjaman dengan ID tersebut tidak ditemukan.")
    except ValueError:  
        print("Input tidak valid. Masukkan ID yang sesuai.")



# Fungsi validasi tanggal
def validate_date(date_str): 
    try: 
        datetime.strptime(date_str, "%Y-%m-%d") 
        return True 
    except ValueError: 
        return False

# Menu utama
def menu_utama(): 
    while True: 
        print("\n=== Sistem Manajemen Perpustakaan ===")
        print("1. Kelola Buku")
        print("2. Kelola Anggota")
        print("3. Kelola Peminjaman")
        print("4. Keluar")
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            kelola_buku()
        elif pilihan == "2":
            kelola_anggota()
        elif pilihan == "3":
            kelola_peminjaman()
        elif pilihan == "4":
            print("Terima kasih telah menggunakan sistem ini!")
            break
        else:
            print("Pilihan tidak valid!")


menu_utama() 


conn.close() 

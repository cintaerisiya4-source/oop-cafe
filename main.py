"""
main.py
Program utama sistem kasir kafe. Jalankan dengan:  python main.py

Materi OOP: class Cafe yang mengatur objek-objek lain (Minuman, Makanan,
Dessert, Pelanggan, Member, Pesanan), serta penanganan exception.
"""

from menu import Minuman, Makanan, Dessert, MenuItem, StokTidakCukupError
from pelanggan import Pelanggan, Member
from pesanan import Pesanan


def baca_angka(pesan):
    """Meminta input angka bulat; mengulang sampai input valid."""
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print("  ! Masukkan angka yang valid.")


class Cafe:
    def __init__(self, nama):
        self.nama = nama
        self.daftar_menu = []
        self.riwayat = []
        self._isi_menu_awal()

    def _isi_menu_awal(self):
        """Membuat objek menu memakai @classmethod dari_dict."""
        data_minuman = [
            {"nama": "Kopi Hitam", "harga": 12000, "stok": 20, "dingin": False},
            {"nama": "Kopi Susu", "harga": 18000, "stok": 20, "dingin": True},
            {"nama": "Teh Tarik", "harga": 15000, "stok": 15, "dingin": False},
            {"nama": "Matcha Latte", "harga": 22000, "stok": 10, "dingin": True},
        ]
        data_makanan = [
            {"nama": "Nasi Goreng", "harga": 25000, "stok": 10, "pedas": True},
            {"nama": "Roti Bakar", "harga": 15000, "stok": 12, "pedas": False},
            {"nama": "Mie Goreng", "harga": 22000, "stok": 10, "pedas": True},
        ]
        data_dessert = [
            {"nama": "Brownies", "harga": 18000, "stok": 8},
            {"nama": "Pudding Coklat", "harga": 12000, "stok": 8},
        ]
        for d in data_minuman:
            self.daftar_menu.append(Minuman.dari_dict(d))
        for d in data_makanan:
            self.daftar_menu.append(Makanan.dari_dict(d))
        for d in data_dessert:
            self.daftar_menu.append(Dessert.dari_dict(d))

    # ---------- TAMPILAN ----------
    def tampilkan_menu(self):
        print(f"\n=== DAFTAR MENU {self.nama.upper()} ===")
        kategori_sebelumnya = None
        for no, menu in enumerate(self.daftar_menu, start=1):
            if menu.kategori() != kategori_sebelumnya:
                kategori_sebelumnya = menu.kategori()
                print(f"\n[{kategori_sebelumnya}]")
            print(f"{no:>2}. {menu}")
        print(f"\nTotal jenis menu: {MenuItem.jumlah_menu}")

    # ---------- FITUR 1: BUAT PESANAN ----------
    def buat_pesanan(self):
        print("\n--- PESANAN BARU ---")
        nama = input("Nama pelanggan        : ").strip() or "Tanpa Nama"
        jenis = input("Apakah member? (y/n)   : ").strip().lower()
        if jenis == "y":
            pelanggan = Member(nama, poin=0)
        else:
            pelanggan = Pelanggan(nama)

        pesanan = Pesanan(pelanggan)
        while True:
            self.tampilkan_menu()
            nomor = baca_angka("\nPilih nomor menu (0 = selesai): ")
            if nomor == 0:
                break
            if not 1 <= nomor <= len(self.daftar_menu):
                print("  ! Nomor menu tidak ada.")
                continue
            menu = self.daftar_menu[nomor - 1]
            jumlah = baca_angka(f"Jumlah {menu.nama}: ")
            try:
                pesanan.tambah_item(menu, jumlah)
                print(f"  + {jumlah} {menu.nama} ditambahkan.")
            except StokTidakCukupError as e:
                print(f"  ! {e}")
            except ValueError as e:
                print(f"  ! {e}")

        if len(pesanan) == 0:
            print("Pesanan kosong, dibatalkan.")
            return

        print("\n" + pesanan.cetak_struk())
        self.proses_pembayaran(pesanan)

    def proses_pembayaran(self, pesanan):
        while True:
            uang = baca_angka("Uang dibayar (0 = batalkan pesanan): ")
            if uang == 0:
                pesanan.batalkan()
                print("Pesanan dibatalkan, stok dikembalikan.")
                return
            if uang < pesanan.total:
                kurang = MenuItem.format_rupiah(pesanan.total - uang)
                print(f"  ! Uang kurang {kurang}.")
                continue
            break

        kembalian = uang - pesanan.total
        print(f"Kembalian: {MenuItem.format_rupiah(kembalian)}")
        poin = pesanan.pelanggan.tambah_poin(pesanan.total)   # polymorphism
        if poin > 0:
            print(f"Selamat! {pesanan.pelanggan.nama} mendapat {poin} poin.")
        self.riwayat.append(pesanan)
        print("Pembayaran berhasil. Terima kasih!")

    # ---------- FITUR 2: TAMBAH STOK ----------
    def tambah_stok(self):
        self.tampilkan_menu()
        nomor = baca_angka("\nPilih nomor menu yang ditambah stoknya: ")
        if not 1 <= nomor <= len(self.daftar_menu):
            print("  ! Nomor menu tidak ada.")
            return
        jumlah = baca_angka("Jumlah tambahan stok: ")
        try:
            self.daftar_menu[nomor - 1].tambah_stok(jumlah)
            print("Stok berhasil ditambah.")
        except ValueError as e:
            print(f"  ! {e}")

    # ---------- FITUR 3: RIWAYAT ----------
    def lihat_riwayat(self):
        print("\n=== RIWAYAT PESANAN ===")
        if not self.riwayat:
            print("Belum ada pesanan.")
            return
        pendapatan = 0
        for p in self.riwayat:
            print(f"{p} -> {MenuItem.format_rupiah(p.total)}")
            pendapatan += p.total
        print(f"\nTotal pendapatan: {MenuItem.format_rupiah(pendapatan)}")

    # ---------- MENU UTAMA ----------
    def jalankan(self):
        print(f"Selamat datang di {self.nama}!")
        while True:
            print("\n===== MENU UTAMA =====")
            print("1. Lihat menu")
            print("2. Buat pesanan")
            print("3. Tambah stok (admin)")
            print("4. Riwayat pesanan")
            print("0. Keluar")
            pilihan = input("Pilih: ").strip()
            if pilihan == "1":
                self.tampilkan_menu()
            elif pilihan == "2":
                self.buat_pesanan()
            elif pilihan == "3":
                self.tambah_stok()
            elif pilihan == "4":
                self.lihat_riwayat()
            elif pilihan == "0":
                print("Terima kasih, sampai jumpa!")
                break
            else:
                print("  ! Pilihan tidak valid.")


if __name__ == "__main__":
    kafe = Cafe("Kafe Senja")
    kafe.jalankan()

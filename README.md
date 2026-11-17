# Sistem Kasir Kafe (Python OOP)

Project sederhana sistem kasir kafe berbasis terminal untuk tugas mata kuliah Pemrograman Berorientasi Objek.

**Nama :** (CINTA ERI SIYA PUTRI HARJA)
**NIM  :** (14012500038)

## Cara Menjalankan
```
python main.py
```
Butuh Python 3.8 atau lebih baru. Tidak perlu install library tambahan.

## Fitur
1. Lihat daftar menu (minuman, makanan, dessert)
2. Buat pesanan, hitung diskon & pajak, cetak struk, kembalian
3. Tambah stok menu
4. Riwayat pesanan dan total pendapatan

## Materi OOP yang Digunakan
| Materi | Lokasi |
|---|---|
| Class & Object, Constructor | semua file |
| Class attribute & instance attribute | `MenuItem.jumlah_menu`, `Pesanan.PAJAK` |
| Encapsulation (private / protected) | `MenuItem.__harga`, `MenuItem._stok` |
| Property (getter & setter) | `MenuItem.harga`, `Pesanan.total` |
| Abstract class & abstract method | `MenuItem` (ABC) |
| Inheritance & `super()` | `Minuman`, `Makanan`, `Dessert`, `Member` |
| Polymorphism / overriding | `hitung_harga()`, `get_diskon()`, `tambah_poin()` |
| `@classmethod` | `MenuItem.dari_dict()` |
| `@staticmethod` | `MenuItem.format_rupiah()` |
| Magic method | `__str__`, `__len__` |
| Composition | `Pesanan` memiliki `Pelanggan` dan `ItemPesanan` |
| Custom exception | `StokTidakCukupError` |

## Struktur File
```
cafe_project/
├── main.py        # program utama (class Cafe)
├── menu.py        # MenuItem, Minuman, Makanan, Dessert
├── pelanggan.py   # Pelanggan, Member
├── pesanan.py     # ItemPesanan, Pesanan
├── README.md
└── .gitignore
```

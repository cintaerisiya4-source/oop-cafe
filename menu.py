"""
menu.py
Berisi class-class untuk menu kafe.

Materi OOP yang dipakai di file ini:
- Class & Object
- Constructor (__init__)
- Class attribute vs Instance attribute
- Encapsulation (atribut private __harga dan protected _stok)
- Property (getter & setter)
- Abstract class & abstract method (ABC)
- Inheritance + super()
- Polymorphism (method overriding)
- @classmethod dan @staticmethod
- Magic method (__str__)
- Custom exception
"""

from abc import ABC, abstractmethod


class StokTidakCukupError(Exception):
    """Exception khusus: dipakai saat stok menu tidak mencukupi."""

    def __init__(self, nama, stok_tersedia):
        super().__init__(f"Stok {nama} tidak cukup (tersisa {stok_tersedia}).")


class MenuItem(ABC):
    """Class induk (abstract) untuk semua menu. Tidak bisa dibuat objeknya langsung."""

    # Class attribute: dipakai bersama oleh semua objek
    jumlah_menu = 0

    def __init__(self, nama, harga, stok):
        self.nama = nama                # atribut public
        self.__harga = 0                # atribut private (name mangling)
        self.harga = harga              # lewat setter, jadi otomatis divalidasi
        self._stok = stok               # atribut protected
        MenuItem.jumlah_menu += 1

    # ---------- PROPERTY ----------
    @property
    def harga(self):
        """Getter: membaca harga."""
        return self.__harga

    @harga.setter
    def harga(self, nilai):
        """Setter: mengubah harga dengan validasi."""
        if nilai <= 0:
            raise ValueError("Harga harus lebih dari 0.")
        self.__harga = nilai

    @property
    def stok(self):
        """Stok hanya bisa dibaca dari luar (read-only)."""
        return self._stok

    # ---------- METHOD BIASA ----------
    def kurangi_stok(self, jumlah):
        if jumlah > self._stok:
            raise StokTidakCukupError(self.nama, self._stok)
        self._stok -= jumlah

    def tambah_stok(self, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah tambahan stok harus lebih dari 0.")
        self._stok += jumlah

    # ---------- ABSTRACT METHOD ----------
    # Wajib dibuat ulang (override) oleh class turunan
    @abstractmethod
    def hitung_harga(self, jumlah):
        """Menghitung total harga untuk 'jumlah' porsi."""

    @abstractmethod
    def kategori(self):
        """Mengembalikan nama kategori menu."""

    # ---------- STATIC METHOD ----------
    @staticmethod
    def format_rupiah(angka):
        """Tidak butuh self/cls, hanya fungsi bantu. Contoh: 15000 -> Rp15.000"""
        return "Rp" + f"{angka:,.0f}".replace(",", ".")

    # ---------- CLASS METHOD ----------
    @classmethod
    def dari_dict(cls, data):
        """Membuat objek dari dictionary. 'cls' bisa Minuman, Makanan, atau Dessert."""
        return cls(**data)

    # ---------- MAGIC METHOD ----------
    def __str__(self):
        return f"{self.nama:<20} {self.format_rupiah(self.harga):>10}   stok: {self._stok}"


class Minuman(MenuItem):
    """Turunan MenuItem. Minuman dingin kena biaya tambahan es."""

    BIAYA_ES = 2000

    def __init__(self, nama, harga, stok, dingin=False):
        super().__init__(nama, harga, stok)   # memanggil constructor class induk
        self.dingin = dingin

    def hitung_harga(self, jumlah):           # overriding
        harga_satuan = self.harga + (self.BIAYA_ES if self.dingin else 0)
        return harga_satuan * jumlah

    def kategori(self):
        return "Minuman"

    def __str__(self):
        suhu = "dingin" if self.dingin else "panas"
        return super().__str__() + f"   ({suhu})"


class Makanan(MenuItem):
    """Turunan MenuItem. Makanan bisa pedas atau tidak."""

    def __init__(self, nama, harga, stok, pedas=False):
        super().__init__(nama, harga, stok)
        self.pedas = pedas

    def hitung_harga(self, jumlah):           # overriding
        return self.harga * jumlah

    def kategori(self):
        return "Makanan"

    def __str__(self):
        return super().__str__() + ("   (pedas)" if self.pedas else "")


class Dessert(MenuItem):
    """Turunan MenuItem. Beli 3 atau lebih dapat diskon 10%."""

    def hitung_harga(self, jumlah):           # overriding (rumus berbeda)
        total = self.harga * jumlah
        if jumlah >= 3:
            total = total * 0.9
        return int(total)

    def kategori(self):
        return "Dessert"

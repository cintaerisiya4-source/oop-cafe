"""
pesanan.py
Berisi class ItemPesanan dan Pesanan.

Materi OOP: Composition (Pesanan memiliki Pelanggan & ItemPesanan),
property, class attribute, magic method (__len__, __str__).
"""

from datetime import datetime


class ItemPesanan:
    """Satu baris pesanan: menu apa dan berapa banyak."""

    def __init__(self, menu, jumlah):
        self.menu = menu
        self.jumlah = jumlah

    @property
    def subtotal(self):
        # Polymorphism: tiap jenis menu punya rumus hitung_harga sendiri
        return self.menu.hitung_harga(self.jumlah)


class Pesanan:
    PAJAK = 0.10            # class attribute: pajak 10%
    jumlah_pesanan = 0      # class attribute: penghitung nomor pesanan

    def __init__(self, pelanggan):
        Pesanan.jumlah_pesanan += 1
        self.no = Pesanan.jumlah_pesanan
        self.pelanggan = pelanggan      # composition
        self.items = []                 # composition (list of ItemPesanan)
        self.waktu = datetime.now()

    def tambah_item(self, menu, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih dari 0.")
        menu.kurangi_stok(jumlah)       # bisa memunculkan StokTidakCukupError
        self.items.append(ItemPesanan(menu, jumlah))

    def batalkan(self):
        """Mengembalikan stok semua item jika pesanan dibatalkan."""
        for item in self.items:
            item.menu.tambah_stok(item.jumlah)
        self.items.clear()

    # ---------- PROPERTY untuk perhitungan ----------
    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items)

    @property
    def diskon(self):
        return int(self.subtotal * self.pelanggan.get_diskon())

    @property
    def pajak(self):
        return int((self.subtotal - self.diskon) * self.PAJAK)

    @property
    def total(self):
        return self.subtotal - self.diskon + self.pajak

    def cetak_struk(self):
        rp = self.items[0].menu.format_rupiah if self.items else str
        garis = "=" * 46
        baris = [
            garis,
            "           STRUK PEMBAYARAN - KAFE",
            garis,
            f"No Pesanan : {self.no}",
            f"Tanggal    : {self.waktu.strftime('%d-%m-%Y %H:%M')}",
            f"Pelanggan  : {self.pelanggan}",
            "-" * 46,
        ]
        for item in self.items:
            baris.append(f"{item.menu.nama:<20} x{item.jumlah:<3} {rp(item.subtotal):>14}")
        baris += [
            "-" * 46,
            f"{'Subtotal':<26} {rp(self.subtotal):>14}",
            f"{'Diskon':<26} {'-' + rp(self.diskon):>14}",
            f"{'Pajak 10%':<26} {rp(self.pajak):>14}",
            f"{'TOTAL':<26} {rp(self.total):>14}",
            garis,
        ]
        return "\n".join(baris)

    # ---------- MAGIC METHOD ----------
    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"Pesanan #{self.no} - {self.pelanggan.nama} ({len(self)} item)"

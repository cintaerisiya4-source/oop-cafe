"""
pelanggan.py
Berisi class Pelanggan dan Member.

Materi OOP: Inheritance, super(), Polymorphism, Property, Magic method.
"""


class Pelanggan:
    """Pelanggan biasa: tidak dapat diskon dan tidak dapat poin."""

    def __init__(self, nama, no_hp="-"):
        self.nama = nama
        self.no_hp = no_hp

    def get_diskon(self):
        return 0.0

    def tambah_poin(self, total_belanja):
        """Pelanggan biasa tidak punya poin, jadi tidak melakukan apa-apa."""
        return 0

    @property
    def status(self):
        return "Reguler"

    def __str__(self):
        return f"{self.nama} ({self.status})"


class Member(Pelanggan):
    """Member: diskon 10% dan mendapat poin setiap belanja."""

    DISKON_MEMBER = 0.10

    def __init__(self, nama, no_hp="-", poin=0):
        super().__init__(nama, no_hp)
        self.poin = poin

    def get_diskon(self):                      # overriding
        return self.DISKON_MEMBER

    def tambah_poin(self, total_belanja):      # overriding
        poin_baru = total_belanja // 10000     # tiap Rp10.000 = 1 poin
        self.poin += poin_baru
        return poin_baru

    @property
    def status(self):
        return f"Member, {self.poin} poin"

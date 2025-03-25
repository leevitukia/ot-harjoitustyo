import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()

    def test_kassa_saldo_oikein(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_kassa_myyty_oikein(self):
        self.assertEqual(self.kassa.edulliset + self.kassa.maukkaat, 0)

    def test_osta_maukas_kateinen(self):
        value = self.kassa.syo_maukkaasti_kateisella(400)
        self.assertEqual(value, 0)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_osta_maukas_kortti(self):
        kortti = Maksukortti(400)

        self.kassa.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(kortti.saldo, 0)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_osta_edullinen_kateinen(self):
        value = self.kassa.syo_edullisesti_kateisella(240)
        self.assertEqual(value, 0)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_osta_edullinen_kortti(self):
        kortti = Maksukortti(240)

        self.kassa.syo_edullisesti_kortilla(kortti)

        self.assertEqual(kortti.saldo, 0)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_osta_maukas_kateinen_saldo_ei_riita(self):
        value = self.kassa.syo_maukkaasti_kateisella(390)
        self.assertEqual(value, 390)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_osta_maukas_kortti_saldo_ei_riita(self):
        kortti = Maksukortti(390)

        self.kassa.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(kortti.saldo, 390)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_osta_edullinen_kateinen_saldo_ei_riita(self):
        value = self.kassa.syo_edullisesti_kateisella(230)
        self.assertEqual(value, 230)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_osta_edullinen_kortti_saldo_ei_riita(self):
        kortti = Maksukortti(230)

        self.kassa.syo_edullisesti_kortilla(kortti)

        self.assertEqual(kortti.saldo, 230)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_lataa_kortille(self):
        kortti = Maksukortti(230)
        self.kassa.lataa_rahaa_kortille(kortti, 10)

        self.assertEqual(kortti.saldo, 240)

    def test_lataa_kortille_negatiivinen(self):
        kortti = Maksukortti(230)
        self.kassa.lataa_rahaa_kortille(kortti, -10)

        self.assertEqual(kortti.saldo, 230)

    def test_rahaa_euroina(self):
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000)


    


import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_aloitus_saldo_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_saldon_lataaminen_toimii(self):
        self.maksukortti.lataa_rahaa(500)

        self.assertEqual(self.maksukortti.saldo, 1500)

    def test_ei_vahenna_jos_saldo_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1100)

        self.assertEqual(self.maksukortti.saldo, 1000)

    def test_vahenee_jos_saldo_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1000)

        self.assertEqual(self.maksukortti.saldo, 0)

    def test_ota_rahaa_palauttaa_true_jos_riittaa(self):
        value = self.maksukortti.ota_rahaa(1000)

        self.assertEqual(value, True)

    def test_ota_rahaa_palauttaa_false_jos_ei_riita(self):
        value = self.maksukortti.ota_rahaa(1100)

        self.assertEqual(value, False)

    def test_saldo_euroina(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_str(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

        

    

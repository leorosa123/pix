import qrcode
import crcmod
from cripto import cripto_valores, decripto_valores


# função responsavel por formatar elementos especificos da escrita padrão
def zero_esq(tamanho, inst=False):
    if inst:
        if len(tamanho) <= 9:
            tamanho = f"050{len(tamanho)}{tamanho}"
            return tamanho
        else:
            tamanho = f"05{len(tamanho)}{tamanho}"
            return tamanho

    if tamanho <= 9:
        return f"0{tamanho}"
    return tamanho


class Pagar_pix():
    def __init__(self, nome_recb, chave_pix, valo_reais, cidade_br, instituicao="PYTHONTEST"):
        # variaveis de pagamento
        self.nome_rec = nome_recb
        self.__chave_pix = chave_pix
        self.__valor_reais = valo_reais
        self.cidade_br = cidade_br
        self.instituicao = instituicao

        # variavel copia e cola
        self.copia_cola = ""

    # formato de escrita padrão para pagamento PIX pelo banco central
    def padrao_banco_central(self):
        payload_format = "000201"
        _script_marchant_account = f"0014BR.GOV.BCB.PIX01{len(self.__chave_pix)}{self.__chave_pix}"
        merchant_account_info_pix = f"26{len(_script_marchant_account)}{_script_marchant_account}"
        merchant_category_code = "52040000"
        transation_currency = "5303986"
        transation_amount = f"54{zero_esq(len(self.__valor_reais))}{self.__valor_reais}"
        country_code = "5802BR"
        merchant_city = f"60{zero_esq(len(self.cidade_br))}{self.cidade_br}"
        name_recb = f"59{zero_esq(len(self.nome_rec))}{self.nome_rec}"
        data_field = f"62{len(zero_esq(self.instituicao, inst=True))}{zero_esq(self.instituicao, inst=True)}"
        crc16 = "6304"
        # retorno da escrita padrão criptografada
        return {"pt1": cripto_valores(payload_format),
                "pt2": cripto_valores(merchant_account_info_pix),
                "pt3": cripto_valores(merchant_category_code),
                "pt4": cripto_valores(transation_currency),
                "pt5": cripto_valores(transation_amount),
                "pt6": cripto_valores(country_code),
                "pt7": cripto_valores(merchant_city),
                "pt8": cripto_valores(name_recb),
                "pt9": cripto_valores(data_field),
                "pt10": cripto_valores(crc16)
                }

    # pix copia e cola para o pagador
    def gerar_payload_completa(self):
        dicts_pay = self.padrao_banco_central()
        payload_concat = ""
        for k, v in dicts_pay.items():
            payload_concat += decripto_valores(dicts_pay[k])

        copia_cola = self.calcular_crc16(payload_concat)
        return copia_cola

    # calculo de toda a escrita padrão validando os dados
    def calcular_crc16(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

        calculo_crc = hex(crc16(str(payload).encode("utf-8")))
        calculo_crc = str(calculo_crc).replace("0x", "").upper()
        self.copia_cola = cripto_valores(f"{payload}{calculo_crc}")
        return decripto_valores(self.copia_cola)

    # pagamento via QRCODE
    def gerar_QRCODE(self):
        qrcode_ = qrcode.make(self.gerar_payload_completa())
        qrcode_.save("pix_copy_cola_real.png")


if __name__ == "__main__":
    pix_paypal = Pagar_pix("nome_de_quem_recebe", "chave_pix[cpf,num,...)", "valors_trans", "cidade_pagador",
                           "instituição")
    print(pix_paypal.gerar_payload_completa())
    pix_paypal.gerar_QRCODE()

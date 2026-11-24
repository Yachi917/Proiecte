# Raport Laboratorul 6: Forensics si Steganografie

## Lucrarea A: Decoderul Universal
- Straturi decode: ['base64', 'base64', 'hex'] -> FLAG{straturi_de_encoding}
- XOR: cheia 128 -> Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}
- Hash spart: password

## Lucrarea B: Forensics si Steganografie

### B1. Magic Bytes
- probe/foto.jpg: jpeg
- probe/ascuns.png: png

### B2. Strings & B4. File Carving
- Semnatura ZIP gasita la offset: 782
- Text/Flag gasit in arhiva: FLAG{ascuns_prin_carving}

### B3. Metadate EXIF si GPS
- Coordonate extrase din foto.jpg: (47.016666, 28.8575)

### B5 & B6. Steganografie LSB
- Mesaj ascuns si dezvaluit din stego.png: FLAG{ascuns_in_pixeli}
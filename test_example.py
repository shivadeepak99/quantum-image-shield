# test_example.py
import argparse
from utils import load_grayscale, save_grayscale, image_entropy, psnr
from encryptor import QuantumSeedImageShield

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Input grayscale image path')
parser.add_argument('--enc-out', default='enc.png')
parser.add_argument('--dec-out', default='dec.png')
args = parser.parse_args()

img = load_grayscale(args.input)
print('Loaded image shape:', img.shape)

shield = QuantumSeedImageShield(img.shape)
encrypted = shield.encrypt(img)
print('Entropy original:', image_entropy(img))
print('Entropy encrypted:', image_entropy(encrypted))

save_grayscale(encrypted, args.enc_out)
print('Encrypted saved to', args.enc_out)

keys = shield.export_keys()
shield2 = QuantumSeedImageShield(img.shape)
shield2.import_keys(keys)
decrypted = shield2.decrypt(encrypted)
save_grayscale(decrypted, args.dec_out)
print('Decrypted saved to', args.dec_out)

print('PSNR original vs decrypted:', psnr(img, decrypted))
print('Exact match:', img.tobytes() == decrypted.tobytes())

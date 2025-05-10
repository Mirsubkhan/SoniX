import demucs.separate
import torch
print(torch.cuda.is_available())  # Должно быть True
demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", r"C:\Users\Guest8\Desktop\GAR8S\Programming\Python\SoniX\presentation\telegram\temp\audio_extracted\df4be2a9f12a4cb5adfcfa759ac230b1.wav", "-d", "cuda"])

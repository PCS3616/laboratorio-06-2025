from pathlib import Path
import subprocess
import tempfile
from base64 import b64decode, b64encode
from typing import List

submission_path = Path("./submission")

# Based in https://doc.rust-lang.org/std/primitive.slice.html#method.chunks
# https://stackoverflow.com/questions/312443/how-do-i-split-a-list-into-equally-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# monoid are awensome
# https://stackoverflow.com/a/952946
def flatten(lss: List[List]):
    return sum(lss, [])

def run_mvn(input_text):
    p = subprocess.run(
        [
            "python", 
            "-m", 
            "MVN.mvnMonitor"
        ],
        input=input_text,
        capture_output=True, 
        text=True,
    )
    return p.stdout

def run_dumper(data_bytes: bytes, base_addres=0x0d00):
    dumper_file = submission_path / "dumper.mvn"
    assert dumper_file.exists(), f"A submissão não contém o arquivo '{dumper_file.name}'"

    data_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    data_file.writelines([
        f"0704	{base_addres:04X}\n", # enderelo inicial
        f"0706	{len(data_bytes)//2:04X}\n", # qtd. de palavras
    ])
    for i, pair_data in enumerate(chunks(data_bytes, 2)):
        data = int.from_bytes(pair_data, 'big')
        line = f"{base_addres+2*i:04X} {data:04X}\n"
        data_file.write(line)
    data_file.flush()

    init_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    init_file.writelines([
        "0000	a700\n",
        "0002	c000\n",
    ])
    init_file.flush()

    out_file = tempfile.NamedTemporaryFile(mode='rb', delete=False)

    print(data_file.name, init_file.name, out_file.name)

    inputs = [
        # load dumper
        f"p {dumper_file.as_posix()}",

        # load dummy data
        f"p {data_file.name}",

        # load "main"
        f"p {init_file.name}",

        # config file
        "s",
        "a",
        "3",
        "00",
        out_file.name,
        "e",

        "r",
        "000",
        "n",
        "x",
    ]
    out = run_mvn('\n'.join(inputs))
    # print(out)

    return out_file.read()


def test_dumper_multiple():
    """
        Testa o dumper para o caso onde a quantidade de 
        palavra é multiplo do tamanho do bloco
    """

    # E vc pensando que não vai usar SD pra nada
    data = [[0xF0, 0xDA] for _ in range(0, 256, 2)]
    bdata = bytes(flatten(data))

    outbytes = run_dumper(bdata)
    expected = b'DQAAgPDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Np6gAAAAAAAAA=='
    assert b64encode(outbytes) == expected, f"Seu código não está correto"

def test_dumper_non_multiple():
    """
        Testa o dumper para o caso onde a quantidade de 
        palavra é multiplo do tamanho do bloco
    """

    # E vc pensando que não vai usar SD pra nada
    data = [[0xF0, 0xDA] for _ in range(0, 258, 2)]
    bdata = bytes(flatten(data))

    outbytes = run_dumper(bdata)
    expected = b'DQAAgPDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Np6gA4AAAHw2v7b'
    assert b64encode(outbytes) == expected, f"Seu código não está correto"

def test_dumper_bigger():
    """
        Testa o dumper para o caso onde a quantidade de 
        palavra não é multiplo do tamanho do bloco
    """

    # E vc pensando que não vai usar SD pra nada
    data = [[x>>8 & 0xFF, x>>0 & 0xFF] for x in range(0, 0x2b0, 2)]
    bdata = bytes(flatten(data))

    outbytes = run_dumper(bdata)
    expected = b'DQAAgAAAAAIABAAGAAgACgAMAA4AEAASABQAFgAYABoAHAAeACAAIgAkACYAKAAqACwALgAwADIANAA2ADgAOgA8AD4AQABCAEQARgBIAEoATABOAFAAUgBUAFYAWABaAFwAXgBgAGIAZABmAGgAagBsAG4AcAByAHQAdgB4AHoAfAB+AIAAggCEAIYAiACKAIwAjgCQAJIAlACWAJgAmgCcAJ4AoACiAKQApgCoAKoArACuALAAsgC0ALYAuAC6ALwAvgDAAMIAxADGAMgAygDMAM4A0ADSANQA1gDYANoA3ADeAOAA4gDkAOYA6ADqAOwA7gDwAPIA9AD2APgA+gD8AP5NAA4AAIABAAECAQQBBgEIAQoBDAEOARABEgEUARYBGAEaARwBHgEgASIBJAEmASgBKgEsAS4BMAEyATQBNgE4AToBPAE+AUABQgFEAUYBSAFKAUwBTgFQAVIBVAFWAVgBWgFcAV4BYAFiAWQBZgFoAWoBbAFuAXABcgF0AXYBeAF6AXwBfgGAAYIBhAGGAYgBigGMAY4BkAGSAZQBlgGYAZoBnAGeAaABogGkAaYBqAGqAawBrgGwAbIBtAG2AbgBugG8Ab4BwAHCAcQBxgHIAcoBzAHOAdAB0gHUAdYB2AHaAdwB3gHgAeIB5AHmAegB6gHsAe4B8AHyAfQB9gH4AfoB/AH+zgAPAABYAgACAgIEAgYCCAIKAgwCDgIQAhICFAIWAhgCGgIcAh4CIAIiAiQCJgIoAioCLAIuAjACMgI0AjYCOAI6AjwCPgJAAkICRAJGAkgCSgJMAk4CUAJSAlQCVgJYAloCXAJeAmACYgJkAmYCaAJqAmwCbgJwAnICdAJ2AngCegJ8An4CgAKCAoQChgKIAooCjAKOApACkgKUApYCmAKaApwCngKgAqICpAKmAqgCqgKsAq7dQA=='
    assert b64encode(outbytes) == expected, f"Seu código não está correto"

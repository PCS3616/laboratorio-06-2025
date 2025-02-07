from pathlib import Path
from math import ceil
import subprocess
import tempfile
from base64 import b64decode, b64encode
from typing import List
from itertools import takewhile

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

def bflatten(lls):
    return bytes(flatten(lls))

def clean_memory_dump(btext: bytes):
    text = btext.decode("utf-8")
    print(text)
    lines = text.split('\n')[:-1]

    result = []

    for l in lines:
        # Line example
        # 0d00:  00  00  00  02  00  04  00  06  00  08  00  0a  00  0c  00  0e
        values = [
            l[7:9],
            l[11:13],
            l[15:17],
            l[19:21],
            l[23:25],
            l[27:29],
            l[31:33],
            l[35:37],
            l[39:41],
            l[43:45],
            l[47:49],
            l[51:53],
            l[55:57],
            l[59:61],
            l[63:65],
            l[67:69],
        ]

        non_empty_values = [int(v, 16) for v in values if v.strip() != '']

        result.extend(non_empty_values)

    return bytes(result)


def mvn_cli(arguments: list[str], output_filepath: str | Path):
    command = f"./mvn-cli {' '.join(arguments)} || mvn-cli {' '.join(arguments)}"
    with open(output_filepath, "w", encoding="utf8") as output_file:
        subprocess.run(command, shell=True, check=True, stdout=output_file)


def executable(main: Path) -> Path:
  asm_program_filepath = Path(f"{main}.asm")
  executable_filepath = Path(f"{main}.mvn")

  assert asm_program_filepath.exists(), f"A submissão não contém o arquivo '{asm_program_filepath.name}'"

  mvn_cli(f"assemble -i {main}.asm".split(), executable_filepath)
  return executable_filepath


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

def run_dumper(encode_bytes: bytes, base_addres=0x0d00):
    dumper_file = executable(submission_path / "dumper")

    data_file = tempfile.NamedTemporaryFile(mode='w')
    data_file.writelines([
        f"0704	{base_addres:04X}\n", # enderelo inicial
        f"0706	{len(encode_bytes)//2:04X}\n", # qtd. de palavras
    ])
    for i, pair_data in enumerate(chunks(encode_bytes, 2)):
        data = int.from_bytes(pair_data, 'big')
        line = f"{base_addres+2*i:04X} {data:04X}\n"
        data_file.write(line)
    data_file.flush()

    init_file = tempfile.NamedTemporaryFile(mode='w')
    init_file.writelines([
        "0000	a700\n",
        "0002	c000\n",
    ])
    init_file.flush()

    out_file = tempfile.NamedTemporaryFile(mode='rb')

    # print(data_file.name, init_file.name, out_file.name)

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

def run_loader(decode_bytes: bytes, base_addres=0x0d00):
    # remove extra data
    # base adress
    # 2 bytes size
    # checksum each 128 bytes

    # print("decode_bytes:", len(decode_bytes))

    n_bytes_without_header = len(decode_bytes) - 10
    n_bytes = n_bytes_without_header - ceil(n_bytes_without_header//130)
    n_words = n_bytes//2
    # print("n_bytes", n_bytes) # 688

    loader_file = executable(submission_path / "loader")

    data_file = tempfile.NamedTemporaryFile(mode='wb')
    data_file.write(decode_bytes)
    data_file.flush()

    init_file = tempfile.NamedTemporaryFile(mode='w')
    init_file.writelines([
        "0000	ab00\n",
        "0002	c000\n",

        f"0704	{base_addres:04X}\n", # endereço inicial
        f"0706	{n_words:04X}\n", # qtd. de palavras
    ])
    init_file.flush()

    out_file = tempfile.NamedTemporaryFile(mode='rb')

    # print(data_file.name, init_file.name, out_file.name)

    inputs = [
        # load dumper
        f"p {loader_file.as_posix()}",

        # load "main"
        f"p {init_file.name}",

        # config file
        "s",
        "a",
        "3",
        "00",
        data_file.name,
        "l",

        "r",
        "000",
        "n",

        f"m {base_addres:04X} {base_addres+2*n_words-1:04X} {out_file.name}",

        "x",
    ]
    out = run_mvn('\n'.join(inputs))
    # print(inputs) #, out)

    return clean_memory_dump(out_file.read())

def test_dumper_multiple():
    # E vc pensando que não vai usar SD pra nada
    data = [[0xF0, 0xDA] for _ in range(0, 256, 2)]

    outbytes = run_dumper(bflatten(data))
    expected = b'DQAAgPDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Np6gAAAAAAAAA=='
    assert outbytes == b64decode(expected), f"Seu código não está correto"

def test_dumper_non_multiple():
    data = [[0xF0, 0xDA] for _ in range(0, 258, 2)]

    outbytes = run_dumper(bflatten(data))
    expected = b'DQAAgPDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Np6gA4AAAHw2v7b'
    assert outbytes == b64decode(expected), f"Seu código não está correto"

def test_dumper_bigger():
    data = [[x>>8 & 0xFF, x>>0 & 0xFF] for x in range(0, 0x2b0, 2)]

    outbytes = run_dumper(bflatten(data))
    expected = b'DQAAgAAAAAIABAAGAAgACgAMAA4AEAASABQAFgAYABoAHAAeACAAIgAkACYAKAAqACwALgAwADIANAA2ADgAOgA8AD4AQABCAEQARgBIAEoATABOAFAAUgBUAFYAWABaAFwAXgBgAGIAZABmAGgAagBsAG4AcAByAHQAdgB4AHoAfAB+AIAAggCEAIYAiACKAIwAjgCQAJIAlACWAJgAmgCcAJ4AoACiAKQApgCoAKoArACuALAAsgC0ALYAuAC6ALwAvgDAAMIAxADGAMgAygDMAM4A0ADSANQA1gDYANoA3ADeAOAA4gDkAOYA6ADqAOwA7gDwAPIA9AD2APgA+gD8AP5NAA4AAIABAAECAQQBBgEIAQoBDAEOARABEgEUARYBGAEaARwBHgEgASIBJAEmASgBKgEsAS4BMAEyATQBNgE4AToBPAE+AUABQgFEAUYBSAFKAUwBTgFQAVIBVAFWAVgBWgFcAV4BYAFiAWQBZgFoAWoBbAFuAXABcgF0AXYBeAF6AXwBfgGAAYIBhAGGAYgBigGMAY4BkAGSAZQBlgGYAZoBnAGeAaABogGkAaYBqAGqAawBrgGwAbIBtAG2AbgBugG8Ab4BwAHCAcQBxgHIAcoBzAHOAdAB0gHUAdYB2AHaAdwB3gHgAeIB5AHmAegB6gHsAe4B8AHyAfQB9gH4AfoB/AH+zgAPAABYAgACAgIEAgYCCAIKAgwCDgIQAhICFAIWAhgCGgIcAh4CIAIiAiQCJgIoAioCLAIuAjACMgI0AjYCOAI6AjwCPgJAAkICRAJGAkgCSgJMAk4CUAJSAlQCVgJYAloCXAJeAmACYgJkAmYCaAJqAmwCbgJwAnICdAJ2AngCegJ8An4CgAKCAoQChgKIAooCjAKOApACkgKUApYCmAKaApwCngKgAqICpAKmAqgCqgKsAq7dQA=='
    assert outbytes == b64decode(expected), f"Seu código não está correto"


def test_loader_multiple():
    data = b'DQAAgPDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Np6gAAAAAAAAA=='

    result = run_loader(b64decode(data))
    expected = bflatten([[0xF0, 0xDA] for _ in range(0, 256, 2)])
    assert result == expected, f"Seu código não está correto"

def test_loader_non_multiple():
    data = b'DQAAgPDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Nrw2vDa8Np6gA4AAAHw2v7b'

    result = run_loader(b64decode(data))
    expected = bflatten([[0xF0, 0xDA] for _ in range(0, 258, 2)])
    assert result == expected, f"Seu código não está correto"

def test_loader_bigger():
    data = b'DQAAgAAAAAIABAAGAAgACgAMAA4AEAASABQAFgAYABoAHAAeACAAIgAkACYAKAAqACwALgAwADIANAA2ADgAOgA8AD4AQABCAEQARgBIAEoATABOAFAAUgBUAFYAWABaAFwAXgBgAGIAZABmAGgAagBsAG4AcAByAHQAdgB4AHoAfAB+AIAAggCEAIYAiACKAIwAjgCQAJIAlACWAJgAmgCcAJ4AoACiAKQApgCoAKoArACuALAAsgC0ALYAuAC6ALwAvgDAAMIAxADGAMgAygDMAM4A0ADSANQA1gDYANoA3ADeAOAA4gDkAOYA6ADqAOwA7gDwAPIA9AD2APgA+gD8AP5NAA4AAIABAAECAQQBBgEIAQoBDAEOARABEgEUARYBGAEaARwBHgEgASIBJAEmASgBKgEsAS4BMAEyATQBNgE4AToBPAE+AUABQgFEAUYBSAFKAUwBTgFQAVIBVAFWAVgBWgFcAV4BYAFiAWQBZgFoAWoBbAFuAXABcgF0AXYBeAF6AXwBfgGAAYIBhAGGAYgBigGMAY4BkAGSAZQBlgGYAZoBnAGeAaABogGkAaYBqAGqAawBrgGwAbIBtAG2AbgBugG8Ab4BwAHCAcQBxgHIAcoBzAHOAdAB0gHUAdYB2AHaAdwB3gHgAeIB5AHmAegB6gHsAe4B8AHyAfQB9gH4AfoB/AH+zgAPAABYAgACAgIEAgYCCAIKAgwCDgIQAhICFAIWAhgCGgIcAh4CIAIiAiQCJgIoAioCLAIuAjACMgI0AjYCOAI6AjwCPgJAAkICRAJGAkgCSgJMAk4CUAJSAlQCVgJYAloCXAJeAmACYgJkAmYCaAJqAmwCbgJwAnICdAJ2AngCegJ8An4CgAKCAoQChgKIAooCjAKOApACkgKUApYCmAKaApwCngKgAqICpAKmAqgCqgKsAq7dQA=='

    result = run_loader(b64decode(data))[:-2]
    expected = bflatten([[x>>8 & 0xFF, x>>0 & 0xFF] for x in range(0, 0x2b0, 2)])
    assert result == expected, f"Seu código não está correto"

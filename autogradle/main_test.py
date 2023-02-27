from pathlib import Path
import subprocess
import tempfile
from base64 import b64decode, b64encode

submission_path = Path("./submission")

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

def test_dumper_not_multiple():
    """
        Testa o dumper para o caso onde a quantidade de 
        palavra não é multiplo do tamanho do bloco
    """
    dumper_file = submission_path / "dumper.mvn"

    assert dumper_file.exists(), f"A submissão não contém o arquivo '{dumper_file.name}'"

    data_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    base_addres = 0x0d00
    n_bytes = 0x2b0
    data_file.writelines([
        f"0704	{base_addres:04X}\n", # enderelo inicial
        f"0706	{n_bytes//2:04X}\n", # qtd. de palavras
    ])
    for i in range(0, n_bytes, 2):
        line = f"{base_addres+i:04X} {i:04X}\n"
        data_file.write(line)
    data_file.flush()

    init_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    init_file.writelines([
        "0000	a700\n",
        "0002	c000\n",
        # "0704	0d00\n",
        # "0706	0158\n",
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

    # Base64 binarry
    expected = b'DQAAgAAAAAIABAAGAAgACgAMAA4AEAASABQAFgAYABoAHAAeACAAIgAkACYAKAAqACwALgAwADIANAA2ADgAOgA8AD4AQABCAEQARgBIAEoATABOAFAAUgBUAFYAWABaAFwAXgBgAGIAZABmAGgAagBsAG4AcAByAHQAdgB4AHoAfAB+AIAAggCEAIYAiACKAIwAjgCQAJIAlACWAJgAmgCcAJ4AoACiAKQApgCoAKoArACuALAAsgC0ALYAuAC6ALwAvgDAAMIAxADGAMgAygDMAM4A0ADSANQA1gDYANoA3ADeAOAA4gDkAOYA6ADqAOwA7gDwAPIA9AD2APgA+gD8AP5NAA4AAIABAAECAQQBBgEIAQoBDAEOARABEgEUARYBGAEaARwBHgEgASIBJAEmASgBKgEsAS4BMAEyATQBNgE4AToBPAE+AUABQgFEAUYBSAFKAUwBTgFQAVIBVAFWAVgBWgFcAV4BYAFiAWQBZgFoAWoBbAFuAXABcgF0AXYBeAF6AXwBfgGAAYIBhAGGAYgBigGMAY4BkAGSAZQBlgGYAZoBnAGeAaABogGkAaYBqAGqAawBrgGwAbIBtAG2AbgBugG8Ab4BwAHCAcQBxgHIAcoBzAHOAdAB0gHUAdYB2AHaAdwB3gHgAeIB5AHmAegB6gHsAe4B8AHyAfQB9gH4AfoB/AH+zgAPAABYAgACAgIEAgYCCAIKAgwCDgIQAhICFAIWAhgCGgIcAh4CIAIiAiQCJgIoAioCLAIuAjACMgI0AjYCOAI6AjwCPgJAAkICRAJGAkgCSgJMAk4CUAJSAlQCVgJYAloCXAJeAmACYgJkAmYCaAJqAmwCbgJwAnICdAJ2AngCegJ8An4CgAKCAoQChgKIAooCjAKOApACkgKUApYCmAKaApwCngKgAqICpAKmAqgCqgKsAq7dQA=='
    outbytes = b64encode(out_file.read())

    assert outbytes == expected, f"Seu código não está correto"


def a_test_dumper_multiple():
    """
        Testa o dumper para o caso onde a quantidade de 
        palavra é multiplo do tamanho do bloco
    """
    dumper_file = submission_path / "dumper.mvn"

    assert dumper_file.exists(), f"A submissão não contém o arquivo '{dumper_file.name}'"

    data_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    base_addres = 0x0d00
    for i in range(0, 100, 2):
        addres = base_addres + i
        data = i
        line = f"{addres:04X} {data:04X}\n"
        data_file.write(line)
    data_file.flush()

    init_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    init_file.writelines([
        "0000	a700\n",
        "0002	c000\n",
        "0704	0d00\n",
        "0706	0158\n",
    ])
    init_file.flush()

    out_file = tempfile.NamedTemporaryFile(mode='rb', delete=False)

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

    # Base64 binarry
    expected = b'DQAAgAAAAAIABAAGAAgACgAMAA4AEAASABQAFgAYABoAHAAeACAAIgAkACYAKAAqACwALgAwADIANAA2ADgAOgA8AD4AQABCAEQARgBIAEoATABOAFAAUgBUAFYAWABaAFwAXgBgAGIAZABmAGgAagBsAG4AcAByAHQAdgB4AHoAfAB+AIAAggCEAIYAiACKAIwAjgCQAJIAlACWAJgAmgCcAJ4AoACiAKQApgCoAKoArACuALAAsgC0ALYAuAC6ALwAvgDAAMIAxADGAMgAygDMAM4A0ADSANQA1gDYANoA3ADeAOAA4gDkAOYA6ADqAOwA7gDwAPIA9AD2APgA+gD8AP5NAA4AAIABAAECAQQBBgEIAQoBDAEOARABEgEUARYBGAEaARwBHgEgASIBJAEmASgBKgEsAS4BMAEyATQBNgE4AToBPAE+AUABQgFEAUYBSAFKAUwBTgFQAVIBVAFWAVgBWgFcAV4BYAFiAWQBZgFoAWoBbAFuAXABcgF0AXYBeAF6AXwBfgGAAYIBhAGGAYgBigGMAY4BkAGSAZQBlgGYAZoBnAGeAaABogGkAaYBqAGqAawBrgGwAbIBtAG2AbgBugG8Ab4BwAHCAcQBxgHIAcoBzAHOAdAB0gHUAdYB2AHaAdwB3gHgAeIB5AHmAegB6gHsAe4B8AHyAfQB9gH4AfoB/AH+zgAPAABYAgACAgIEAgYCCAIKAgwCDgIQAhICFAIWAhgCGgIcAh4CIAIiAiQCJgIoAioCLAIuAjACMgI0AjYCOAI6AjwCPgJAAkICRAJGAkgCSgJMAk4CUAJSAlQCVgJYAloCXAJeAmACYgJkAmYCaAJqAmwCbgJwAnICdAJ2AngCegJ8An4CgAKCAoQChgKIAooCjAKOApACkgKUApYCmAKaApwCngKgAqICpAKmAqgCqgKsAq7dQA=='
    outbytes = b64encode(out_file.read())

    assert outbytes == expected, f"Seu código não está correto"
